/**
 * One hover film for doors, guide cards, the latest drop, and video cards.
 * A fine pointer fades the film in on hover or keyboard focus.
 * Phones and coarse pointers play the single most visible card.
 * Save-data, 2g, reduced motion, or a failed load stay on the poster.
 */

import { onReducedMotionChange, prefersReducedMotion } from "./motion";

type NetInfo = {
	saveData?: boolean;
	effectiveType?: string;
	addEventListener?: (type: string, listener: () => void) => void;
	removeEventListener?: (type: string, listener: () => void) => void;
};

type Slot = {
	root: HTMLElement;
	card: HTMLElement;
	video: HTMLVideoElement;
	armed: boolean;
	failed: boolean;
	want: boolean;
	ratio: number;
	pauseTimer: number;
};

const NEAR = "300px";
const VISIBLE = 0.6;
const FADE_OUT_MS = 400;

let slots: Slot[] = [];
let stopReduced: (() => void) | null = null;
let nearObserver: IntersectionObserver | null = null;
let viewObserver: IntersectionObserver | null = null;
let fineQuery: MediaQueryList | null = null;
let phoneQuery: MediaQueryList | null = null;
const unlisten: Array<() => void> = [];

function connection(): NetInfo | undefined {
	return (navigator as Navigator & { connection?: NetInfo }).connection;
}

function posterOnly(): boolean {
	if (prefersReducedMotion()) return true;
	const net = connection();
	if (net?.saveData) return true;
	const kind = net?.effectiveType;
	return kind === "2g" || kind === "slow-2g";
}

/** Laptop hover. Phones and coarse pointers use the in-view player. */
function hoverMode(): boolean {
	if (posterOnly()) return false;
	const fine = fineQuery?.matches ?? window.matchMedia("(hover: hover) and (pointer: fine)").matches;
	const phone = phoneQuery?.matches ?? window.matchMedia("(width < 768px), (pointer: coarse)").matches;
	return fine && !phone;
}

function arm(slot: Slot): void {
	if (slot.armed || slot.failed || posterOnly()) return;
	const sources = [...slot.video.querySelectorAll("source")];
	let attached = false;
	sources.forEach((source) => {
		const next = source.dataset.src;
		if (!next || source.getAttribute("src")) return;
		source.src = next;
		attached = true;
	});
	if (!attached && !slot.video.currentSrc) return;
	slot.armed = true;
	slot.video.preload = "metadata";
	slot.video.load();
}

function disarm(slot: Slot): void {
	window.clearTimeout(slot.pauseTimer);
	slot.want = false;
	slot.root.classList.remove("is-on");
	slot.video.pause();
	if (!slot.armed) return;
	slot.video.querySelectorAll("source").forEach((source) => source.removeAttribute("src"));
	slot.video.removeAttribute("src");
	slot.video.preload = "none";
	slot.video.load();
	slot.armed = false;
}

function show(slot: Slot): void {
	if (slot.failed || posterOnly()) return;
	slot.want = true;
	window.clearTimeout(slot.pauseTimer);
	arm(slot);
	slot.video.muted = true;
	const generation = slot.want;
	const reveal = (): void => {
		if (generation && slot.want) slot.root.classList.add("is-on");
	};
	if (slot.video.readyState >= 2 && !slot.video.paused) {
		reveal();
		return;
	}
	slot.video.addEventListener("playing", reveal, { once: true });
	void slot.video.play().catch((error: unknown) => {
		if (!slot.want) return;
		const name = error instanceof DOMException ? error.name : "";
		if (name === "AbortError") return;
		slot.failed = true;
		disarm(slot);
	});
}

function hide(slot: Slot): void {
	slot.want = false;
	slot.root.classList.remove("is-on");
	window.clearTimeout(slot.pauseTimer);
	slot.pauseTimer = window.setTimeout(() => {
		if (!slot.want) slot.video.pause();
	}, FADE_OUT_MS);
}

function cardHot(slot: Slot): boolean {
	return slot.card.matches(":hover") || slot.card.matches(":focus-visible") || slot.card.matches(":focus-within");
}

function sync(): void {
	if (posterOnly()) {
		slots.forEach((slot) => disarm(slot));
		return;
	}
	if (document.hidden) {
		slots.forEach((slot) => {
			slot.want = false;
			slot.root.classList.remove("is-on");
			window.clearTimeout(slot.pauseTimer);
			slot.video.pause();
		});
		return;
	}
	if (hoverMode()) {
		slots.forEach((slot) => {
			if (slot.want || cardHot(slot)) show(slot);
			else hide(slot);
		});
		return;
	}
	let best: Slot | null = null;
	for (const slot of slots) {
		if (slot.failed || slot.ratio < VISIBLE) continue;
		if (!best || slot.ratio > best.ratio) best = slot;
	}
	slots.forEach((slot) => {
		if (slot === best) show(slot);
		else hide(slot);
	});
}

function bindSlot(slot: Slot): void {
	const onEnter = (): void => {
		if (!hoverMode()) return;
		show(slot);
	};
	const onLeave = (event: PointerEvent): void => {
		if (!hoverMode()) return;
		const next = event.relatedTarget;
		if (next instanceof Node && slot.card.contains(next)) return;
		if (slot.card.matches(":focus-visible")) return;
		hide(slot);
	};
	const onFocus = (): void => {
		if (!hoverMode()) return;
		if (slot.card.matches(":focus-visible") || slot.card.querySelector(":focus-visible")) show(slot);
	};
	const onBlur = (event: FocusEvent): void => {
		if (!hoverMode()) return;
		const next = event.relatedTarget;
		if (next instanceof Node && slot.card.contains(next)) return;
		hide(slot);
	};
	const onError = (): void => {
		slot.failed = true;
		disarm(slot);
	};
	slot.card.addEventListener("pointerenter", onEnter);
	slot.card.addEventListener("pointerleave", onLeave);
	slot.card.addEventListener("focusin", onFocus);
	slot.card.addEventListener("focusout", onBlur);
	slot.video.addEventListener("error", onError);
	unlisten.push(() => {
		slot.card.removeEventListener("pointerenter", onEnter);
		slot.card.removeEventListener("pointerleave", onLeave);
		slot.card.removeEventListener("focusin", onFocus);
		slot.card.removeEventListener("focusout", onBlur);
		slot.video.removeEventListener("error", onError);
	});
}

function releaseListeners(): void {
	unlisten.splice(0).forEach((stop) => stop());
	nearObserver?.disconnect();
	viewObserver?.disconnect();
	nearObserver = null;
	viewObserver = null;
	stopReduced?.();
	stopReduced = null;
	fineQuery?.removeEventListener("change", sync);
	phoneQuery?.removeEventListener("change", sync);
	fineQuery = null;
	phoneQuery = null;
	const net = connection();
	net?.removeEventListener?.("change", sync);
	slots.forEach((slot) => {
		window.clearTimeout(slot.pauseTimer);
		slot.video.pause();
		slot.root.classList.remove("is-on");
	});
	slots = [];
}

export function releaseHoverVideos(): void {
	document.removeEventListener("visibilitychange", sync);
	releaseListeners();
}

export function bootHoverVideos(): void {
	releaseHoverVideos();
	const roots = [...document.querySelectorAll<HTMLElement>("[data-hover-video]")];
	slots = roots.flatMap((root) => {
		const video = root.querySelector("video");
		if (!video) return [];
		const card = root.closest<HTMLElement>("[data-hover-card]") ?? root;
		return [
			{
				root,
				card,
				video,
				armed: false,
				failed: false,
				want: false,
				ratio: 0,
				pauseTimer: 0,
			},
		];
	});
	if (slots.length === 0) return;

	slots.forEach(bindSlot);
	fineQuery = window.matchMedia("(hover: hover) and (pointer: fine)");
	phoneQuery = window.matchMedia("(width < 768px), (pointer: coarse)");
	fineQuery.addEventListener("change", sync);
	phoneQuery.addEventListener("change", sync);
	stopReduced = onReducedMotionChange(sync);
	connection()?.addEventListener?.("change", sync);
	document.addEventListener("visibilitychange", sync);

	if ("IntersectionObserver" in window) {
		nearObserver = new IntersectionObserver(
			(entries) => {
				if (posterOnly()) return;
				entries.forEach((entry) => {
					if (!entry.isIntersecting) return;
					const slot = slots.find((item) => item.root === entry.target);
					if (!slot) return;
					arm(slot);
				});
			},
			{ rootMargin: NEAR, threshold: 0 },
		);
		viewObserver = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					const slot = slots.find((item) => item.root === entry.target);
					if (!slot) return;
					slot.ratio = entry.isIntersecting ? entry.intersectionRatio : 0;
				});
				if (!hoverMode()) sync();
			},
			{ threshold: [0, 0.25, 0.5, 0.6, 0.75, 1] },
		);
		slots.forEach((slot) => {
			nearObserver?.observe(slot.root);
			viewObserver?.observe(slot.root);
		});
	}
}
