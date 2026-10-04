import { isCurrentPath } from "../data/nav";
import { bootAboutParallax } from "./about-parallax";
import { releaseFilterShelf } from "./filter-shelf";
import { bootGuideCover } from "./guide-cover";
import { bootGuidesFilter } from "./guides-filter";
import { initHero } from "./hero-scrub";
import { bootDoors } from "./home-doors";
import { bootDrop } from "./home-drop";
import { bootPromise } from "./home-promise";
import { bootJoinGlow } from "./join-glow";
import { gsap, isMobile, onReducedMotionChange, prefersReducedMotion, ScrollTrigger } from "./motion";
import { bootPromptsPage, releasePromptCards } from "./prompt-cards";
import { bootReveals, releaseReveals } from "./reveals";
import { destroySmoothScroll, initSmoothScroll } from "./smooth-scroll";
import { releaseVideoCards, bootVideoCards } from "./video-cards";

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
 * There is no cursor module. The only tilt is the door face inside
 * LibraryDoors. Its script runs once; page-load calls bootDoors again.
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
	closeMenu();
	closeDialogs();
	parkHeader();
	try {
		window.dispatchEvent(new Event("pagehide"));
	} catch {
		// Old page cleanup threw. Keep tearing the scroll system down.
	}
	releaseFilterShelf();
	releasePromptCards();
	releaseVideoCards();
	releaseReveals();
	gsap.killTweensOf("[data-join-glow]");
	document.querySelectorAll("video").forEach((video) => {
		video.pause();
	});
	destroySmoothScroll();
	for (const trigger of ScrollTrigger.getAll()) trigger.kill();
}

function onPage(): void {
	initSmoothScroll();
	bootReveals();
	bootPromise();
	bootDoors();
	bootDrop();
	bootGuidesFilter();
	bootPromptsPage();
	bootVideoCards();
	bootAboutParallax();
	bootGuideCover();
	bootJoinGlow();
	bootJoinBands();
	const hero = document.querySelector<HTMLElement>("[data-hero]");
	if (hero) initHero(hero);
	syncCurrent(window.location.pathname);
	const band = document.querySelector<HTMLElement>("[data-route-band]");
	if (band) band.style.transform = "";
	ScrollTrigger.refresh();
	const pending = finish;
	finish = null;
	pending?.then(() => ScrollTrigger.refresh()).catch(() => undefined);
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
					duration: 2,
					ease: "sine.inOut",
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
