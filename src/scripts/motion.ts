import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

const hasWindow = typeof window !== "undefined";

export { gsap, ScrollTrigger };

/**
 * Shared easing and timing. Scrubbed tweens use ease.linear.
 * Scroll weights that belong to one timeline stay next to that timeline.
 */
export const ease = {
	out: "power3.out",
	in: "power3.in",
	inSoft: "power2.in",
	inOut: "power2.inOut",
	/** Small UI only. Page-scale motion stays on ease.out. */
	playful: "back.out(1.4)",
	sine: "sine.inOut",
	linear: "none",
	expo: "expo.out",
} as const;

export const duration = {
	press: 0.18,
	ui: 0.28,
	fast: 0.35,
	settle: 0.6,
	base: 0.8,
	/** Cover settle on the home drop. Longer than a UI move, shorter than a dwell. */
	cover: 1.05,
	slow: 1.4,
	dwell: 2.2,
} as const;

export const stagger = 0.06;

if (hasWindow) {
	gsap.registerPlugin(ScrollTrigger);
	gsap.defaults({
		duration: duration.base,
		ease: ease.out,
	});
}

type ReducedListener = (reduced: boolean) => void;

const reducedListeners = new Set<ReducedListener>();
let reducedQuery: MediaQueryList | null = null;

function ensureReducedListener(): void {
	if (!hasWindow || reducedQuery) return;
	reducedQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
	reducedQuery.addEventListener("change", () => {
		const reduced = reducedQuery?.matches ?? false;
		reducedListeners.forEach((listener) => listener(reduced));
	});
}

/** Current reduced-motion setting. Listens for OS changes for onReducedMotionChange. */
export function prefersReducedMotion(): boolean {
	if (!hasWindow) return false;
	ensureReducedListener();
	return reducedQuery?.matches ?? false;
}

/** Fires when the reduced-motion preference changes. Returns an unsubscribe. */
export function onReducedMotionChange(listener: ReducedListener): () => void {
	ensureReducedListener();
	reducedListeners.add(listener);
	return () => {
		reducedListeners.delete(listener);
	};
}

/** True under 768px, or when the primary pointer is coarse. */
export function isMobile(): boolean {
	if (!hasWindow) return false;
	return window.matchMedia("(width < 768px), (pointer: coarse)").matches;
}
