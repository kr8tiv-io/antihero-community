import { duration, ease, gsap, isMobile, prefersReducedMotion } from "./motion";

/**
 * Press, hover zoom, and nudge. Transform only.
 * Phones and coarse pointers get the press and skip the hover moves.
 * Reduced motion leaves every control still.
 * The wordmark is never a target.
 */

const PRESS =
	"button, a.label-box, a.missing-home, a.guide-card__link, a.note, a.guide-prompt, a.post-ref, a.credits-name, a.video-hit, a.drop-cover, a.drop-play, a.drop-pdf, a.drop-read, a[data-magnetic]";
const SKIP = "a.wordmark, a.site-footer__mark";

const touched = new Set<HTMLElement>();
let listening = false;
let pressed: HTMLElement | null = null;

function allowHover(): boolean {
	if (prefersReducedMotion() || isMobile()) return false;
	return window.matchMedia("(hover: hover) and (pointer: fine)").matches;
}

function track(el: HTMLElement): void {
	touched.add(el);
}

function hostFrom(event: Event): HTMLElement | null {
	const target = event.target;
	if (!(target instanceof Element)) return null;
	const host = target.closest("a, button");
	return host instanceof HTMLElement ? host : null;
}

function insideHost(host: HTMLElement, node: EventTarget | null): boolean {
	return node instanceof Node && host.contains(node);
}

function zoomTo(el: HTMLElement, on: boolean): void {
	track(el);
	gsap.to(el, {
		scale: on ? 1.04 : 1,
		duration: duration.settle,
		ease: ease.out,
		overwrite: "auto",
		transformOrigin: "center center",
	});
}

function nudgeTo(el: HTMLElement, on: boolean): void {
	track(el);
	const axis = el.dataset.nudge === "y" ? "y" : "x";
	const amount = on ? (axis === "y" ? -6 : 8) : 0;
	gsap.to(el, {
		[axis]: amount,
		duration: duration.fast,
		ease: ease.out,
		overwrite: "auto",
	});
}

function hoverHosts(host: HTMLElement, on: boolean): void {
	host.querySelectorAll<HTMLElement>("[data-zoom]").forEach((el) => zoomTo(el, on));
	const nudges = new Set<HTMLElement>();
	if (host.matches("[data-nudge]")) nudges.add(host);
	host.querySelectorAll<HTMLElement>("[data-nudge]").forEach((el) => nudges.add(el));
	nudges.forEach((el) => nudgeTo(el, on));
}

function onOver(event: PointerEvent): void {
	if (!allowHover()) return;
	const host = hostFrom(event);
	if (!host || insideHost(host, event.relatedTarget)) return;
	hoverHosts(host, true);
}

function onOut(event: PointerEvent): void {
	if (!allowHover()) return;
	const host = hostFrom(event);
	if (!host || insideHost(host, event.relatedTarget)) return;
	hoverHosts(host, false);
}

function onFocusIn(event: FocusEvent): void {
	if (!allowHover()) return;
	const host = hostFrom(event);
	if (!host) return;
	hoverHosts(host, true);
}

function onFocusOut(event: FocusEvent): void {
	if (!allowHover()) return;
	const host = hostFrom(event);
	if (!host || insideHost(host, event.relatedTarget)) return;
	hoverHosts(host, false);
}

function pressTarget(event: Event): HTMLElement | null {
	const target = event.target;
	if (!(target instanceof Element)) return null;
	if (target.closest(SKIP)) return null;
	const el = target.closest(PRESS);
	if (!(el instanceof HTMLElement)) return null;
	if (el.matches(":disabled, [aria-disabled='true']")) return null;
	return el;
}

function releasePress(): void {
	const el = pressed;
	pressed = null;
	if (!el) return;
	if (prefersReducedMotion()) {
		gsap.set(el, { scale: 1 });
		return;
	}
	track(el);
	gsap.to(el, {
		scale: 1,
		duration: duration.press,
		ease: ease.out,
		overwrite: "auto",
	});
}

function onDown(event: PointerEvent): void {
	if (prefersReducedMotion()) return;
	if (event.pointerType === "mouse" && event.button !== 0) return;
	const el = pressTarget(event);
	if (!el) return;
	pressed = el;
	track(el);
	gsap.to(el, {
		scale: isMobile() ? 0.985 : 0.97,
		duration: duration.press,
		ease: ease.out,
		overwrite: "auto",
		transformOrigin: "center center",
	});
}

/** One listener set for the tab. Safe to call again after a swap. */
export function bootPointer(): void {
	if (typeof window === "undefined" || listening) return;
	listening = true;
	document.addEventListener("pointerover", onOver);
	document.addEventListener("pointerout", onOut);
	document.addEventListener("focusin", onFocusIn);
	document.addEventListener("focusout", onFocusOut);
	document.addEventListener("pointerdown", onDown);
	document.addEventListener("pointerup", releasePress);
	document.addEventListener("pointercancel", releasePress);
	window.addEventListener("blur", releasePress);
}

/** Drop inline press, zoom, and nudge before the next page paints. */
export function releasePointer(): void {
	pressed = null;
	for (const el of touched) {
		gsap.killTweensOf(el);
		gsap.set(el, { clearProps: "transform" });
	}
	touched.clear();
}
