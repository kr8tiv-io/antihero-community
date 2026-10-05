import { duration, ease, gsap, onReducedMotionChange, prefersReducedMotion } from "./motion";

export function bootPromise(): void {
	const root = document.querySelector<HTMLElement>("[data-promise]");
	if (!root || root.dataset.promiseReady === "true") return;
	root.dataset.promiseReady = "true";

	const photo = root.querySelector<HTMLElement>("[data-promise-photo]");
	const stage = root.querySelector<HTMLElement>("[data-promise-stage]");
	const hero = document.querySelector<HTMLElement>("[data-hero]");
	const words = [...root.querySelectorAll<HTMLElement>("[data-promise-word]")];
	const sub = root.querySelector<HTMLElement>("[data-promise-sub]");
	const lines = [...root.querySelectorAll<HTMLElement>("[data-promise-line]")];
	const mobileQuery = window.matchMedia("(max-width: 767px)");
	let ctx: gsap.Context | undefined;

	const tilt = (_index: number, element: Element) => Number((element as HTMLElement).dataset.rot ?? 0);

	function travel(): number {
		if (mobileQuery.matches) return window.innerHeight * 0.05;
		return ((root?.offsetHeight ?? 0) + window.innerHeight) * 0.07;
	}

	function mark(on: boolean): void {
		const value = on ? "transform, opacity" : "auto";
		for (const el of [...words, sub, ...lines]) {
			if (el) el.style.willChange = value;
		}
	}

	function setup(reduced: boolean): void {
		ctx?.revert();
		ctx = undefined;
		if (!photo || !sub || words.length === 0) return;

		if (reduced) {
			root!.classList.add("is-still");
			gsap.set([photo, sub, ...words, ...lines], { clearProps: "transform,opacity,filter" });
			photo.style.willChange = "auto";
			mark(false);
			return;
		}

		root!.classList.remove("is-still");
		const phone = mobileQuery.matches;

		ctx = gsap.context(() => {
			gsap.set(photo, { scale: 1.12, opacity: 0, y: () => travel(), transformOrigin: "center center" });
			gsap.set(words, {
				y: phone ? 22 : 28,
				opacity: 0,
				rotation: tilt,
				transformOrigin: "left center",
			});
			gsap.set(sub, { y: 16, opacity: 0 });
			gsap.set(lines, { y: 12, opacity: 0 });

			const flight = gsap.timeline({
				defaults: { ease: ease.linear },
				scrollTrigger: {
					trigger: root,
					start: "top bottom",
					end: "bottom top",
					scrub: true,
					invalidateOnRefresh: true,
					onToggle: (self) => {
						photo.style.willChange = self.isActive ? "transform, opacity" : "auto";
					},
				},
			});
			flight.fromTo(
				photo,
				{ scale: 1.12, opacity: 0, y: () => travel() },
				{ scale: 1, opacity: 1, y: () => travel() * 0.35, duration: 0.08, immediateRender: false },
				0,
			);
			flight.to(photo, { y: () => -travel(), duration: 0.92, immediateRender: false }, 0.08);

			const reveal = gsap.timeline({
				scrollTrigger: {
					trigger: phone ? (hero ?? root) : (stage ?? root),
					start: phone ? "bottom top" : "top 60%",
					toggleActions: "play none none reverse",
				},
				onStart: () => mark(true),
				onComplete: () => mark(false),
				onReverseComplete: () => mark(false),
			});
			reveal.to(words, {
				y: 0,
				opacity: 1,
				rotation: tilt,
				duration: duration.base,
				stagger: 0.12,
				ease: ease.expo,
				immediateRender: false,
			});
			const afterWords = 0.12 * Math.max(0, words.length - 1) + 0.48;
			reveal.to(
				sub,
				{ y: 0, opacity: 1, duration: 0.7, ease: ease.expo, immediateRender: false },
				afterWords,
			);
			reveal.to(
				lines,
				{
					y: 0,
					opacity: 1,
					duration: 0.55,
					stagger: 0.09,
					ease: ease.expo,
					immediateRender: false,
				},
				afterWords + 0.4,
			);
		}, root);
	}

	const rebuild = () => setup(prefersReducedMotion());
	const stopReduced = onReducedMotionChange(rebuild);
	mobileQuery.addEventListener("change", rebuild);
	rebuild();

	window.addEventListener(
		"pagehide",
		() => {
			ctx?.revert();
			stopReduced();
			mobileQuery.removeEventListener("change", rebuild);
		},
		{ once: true },
	);
}
