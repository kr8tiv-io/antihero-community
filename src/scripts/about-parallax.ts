import { ease, gsap, ScrollTrigger, onReducedMotionChange, prefersReducedMotion } from "./motion";

/**
 * About hero parallax. Transform only.
 * Desktop: mist travels furthest, the photo less, the headline least.
 * Phone keeps the photo drift and leaves mist and type still.
 * Reduced motion leaves every layer still.
 * Scrub replaces duration. ease none keeps the drift linear.
 */
export function bootAboutParallax(): void {
	const root = document.querySelector<HTMLElement>("[data-about-hero]");
	const photo = root?.querySelector<HTMLElement>("[data-about-photo]");
	const mist = root?.querySelector<HTMLElement>("[data-about-mist]");
	const copy = root?.querySelector<HTMLElement>("[data-about-copy]");
	if (!root || !photo || !mist || !copy || root.dataset.aboutReady === "true") return;

	root.dataset.aboutReady = "true";

	const phoneQuery = window.matchMedia("(max-width: 767px)");
	let ctx: gsap.Context | undefined;

	const clear = (): void => {
		ctx?.revert();
		ctx = undefined;
		root.classList.remove("is-live");
		gsap.set([photo, mist, copy], { clearProps: "transform" });
	};

	const travel = (portion: number): number => root.offsetHeight * portion;

	const setup = (reduced: boolean): void => {
		clear();
		if (reduced) return;

		const phone = phoneQuery.matches;
		root.classList.add("is-live");

		const layer = () => ({
			trigger: root,
			start: "top top",
			end: phone ? "center top" : "bottom top",
			scrub: phone ? 0.4 : 1.2,
			invalidateOnRefresh: true,
		});

		ctx = gsap.context(() => {
			gsap.fromTo(
				photo,
				{ y: () => travel(phone ? 0.03 : 0.05) },
				{
					y: () => travel(phone ? -0.06 : -0.12),
					ease: ease.linear,
					scrollTrigger: layer(),
				},
			);

			if (phone) return;

			gsap.fromTo(
				mist,
				{ y: () => travel(0.1) },
				{
					y: () => travel(-0.22),
					ease: ease.linear,
					scrollTrigger: layer(),
				},
			);

			gsap.fromTo(
				copy,
				{ y: () => travel(0.015) },
				{
					y: () => travel(-0.04),
					ease: ease.linear,
					scrollTrigger: layer(),
				},
			);
		}, root);
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
				if (trigger.trigger === root) trigger.kill();
			});
		},
		{ once: true },
	);
}
