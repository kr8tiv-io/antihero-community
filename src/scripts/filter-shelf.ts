import { Flip, gsap, onReducedMotionChange, prefersReducedMotion } from "./motion";

/**
 * Shared category shelf. ?c=brand is the shareable filter.
 * pushState writes it, popstate reads it, so Back restores the previous filter.
 * Flip shuffles the grid. Reduced motion swaps visibility and does not tween.
 */

const CLEAR = "opacity,transform,scale,x,y,top,left,width,height,position";

export interface FilterShelfOptions {
	root: string;
	grid: string;
	card: string;
	empty: string;
	status: string;
	shelf: string;
	/** Singular noun for the status line, "guide" or "prompt". */
	noun: string;
	emptyStatus: string;
	readyKey: string;
}

export function bootFilterShelf(options: FilterShelfOptions): void {
	const root = document.querySelector<HTMLElement>(options.root);
	if (!root || root.dataset[options.readyKey] === "true") return;

	const grid = root.querySelector<HTMLElement>(options.grid);
	const empty = root.querySelector<HTMLElement>(options.empty);
	const status = root.querySelector<HTMLElement>(options.status);
	const shelf = root.querySelector<HTMLElement>(options.shelf);
	if (!grid || !empty || !shelf) return;

	root.dataset[options.readyKey] = "true";

	const buttons = [...shelf.querySelectorAll<HTMLButtonElement>("[data-filter]")];
	const known = new Set(buttons.map((button) => button.dataset.filter).filter((id): id is string => Boolean(id)));
	const cards = (): HTMLElement[] => [...grid.querySelectorAll<HTMLElement>(options.card)];

	let current = readFilter(known);
	let running: gsap.core.Animation | undefined;

	const clearMotion = (): void => {
		running?.kill();
		running = undefined;
		gsap.set(cards(), { clearProps: CLEAR });
	};

	const apply = (filter: string, animate: boolean): void => {
		const items = cards();
		const reduce = !animate || prefersReducedMotion();
		if (running) clearMotion();

		const state = reduce ? null : Flip.getState(items);
		let spot = 0;
		let shown = 0;

		for (const card of items) {
			const match = filter === "all" || card.dataset.category === filter;
			card.classList.toggle("is-gone", !match);
			card.setAttribute("aria-hidden", match ? "false" : "true");
			if (!match) continue;
			card.dataset.spot = String(spot % 4);
			spot += 1;
			shown += 1;
		}

		empty.hidden = shown > 0;

		for (const button of buttons) {
			button.setAttribute("aria-pressed", button.dataset.filter === filter ? "true" : "false");
		}

		if (animate && status) {
			status.textContent =
				shown === 0
					? options.emptyStatus
					: `Showing ${shown} ${shown === 1 ? options.noun : `${options.noun}s`}.`;
		}

		const notify = (): void => {
			root.dispatchEvent(new CustomEvent("filtershelf:change"));
		};

		if (!state) {
			notify();
			return;
		}

		running = Flip.from(state, {
			absolute: true,
			stagger: 0.03,
			duration: 0.6,
			ease: "power2.inOut",
			onEnter: (els) =>
				gsap.fromTo(
					els,
					{ opacity: 0, scale: 0.9 },
					{ opacity: 1, scale: 1, duration: 0.6, ease: "power2.inOut", stagger: 0.03 },
				),
			onLeave: (els) =>
				gsap.to(els, {
					opacity: 0,
					scale: 0.9,
					duration: 0.6,
					ease: "power2.inOut",
					stagger: 0.03,
				}),
			onComplete: () => {
				running = undefined;
				notify();
			},
		});
	};

	const writeUrl = (filter: string): void => {
		const url = new URL(window.location.href);
		if (filter === "all") url.searchParams.delete("c");
		else url.searchParams.set("c", filter);
		const next = `${url.pathname}${url.search}${url.hash}`;
		const here = `${window.location.pathname}${window.location.search}${window.location.hash}`;
		if (next === here) return;
		history.pushState({ filter }, "", next);
	};

	const pinButton = (filter: string): void => {
		const button = buttons.find((item) => item.dataset.filter === filter);
		if (!button) return;
		const left = button.offsetLeft - (shelf.clientWidth - button.offsetWidth) / 2;
		shelf.scrollTo({ left: Math.max(0, left), behavior: "auto" });
	};

	apply(current, false);
	if (current === "all" && new URLSearchParams(window.location.search).has("c")) {
		const url = new URL(window.location.href);
		url.searchParams.delete("c");
		history.replaceState({ filter: "all" }, "", `${url.pathname}${url.search}${url.hash}`);
	}

	shelf.addEventListener("click", (event) => {
		const button = (event.target as Element | null)?.closest<HTMLButtonElement>("[data-filter]");
		if (!button || !shelf.contains(button)) return;
		const filter = button.dataset.filter;
		if (!filter || filter === current || !known.has(filter)) return;
		current = filter;
		apply(filter, true);
		writeUrl(filter);
		pinButton(filter);
	});

	window.addEventListener("popstate", () => {
		current = readFilter(known);
		apply(current, true);
		pinButton(current);
	});

	onReducedMotionChange((reduced) => {
		if (!reduced) return;
		clearMotion();
		apply(current, false);
	});
}

function readFilter(known: Set<string>): string {
	const raw = new URLSearchParams(window.location.search).get("c");
	if (!raw) return "all";
	const value = raw.toLowerCase();
	return known.has(value) ? value : "all";
}
