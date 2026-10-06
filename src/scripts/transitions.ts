import { isCurrentPath } from "../data/nav";
import { bootCursor, releaseCursorMotion } from "./cursor";
import { bootEasterEgg } from "./easter-egg";
import { duration, ease, gsap, isMobile, onReducedMotionChange, prefersReducedMotion, ScrollTrigger } from "./motion";
import { bootPointer, releasePointer } from "./pointer";
import { bootReveals, releaseReveals } from "./reveals";
import { destroySmoothScroll, initSmoothScroll } from "./smooth-scroll";
import { bootStarfield, releaseStarfield } from "./starfield";
import { bootTracers, destroyTracers } from "./tracers";

/**
 * Page modules stay out of this file's static graph. Each one loads on the
 * route that has its markup, including the trip back through ClientRouter.
 */
let releaseShelf: (() => void) | null = null;
let releasePrompts: (() => void) | null = null;
let releaseGoals: (() => void) | null = null;
let releaseVideos: (() => void) | null = null;
let releaseHover: (() => void) | null = null;

/**
 * One listener set for the life of the tab.
 * astro:page-load also fires on the first load, after the layout script has
 * already booted Lenis and reveals, so every boot below has to no-op when
 * the current DOM is already live.
 *
 * Hero.astro calls initHero on the first visit only. Astro does not re-run
 * that script on the way back, and hero-scrub.ts has no page-load listener.
 * This file calls initHero on page-load instead. Leaving home dispatches
 * pagehide so the hero's own cleanup stops the old loop.
 *
 * bootCursor stamps labels again after each swap. The ring lives on
 * documentElement, so the body replacement does not drop it.
 * The only tilt is the door face inside LibraryDoors. Its script runs
 * once; page-load calls bootDoors again.
 */

const PARKED_OFF = "translateY(110%)";
const CAPTURE_ON_EDGE = "translateY(0)";

type PrepEvent = Event & {
	loader: () => Promise<void> | void;
	sourceElement: EventTarget | null;
	newDocument: Document;
	defaultPrevented: boolean;
	signal?: AbortSignal;
};

type SwapEvent = Event & {
	to?: URL;
	viewTransition?: { finished: Promise<void> };
};

let listening = false;
let finish: Promise<void> | null = null;

export function bootTransitions(): void {
	if (listening || typeof window === "undefined") return;
	listening = true;
	armCapture();
	document.addEventListener("astro:before-preparation", onPrep);
	document.addEventListener("astro:before-swap", onSwap);
	document.addEventListener("astro:page-load", onPage);
}

/**
 * The old snapshot is taken synchronously inside startViewTransition.
 * Pull the live band onto the bottom edge in that same turn so the
 * picture has pixels, with no frame where the bar sits on screen.
 */
function armCapture(): void {
	const native = document.startViewTransition?.bind(document);
	if (!native) return;
	document.startViewTransition = (callback) => {
		releaseStarfield();
		if (!prefersReducedMotion()) {
			const band = document.querySelector<HTMLElement>("[data-route-band]");
			if (band) band.style.transform = CAPTURE_ON_EDGE;
		}
		return native(callback);
	};
}

function onPrep(event: Event): void {
	const prep = event as PrepEvent;
	const run = prep.loader;
	if (typeof run !== "function") return;
	prep.loader = async () => {
		await run();
		if (prep.defaultPrevented || prep.signal?.aborted) return;
		if (!prep.newDocument || prep.newDocument === document) return;
		const name = resolveName(prep.sourceElement, prep.newDocument);
		paintBand(document, name, "old");
		paintBand(prep.newDocument, name, "new");
	};
}

function onSwap(event: Event): void {
	const swap = event as SwapEvent;
	finish = swap.viewTransition?.finished ?? null;
	syncCurrent(swap.to?.pathname ?? window.location.pathname);
	releaseStarfield();
	destroyTracers();
	releaseCursorMotion();
	closeMenu();
	closeDialogs();
	parkHeader();
	try {
		window.dispatchEvent(new Event("pagehide"));
	} catch {
		// Old page cleanup threw. Keep tearing the scroll system down.
	}
	releaseShelf?.();
	releasePrompts?.();
	releaseGoals?.();
	releaseGoals = null;
	releaseVideos?.();
	releaseHover?.();
	releaseHover = null;
	releasePointer();
	releaseReveals();
	gsap.killTweensOf("[data-join-glow]");
	document.querySelectorAll("video").forEach((video) => {
		video.pause();
		video.querySelectorAll("source").forEach((source) => source.remove());
		video.removeAttribute("src");
		try {
			video.load();
		} catch {
			// The old document is already leaving.
		}
	});
	destroySmoothScroll();
	for (const trigger of ScrollTrigger.getAll()) trigger.kill();
}

function onPage(): void {
	initSmoothScroll();
	bootReveals();
	bootPointer();
	bootCursor();
	bootEasterEgg();
	bootStarfield();
	bootTracers();
	bootJoinBands();
	syncCurrent(window.location.pathname);
	const band = document.querySelector<HTMLElement>("[data-route-band]");
	if (band) band.style.transform = "";
	const pending = finish;
	finish = null;
	void bootRoute().finally(() => {
		ScrollTrigger.refresh();
		pending?.then(() => ScrollTrigger.refresh()).catch(() => undefined);
	});
}

/** Load the scripts this document actually uses. Other routes never download them. */
function bootRoute(): Promise<void> {
	const jobs: Array<Promise<void>> = [];

	if (document.querySelector("[data-hero]")) {
		jobs.push(
			import("./hero-scrub").then((mod) => {
				const hero = document.querySelector<HTMLElement>("[data-hero]");
				if (hero) mod.initHero(hero);
			}),
		);
	}
	if (document.querySelector("[data-doors]")) {
		jobs.push(import("./home-doors").then((mod) => mod.bootDoors()));
	}
	if (document.querySelector("[data-hover-video]")) {
		jobs.push(
			import("./hover-video").then((mod) => {
				releaseHover = mod.releaseHoverVideos;
				mod.bootHoverVideos();
			}),
		);
	}
	if (document.querySelector("[data-drop]")) {
		jobs.push(import("./home-drop").then((mod) => mod.bootDrop()));
	}
	if (document.querySelector("[data-promise]")) {
		jobs.push(import("./home-promise").then((mod) => mod.bootPromise()));
	}
	if (document.querySelector("[data-guides]")) {
		jobs.push(
			import("./filter-shelf").then((mod) => {
				releaseShelf = mod.releaseFilterShelf;
			}),
		);
		jobs.push(import("./guides-filter").then((mod) => mod.bootGuidesFilter()));
	}
	if (document.querySelector("[data-prompts]")) {
		jobs.push(
			import("./prompt-cards").then((mod) => {
				releasePrompts = mod.releasePromptCards;
				mod.bootPromptCards();
			}),
		);
		jobs.push(
			import("./prompt-goal-menu").then((mod) => {
				releaseGoals = mod.releasePromptGoals;
				mod.bootPromptGoals();
			}),
		);
	}
	if (document.querySelector("[data-video-modal]")) {
		jobs.push(
			import("./video-cards").then((mod) => {
				releaseVideos = mod.releaseVideoCards;
				mod.bootVideoCards();
			}),
		);
	}
	if (document.querySelector("[data-about-hero]")) {
		jobs.push(import("./about-parallax").then((mod) => mod.bootAboutParallax()));
	}
	if (document.querySelector("[data-guide-detail]")) {
		jobs.push(import("./guide-cover").then((mod) => mod.bootGuideCover()));
	}
	if (document.querySelector("[data-join-page]")) {
		jobs.push(import("./join-glow").then((mod) => mod.bootJoinGlow()));
	}

	return Promise.all(jobs).then(() => undefined);
}

function resolveName(source: EventTarget | null, doc: Document): string {
	const link = source instanceof Element ? source.closest("a") : null;
	const labeled = link?.getAttribute("data-label")?.trim();
	if (labeled) return labeled;
	return titleName(doc.querySelector("title")?.textContent ?? "");
}

function titleName(title: string): string {
	const stripped = title.replace(/\s·\sAntiHero AI\s*$/, "").trim();
	if (!stripped || stripped === "AntiHero AI") return "Home";
	return stripped;
}

function paintBand(doc: Document, name: string, phase: "old" | "new"): void {
	const band = doc.querySelector<HTMLElement>("[data-route-band]");
	const label = band?.querySelector<HTMLElement>("[data-route-name]");
	if (!band || !label) return;
	const reduced = prefersReducedMotion();
	const showName = !reduced && !isMobile();
	label.textContent = showName ? name : "";
	label.toggleAttribute("data-long", showName && name.length > 22);
	band.style.transform = phase === "new" && !reduced ? CAPTURE_ON_EDGE : PARKED_OFF;
}

function syncCurrent(pathname: string): void {
	document.querySelectorAll<HTMLAnchorElement>("[data-nav]").forEach((link) => {
		if (isCurrentPath(link.pathname, pathname)) link.setAttribute("aria-current", "page");
		else link.removeAttribute("aria-current");
	});
}

function closeMenu(): void {
	document.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
}

function closeDialogs(): void {
	document.querySelectorAll("dialog[open]").forEach((dialog) => {
		if (dialog instanceof HTMLDialogElement) dialog.close();
	});
}

function parkHeader(): void {
	const header = document.querySelector<HTMLElement>("[data-header]");
	const scrim = document.querySelector<HTMLElement>("[data-header-scrim]");
	if (header) {
		gsap.set(header, { yPercent: 0 });
		header.classList.remove("is-scrolled");
	}
	if (scrim) gsap.set(scrim, { opacity: 0 });
}

/** JoinBand.astro boots the first band it sees and then Astro will not re-run it. */
function bootJoinBands(): void {
	document.querySelectorAll<HTMLElement>("[data-join-band]").forEach((band) => {
		if (band.dataset.glowReady === "true") return;
		const glow = band.querySelector<HTMLElement>("[data-join-glow]");
		if (!glow) return;
		band.dataset.glowReady = "true";

		let tween: gsap.core.Tween | undefined;
		const start = (): void => {
			tween?.kill();
			tween = undefined;
			if (prefersReducedMotion()) {
				gsap.set(glow, { scale: 1, opacity: 0.5 });
				return;
			}
			const peak = isMobile() ? 1.05 : 1.12;
			tween = gsap.fromTo(
				glow,
				{ scale: 1, opacity: 0.35 },
				{
					scale: peak,
					opacity: 0.72,
					duration: duration.dwell,
					ease: ease.sine,
					yoyo: true,
					repeat: -1,
				},
			);
		};

		start();
		const stop = onReducedMotionChange(start);
		window.addEventListener(
			"pagehide",
			() => {
				tween?.kill();
				stop();
				gsap.set(glow, { clearProps: "transform,opacity" });
			},
			{ once: true },
		);
	});
}
