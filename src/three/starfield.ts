/**
 * A wide field of tiny points drifting toward the camera.
 * Original shader. Nothing here is copied from another site.
 *
 * Camera looks down -z. Tilt is written only as camera.rotation:
 * mouse above center sets rotation.x positive, which pitches the look
 * direction up (+y). Mouse to the right sets rotation.y negative, which
 * yaws the look direction toward +x (screen right while unpitched).
 * Checked with getWorldDirection: yaw -2deg => dir.x > 0, pitch +2deg => dir.y > 0.
 */

import * as THREE from "three";

const COUNT = 1500;
const MAX_DPR = 1.5;
const MAX_TILT = (2 * Math.PI) / 180;
const RED_SHARE = 0.03;

const WHITE = [1, 1, 1];
const BONE = [236 / 255, 232 / 255, 225 / 255];
const RED = [224 / 255, 38 / 255, 30 / 255];

const VERT = /* glsl */ `
attribute float aSeed;
attribute float aSize;
attribute vec3 aColor;
uniform float uTime;
uniform float uWarp;
varying vec3 vColor;
varying float vWarp;

void main() {
	vec3 pos = position;
	float span = 38.0;
	float speed = 0.42 + aSeed * 0.7;
	float travel = uTime * speed * (1.0 + uWarp * 2.4);
	pos.z = mod(pos.z + span + travel, span) - span;

	vec4 mv = modelViewMatrix * vec4(pos, 1.0);
	gl_Position = projectionMatrix * mv;

	float dist = max(-mv.z, 0.25);
	gl_PointSize = clamp(aSize * (20.0 / dist), 1.0, 3.1);

	vColor = aColor;
	vWarp = uWarp;
}
`;

const FRAG = /* glsl */ `
precision mediump float;
uniform vec2 uResolution;
varying vec3 vColor;
varying float vWarp;

void main() {
	vec2 p = gl_PointCoord - vec2(0.5);
	vec2 fromCenter = gl_FragCoord.xy - uResolution * 0.5;
	float span = length(fromCenter);
	vec2 axis = span > 1.0 ? fromCenter / span : vec2(0.0, 1.0);
	float along = dot(p, axis);
	float across = dot(p, vec2(-axis.y, axis.x));
	along /= 1.0 + vWarp * 8.0;
	float disc = length(vec2(along, across));
	float alpha = smoothstep(0.5, 0.08, disc);
	if (alpha < 0.015) discard;
	gl_FragColor = vec4(vColor, alpha * 0.72);
}
`;

export type StarfieldStats = {
	frameMs: number;
	gpuBytes: number;
	points: number;
	paused: boolean;
	antialias: boolean;
	pixelRatio: number;
	depth: boolean;
	cover: number;
	opacity: number;
	tiltX: number;
	tiltY: number;
	warp: number;
};

type CanvasStats = HTMLCanvasElement & { __ah?: StarfieldStats };

export function createStarfield(path: string): { destroy: () => void; path: string } | null {
	const canvas = document.createElement("canvas");
	canvas.className = "ah-starfield";
	canvas.setAttribute("aria-hidden", "true");
	canvas.style.opacity = "0";

	let renderer: THREE.WebGLRenderer;
	try {
		renderer = new THREE.WebGLRenderer({
			canvas,
			antialias: false,
			alpha: true,
			depth: false,
			stencil: false,
			powerPreference: "high-performance",
			premultipliedAlpha: false,
			failIfMajorPerformanceCaveat: true,
		});
	} catch {
		return null;
	}

	renderer.setClearColor(0x000000, 0);
	renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, MAX_DPR));
	document.documentElement.append(canvas);

	const scene = new THREE.Scene();
	const camera = new THREE.PerspectiveCamera(58, 1, 0.1, 70);
	camera.position.set(0, 0, 0);

	const geometry = new THREE.BufferGeometry();
	const positions = new Float32Array(COUNT * 3);
	const colors = new Float32Array(COUNT * 3);
	const seeds = new Float32Array(COUNT);
	const sizes = new Float32Array(COUNT);
	const rand = mulberry32(0x51a7);

	for (let i = 0; i < COUNT; i++) {
		positions[i * 3] = (rand() - 0.5) * 30;
		positions[i * 3 + 1] = (rand() - 0.5) * 18;
		positions[i * 3 + 2] = -1.2 - rand() * 36;
		const tint = rand() < RED_SHARE ? RED : rand() < 0.5 ? BONE : WHITE;
		colors[i * 3] = tint[0];
		colors[i * 3 + 1] = tint[1];
		colors[i * 3 + 2] = tint[2];
		seeds[i] = rand();
		sizes[i] = 1.15 + rand() * 1.15;
	}

	geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
	geometry.setAttribute("aColor", new THREE.BufferAttribute(colors, 3));
	geometry.setAttribute("aSeed", new THREE.BufferAttribute(seeds, 1));
	geometry.setAttribute("aSize", new THREE.BufferAttribute(sizes, 1));

	const uniforms = {
		uTime: { value: 0 },
		uWarp: { value: 0 },
		uResolution: { value: new THREE.Vector2(1, 1) },
	};

	const material = new THREE.ShaderMaterial({
		uniforms,
		vertexShader: VERT,
		fragmentShader: FRAG,
		transparent: true,
		depthTest: false,
		depthWrite: false,
		toneMapped: false,
	});

	scene.add(new THREE.Points(geometry, material));

	let dead = false;
	let looping = false;
	let raf = 0;
	let last = performance.now();
	let elapsed = 0;
	let opacity = 0;
	let coverTarget = 0;
	let warp = 0;
	let warpTarget = 0;
	let tiltX = 0;
	let tiltY = 0;
	let aimX = 0;
	let aimY = 0;
	let frameAvg = 0;
	let frames = 0;
	let ratioCap = MAX_DPR;
	let lastScroll = window.scrollY;
	let lastScrollAt = performance.now();
	let sampleTimer = 0;

	const resize = (): void => {
		const w = Math.max(window.innerWidth, 1);
		const h = Math.max(window.innerHeight, 1);
		renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, ratioCap));
		renderer.setSize(w, h, false);
		camera.aspect = w / h;
		camera.updateProjectionMatrix();
		uniforms.uResolution.value.set(renderer.domElement.width, renderer.domElement.height);
	};

	const publish = (frameMs: number, paused: boolean): void => {
		const gl = renderer.getContext();
		const attrs = gl.getContextAttributes();
		const colorBytes = gl.drawingBufferWidth * gl.drawingBufferHeight * 4;
		const geomBytes = COUNT * (3 + 3 + 1 + 1) * 4;
		const stats: StarfieldStats = {
			frameMs,
			gpuBytes: colorBytes + geomBytes,
			points: COUNT,
			paused,
			antialias: attrs?.antialias ?? true,
			pixelRatio: renderer.getPixelRatio(),
			depth: attrs?.depth ?? true,
			cover: coverTarget,
			opacity,
			tiltX: camera.rotation.x,
			tiltY: camera.rotation.y,
			warp,
		};
		(canvas as CanvasStats).__ah = stats;
	};

	const loop = (now: number): void => {
		if (dead) {
			looping = false;
			return;
		}

		const dt = Math.min((now - last) / 1000, 0.05);
		last = now;
		elapsed += dt;
		warp += (warpTarget - warp) * 0.12;
		warpTarget *= 0.92;
		tiltX += (aimX - tiltX) * 0.08;
		tiltY += (aimY - tiltY) * 0.08;
		opacity += (coverTarget - opacity) * 0.08;
		canvas.style.opacity = opacity < 0.012 ? "0" : opacity.toFixed(3);

		camera.rotation.x = tiltX;
		camera.rotation.y = tiltY;
		uniforms.uTime.value = elapsed;
		uniforms.uWarp.value = warp;

		const hidden = document.hidden;
		const settled = opacity < 0.012 && coverTarget < 0.02;
		if (hidden || settled) {
			looping = false;
			publish(frameAvg, true);
			return;
		}

		const t0 = performance.now();
		renderer.render(scene, camera);
		const frameMs = performance.now() - t0;
		frameAvg = frameAvg === 0 ? frameMs : frameAvg * 0.9 + frameMs * 0.1;
		frames += 1;
		if (frames === 24 && frameAvg > 2 && ratioCap > 1) {
			ratioCap = 1;
			resize();
		}
		if (frames % 20 === 0) publish(frameAvg, false);

		raf = requestAnimationFrame(loop);
	};

	const wake = (): void => {
		if (dead || looping || document.hidden) return;
		looping = true;
		last = performance.now();
		raf = requestAnimationFrame(loop);
	};

	const sample = (): void => {
		if (dead || document.hidden) return;
		coverTarget = openFraction(canvas);
		if (coverTarget >= 0.02) wake();
	};

	const onPointer = (event: PointerEvent): void => {
		if (event.pointerType === "touch") return;
		const w = Math.max(window.innerWidth, 1);
		const h = Math.max(window.innerHeight, 1);
		const nx = (event.clientX / w) * 2 - 1;
		const ny = 1 - (event.clientY / h) * 2;
		aimY = THREE.MathUtils.clamp(-nx, -1, 1) * MAX_TILT;
		aimX = THREE.MathUtils.clamp(ny, -1, 1) * MAX_TILT;
	};

	const onLeave = (): void => {
		aimX = 0;
		aimY = 0;
	};

	const onScroll = (): void => {
		const now = performance.now();
		const dt = Math.max((now - lastScrollAt) / 1000, 0.016);
		const speed = Math.abs(window.scrollY - lastScroll) / dt;
		lastScroll = window.scrollY;
		lastScrollAt = now;
		warpTarget = Math.max(warpTarget, Math.min(speed / 2800, 1));
		sample();
		wake();
	};

	const onVisibility = (): void => {
		if (!document.hidden) {
			sample();
			wake();
		}
	};

	resize();
	window.addEventListener("pointermove", onPointer, { passive: true });
	document.documentElement.addEventListener("pointerleave", onLeave);
	window.addEventListener("scroll", onScroll, { passive: true });
	window.addEventListener("resize", resize);
	document.addEventListener("visibilitychange", onVisibility);
	sampleTimer = window.setInterval(sample, 400);
	window.setTimeout(sample, 60);
	publish(0, true);

	return {
		path,
		destroy: () => {
			dead = true;
			looping = false;
			cancelAnimationFrame(raf);
			window.clearInterval(sampleTimer);
			window.removeEventListener("pointermove", onPointer);
			document.documentElement.removeEventListener("pointerleave", onLeave);
			window.removeEventListener("scroll", onScroll);
			window.removeEventListener("resize", resize);
			document.removeEventListener("visibilitychange", onVisibility);
			geometry.dispose();
			material.dispose();
			renderer.dispose();
			renderer.forceContextLoss();
			canvas.remove();
		},
	};
}

function openFraction(canvas: HTMLCanvasElement): number {
	const w = window.innerWidth;
	const h = window.innerHeight;
	const cols = 4;
	const rows = 3;
	let open = 0;
	for (let row = 0; row < rows; row++) {
		for (let col = 0; col < cols; col++) {
			const x = ((col + 0.5) / cols) * w;
			const y = ((row + 0.5) / rows) * h;
			if (pointOpen(x, y, canvas)) open += 1;
		}
	}
	return open / (cols * rows);
}

function pointOpen(x: number, y: number, canvas: HTMLCanvasElement): boolean {
	const hit = document.elementFromPoint(x, y);
	if (!hit || hit === canvas) return true;
	let node: Element | null = hit;
	while (node && node !== document.body && node !== document.documentElement) {
		if (node.closest("[data-hero]")) return false;
		if (alphaOf(getComputedStyle(node).backgroundColor) >= 0.88) return false;
		node = node.parentElement;
	}
	return true;
}

function alphaOf(color: string): number {
	if (!color || color === "transparent") return 0;
	const parts = color
		.replace(/rgba?\(/, "")
		.replace(")", "")
		.split(/[,\s/]+/)
		.filter(Boolean);
	if (parts.length >= 4) {
		const alpha = Number(parts[3]);
		return Number.isFinite(alpha) ? alpha : 1;
	}
	return parts.length >= 3 ? 1 : 0;
}

function mulberry32(seed: number): () => number {
	let state = seed;
	return () => {
		state = (state + 0x6d2b79f5) | 0;
		let t = Math.imul(state ^ (state >>> 15), 1 | state);
		t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
		return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
	};
}
