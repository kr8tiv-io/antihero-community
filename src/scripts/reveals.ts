import {
	gsap,
	ScrollTrigger,
	ease,
	stagger as lineStagger,
	prefersReducedMotion,
	onReducedMotionChange,
	isMobile,
} from "./motion";

/**
 * Scroll reveals. Start states are set here, never in CSS, so a failed script
 * leaves every heading, paragraph, and image visible.
 *
 * ScrollTrigger.batch builds one trigger per element and only groups the callbacks.
 * A 30-card grid would still be 30 triggers. Grids use one ScrollTrigger on the
 * parent and stagger the children that cross the line together. Batch is for the
 * short standalone sets (a hero image, a heading that sits outside a group).
 */

const START = "top 85%";
const CHILD_STAGGER = 0.08;
const CLEAR = "transform,opacity,visibility,clipPath";

type Tuner = {
	y: number;
	inset: number;
	scale: number;
	box: number;
	text: number;
	fade: number;
	clip: number;
	count: number;
	lead: number;
};

let booted = false;
let teardown: (() => void) | null = null;
let stopWatching: (() => void) | null = null;

export function bootReveals(): void {
	if (booted || typeof window === "undefined") return;
	booted = true;

	const unsub = onReducedMotionChange(() => rebuild());
	const mq = window.matchMedia("(width < 768px), (pointer: coarse)");
	const onMq = (): void => rebuild();
	mq.addEventListener("change", onMq);
	stopWatching = () => {
		unsub();
		mq.removeEventListener("change", onMq);
	};

	rebuild();
}

function tune(): Tuner {
	const phone = isMobile();
	const scale = phone ? 0.72 : 1;
	return {
		y: phone ? 12 : 24,
		inset: phone ? 14 : 22,
		scale: phone ? 1.04 : 1.1,
		box: 0.55 * scale,
		text: 0.5 * scale,
		fade: 0.7 * scale,
		clip: 0.8 * scale,
		count: phone ? 0.28 : 0.45,
		lead: phone ? 0.1 : 0.16,
	};
}

function rebuild(): void {
	teardown?.();
	teardown = null;
	if (prefersReducedMotion()) {
		publish(0);
		return;
	}
	teardown = setup(document);
}

function publish(revealCount: number): void {
	document.documentElement.dataset.revealTriggers = String(revealCount);
	document.documentElement.dataset.scrollTriggers = String(ScrollTrigger.getAll().length);
}

function elementChildren(parent: ParentNode): HTMLElement[] {
	return [...parent.children].filter((node): node is HTMLElement => node instanceof HTMLElement);
}

function units(parent: HTMLElement): HTMLElement[] {
	let kids = elementChildren(parent);
	const only = kids[0];
	if (
		kids.length === 1 &&
		only &&
		only.childElementCount > 1 &&
		only.getAttribute("data-reveal") !== "stagger" &&
		!only.matches(
			"[data-reveal-heading], [data-guide-card], [data-prompt-card], [data-video-card], a, p, li, h1, h2, h3",
		)
	) {
		kids = elementChildren(only);
	}

	const out: HTMLElement[] = [];
	for (const kid of kids) {
		if (kid.classList.contains("visually-hidden")) continue;
		if (kid.tagName === "OL" || kid.tagName === "UL") {
			out.push(...elementChildren(kid));
			continue;
		}
		if (kid.getAttribute("data-reveal") === "contents") {
			out.push(...unwrap(kid));
			continue;
		}
		out.push(kid);
	}
	return out;
}

function unwrap(el: HTMLElement): HTMLElement[] {
	let kids = elementChildren(el);
	const only = kids[0];
	if (
		kids.length === 1 &&
		only &&
		only.childElementCount > 1 &&
		!only.matches("a, p, li, h1, h2, h3, blockquote, pre")
	) {
		kids = elementChildren(only);
	}
	return kids.filter((kid) => !kid.classList.contains("visually-hidden"));
}

function canPlay(el: HTMLElement): boolean {
	if (el.classList.contains("is-gone")) return false;
	if (el.closest("[hidden], .is-gone")) return false;
	const rect = el.getBoundingClientRect();
	return rect.width > 0 && rect.height > 0;
}

function inView(el: HTMLElement): boolean {
	const rect = el.getBoundingClientRect();
	return rect.top < window.innerHeight * 0.85 && rect.bottom > 0;
}

function played(el: HTMLElement): boolean {
	return el.dataset.revealPlayed === "1";
}

function inScope(node: HTMLElement, scope: HTMLElement | null): boolean {
	return node.closest<HTMLElement>("[data-reveal='stagger']") === scope;
}

function shouldFade(el: HTMLElement): boolean {
	if (el.matches("[data-reveal-heading], [data-reveal='clip']")) return false;
	if (el.matches("[data-guide-card], [data-prompt-card], [data-video-card]")) return false;
	if (el.querySelector("[data-reveal-heading]")) return el.matches("[data-reveal='fade-up']");
	return true;
}

function setup(root: ParentNode): () => void {
	const touched = new Set<HTMLElement>();
	const owned: ScrollTrigger[] = [];
	const groups = new Map<HTMLElement, HTMLElement[]>();
	const observers: MutationObserver[] = [];
	const standalones: HTMLElement[] = [];

	prepare(root, touched);

	function flush(parent: HTMLElement): void {
		const kids = groups.get(parent);
		if (!kids) return;
		const ready = kids.filter((kid) => !played(kid) && canPlay(kid) && inView(kid));
		ready.forEach((kid, index) => playNode(kid, index * CHILD_STAGGER, touched));
	}

	const staggerParents = [...root.querySelectorAll<HTMLElement>("[data-reveal='stagger']")];
	for (const parent of staggerParents) {
		const kids = units(parent);
		groups.set(parent, kids);
		const trigger = ScrollTrigger.create({
			trigger: parent,
			start: "top bottom",
			end: "bottom top",
			onEnter: () => flush(parent),
			onEnterBack: () => flush(parent),
			onUpdate: () => flush(parent),
			onRefresh: () => flush(parent),
		});
		owned.push(trigger);

		const observer = new MutationObserver(() => flush(parent));
		observer.observe(parent, {
			subtree: true,
			attributes: true,
			attributeFilter: ["class", "hidden"],
		});
		observers.push(observer);
	}

	batchStandalone(root, "[data-reveal-heading]", owned, touched, standalones);
	batchStandalone(root, "[data-reveal='fade-up']", owned, touched, standalones);
	batchStandalone(root, "[data-reveal='clip']", owned, touched, standalones);
	batchStandalone(root, "[data-reveal-count]", owned, touched, standalones);

	const onRefresh = (): void => {
		for (const parent of groups.keys()) flush(parent);
	};
	ScrollTrigger.addEventListener("refresh", onRefresh);

	ScrollTrigger.refresh();
	for (const parent of groups.keys()) flush(parent);
	const waiting = standalones.filter((el) => !played(el) && canPlay(el) && inView(el));
	waiting.forEach((el, index) => playNode(el, index * CHILD_STAGGER, touched));

	let alive = true;
	const report = (): void => {
		if (alive) publish(owned.length);
	};
	report();
	requestAnimationFrame(report);
	window.addEventListener("load", report, { once: true });

	return () => {
		alive = false;
		window.removeEventListener("load", report);
		ScrollTrigger.removeEventListener("refresh", onRefresh);
		for (const observer of observers) observer.disconnect();
		for (const trigger of owned) trigger.kill();
		for (const el of touched) {
			gsap.killTweensOf(el);
			gsap.set(el, { clearProps: CLEAR });
			delete el.dataset.revealPlayed;
			if (el.dataset.revealFinal) el.textContent = el.dataset.revealFinal;
		}
		groups.clear();
		publish(0);
	};
}

function prepare(root: ParentNode, touched: Set<HTMLElement>): void {
	const t = tune();

	for (const line of root.querySelectorAll<HTMLElement>(".reveal-heading__line")) {
		gsap.set(line, { scaleX: 0, transformOrigin: "left center" });
		touched.add(line);
	}
	for (const text of root.querySelectorAll<HTMLElement>(".reveal-heading__text")) {
		gsap.set(text, { yPercent: 105 });
		touched.add(text);
	}
	for (const clip of root.querySelectorAll<HTMLElement>("[data-reveal='clip']")) {
		gsap.set(clip, {
			clipPath: `inset(${t.inset}% ${t.inset}% ${t.inset}% ${t.inset}%)`,
			scale: t.scale,
			transformOrigin: "center center",
		});
		touched.add(clip);
	}

	const fade = new Set<HTMLElement>();
	for (const parent of root.querySelectorAll<HTMLElement>("[data-reveal='stagger']")) {
		for (const kid of units(parent)) collectFades(kid, parent, fade);
	}
	for (const node of root.querySelectorAll<HTMLElement>("[data-reveal='fade-up']")) {
		if (!node.closest("[data-reveal='stagger']")) fade.add(node);
	}
	for (const node of fade) {
		gsap.set(node, { y: t.y, opacity: 0 });
		touched.add(node);
	}

	for (const count of root.querySelectorAll<HTMLElement>("[data-reveal-count]")) {
		if (!count.dataset.revealFinal) count.dataset.revealFinal = count.textContent?.trim() ?? "";
		touched.add(count);
	}
}

function collectFades(el: HTMLElement, scope: HTMLElement, into: Set<HTMLElement>): void {
	if (shouldFade(el)) {
		into.add(el);
		return;
	}
	for (const node of el.querySelectorAll<HTMLElement>("[data-reveal='fade-up']")) {
		if (inScope(node, scope)) into.add(node);
	}
}

function batchStandalone(
	root: ParentNode,
	selector: string,
	owned: ScrollTrigger[],
	touched: Set<HTMLElement>,
	standalones: HTMLElement[],
): void {
	const els = [...root.querySelectorAll<HTMLElement>(selector)].filter((el) => {
		if (el.closest("[data-reveal='stagger']")) return false;
		if (standalones.includes(el)) return false;
		return true;
	});
	if (els.length === 0) return;
	standalones.push(...els);

	const batch = ScrollTrigger.batch(els, {
		start: START,
		interval: CHILD_STAGGER,
		onEnter: (batchEls) => {
			batchEls.forEach((node, index) => {
				if (node instanceof HTMLElement) playNode(node, index * CHILD_STAGGER, touched);
			});
		},
	});
	owned.push(...batch);
}

function playNode(el: HTMLElement, delay: number, touched: Set<HTMLElement>): void {
	if (played(el) || !canPlay(el)) return;
	el.dataset.revealPlayed = "1";

	const t = tune();
	const scope = el.closest<HTMLElement>("[data-reveal='stagger']");
	const tl = gsap.timeline({ delay });

	const headings = (
		el.matches("[data-reveal-heading]")
			? [el]
			: [...el.querySelectorAll<HTMLElement>("[data-reveal-heading]")]
	).filter((node) => inScope(node, scope));

	headings.forEach((heading, headingIndex) => {
		const lines = [...heading.querySelectorAll<HTMLElement>(".reveal-heading__line")];
		const texts = [...heading.querySelectorAll<HTMLElement>(".reveal-heading__text")];
		const base = headingIndex * lineStagger;
		lines.forEach((line, index) => {
			tl.to(
				line,
				{ scaleX: 1, duration: t.box, ease: ease.out },
				base + index * lineStagger,
			);
		});
		texts.forEach((text, index) => {
			tl.to(
				text,
				{ yPercent: 0, duration: t.text, ease: ease.out },
				base + t.lead + index * lineStagger,
			);
		});
	});

	const clips = (
		el.matches("[data-reveal='clip']")
			? [el]
			: [...el.querySelectorAll<HTMLElement>("[data-reveal='clip']")]
	).filter((node) => inScope(node, scope));

	for (const clip of clips) {
		tl.to(
			clip,
			{
				clipPath: "inset(0% 0% 0% 0%)",
				scale: 1,
				duration: t.clip,
				ease: ease.out,
				onComplete: () => gsap.set(clip, { clearProps: "transform,clipPath" }),
			},
			0,
		);
	}

	const counts = (
		el.matches("[data-reveal-count]")
			? [el]
			: [...el.querySelectorAll<HTMLElement>("[data-reveal-count]")]
	).filter((node) => inScope(node, scope));

	counts.forEach((count, index) => {
		playCount(count, tl, index * CHILD_STAGGER, t.count);
	});

	const fadeSet = new Set<HTMLElement>();
	if (scope) collectFades(el, scope, fadeSet);
	else if (el.matches("[data-reveal='fade-up']")) fadeSet.add(el);
	const fades = [...fadeSet];

	fades.forEach((node, index) => {
		tl.to(
			node,
			{
				y: 0,
				opacity: 1,
				duration: t.fade,
				ease: ease.out,
				onComplete: () => gsap.set(node, { clearProps: "transform,opacity,visibility" }),
			},
			index * CHILD_STAGGER,
		);
	});

	touched.add(el);
}

function playCount(el: HTMLElement, tl: gsap.core.Timeline, at: number, duration: number): void {
	const finalText = el.dataset.revealFinal ?? el.textContent?.trim() ?? "";
	el.dataset.revealFinal = finalText;
	const match = /^(\D*)(\d+)(\D*)$/.exec(finalText);
	if (!match) return;
	const prefix = match[1] ?? "";
	const digits = match[2] ?? "0";
	const suffix = match[3] ?? "";
	const target = Number(digits);
	const width = digits.length;
	const proxy = { n: 0 };
	el.textContent = `${prefix}${String(0).padStart(width, "0")}${suffix}`;
	tl.to(
		proxy,
		{
			n: target,
			duration,
			ease: ease.out,
			onUpdate: () => {
				el.textContent = `${prefix}${String(Math.round(proxy.n)).padStart(width, "0")}${suffix}`;
			},
			onComplete: () => {
				el.textContent = finalText;
			},
		},
		at,
	);
}

void stopWatching;
