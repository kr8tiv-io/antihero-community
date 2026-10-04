/**
 * Pop-up goal menu for /prompts.
 * Lenis stops while the dialog is open and starts again on close.
 * Phones and reduced motion never get the wipe or the stagger.
 */

import { ease, gsap, isMobile, onReducedMotionChange, prefersReducedMotion, ScrollTrigger } from "./motion";
import { getLenis } from "./smooth-scroll";

const DESK_CLIP = "inset(0% 0% 100% 0%)";
const OPEN_CLIP = "inset(0% 0% 0% 0%)";

let releaseActive: (() => void) | null = null;

export function releasePromptGoals(): void {
	releaseActive?.();
	releaseActive = null;
}

export function bootPromptGoals(): void {
	const root = document.querySelector<HTMLElement>("[data-prompts]");
	if (!root || root.dataset.goalsReady === "true") return;

	const menu = root.querySelector<HTMLElement>("[data-goal-menu]");
	const dialog = root.querySelector<HTMLElement>("[data-goal-dialog]");
	const sheet = root.querySelector<HTMLElement>("[data-goal-sheet]");
	const list = root.querySelector<HTMLElement>("[data-goal-list]");
	const bar = root.querySelector<HTMLElement>("[data-goal-bar]");
	const here = root.querySelector<HTMLElement>("[data-goal-here]");
	const hereCount = root.querySelector<HTMLElement>("[data-goal-here-count]");
	const sticky = root.querySelector<HTMLButtonElement>("[data-goal-sticky]");
	const sentinel = root.querySelector<HTMLElement>("[data-goal-sentinel]");
	if (!menu || !dialog || !sheet || !list || !bar || !here || !hereCount || !sticky || !sentinel) return;

	releasePromptGoals();
	root.dataset.goalsReady = "true";

	const links = (): HTMLAnchorElement[] => [...list.querySelectorAll<HTMLAnchorElement>("[data-goal-link]")];
	const sections = (): HTMLElement[] => [...root.querySelectorAll<HTMLElement>("[data-goal-section]")];
	const openers = (): HTMLButtonElement[] => [...menu.querySelectorAll<HTMLButtonElement>("[data-goal-open]")];

	let generation = 0;
	let open = false;
	let opener: HTMLElement | null = null;
	let clipFrom = DESK_CLIP;
	let currentId = "";
	let stickyOn = false;
	let timeline: gsap.core.Timeline | null = null;

	const headerOffset = (): number => {
		const raw = getComputedStyle(document.documentElement).getPropertyValue("--header-h");
		const value = Number.parseFloat(raw);
		return Number.isFinite(value) ? value : 56;
	};

	const setExpanded = (value: boolean): void => {
		for (const button of openers()) button.setAttribute("aria-expanded", value ? "true" : "false");
	};

	const lock = (): void => {
		document.documentElement.classList.add("goal-open");
		getLenis()?.stop();
	};

	const unlock = (): void => {
		document.documentElement.classList.remove("goal-open");
		getLenis()?.start();
	};

	const killMotion = (): void => {
		timeline?.kill();
		timeline = null;
		gsap.killTweensOf([dialog, sheet, bar, sticky, ...links()]);
	};

	const hideBar = (): void => {
		gsap.to(bar, {
			scaleX: 0,
			duration: prefersReducedMotion() ? 0 : 0.25,
			ease: ease.out,
			overwrite: "auto",
		});
	};

	const moveBar = (link: HTMLElement): void => {
		if (isMobile()) return;
		const label = link.querySelector<HTMLElement>(".goal-link__label") ?? link;
		if (label.offsetWidth < 1) return;
		if (bar.parentElement !== link) link.appendChild(bar);
		const y = label.offsetTop + label.offsetHeight + 6;
		gsap.set(bar, {
			x: 0,
			y,
			width: label.offsetWidth,
			scaleX: 0,
			transformOrigin: "left center",
		});
		gsap.to(bar, {
			scaleX: 1,
			duration: prefersReducedMotion() ? 0 : 0.35,
			ease: ease.out,
			overwrite: "auto",
		});
	};

	const syncHere = (): void => {
		const blocks = sections();
		if (blocks.length === 0) return;
		const mark = headerOffset() + 32;
		let current = blocks[0];
		if (!current) return;
		for (const section of blocks) {
			if (section.getBoundingClientRect().top <= mark) current = section;
		}
		const id = current.dataset.goal ?? "";
		if (id === currentId) return;
		currentId = id;
		const label = current.dataset.label ?? "";
		const count = current.dataset.countLabel ?? "";
		here.textContent = label;
		hereCount.textContent = count;
		sticky.setAttribute("aria-label", `You're in: ${label}, ${count}. What are you trying to do?`);
		for (const link of links()) {
			if (link.dataset.goal === id) link.setAttribute("aria-current", "true");
			else link.removeAttribute("aria-current");
		}
	};

	const setSticky = (show: boolean): void => {
		if (show === stickyOn) return;
		stickyOn = show;
		gsap.killTweensOf(sticky);
		if (!show) {
			const hide = (): void => {
				if (stickyOn) return;
				sticky.hidden = true;
				gsap.set(sticky, { clearProps: "transform,opacity,visibility" });
			};
			if (prefersReducedMotion()) {
				hide();
				return;
			}
			gsap.to(sticky, {
				autoAlpha: 0,
				y: isMobile() ? 12 : -8,
				duration: 0.25,
				ease: ease.out,
				overwrite: "auto",
				onComplete: hide,
			});
			return;
		}
		sticky.hidden = false;
		if (prefersReducedMotion()) {
			gsap.set(sticky, { autoAlpha: 1, y: 0 });
			return;
		}
		gsap.fromTo(
			sticky,
			{ autoAlpha: 0, y: isMobile() ? 12 : -8 },
			{ autoAlpha: 1, y: 0, duration: 0.35, ease: ease.out, overwrite: "auto" },
		);
	};

	const syncSticky = (): void => {
		setSticky(sentinel.getBoundingClientRect().bottom <= 8);
	};

	const focusables = (): HTMLElement[] =>
		[...dialog.querySelectorAll<HTMLElement>("button:not([disabled]), a[href]")].filter(
			(el) => el.tabIndex >= 0 && el.getClientRects().length > 0,
		);

	const phoneClip = (trigger: HTMLElement): string => {
		const sheetRect = sheet.getBoundingClientRect();
		const triggerRect = trigger.getBoundingClientRect();
		if (sheetRect.height < 1 || triggerRect.height < 1) return "inset(100% 0% 0% 0%)";
		const overlaps = triggerRect.bottom > sheetRect.top && triggerRect.top < sheetRect.bottom;
		if (!overlaps) return triggerRect.top < sheetRect.top ? DESK_CLIP : "inset(100% 0% 0% 0%)";
		const clamp = (value: number): number => Math.min(100, Math.max(0, value));
		const top = clamp(((triggerRect.top - sheetRect.top) / sheetRect.height) * 100);
		const right = clamp(((sheetRect.right - triggerRect.right) / sheetRect.width) * 100);
		const bottom = clamp(((sheetRect.bottom - triggerRect.bottom) / sheetRect.height) * 100);
		const left = clamp(((triggerRect.left - sheetRect.left) / sheetRect.width) * 100);
		return `inset(${top}% ${right}% ${bottom}% ${left}%)`;
	};

	const settleLines = (): void => {
		gsap.set(links(), { clearProps: "transform,opacity" });
		list.classList.remove("is-rising");
	};

	const hideDialog = (): void => {
		dialog.classList.remove("is-open");
		dialog.setAttribute("aria-hidden", "true");
		dialog.setAttribute("inert", "");
		gsap.set(dialog, { autoAlpha: 0 });
		gsap.set(sheet, { clearProps: "clipPath" });
		settleLines();
		hideBar();
		setExpanded(false);
	};

	const scrollToTarget = (el: HTMLElement, behavior: "smooth" | "auto", done: () => void): void => {
		let finished = false;
		const finish = (): void => {
			if (finished) return;
			finished = true;
			done();
		};
		const margin = Number.parseFloat(getComputedStyle(el).scrollMarginTop);
		const nativeOffset = Number.isFinite(margin) && margin > 0 ? margin : headerOffset();
		const top = window.scrollY + el.getBoundingClientRect().top - nativeOffset;
		const lenis = getLenis();
		if (lenis) {
			// Lenis already honors scroll-margin. A second offset would land short.
			lenis.scrollTo(el, {
				offset: 0,
				immediate: behavior === "auto",
				force: true,
				onComplete: finish,
			});
			window.setTimeout(finish, 1800);
			return;
		}
		window.scrollTo({ top: Math.max(0, top), behavior });
		if (behavior === "auto") {
			finish();
			return;
		}
		window.addEventListener("scrollend", () => finish(), { once: true });
		window.setTimeout(finish, 1200);
	};

	const goToGoal = (id: string): void => {
		const section = document.getElementById(`goal-${id}`);
		if (!(section instanceof HTMLElement) || !root.contains(section)) return;
		const url = new URL(window.location.href);
		url.searchParams.delete("c");
		url.searchParams.set("goal", id);
		url.hash = "";
		history.replaceState(null, "", `${url.pathname}?goal=${encodeURIComponent(id)}`);
		const behavior = prefersReducedMotion() ? "auto" : "smooth";
		const heading = section.querySelector<HTMLElement>("[data-goal-title]");
		scrollToTarget(section, behavior, () => {
			heading?.focus({ preventScroll: true });
			currentId = "";
			syncHere();
			syncSticky();
		});
	};

	const openMenu = (from: HTMLElement): void => {
		if (open) return;
		const token = ++generation;
		open = true;
		opener = from;
		setExpanded(true);
		dialog.removeAttribute("inert");
		dialog.setAttribute("aria-hidden", "false");
		lock();
		killMotion();

		const reduced = prefersReducedMotion();
		const lines = links();
		const current = lines.find((link) => link.dataset.goal === currentId) ?? lines[0];

		if (reduced) {
			clipFrom = OPEN_CLIP;
			gsap.set(sheet, { clipPath: OPEN_CLIP });
			gsap.set(lines, { yPercent: 0, opacity: 1, clearProps: "transform" });
			dialog.classList.add("is-open");
			timeline = gsap.timeline({
				onComplete: () => {
					if (token !== generation) return;
					current?.focus({ preventScroll: true });
				},
			});
			timeline.fromTo(dialog, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.2, ease: "none" });
			current?.focus({ preventScroll: true });
			return;
		}

		clipFrom = isMobile() ? phoneClip(from) : DESK_CLIP;
		gsap.set(sheet, { clipPath: clipFrom });
		gsap.set(lines, { yPercent: 110, opacity: 0 });
		gsap.set(bar, { scaleX: 0 });
		gsap.set(dialog, { autoAlpha: 1 });
		dialog.classList.add("is-open");
		list.classList.add("is-rising");
		const stagger = isMobile() ? 0.03 : 0.05;
		timeline = gsap.timeline({
			onComplete: () => {
				if (token !== generation) return;
				settleLines();
			},
		});
		timeline.to(sheet, { clipPath: OPEN_CLIP, duration: isMobile() ? 0.5 : 0.62, ease: ease.out }, 0);
		timeline.to(
			lines,
			{ yPercent: 0, opacity: 1, duration: isMobile() ? 0.4 : 0.5, stagger, ease: ease.out },
			isMobile() ? 0.08 : 0.16,
		);
		current?.focus({ preventScroll: true });
	};

	const closeMenu = (goalId?: string): void => {
		if (!open) return;
		const token = ++generation;
		open = false;
		const back = opener;
		killMotion();
		const reduced = prefersReducedMotion();
		const lines = links();

		const finish = (): void => {
			if (token !== generation) return;
			hideDialog();
			unlock();
			if (goalId) {
				goToGoal(goalId);
				return;
			}
			back?.focus({ preventScroll: true });
		};

		if (reduced) {
			timeline = gsap.timeline({ onComplete: finish });
			timeline.to(dialog, { autoAlpha: 0, duration: 0.2, ease: "none" });
			return;
		}

		list.classList.add("is-rising");
		timeline = gsap.timeline({ onComplete: finish });
		timeline.to(
			lines,
			{
				yPercent: 110,
				opacity: 0,
				duration: isMobile() ? 0.28 : 0.32,
				stagger: { each: isMobile() ? 0.02 : 0.04, from: "end" },
				ease: "power2.in",
			},
			0,
		);
		timeline.to(sheet, { clipPath: clipFrom, duration: isMobile() ? 0.38 : 0.45, ease: "power3.in" }, 0.08);
	};

	const moveGoal = (direction: number): void => {
		const all = links();
		if (all.length === 0) return;
		const index = all.findIndex((link) => link === document.activeElement);
		if (index === -1) {
			(direction > 0 ? all[0] : all[all.length - 1])?.focus();
			return;
		}
		all[(index + direction + all.length) % all.length]?.focus();
	};

	const onKey = (event: KeyboardEvent): void => {
		if (!open) return;
		if (event.key === "Escape") {
			event.preventDefault();
			closeMenu();
			return;
		}
		if (event.key === "ArrowDown" || event.key === "ArrowRight") {
			event.preventDefault();
			moveGoal(1);
			return;
		}
		if (event.key === "ArrowUp" || event.key === "ArrowLeft") {
			event.preventDefault();
			moveGoal(-1);
			return;
		}
		if (event.key === "Home") {
			event.preventDefault();
			links()[0]?.focus();
			return;
		}
		if (event.key === "End") {
			event.preventDefault();
			const all = links();
			all[all.length - 1]?.focus();
			return;
		}
		if (event.key !== "Tab") return;
		const nodes = focusables();
		if (nodes.length === 0) return;
		const first = nodes[0];
		const last = nodes[nodes.length - 1];
		const active = document.activeElement;
		if (event.shiftKey && (active === first || !nodes.includes(active as HTMLElement))) {
			event.preventDefault();
			last?.focus();
		} else if (!event.shiftKey && (active === last || !nodes.includes(active as HTMLElement))) {
			event.preventDefault();
			first?.focus();
		}
	};

	const onClick = (event: MouseEvent): void => {
		const target = event.target;
		if (!(target instanceof Element) || !menu.contains(target)) return;
		const link = target.closest<HTMLAnchorElement>("[data-goal-link]");
		if (link && list.contains(link)) {
			event.preventDefault();
			const id = link.dataset.goal;
			if (id) closeMenu(id);
			return;
		}
		if (target.closest("[data-goal-close]")) {
			event.preventDefault();
			closeMenu();
			return;
		}
		const button = target.closest<HTMLButtonElement>("[data-goal-open]");
		if (!button || !menu.contains(button)) return;
		event.preventDefault();
		if (open) closeMenu();
		else openMenu(button);
	};

	const onOver = (event: Event): void => {
		if (!open || isMobile()) return;
		const link = (event.target as Element | null)?.closest<HTMLElement>("[data-goal-link]");
		if (!link || !list.contains(link)) return;
		moveBar(link);
	};

	const onFocusIn = (event: Event): void => {
		if (!open || isMobile()) return;
		const link = (event.target as Element | null)?.closest<HTMLElement>("[data-goal-link]");
		if (!link || !list.contains(link)) return;
		moveBar(link);
	};

	const onLeave = (): void => {
		const active = document.activeElement;
		if (active instanceof HTMLElement && active.matches("[data-goal-link]") && list.contains(active)) {
			moveBar(active);
			return;
		}
		hideBar();
	};

	const decodeHash = (): string => {
		const hash = window.location.hash;
		if (!hash || hash === "#") return "";
		try {
			return decodeURIComponent(hash.slice(1));
		} catch {
			return "";
		}
	};

	const land = (): void => {
		const hashId = decodeHash();
		const hashEl = hashId ? document.getElementById(hashId) : null;
		const hashHere = hashEl instanceof HTMLElement && root.contains(hashEl) ? hashEl : null;
		const params = new URLSearchParams(window.location.search);
		const named = params.get("goal");
		const legacy = params.get("c") === "websites" ? "websites" : null;
		const goalId = named || legacy;
		const goalEl = goalId ? document.getElementById(`goal-${goalId}`) : null;
		const goalHere = goalEl instanceof HTMLElement && root.contains(goalEl) ? goalEl : null;

		if (legacy && goalHere) {
			params.delete("c");
			if (!params.get("goal")) params.set("goal", "websites");
			const query = params.toString();
			const hash = hashHere ? window.location.hash : "";
			history.replaceState(null, "", `${window.location.pathname}${query ? `?${query}` : ""}${hash}`);
		}

		const target = hashHere ?? goalHere;
		if (!target) {
			syncHere();
			syncSticky();
			return;
		}
		const goalSection = target.hasAttribute("data-goal-section") ? target : null;
		scrollToTarget(target, "auto", () => {
			if (goalSection) {
				goalSection.querySelector<HTMLElement>("[data-goal-title]")?.focus({ preventScroll: true });
			}
			currentId = "";
			syncHere();
			syncSticky();
			ScrollTrigger.refresh();
		});
	};

	menu.addEventListener("click", onClick);
	document.addEventListener("keydown", onKey);
	list.addEventListener("pointerover", onOver);
	list.addEventListener("focusin", onFocusIn);
	list.addEventListener("pointerleave", onLeave);

	const place = ScrollTrigger.create({
		trigger: root,
		start: "top top",
		end: "bottom bottom",
		onUpdate: () => {
			syncHere();
			syncSticky();
		},
		onRefresh: () => {
			currentId = "";
			syncHere();
			syncSticky();
		},
	});

	const stopReduced = onReducedMotionChange(() => {
		if (!open) return;
		killMotion();
		if (prefersReducedMotion()) {
			gsap.set(sheet, { clipPath: OPEN_CLIP });
			gsap.set(dialog, { autoAlpha: 1 });
			settleLines();
		}
	});

	const frame = window.requestAnimationFrame(() => {
		land();
		ScrollTrigger.refresh();
	});

	releaseActive = () => {
		window.cancelAnimationFrame(frame);
		generation += 1;
		open = false;
		menu.removeEventListener("click", onClick);
		document.removeEventListener("keydown", onKey);
		list.removeEventListener("pointerover", onOver);
		list.removeEventListener("focusin", onFocusIn);
		list.removeEventListener("pointerleave", onLeave);
		place.kill();
		stopReduced();
		killMotion();
		hideDialog();
		unlock();
		if (root.isConnected) root.dataset.goalsReady = "";
	};
}
