import { gsap, ScrollTrigger, onReducedMotionChange, prefersReducedMotion } from "./motion";

export function bootDrop(): void {
	

	const root = document.querySelector<HTMLElement>("[data-drop]");
	if (root && root.dataset.dropReady !== "true") {
		root.dataset.dropReady = "true";

		const media = root.querySelector<HTMLElement>("[data-drop-media]");
		const bits = [...root.querySelectorAll<HTMLElement>("[data-drop-in]")];
		const phoneQuery = window.matchMedia("(max-width: 767px)");
		let ctx: gsap.Context | undefined;
		let tween: gsap.core.Timeline | undefined;
		const unlisten: Array<() => void> = [];

		function clearMotion(): void {
			unlisten.splice(0).forEach((stop) => stop());
			ctx?.revert();
			ctx = undefined;
			tween = undefined;
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
				if (media && !phone) {
					gsap.set(media, { scale: 1.06, transformOrigin: "50% 42%" });
				} else if (media) {
					gsap.set(media, { opacity: 0 });
				}
				gsap.set(bits, { y: phone ? 12 : 24, opacity: 0 });

				tween = gsap.timeline({ paused: true });
				if (media && !phone) {
					tween.to(media, { scale: 1, duration: 1.05, ease: "power3.out" }, 0);
				} else if (media) {
					tween.to(media, { opacity: 1, duration: 0.5, ease: "power3.out" }, 0);
				}
				tween.to(
					bits,
					{
						y: 0,
						opacity: 1,
						duration: phone ? 0.5 : 0.8,
						stagger: 0.1,
						ease: "power3.out",
						immediateRender: false,
					},
					0.05,
				);

				const trigger = ScrollTrigger.create({
					trigger: root,
					start: "top 82%",
					onEnter: () => tween?.play(),
					onEnterBack: () => tween?.play(),
					onLeaveBack: () => tween?.reverse(),
				});
				if (trigger.progress > 0) tween.play();
			}, root);

			const onFocus = () => tween?.play();
			root.addEventListener("focusin", onFocus);
			unlisten.push(() => root.removeEventListener("focusin", onFocus));
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
