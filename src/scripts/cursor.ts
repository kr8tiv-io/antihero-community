/**
 * Desktop cursor, magnetic pull, and the email-submit check.
 * No import-time side effects: nav.ts and prompt-cards.ts call setSwapText.
 * The ring is appended to documentElement so a view transition can replace body.
 * Hero.astro and JoinBand.astro stay untouched. bootCursor stamps them.
 */

import { gsap, onReducedMotionChange, prefersReducedMotion } from "./motion";

const FINE = "(hover: hover) and (pointer: fine)";
const LERP = 0.2;
const MAGNET = 8;
const SETTLE = 0.35;

const JOIN =
	".desk-nav__join, .menu-join, .join-go, .site-footer__group, .join-button, .hero-join";

type Magnet = { x: number; y: number; tx: number; ty: number };

let listening = false;
let loopOn = false;
let raf = 0;
let enabled = false;
let visible = false;
let primed = false;
let overField = false;
let dialogBlocked = false;
let label = "";
let pointerX = 0;
let pointerY = 0;
let ringX = 0;
let ringY = 0;
let currentMagnet: HTMLElement | null = null;
let cursorEl: HTMLElement | null = null;
let wordEl: HTMLElement | null = null;

const magnets = new Set<HTMLElement>();
const magnetState = new WeakMap<HTMLElement, Magnet>();

/** Write every duplicate label line. Falls back when a control has no slide yet. */
export function setSwapText(root: ParentNode, text: string): void {
	const lines = root.querySelectorAll<HTMLElement>(".swap-label__line");
	if (lines.length === 0) {
		if (root instanceof HTMLElement) root.textContent = text;
		return;
	}
	lines.forEach((line) => {
		line.textContent = text;
	});
}

export function bootCursor(): void {
	stamp();
	upgradeProtected();
	refreshDialog();
	applyMode();
	if (listening || typeof window === "undefined") return;
	listening = true;
	buildCursor();
	applyMode();

	document.addEventListener("pointermove", onPointerMove, { passive: true });
	document.addEventListener("pointerdown", onPointerMove, { passive: true });
	document.documentElement.addEventListener("pointerleave", onPointerLeave);
	document.addEventListener("pointercancel", onPointerLeave);
	document.addEventListener("toggle", onToggle, true);
	document.addEventListener("submit", onSubmit);
	window.matchMedia(FINE).addEventListener("change", applyMode);
	onReducedMotionChange(applyMode);
}

/** Drop magnetic offsets on persisted header and footer before the swap. */
export function releaseCursorMotion(): void {
	currentMagnet = null;
	for (const el of magnets) {
		if (!gsap.isTweening(el)) el.style.transform = "";
	}
	magnets.clear();
}

function stamp(): void {
	mark("[data-door]", "Go in", false);
	mark(".guide-card__link", "Read", false);
	mark("[data-copy]", "Copy", true);
	mark("[data-video-card] .video-hit, [data-video-open]", "Play", false);
	mark(JOIN, "Join", true);
}

function mark(selector: string, word: string, magnetic: boolean): void {
	document.querySelectorAll<HTMLElement>(selector).forEach((el) => {
		el.dataset.cursor = word;
		if (magnetic) el.dataset.magnetic = "true";
	});
}

function upgradeProtected(): void {
	document.querySelectorAll<HTMLElement>(".hero-join, .join-button").forEach(upgradeSwap);
}

function upgradeSwap(el: HTMLElement): void {
	if (el.querySelector(":scope > .swap-label")) return;
	const hidden = [...el.querySelectorAll<HTMLElement>(":scope > .visually-hidden")];
	for (const node of hidden) node.remove();
	const text = (el.textContent ?? "").replace(/\s+/g, " ").trim();
	el.replaceChildren();
	const wrap = document.createElement("span");
	wrap.className = "swap-label";
	const first = document.createElement("span");
	first.className = "swap-label__line";
	first.textContent = text;
	const second = document.createElement("span");
	second.className = "swap-label__line";
	second.setAttribute("aria-hidden", "true");
	second.textContent = text;
	wrap.append(first, second);
	el.append(wrap);
	for (const node of hidden) el.append(node);
}

function buildCursor(): void {
	if (cursorEl?.isConnected) return;
	const root = document.createElement("div");
	root.className = "ah-cursor";
	root.setAttribute("aria-hidden", "true");
	const ring = document.createElement("span");
	ring.className = "ah-cursor__ring";
	const word = document.createElement("span");
	word.className = "ah-cursor__word";
	root.append(ring, word);
	document.documentElement.append(root);
	cursorEl = root;
	wordEl = word;
}

function applyMode(): void {
	const fine = window.matchMedia(FINE).matches;
	enabled = fine && !prefersReducedMotion();
	if (!enabled) {
		visible = false;
		overField = false;
		label = "";
		if (wordEl) wordEl.textContent = "";
		releaseCursorMotion();
	}
	paintCursor();
}

function paintCursor(): void {
	const show = enabled && visible && !overField && !dialogBlocked;
	document.documentElement.classList.toggle("ah-use-cursor", enabled && !dialogBlocked);
	document.documentElement.classList.toggle("ah-cursor-field", show ? false : overField && enabled);
	cursorEl?.classList.toggle("is-on", show);
	cursorEl?.classList.toggle("is-hot", show && label.length > 0);
}

function onPointerMove(event: PointerEvent): void {
	if (!enabled || event.pointerType === "touch") {
		if (event.pointerType === "touch") {
			visible = false;
			paintCursor();
		}
		return;
	}
	pointerX = event.clientX;
	pointerY = event.clientY;
	if (!primed) {
		ringX = pointerX;
		ringY = pointerY;
		primed = true;
	}
	visible = true;
	syncHit(event.clientX, event.clientY);
	start();
}

function onPointerLeave(): void {
	visible = false;
	releaseMagnet();
	paintCursor();
	start();
}

function onToggle(event: Event): void {
	if (!(event.target instanceof HTMLDialogElement)) return;
	refreshDialog();
	if (dialogBlocked) releaseMagnet();
	paintCursor();
}

function refreshDialog(): void {
	dialogBlocked = document.querySelector("dialog[open]") !== null;
}

function syncHit(x: number, y: number): void {
	const hit = document.elementFromPoint(x, y);
	const field = hit?.closest("input, textarea, select, [contenteditable='true']");
	overField = field instanceof Element;
	const next = hit?.closest<HTMLElement>("[data-cursor]")?.dataset.cursor ?? "";
	if (next !== label) {
		label = next;
		if (wordEl) wordEl.textContent = next;
	}
	const magnet = hit?.closest<HTMLElement>("[data-magnetic]") ?? null;
	if (magnet !== currentMagnet) {
		if (currentMagnet) park(currentMagnet);
		currentMagnet = magnet;
	}
	paintCursor();
}

function park(el: HTMLElement): void {
	const state = magnetState.get(el);
	if (!state) return;
	state.tx = 0;
	state.ty = 0;
	magnets.add(el);
}

function releaseMagnet(): void {
	if (currentMagnet) park(currentMagnet);
	currentMagnet = null;
}

function ensure(el: HTMLElement): Magnet {
	let state = magnetState.get(el);
	if (!state) {
		state = { x: 0, y: 0, tx: 0, ty: 0 };
		magnetState.set(el, state);
	}
	return state;
}

function aim(el: HTMLElement, x: number, y: number): void {
	if (gsap.isTweening(el)) return;
	const state = ensure(el);
	const rect = el.getBoundingClientRect();
	const cx = rect.left + rect.width / 2 - state.x;
	const cy = rect.top + rect.height / 2 - state.y;
	let dx = x - cx;
	let dy = y - cy;
	const dist = Math.hypot(dx, dy);
	if (dist > MAGNET && dist > 0) {
		dx = (dx / dist) * MAGNET;
		dy = (dy / dist) * MAGNET;
	}
	state.tx = dx;
	state.ty = dy;
	magnets.add(el);
}

function start(): void {
	if (loopOn) return;
	loopOn = true;
	raf = requestAnimationFrame(frame);
}

function frame(): void {
	if (enabled && currentMagnet && visible && !dialogBlocked) {
		aim(currentMagnet, pointerX, pointerY);
	}

	const dx = pointerX - ringX;
	const dy = pointerY - ringY;
	ringX += dx * LERP;
	ringY += dy * LERP;
	if (cursorEl) {
		cursorEl.style.transform = `translate3d(${ringX}px, ${ringY}px, 0)`;
	}

	let moving = Math.hypot(dx, dy) > SETTLE;
	for (const el of [...magnets]) {
		const state = magnetState.get(el);
		if (!state || !el.isConnected) {
			magnets.delete(el);
			continue;
		}
		if (gsap.isTweening(el)) {
			moving = true;
			continue;
		}
		state.x += (state.tx - state.x) * LERP;
		state.y += (state.ty - state.y) * LERP;
		const left = Math.hypot(state.tx - state.x, state.ty - state.y);
		const home = Math.hypot(state.tx, state.ty) < SETTLE && left < SETTLE;
		if (home) {
			state.x = 0;
			state.y = 0;
			el.style.transform = "";
			magnets.delete(el);
		} else {
			el.style.transform = `translate3d(${state.x.toFixed(2)}px, ${state.y.toFixed(2)}px, 0)`;
			moving = true;
		}
	}

	if (moving && loopOn) raf = requestAnimationFrame(frame);
	else {
		loopOn = false;
		raf = 0;
	}
}

function onSubmit(event: Event): void {
	const form = event.target;
	if (!(form instanceof HTMLFormElement) || !form.classList.contains("email-form")) return;
	if (form.dataset.sending === "1") {
		event.preventDefault();
		return;
	}
	if (!form.checkValidity()) return;
	event.preventDefault();
	form.dataset.sending = "1";
	const button = form.querySelector<HTMLButtonElement>(".email-form__submit");
	button?.classList.add("is-sent");
	const wait = prefersReducedMotion() ? 80 : 420;
	window.setTimeout(() => {
		if (!form.isConnected) return;
		form.submit();
	}, wait);
}
