/**
 * Faint points of light that walk borders.
 * Quiet on purpose: one or two at a time, never over the hero, the
 * starfield, or the Promise film. Raw WebGL only. This file does not
 * import three.
 */

import { onReducedMotionChange, prefersReducedMotion } from "./motion";
import { getLenis } from "./smooth-scroll";

const KINDS = new Set(["edge", "rule", "outline", "underline"]);
const BANNED = "[data-hero], .join-band, [data-promise], .wordmark, .site-footer__mark";

const WHITE: Rgb = [1, 1, 1];
const BONE: Rgb = [236 / 255, 232 / 255, 225 / 255];
const ASH: Rgb = [138 / 255, 144 / 255, 150 / 255];
const RED: Rgb = [224 / 255, 38 / 255, 30 / 255];
const EMBER: Rgb = [163 / 255, 22 / 255, 15 / 255];

const FADE = 1.5;
const MAX_POINTS = 220;
const STRIDE = 7;

type Kind = "edge" | "rule" | "outline" | "underline";
type Rgb = [number, number, number];

type Target = {
	el: HTMLElement;
	kind: Kind;
	hot: boolean;
	onScreen: boolean;
	x: number;
	y: number;
	w: number;
	h: number;
	radius: number;
	restUntil: number;
	measured: number;
};

type Tracer = {
	target: Target;
	distance: number;
	speed: number;
	tail: number;
	born: number;
	life: number;
	red: boolean;
};

type GlBundle = {
	gl: WebGLRenderingContext;
	program: WebGLProgram;
	buffer: WebGLBuffer;
	resolution: WebGLUniformLocation | null;
	lose: WEBGL_lose_context | null;
};

const VERT = `
attribute vec2 a_pos;
attribute float a_size;
attribute float a_alpha;
attribute vec3 a_color;
uniform vec2 u_resolution;
varying float v_alpha;
varying vec3 v_color;
void main() {
	vec2 clip = (a_pos / u_resolution) * 2.0 - 1.0;
	clip.y = -clip.y;
	gl_Position = vec4(clip, 0.0, 1.0);
	gl_PointSize = a_size;
	v_alpha = a_alpha;
	v_color = a_color;
}
`;

const FRAG = `
precision mediump float;
varying float v_alpha;
varying vec3 v_color;
void main() {
	vec2 p = gl_PointCoord - vec2(0.5);
	float d = length(p);
	if (d > 0.5) discard;
	float core = smoothstep(0.16, 0.0, d);
	float halo = smoothstep(0.5, 0.1, d);
	float glow = core * 0.9 + halo * 0.28;
	float alpha = v_alpha * glow;
	gl_FragColor = vec4(v_color * alpha, alpha);
}
`;

let running = false;
let canvas: HTMLCanvasElement | null = null;
let gpu: GlBundle | null = null;
let targets: Target[] = [];
let alive: Tracer[] = [];
let raf = 0;
let wake = 0;
let nextSpawn = 0;
let lastFrame = 0;
let frameMs = 0;
let frameSamples = 0;
let reduced = false;
let stopReduced: (() => void) | null = null;
let resizeObserver: ResizeObserver | null = null;
let intersectionObserver: IntersectionObserver | null = null;
let menuObserver: MutationObserver | null = null;
let unlistenLenis: (() => void) | null = null;
let scrollListening = false;
let measureQueued = false;
let dpr = 1;
const data = new Float32Array(MAX_POINTS * STRIDE);

function phone(): boolean {
	return window.matchMedia("(max-width: 767px), (pointer: coarse)").matches;
}

function cap(): number {
	return phone() ? 2 : 4;
}

function rand(min: number, max: number): number {
	return min + Math.random() * (max - min);
}

function smooth(t: number): number {
	const x = Math.min(1, Math.max(0, t));
	return x * x * (3 - 2 * x);
}

function kindOf(value: string | null): Kind {
	if (value && KINDS.has(value)) return value as Kind;
	return "edge";
}

function menuOpen(): boolean {
	return document.documentElement.classList.contains("menu-open");
}

function allowed(el: HTMLElement): boolean {
	if (el.closest(BANNED)) return false;
	if (!menuOpen()) return true;
	return Boolean(el.closest("#site-menu, [data-menu-button]"));
}

function radiusOf(el: HTMLElement): number {
	const raw = Number.parseFloat(getComputedStyle(el).borderTopLeftRadius);
	return Number.isFinite(raw) ? raw : 0;
}

function readBox(target: Target, now: number): void {
	const el = target.el;
	target.measured = now;
	if (!el.isConnected) {
		target.onScreen = false;
		return;
	}
	const style = getComputedStyle(el);
	if (style.display === "none" || style.visibility === "hidden") {
		target.onScreen = false;
		target.w = 0;
		return;
	}
	const box = el.getBoundingClientRect();
	target.x = box.left;
	target.y = box.top;
	target.w = box.width;
	target.h = box.height;
	target.radius = radiusOf(el);
	const seen = box.bottom > 0 && box.top < window.innerHeight && box.right > 0 && box.left < window.innerWidth;
	target.onScreen = seen && box.width > 8 && box.height > 1.5;
}

function clampRadius(target: Target): number {
	return Math.max(0, Math.min(target.radius, target.w / 2, target.h / 2));
}

function pathLength(target: Target): number {
	if (target.kind === "rule" || target.kind === "underline") return Math.max(target.w, 1);
	const r = clampRadius(target);
	const top = Math.max(0, target.w - 2 * r);
	const side = Math.max(0, target.h - 2 * r);
	const arc = r > 0 ? (Math.PI / 2) * r : 0;
	return 2 * (top + side) + 4 * arc;
}

function pointAt(target: Target, dist: number): { x: number; y: number } {
	if (target.kind === "rule" || target.kind === "underline") {
		const len = Math.max(target.w, 1);
		const d = ((dist % len) + len) % len;
		const y = target.kind === "underline" ? target.y + target.h - 0.5 : target.y + target.h * 0.5;
		return { x: target.x + d, y };
	}
	const r = clampRadius(target);
	const top = Math.max(0, target.w - 2 * r);
	const side = Math.max(0, target.h - 2 * r);
	const arc = r > 0 ? (Math.PI / 2) * r : 0;
	const total = 2 * (top + side) + 4 * arc || 1;
	let d = ((dist % total) + total) % total;
	const x0 = target.x;
	const y0 = target.y;
	const w = target.w;
	const h = target.h;

	const take = (len: number): number | null => {
		if (len <= 0) return null;
		if (d <= len) return d;
		d -= len;
		return null;
	};

	const alongTop = take(top);
	if (alongTop !== null) return { x: x0 + r + alongTop, y: y0 };
	const cornerTR = take(arc);
	if (cornerTR !== null) {
		const ang = -Math.PI / 2 + (cornerTR / arc) * (Math.PI / 2);
		return { x: x0 + w - r + Math.cos(ang) * r, y: y0 + r + Math.sin(ang) * r };
	}
	const alongRight = take(side);
	if (alongRight !== null) return { x: x0 + w, y: y0 + r + alongRight };
	const cornerBR = take(arc);
	if (cornerBR !== null) {
		const ang = (cornerBR / arc) * (Math.PI / 2);
		return { x: x0 + w - r + Math.cos(ang) * r, y: y0 + h - r + Math.sin(ang) * r };
	}
	const alongBottom = take(top);
	if (alongBottom !== null) return { x: x0 + w - r - alongBottom, y: y0 + h };
	const cornerBL = take(arc);
	if (cornerBL !== null) {
		const ang = Math.PI / 2 + (cornerBL / arc) * (Math.PI / 2);
		return { x: x0 + r + Math.cos(ang) * r, y: y0 + h - r + Math.sin(ang) * r };
	}
	const alongLeft = take(side);
	if (alongLeft !== null) return { x: x0, y: y0 + h - r - alongLeft };
	const cornerTL = arc > 0 ? d / arc : 0;
	const ang = Math.PI + cornerTL * (Math.PI / 2);
	return { x: x0 + r + Math.cos(ang) * r, y: y0 + r + Math.sin(ang) * r };
}

function fadeOf(age: number, life: number): number {
	if (age < FADE) return smooth(age / FADE);
	if (age > life - FADE) return smooth((life - age) / FADE);
	return 1;
}

function compile(gl: WebGLRenderingContext, type: number, source: string): WebGLShader | null {
	const shader = gl.createShader(type);
	if (!shader) return null;
	gl.shaderSource(shader, source);
	gl.compileShader(shader);
	if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
		gl.deleteShader(shader);
		return null;
	}
	return shader;
}

function mountGl(surface: HTMLCanvasElement): GlBundle | null {
	const gl = surface.getContext("webgl", {
		alpha: true,
		antialias: false,
		depth: false,
		stencil: false,
		premultipliedAlpha: true,
		powerPreference: "low-power",
	});
	if (!gl) return null;
	const vert = compile(gl, gl.VERTEX_SHADER, VERT);
	const frag = compile(gl, gl.FRAGMENT_SHADER, FRAG);
	if (!vert || !frag) return null;
	const program = gl.createProgram();
	const buffer = gl.createBuffer();
	if (!program || !buffer) return null;
	gl.attachShader(program, vert);
	gl.attachShader(program, frag);
	gl.bindAttribLocation(program, 0, "a_pos");
	gl.bindAttribLocation(program, 1, "a_size");
	gl.bindAttribLocation(program, 2, "a_alpha");
	gl.bindAttribLocation(program, 3, "a_color");
	gl.linkProgram(program);
	gl.deleteShader(vert);
	gl.deleteShader(frag);
	if (!gl.getProgramParameter(program, gl.LINK_STATUS)) return null;
	gl.useProgram(program);
	gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
	gl.bufferData(gl.ARRAY_BUFFER, data.byteLength, gl.DYNAMIC_DRAW);
	const stride = STRIDE * 4;
	gl.enableVertexAttribArray(0);
	gl.vertexAttribPointer(0, 2, gl.FLOAT, false, stride, 0);
	gl.enableVertexAttribArray(1);
	gl.vertexAttribPointer(1, 1, gl.FLOAT, false, stride, 8);
	gl.enableVertexAttribArray(2);
	gl.vertexAttribPointer(2, 1, gl.FLOAT, false, stride, 12);
	gl.enableVertexAttribArray(3);
	gl.vertexAttribPointer(3, 3, gl.FLOAT, false, stride, 16);
	gl.enable(gl.BLEND);
	gl.blendFunc(gl.ONE, gl.ONE);
	return {
		gl,
		program,
		buffer,
		resolution: gl.getUniformLocation(program, "u_resolution"),
		lose: gl.getExtension("WEBGL_lose_context"),
	};
}

function fitCanvas(): void {
	if (!canvas || !gpu) return;
	dpr = phone() ? 1 : Math.min(1.5, window.devicePixelRatio || 1);
	const width = Math.max(1, Math.round(window.innerWidth * dpr));
	const height = Math.max(1, Math.round(window.innerHeight * dpr));
	if (canvas.width !== width || canvas.height !== height) {
		canvas.width = width;
		canvas.height = height;
	}
	gpu.gl.viewport(0, 0, width, height);
	gpu.gl.uniform2f(gpu.resolution, window.innerWidth, window.innerHeight);
}

function publish(mode: string): void {
	if (!canvas) return;
	canvas.dataset.tracerMode = mode;
	canvas.dataset.tracerAlive = String(alive.length);
	canvas.dataset.tracerRed = alive.some((tracer) => tracer.red) ? "1" : "0";
	if (frameSamples > 0) {
		canvas.dataset.tracerMs = (frameMs / frameSamples).toFixed(3);
	}
}

function clearFrame(): void {
	if (!gpu || !canvas) return;
	const gl = gpu.gl;
	gl.clearColor(0, 0, 0, 0);
	gl.clear(gl.COLOR_BUFFER_BIT);
}

function pushPoint(index: number, x: number, y: number, size: number, alpha: number, color: Rgb): number {
	if (index >= MAX_POINTS) return index;
	const offset = index * STRIDE;
	data[offset] = x;
	data[offset + 1] = y;
	data[offset + 2] = size * dpr;
	data[offset + 3] = alpha;
	data[offset + 4] = color[0];
	data[offset + 5] = color[1];
	data[offset + 6] = color[2];
	return index + 1;
}

function writeTracer(tracer: Tracer, fade: number, index: number, now: number): number {
	const target = tracer.target;
	if (now - target.measured > 280) readBox(target, now);
	if (target.w < 8) return index;
	const length = pathLength(target);
	const tail = Math.min(tracer.tail, Math.max(18, length * 0.85));
	const steps = Math.max(6, Math.min(36, Math.round(tail / 4)));
	const head = tracer.red ? RED : WHITE;
	const near = tracer.red ? RED : BONE;
	const far = tracer.red ? EMBER : ASH;
	for (let step = steps; step >= 1; step -= 1) {
		const t = step / steps;
		const point = pointAt(target, tracer.distance - tail * t);
		const color: Rgb = [
			near[0] + (far[0] - near[0]) * t,
			near[1] + (far[1] - near[1]) * t,
			near[2] + (far[2] - near[2]) * t,
		];
		const alpha = fade * (1 - t) * (1 - t) * 0.22;
		index = pushPoint(index, point.x, point.y, 5 + (1 - t) * 6, alpha, color);
	}
	const headPoint = pointAt(target, tracer.distance);
	return pushPoint(index, headPoint.x, headPoint.y, 13, fade * 0.42, head);
}

function draw(now: number): void {
	if (!gpu) return;
	const gl = gpu.gl;
	gl.clearColor(0, 0, 0, 0);
	gl.clear(gl.COLOR_BUFFER_BIT);
	let index = 0;
	for (const tracer of alive) {
		const age = (now - tracer.born) / 1000;
		const fade = fadeOf(age, tracer.life);
		if (fade <= 0.01) continue;
		index = writeTracer(tracer, fade, index, now);
	}
	if (index === 0) return;
	gl.bufferSubData(gl.ARRAY_BUFFER, 0, data.subarray(0, index * STRIDE));
	gl.drawArrays(gl.POINTS, 0, index);
}

function paintGlint(): void {
	if (!gpu || !canvas) return;
	fitCanvas();
	const now = performance.now();
	const picks = targets.filter((target) => target.onScreen && (target.kind === "rule" || target.kind === "underline" || target.kind === "outline")).slice(0, 2);
	const gl = gpu.gl;
	gl.clearColor(0, 0, 0, 0);
	gl.clear(gl.COLOR_BUFFER_BIT);
	let index = 0;
	for (const target of picks) {
		readBox(target, now);
		if (!target.onScreen) continue;
		const point = pointAt(target, pathLength(target) * 0.35);
		index = pushPoint(index, point.x, point.y, 10, 0.34, BONE);
	}
	if (index > 0) {
		gl.bufferSubData(gl.ARRAY_BUFFER, 0, data.subarray(0, index * STRIDE));
		gl.drawArrays(gl.POINTS, 0, index);
	}
	publish("reduced");
}

function redAllowed(): boolean {
	return !alive.some((tracer) => tracer.red);
}

function anyVisibleAlive(): boolean {
	return alive.some((tracer) => tracer.target.onScreen && tracer.target.w > 8);
}

function spawn(now: number): void {
	if (alive.length >= cap()) {
		nextSpawn = now + rand(phone() ? 4200 : 2800, phone() ? 7000 : 5200);
		return;
	}
	const pool = targets.filter((target) => {
		if (!target.onScreen || !allowed(target.el)) return false;
		if (now < target.restUntil) return false;
		if (target.w < 8) return false;
		return !alive.some((tracer) => tracer.target === target);
	});
	if (pool.length === 0) {
		nextSpawn = now + rand(1600, 3200);
		return;
	}
	const target = pool[Math.floor(Math.random() * pool.length)]!;
	readBox(target, now);
	if (!target.onScreen) {
		nextSpawn = now + rand(1600, 3200);
		return;
	}
	const red = target.hot && redAllowed() && Math.random() < 1 / 12;
	const length = pathLength(target);
	alive.push({
		target,
		distance: Math.random() * length,
		speed: rand(phone() ? 18 : 22, phone() ? 40 : 58),
		tail: rand(40, 120),
		born: now,
		life: rand(6.5, 10.5),
		red,
	});
	nextSpawn = now + rand(phone() ? 4200 : 2800, phone() ? 7000 : 5200);
}

function step(now: number): void {
	if (menuOpen()) {
		alive = alive.filter((tracer) => allowed(tracer.target.el));
	}
	for (let i = alive.length - 1; i >= 0; i -= 1) {
		const tracer = alive[i]!;
		const age = (now - tracer.born) / 1000;
		if (age >= tracer.life) {
			tracer.target.restUntil = now + rand(12000, 24000);
			alive.splice(i, 1);
			continue;
		}
		const pace = 0.72 + 0.28 * Math.sin(Math.PI * (age / tracer.life));
		const dt = Math.min(0.05, (now - lastFrame) / 1000);
		tracer.distance += tracer.speed * pace * dt;
	}
	if (now >= nextSpawn) spawn(now);
}

function frame(now: number): void {
	raf = 0;
	if (!running || reduced || document.hidden) return;
	const started = performance.now();
	if (lastFrame === 0) lastFrame = now;
	step(now);
	const drawing = anyVisibleAlive();
	if (drawing) draw(now);
	else clearFrame();
	lastFrame = now;
	const cost = performance.now() - started;
	frameMs += cost;
	frameSamples += 1;
	publish(gpu ? "webgl" : "css");
	if (!drawing) {
		scheduleWake();
		return;
	}
	raf = requestAnimationFrame(frame);
}

function kick(): void {
	if (!running || reduced || document.hidden || raf) return;
	if (!anyVisibleAlive()) {
		scheduleWake();
		return;
	}
	if (wake) {
		window.clearTimeout(wake);
		wake = 0;
	}
	lastFrame = 0;
	raf = requestAnimationFrame(frame);
}

function scheduleWake(): void {
	if (wake || raf || !running || reduced || document.hidden) return;
	const delay = Math.max(400, nextSpawn - performance.now());
	wake = window.setTimeout(() => {
		wake = 0;
		if (!running || reduced || document.hidden) return;
		const now = performance.now();
		if (lastFrame === 0) lastFrame = now;
		if (alive.length > 0) step(now);
		else if (targets.some((target) => target.onScreen)) spawn(now);
		lastFrame = now;
		if (anyVisibleAlive()) kick();
		else scheduleWake();
	}, delay);
}

function stopLoop(): void {
	if (raf) cancelAnimationFrame(raf);
	raf = 0;
	if (wake) window.clearTimeout(wake);
	wake = 0;
}

function measureVisible(): void {
	measureQueued = false;
	const now = performance.now();
	for (const target of targets) {
		if (!target.onScreen && !alive.some((tracer) => tracer.target === target)) continue;
		readBox(target, now);
	}
	if (reduced) paintGlint();
	else if (anyVisibleAlive()) kick();
}

function queueMeasure(): void {
	if (measureQueued) return;
	measureQueued = true;
	requestAnimationFrame(measureVisible);
}

function bindScroll(): void {
	unbindScroll();
	const lenis = getLenis();
	if (lenis) {
		const off = lenis.on("scroll", queueMeasure);
		unlistenLenis = typeof off === "function" ? off : null;
		return;
	}
	window.addEventListener("scroll", queueMeasure, { passive: true });
	scrollListening = true;
}

function unbindScroll(): void {
	unlistenLenis?.();
	unlistenLenis = null;
	if (scrollListening) window.removeEventListener("scroll", queueMeasure);
	scrollListening = false;
}

function collect(): Target[] {
	const found: Target[] = [];
	document.querySelectorAll<HTMLElement>("[data-tracer]").forEach((el) => {
		if (!allowed(el)) return;
		found.push({
			el,
			kind: kindOf(el.dataset.tracer ?? null),
			hot: el.hasAttribute("data-tracer-hot"),
			onScreen: false,
			x: 0,
			y: 0,
			w: 0,
			h: 0,
			radius: 0,
			restUntil: 0,
			measured: 0,
		});
	});
	return found;
}

function watchTargets(): void {
	resizeObserver?.disconnect();
	intersectionObserver?.disconnect();
	resizeObserver = new ResizeObserver((entries) => {
		const now = performance.now();
		for (const entry of entries) {
			const target = targets.find((item) => item.el === entry.target);
			if (target) readBox(target, now);
		}
		if (reduced) paintGlint();
	});
	intersectionObserver = new IntersectionObserver(
		(entries) => {
			const now = performance.now();
			for (const entry of entries) {
				const target = targets.find((item) => item.el === entry.target);
				if (!target) continue;
				target.onScreen = entry.isIntersecting;
				if (entry.isIntersecting) readBox(target, now);
			}
			if (reduced) paintGlint();
			else if (anyVisibleAlive()) kick();
			else if (alive.length === 0) scheduleWake();
		},
		{ rootMargin: "40px" },
	);
	for (const target of targets) {
		resizeObserver.observe(target.el);
		intersectionObserver.observe(target.el);
	}
}

function onVisibility(): void {
	if (document.hidden) {
		stopLoop();
		return;
	}
	if (reduced) paintGlint();
	else kick();
}

function onResize(): void {
	fitCanvas();
	queueMeasure();
}

function mountFallback(): void {
	const ranked = [...targets].sort((a, b) => Number(b.hot) - Number(a.hot));
	const picks = ranked.filter((target) => target.kind !== "edge").slice(0, 3);
	const chosen = picks.length > 0 ? picks : ranked.slice(0, 2);
	for (const target of chosen) {
		const el = target.el;
		const previous = el.style.position;
		if (getComputedStyle(el).position === "static") el.style.position = "relative";
		const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
		svg.setAttribute("class", "ah-tracer-fallback");
		svg.setAttribute("aria-hidden", "true");
		svg.setAttribute("viewBox", "0 0 100 100");
		svg.setAttribute("preserveAspectRatio", "none");
		svg.dataset.previousPosition = previous;
		svg.style.cssText = "position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible;opacity:0.7";
		const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
		rect.setAttribute("x", "1");
		rect.setAttribute("y", "1");
		rect.setAttribute("width", "98");
		rect.setAttribute("height", "98");
		rect.setAttribute("fill", "none");
		rect.setAttribute("stroke", "#ECE8E1");
		rect.setAttribute("stroke-width", "1.5");
		rect.setAttribute("vector-effect", "non-scaling-stroke");
		rect.setAttribute("pathLength", "100");
		rect.setAttribute("stroke-dasharray", "2.5 97.5");
		rect.setAttribute("stroke-linecap", "round");
		const motion = document.createElementNS("http://www.w3.org/2000/svg", "animate");
		motion.setAttribute("attributeName", "stroke-dashoffset");
		motion.setAttribute("from", "0");
		motion.setAttribute("to", "-100");
		motion.setAttribute("dur", "18s");
		motion.setAttribute("repeatCount", "indefinite");
		rect.append(motion);
		svg.append(rect);
		el.append(svg);
	}
	if (canvas) canvas.dataset.tracerMode = "css";
}

function clearFallback(): void {
	document.querySelectorAll<SVGElement>(".ah-tracer-fallback").forEach((node) => {
		const host = node.parentElement;
		if (host && node.dataset.previousPosition === "") host.style.position = "";
		node.remove();
	});
}

function applyMotion(next: boolean): void {
	reduced = next;
	stopLoop();
	alive = [];
	if (!running) return;
	if (reduced) {
		if (gpu) paintGlint();
		return;
	}
	clearFrame();
	nextSpawn = performance.now() + rand(700, 1400);
	scheduleWake();
}

function mount(): void {
	running = true;
	reduced = prefersReducedMotion();
	targets = collect();
	alive = [];
	if (targets.length === 0) {
		running = false;
		return;
	}
	canvas = document.createElement("canvas");
	canvas.className = "ah-tracers";
	canvas.setAttribute("aria-hidden", "true");
	canvas.style.cssText = "position:fixed;inset:0;width:100%;height:100%;display:block;pointer-events:none;z-index:45;";
	document.documentElement.append(canvas);
	gpu = mountGl(canvas);
	if (!gpu) {
		canvas.dataset.tracerMode = "css";
		if (!reduced) mountFallback();
		else canvas.dataset.tracerMode = "reduced";
	} else {
		fitCanvas();
	}
	watchTargets();
	bindScroll();
	const now = performance.now();
	for (const target of targets) readBox(target, now);
	if (reduced && gpu) paintGlint();
	stopReduced = onReducedMotionChange(applyMotion);
	menuObserver = new MutationObserver(() => {
		if (menuOpen()) alive = alive.filter((tracer) => allowed(tracer.target.el));
		if (reduced) paintGlint();
	});
	menuObserver.observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });
	window.addEventListener("resize", onResize);
	document.addEventListener("visibilitychange", onVisibility);
	if (!reduced && gpu) {
		nextSpawn = now + rand(700, 1400);
		scheduleWake();
	}
}

export function destroyTracers(): void {
	running = false;
	stopLoop();
	stopReduced?.();
	stopReduced = null;
	resizeObserver?.disconnect();
	resizeObserver = null;
	intersectionObserver?.disconnect();
	intersectionObserver = null;
	menuObserver?.disconnect();
	menuObserver = null;
	unbindScroll();
	window.removeEventListener("resize", onResize);
	document.removeEventListener("visibilitychange", onVisibility);
	clearFallback();
	gpu?.lose?.loseContext();
	gpu = null;
	canvas?.remove();
	canvas = null;
	targets = [];
	alive = [];
	frameMs = 0;
	frameSamples = 0;
	lastFrame = 0;
}

export function bootTracers(): void {
	if (typeof window === "undefined") return;
	if (running && canvas?.isConnected) return;
	destroyTracers();
	mount();
}
