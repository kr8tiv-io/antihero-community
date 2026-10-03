import gsap from "gsap";
import { Flip } from "gsap/Flip";
import { ScrollTrigger } from "gsap/ScrollTrigger";

const hasWindow = typeof window !== "undefined";

export { gsap, ScrollTrigger, Flip };

export const ease = {
  out: "power3.out",
  inOut: "power2.inOut",
  /** Small UI only. Page-scale motion stays on ease.out. */
  playful: "back.out(1.4)",
} as const;

export const duration = {
  fast: 0.35,
  base: 0.8,
  slow: 1.4,
} as const;

export const stagger = 0.06;

if (hasWindow) {
  gsap.registerPlugin(ScrollTrigger, Flip);
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
