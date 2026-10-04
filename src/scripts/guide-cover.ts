import { gsap, ScrollTrigger, onReducedMotionChange, prefersReducedMotion } from "./motion";

/**
 * Slow cover drift. Transform only. Phone travels less.
 * Reduced motion leaves the cover still and fully visible.
 * Scrub replaces duration. ease none keeps the drift linear.
 */
export function bootGuideCover(): void {
	const root = document.querySelector<HTMLElement>("[data-guide-detail]");
	const frame = root?.querySelector<HTMLElement>("[data-guide-cover-frame]");
	const drift = root?.querySelector<HTMLElement>("[data-guide-cover]");
	if (!root || !frame || !drift || frame.dataset.coverReady === "true") return;

	frame.dataset.coverReady = "true";

	const phoneQuery = window.matchMedia("(max-width: 767px)");
	let ctx: gsap.Context | undefined;

	const clear = (): void => {
		ctx?.revert();
		ctx = undefined;
		gsap.set(drift, { clearProps: "transform" });
	};

	const setup = (reduced: boolean): void => {
		clear();
		if (reduced) return;

		const phone = phoneQuery.matches;
		const scale = phone ? 1.04 : 1.12;
		const travel = phone ? 10 : 36;

		ctx = gsap.context(() => {
			gsap.fromTo(
				drift,
				{ y: travel / 2, scale, transformOrigin: "50% 42%" },
				{
					y: travel / -2,
					scale,
					ease: "none",
					scrollTrigger: {
						trigger: frame,
						start: "top bottom",
						end: phone ? "center center" : "bottom top",
						scrub: phone ? 0.4 : 1.2,
					},
				},
			);
		}, frame);
	};

	const rebuild = (): void => setup(prefersReducedMotion());
	const stopReduced = onReducedMotionChange(rebuild);
	phoneQuery.addEventListener("change", rebuild);
	rebuild();

	window.addEventListener(
		"pagehide",
		() => {
			clear();
			stopReduced();
			phoneQuery.removeEventListener("change", rebuild);
			ScrollTrigger.getAll().forEach((trigger) => {
				if (trigger.trigger === frame) trigger.kill();
			});
		},
		{ once: true },
	);
}
