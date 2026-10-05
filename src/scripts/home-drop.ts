import { ease, gsap, onReducedMotionChange, prefersReducedMotion } from "./motion";

export function bootDrop(): void {
	

	const root = document.querySelector<HTMLElement>("[data-drop]");
	if (root && root.dataset.dropReady !== "true") {
		root.dataset.dropReady = "true";

		const media = root.querySelector<HTMLElement>("[data-drop-media]");
		const bits = [...root.querySelectorAll<HTMLElement>("[data-drop-in]")];
		const phoneQuery = window.matchMedia("(max-width: 767px)");
		let ctx: gsap.Context | undefined;

		function clearMotion(): void {
			ctx?.revert();
			ctx = undefined;
		}

		function setup(reduced: boolean): void {
			clearMotion();

			const nodes = [media, ...bits].filter((node): node is HTMLElement => Boolean(node));
			if (reduced) {
				gsap.set(nodes, { clearProps: "transform,opacity" });
				return;
			}

			const phone = phoneQuery.matches;
			ctx = gsap.context(() => {
				const range = {
					trigger: root,
					start: "top 94%",
					end: phone ? "top 72%" : "top 52%",
					scrub: true,
				};
				if (media) {
					gsap.fromTo(
						media,
						{ scale: phone ? 1.04 : 1.12, y: phone ? 6 : 16, transformOrigin: "50% 42%" },
						{ scale: 1, y: 0, ease: ease.linear, scrollTrigger: range },
					);
				}
				if (bits.length > 0) {
					gsap.fromTo(
						bits,
						{ y: phone ? 8 : 16, opacity: 0 },
						{
							y: 0,
							opacity: 1,
							stagger: 0.035,
							ease: ease.linear,
							scrollTrigger: {
								trigger: root,
								start: "top 88%",
								end: phone ? "top 66%" : "top 50%",
								scrub: true,
							},
						},
					);
				}
			}, root);
		}

		const rebuild = () => setup(prefersReducedMotion());
		const stopReduced = onReducedMotionChange(rebuild);
		phoneQuery.addEventListener("change", rebuild);
		rebuild();

		window.addEventListener("pagehide", () => {
			clearMotion();
			stopReduced();
			phoneQuery.removeEventListener("change", rebuild);
		}, { once: true });
	}
}
