/**
 * Hidden door. Type hero outside a field, or tap the footer wordmark
 * five times quickly on a phone. The real logo files stay as they are.
 * The hot state is a short overlay on the header and footer marks only.
 */

import { isCurrentPath } from "../data/nav";
import { duration, ease, gsap, isMobile, prefersReducedMotion } from "./motion";

const KEY = "ah-egg-hero";
const FIRST =
	"Be your own hero. You found the hidden door. There's no prize. You're just cool now.";
const AGAIN = "Back again. Respect.";
const WORD = "hero";
const LETTER_GAP = 1200;
const TAP_GAP = 650;
const TAP_WINDOW = 2400;
const TAP_NEED = 5;
const HOLD = 4000;
const PHONE = "(pointer: coarse), (max-width: 767px)";
const MARKS = "header.site-header .wordmark, .site-footer .site-footer__mark";

let listening = false;
let buffer = "";
let lastLetter = 0;
let taps = 0;
let lastTap = 0;
let tapStarted = 0;
let downX = 0;
let downY = 0;
let tracking = false;
let generation = 0;
let tween: gsap.core.Tween | null = null;
let hideTimer = 0;

export function bootEasterEgg(): void {
	if (typeof window === "undefined") return;
	armMarks();
	ensureShell();
	if (listening) return;
	listening = true;
	document.addEventListener("keydown", onKey, true);
	document.addEventListener("pointerdown", onPointerDown, true);
	document.addEventListener("click", onFooterClick, true);
}

function armMarks(): void {
	document.querySelectorAll<HTMLElement>(MARKS).forEach((mark) => {
		if (mark.querySelector(".egg-hero")) return;
		const img = mark.querySelector("img");
		if (!img) return;
		const src = img.currentSrc || img.src;
		if (!src) return;
		const layer = document.createElement("span");
		layer.className = "egg-hero";
		layer.setAttribute("aria-hidden", "true");
		const plate = document.createElement("span");
		plate.className = "egg-hero__plate";
		const clone = document.createElement("img");
		clone.src = src;
		clone.alt = "";
		clone.draggable = false;
		layer.append(plate, clone);
		mark.append(layer);
	});
}

function ensureShell(): HTMLElement {
	let box = document.querySelector<HTMLElement>(".ah-egg__box");
	if (box) return box;
	const root = document.createElement("div");
	root.className = "ah-egg";
	root.setAttribute("data-egg", "");
	root.setAttribute("aria-hidden", "true");
	box = document.createElement("p");
	box.className = "ah-egg__box";
	root.append(box);
	document.documentElement.append(root);

	const live = document.createElement("div");
	live.className = "visually-hidden";
	live.setAttribute("data-egg-live", "");
	live.setAttribute("aria-live", "polite");
	live.setAttribute("aria-atomic", "true");
	document.documentElement.append(live);

	gsap.set(box, { xPercent: -120, opacity: 0 });
	return box;
}

function onKey(event: KeyboardEvent): void {
	if (event.metaKey || event.ctrlKey || event.altKey || event.isComposing || event.repeat) return;
	if (inField(event.target)) {
		buffer = "";
		return;
	}
	const key = event.key.toLowerCase();
	if (!/^[a-z]$/.test(key)) return;
	const now = performance.now();
	if (now - lastLetter > LETTER_GAP) buffer = "";
	lastLetter = now;
	buffer = (buffer + key).slice(-WORD.length);
	if (buffer !== WORD) return;
	buffer = "";
	fire();
}

function onPointerDown(event: PointerEvent): void {
	if (!phone() || !event.isPrimary || event.button !== 0) {
		tracking = false;
		return;
	}
	tracking = !!footerMark(event.target);
	downX = event.clientX;
	downY = event.clientY;
}

function onFooterClick(event: MouseEvent): void {
	if (!phone() || event.button !== 0) return;
	if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
	const mark = footerMark(event.target);
	if (!mark) return;
	if (tracking && Math.hypot(event.clientX - downX, event.clientY - downY) > 14) {
		taps = 0;
		tracking = false;
		return;
	}
	const now = performance.now();
	const stale = now - lastTap > TAP_GAP || (taps > 0 && now - tapStarted > TAP_WINDOW);
	if (stale) taps = 0;
	if (taps === 0) tapStarted = now;
	taps += 1;
	lastTap = now;
	// A lone tap still follows the link. Extra taps in the combo do not,
	// and a phone already on Home does not reload Home under the combo.
	const here = mark instanceof HTMLAnchorElement && isCurrentPath(mark.pathname, window.location.pathname);
	if (taps >= 2 || here) {
		event.preventDefault();
		event.stopPropagation();
	}
	if (taps < TAP_NEED) return;
	taps = 0;
	fire();
}

function fire(): void {
	const text = takeMessage();
	const box = ensureShell();
	const gen = ++generation;
	box.textContent = text;
	announce(text);
	setHot(true);
	tween?.kill();
	window.clearTimeout(hideTimer);

	const reduced = prefersReducedMotion();
	const mobile = isMobile();
	const hold = (): void => {
		if (gen !== generation) return;
		hideTimer = window.setTimeout(() => {
			if (gen !== generation) return;
			hide();
		}, HOLD);
	};

	if (reduced) {
		gsap.set(box, { xPercent: 0, opacity: 1 });
		hold();
		return;
	}

	tween = gsap.fromTo(
		box,
		{ xPercent: -120, opacity: 0 },
		{
			xPercent: 0,
			opacity: 1,
			duration: mobile ? duration.ui : duration.fast,
			ease: mobile ? ease.out : ease.playful,
			overwrite: true,
			onComplete: hold,
		},
	);
}

function hide(): void {
	setHot(false);
	const box = document.querySelector<HTMLElement>(".ah-egg__box");
	if (!box) return;
	tween?.kill();
	if (prefersReducedMotion()) {
		gsap.set(box, { opacity: 0 });
		return;
	}
	tween = gsap.to(box, {
		xPercent: -120,
		opacity: 0,
		duration: isMobile() ? duration.ui : duration.fast,
		ease: ease.in,
		overwrite: true,
	});
}

function announce(text: string): void {
	const live = document.querySelector<HTMLElement>("[data-egg-live]");
	if (!live) return;
	live.textContent = "";
	window.setTimeout(() => {
		if (live.textContent === "") live.textContent = text;
	}, 40);
}

function takeMessage(): string {
	let seen = false;
	try {
		seen = window.localStorage.getItem(KEY) === "1";
	} catch {
		seen = false;
	}
	try {
		window.localStorage.setItem(KEY, "1");
	} catch {
		// Storage can be blocked. The first line still shows.
	}
	return seen ? AGAIN : FIRST;
}

function setHot(on: boolean): void {
	document.querySelectorAll<HTMLElement>(MARKS).forEach((mark) => {
		mark.classList.toggle("is-hot", on);
	});
}

function footerMark(target: EventTarget | null): HTMLElement | null {
	if (!(target instanceof Element)) return null;
	const mark = target.closest(".site-footer .site-footer__mark");
	return mark instanceof HTMLElement ? mark : null;
}

function inField(target: EventTarget | null): boolean {
	if (!(target instanceof Element)) return false;
	if (target.closest("input, textarea, select, [contenteditable=''], [contenteditable='true']")) {
		return true;
	}
	return target instanceof HTMLElement && target.isContentEditable;
}

function phone(): boolean {
	return window.matchMedia(PHONE).matches;
}
