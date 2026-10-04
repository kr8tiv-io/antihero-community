import { gsap, onReducedMotionChange, prefersReducedMotion } from "./motion";

export function bootPromise(): void {
	

	const root = document.querySelector<HTMLElement>("[data-promise]");
	if (root && root.dataset.promiseReady !== "true") {
		root.dataset.promiseReady = "true";

		const photo = root.querySelector<HTMLElement>("[data-promise-photo]");
		const words = [...root.querySelectorAll<HTMLElement>("[data-promise-word]")];
		const sub = root.querySelector<HTMLElement>("[data-promise-sub]");
		const lines = [...root.querySelectorAll<HTMLElement>("[data-promise-line]")];
		const mobileQuery = window.matchMedia("(max-width: 767px)");
		let ctx: gsap.Context | undefined;

		const tilt = (_index: number, element: Element) => Number((element as HTMLElement).dataset.rot ?? 0);

		/** Image lags the scroll by 20 percent, so it travels at 0.8x. */
		function lag(): number {
			return (root!.offsetHeight + window.innerHeight) * 0.1;
		}

		function setup(reduced: boolean): void {
			ctx?.revert();
			ctx = undefined;
			if (!photo || !sub || words.length === 0) return;

			if (reduced) {
				root!.classList.add("is-still");
				gsap.set([photo, sub, ...words, ...lines], { clearProps: "transform,opacity" });
				return;
			}

			root!.classList.remove("is-still");
			ctx = gsap.context(() => {
				// A staggered from() only hides the first item until its slot.
				// Set the whole group up front so every line can fall.
				const park = (targets: HTMLElement[], y: number) => {
					gsap.set(targets, {
						y,
						opacity: 0,
						rotation: targets === words ? tilt : 0,
					});
				};

				if (mobileQuery.matches) {
					park(words, -60);
					park([sub], 20);
					park(lines, 14);
					const drop = gsap.timeline({
						scrollTrigger: {
							trigger: root,
							start: "top 78%",
							toggleActions: "play none none reverse",
						},
					});
					drop.to(words, {
						y: 0,
						rotation: 0,
						opacity: 1,
						duration: 0.48,
						stagger: 0.12,
						ease: "power3.out",
						immediateRender: false,
					});
					drop.to(sub, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out", immediateRender: false }, ">");
					drop.to(
						lines,
						{
							y: 0,
							opacity: 1,
							duration: 0.35,
							stagger: 0.08,
							ease: "power3.out",
							immediateRender: false,
						},
						">-0.05",
					);
					return;
				}

				gsap.fromTo(
					photo,
					{ scale: 1.12, y: () => lag() },
					{
						scale: 1,
						y: () => -lag(),
						ease: "none",
						scrollTrigger: {
							trigger: root,
							start: "top bottom",
							end: "bottom top",
							scrub: true,
							invalidateOnRefresh: true,
						},
					},
				);

				park(words, -60);
				park([sub], 24);
				park(lines, 16);
				const tl = gsap.timeline({
					scrollTrigger: {
						trigger: root,
						start: "top 65%",
						end: "center center",
						scrub: 0.5,
						invalidateOnRefresh: true,
					},
				});
				tl.to(
					words,
					{
						y: 0,
						rotation: 0,
						opacity: 1,
						duration: 0.45,
						stagger: 0.07,
						ease: "back.out(1.4)",
						immediateRender: false,
					},
					0,
				);
				const landed = 0.07 * (words.length - 1) + 0.45;
				tl.to(sub, { y: 0, opacity: 1, duration: 0.35, ease: "power3.out", immediateRender: false }, landed);
				tl.to(
					lines,
					{
						y: 0,
						opacity: 1,
						duration: 0.3,
						stagger: 0.07,
						ease: "power3.out",
						immediateRender: false,
					},
					landed + 0.28,
				);
			}, root);
		}

		const rebuild = () => setup(prefersReducedMotion());
		const stopReduced = onReducedMotionChange(rebuild);
		mobileQuery.addEventListener("change", rebuild);
		rebuild();

		window.addEventListener("pagehide", () => {
			ctx?.revert();
			stopReduced();
			mobileQuery.removeEventListener("change", rebuild);
		}, { once: true });
	}
}
