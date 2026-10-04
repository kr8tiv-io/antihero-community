import Lenis from "lenis";
import { gsap, isMobile, ScrollTrigger, onReducedMotionChange, prefersReducedMotion } from "./motion";

/**
 * One window scroller for the whole site.
 * Page transitions should call destroySmoothScroll(), then initSmoothScroll().
 * Reduced motion and phones never construct Lenis. Touch stays native.
 */

let lenis: Lenis | null = null;
let ticker: ((time: number) => void) | null = null;
let unlistenScroll: (() => void) | null = null;
let unlistenClicks: (() => void) | null = null;
let unlistenPop: (() => void) | null = null;
let unlistenDialog: (() => void) | null = null;
let menuObserver: MutationObserver | null = null;
let reducedUnsub: (() => void) | null = null;
let scrollToken = 0;

const GSAP_LAG_THRESHOLD = 500;
const GSAP_LAG_ADJUSTED = 33;

export function getLenis(): Lenis | null {
	return lenis;
}

function headerOffset(): number {
	const raw = getComputedStyle(document.documentElement).getPropertyValue("--header-h");
	const value = Number.parseFloat(raw);
	return Number.isFinite(value) ? value : 56;
}

function scrollOffset(el: HTMLElement): number {
	const margin = Number.parseFloat(getComputedStyle(el).scrollMarginTop);
	if (Number.isFinite(margin) && margin > 0) return 0;
	return -headerOffset();
}

function focusTarget(el: HTMLElement): void {
	if (!el.isConnected) return;
	const naturally = el.matches("a[href], button, input, textarea, select, summary, [tabindex]");
	if (!naturally) el.setAttribute("tabindex", "-1");
	el.focus({ preventScroll: true });
}

function findHashTarget(hash: string): HTMLElement | null {
	if (!hash || hash === "#") return null;
	let id = hash.slice(1);
	try {
		id = decodeURIComponent(id);
	} catch {
		return null;
	}
	const byId = document.getElementById(id);
	if (byId) return byId;
	try {
		const node = document.querySelector(hash);
		return node instanceof HTMLElement ? node : null;
	} catch {
		return null;
	}
}

function samePageHash(link: HTMLAnchorElement): string | null {
	if (link.target && link.target !== "_self") return null;
	if (link.hasAttribute("download")) return null;
	let url: URL;
	try {
		url = new URL(link.href, window.location.href);
	} catch {
		return null;
	}
	if (url.origin !== window.location.origin) return null;
	const path = (value: string) => value.replace(/\/$/, "") || "/";
	if (path(url.pathname) !== path(window.location.pathname)) return null;
	if (!url.hash || url.hash === "#") return null;
	return url.hash;
}

function scrollToHash(hash: string, behavior: "smooth" | "immediate"): void {
	if (!lenis) return;
	const dest = findHashTarget(hash);
	if (!dest) return;
	const token = ++scrollToken;
	lenis.scrollTo(dest, {
		offset: scrollOffset(dest),
		immediate: behavior === "immediate",
		onComplete: () => {
			if (token !== scrollToken) return;
			focusTarget(dest);
		},
	});
}

function blocked(): boolean {
	return (
		document.documentElement.classList.contains("menu-open") ||
		document.querySelector("dialog[open]") !== null
	);
}

function syncHold(): void {
	if (!lenis) return;
	if (blocked()) lenis.stop();
	else lenis.start();
}

export function destroySmoothScroll(): void {
	unlistenScroll?.();
	unlistenScroll = null;
	unlistenClicks?.();
	unlistenClicks = null;
	unlistenPop?.();
	unlistenPop = null;
	unlistenDialog?.();
	unlistenDialog = null;
	menuObserver?.disconnect();
	menuObserver = null;
	if (ticker) gsap.ticker.remove(ticker);
	ticker = null;
	lenis?.destroy();
	lenis = null;
	gsap.ticker.lagSmoothing(GSAP_LAG_THRESHOLD, GSAP_LAG_ADJUSTED);
	ScrollTrigger.update();
}

function nativeScroll(): boolean {
	return prefersReducedMotion() || isMobile();
}

function syncLenis(): void {
	if (nativeScroll()) destroySmoothScroll();
	else create();
}

function create(): Lenis | null {
	if (nativeScroll()) {
		destroySmoothScroll();
		return null;
	}
	if (lenis) return lenis;

	const instance = new Lenis({
		lerp: 0.1,
		smoothWheel: true,
		syncTouch: false,
		autoRaf: false,
		anchors: false,
		// We never construct Lenis while motion is reduced, so this must not keep a dummy instance alive.
		respectReducedMotion: false,
		// Shelves, the menu list, and door rows keep their own overflow scroll.
		allowNestedScroll: true,
	});
	lenis = instance;

	unlistenScroll = instance.on("scroll", () => {
		ScrollTrigger.update();
	});

	ticker = (time: number) => {
		instance.raf(time * 1000);
	};
	gsap.ticker.add(ticker);
	gsap.ticker.lagSmoothing(0);

	const onClick = (event: MouseEvent) => {
		if (event.defaultPrevented) return;
		if (event.button !== 0) return;
		if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
		const target = event.target;
		if (!(target instanceof Element)) return;
		const link = target.closest("a");
		if (!(link instanceof HTMLAnchorElement)) return;
		const hash = samePageHash(link);
		if (!hash || !findHashTarget(hash)) return;
		if (instance.isStopped) return;
		event.preventDefault();
		const next = `${window.location.pathname}${window.location.search}${hash}`;
		if (`${window.location.pathname}${window.location.search}${window.location.hash}` !== next) {
			history.pushState(null, "", next);
		}
		scrollToHash(hash, "smooth");
	};
	document.addEventListener("click", onClick);
	unlistenClicks = () => document.removeEventListener("click", onClick);

	const onPop = () => {
		requestAnimationFrame(() => {
			if (window.location.hash && findHashTarget(window.location.hash)) {
				scrollToHash(window.location.hash, "immediate");
				return;
			}
			instance.scrollTo(window.scrollY, { immediate: true });
		});
	};
	window.addEventListener("popstate", onPop);
	unlistenPop = () => window.removeEventListener("popstate", onPop);

	const onToggle = (event: Event) => {
		if (event.target instanceof HTMLDialogElement) syncHold();
	};
	document.addEventListener("toggle", onToggle, true);
	unlistenDialog = () => document.removeEventListener("toggle", onToggle, true);

	menuObserver = new MutationObserver(syncHold);
	menuObserver.observe(document.documentElement, {
		attributes: true,
		attributeFilter: ["class"],
	});

	syncHold();
	return instance;
}

export function initSmoothScroll(): Lenis | null {
	if (!reducedUnsub) {
		reducedUnsub = onReducedMotionChange(syncLenis);
		window.matchMedia("(width < 768px), (pointer: coarse)").addEventListener("change", syncLenis);
	}
	return create();
}
