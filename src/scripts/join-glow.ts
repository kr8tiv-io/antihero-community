import { gsap, onReducedMotionChange, prefersReducedMotion } from "./motion";

/**
 * Soft pulse behind the join button. Scale and opacity only.
 * Phone scale stays smaller. Reduced motion holds a still glow.
 */
export function bootJoinGlow(): void {
	const root = document.querySelector<HTMLElement>("[data-join-page]");
	const glow = root?.querySelector<HTMLElement>("[data-join-glow]");
	if (!root || !glow || root.dataset.glowReady === "true") return;

	root.dataset.glowReady = "true";

	const phoneQuery = window.matchMedia("(max-width: 767px)");
	let tween: gsap.core.Tween | undefined;

	const start = (): void => {
		tween?.kill();
		tween = undefined;
		if (prefersReducedMotion()) {
			root.classList.remove("is-live");
			gsap.set(glow, { scale: 1, opacity: 0.35 });
			return;
		}

		root.classList.add("is-live");
		const peak = phoneQuery.matches ? 1.05 : 1.14;
		tween = gsap.fromTo(
			glow,
			{ scale: 1, opacity: 0.28 },
			{
				scale: peak,
				opacity: 0.62,
				duration: 2.2,
				ease: "sine.inOut",
				yoyo: true,
				repeat: -1,
			},
		);
	};

	start();
	const stopReduced = onReducedMotionChange(start);
	phoneQuery.addEventListener("change", start);

	window.addEventListener(
		"pagehide",
		() => {
			tween?.kill();
			stopReduced();
			phoneQuery.removeEventListener("change", start);
			gsap.set(glow, { clearProps: "transform,opacity" });
		},
		{ once: true },
	);
}
