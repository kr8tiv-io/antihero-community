import { duration, ease, gsap, ScrollTrigger, onReducedMotionChange, prefersReducedMotion } from "./motion";

export function bootDoors(): void {
	const root = document.querySelector<HTMLElement>("[data-doors]");
	if (!root || root.dataset.doorsReady === "true") return;
	root.dataset.doorsReady = "true";

	const doors = [...root.querySelectorAll<HTMLElement>("[data-door]")];
	const faces = [...root.querySelectorAll<HTMLElement>("[data-door-face]")];
	const hoverQuery = window.matchMedia("(min-width: 768px) and (hover: hover) and (pointer: fine)");
	let ctx: gsap.Context | undefined;
	let enterTween: gsap.core.Tween | undefined;
	const unlisten: Array<() => void> = [];

	function clearMotion(): void {
		unlisten.splice(0).forEach((stop) => stop());
		ctx?.revert();
		ctx = undefined;
		enterTween = undefined;
	}

	function bindTilt(door: HTMLElement, face: HTMLElement): void {
		const rotX = gsap.quickTo(face, "rotationX", { duration: duration.settle, ease: ease.out });
		const rotY = gsap.quickTo(face, "rotationY", { duration: duration.settle, ease: ease.out });
		const lift = gsap.quickTo(face, "y", { duration: duration.fast, ease: ease.out });

		const rest = () => {
			rotX(0);
			rotY(0);
			if (!door.matches(":hover") && !door.matches(":focus-visible")) lift(0);
		};

		const onMove = (event: PointerEvent) => {
			const rect = face.getBoundingClientRect();
			const nx = (event.clientX - rect.left) / rect.width - 0.5;
			const ny = (event.clientY - rect.top) / rect.height - 0.5;
			rotY(Math.max(-6, Math.min(6, nx * 12)));
			rotX(Math.max(-6, Math.min(6, ny * -12)));
		};
		const onEnter = () => lift(-8);
		const onFocus = () => lift(-8);

		door.addEventListener("pointermove", onMove);
		door.addEventListener("pointerenter", onEnter);
		door.addEventListener("pointerleave", rest);
		door.addEventListener("focus", onFocus);
		door.addEventListener("blur", rest);
		unlisten.push(() => {
			door.removeEventListener("pointermove", onMove);
			door.removeEventListener("pointerenter", onEnter);
			door.removeEventListener("pointerleave", rest);
			door.removeEventListener("focus", onFocus);
			door.removeEventListener("blur", rest);
			gsap.set(face, { clearProps: "transform" });
		});
	}

	function setup(reduced: boolean): void {
		clearMotion();

		if (reduced) {
			gsap.set(doors, { clearProps: "transform,opacity" });
			gsap.set(faces, { clearProps: "transform" });
			return;
		}

		const rise = hoverQuery.matches ? 56 : 28;
		ctx = gsap.context(() => {
			gsap.set(doors, { y: rise, opacity: 0 });
			enterTween = gsap.to(doors, {
				y: 0,
				opacity: 1,
				duration: hoverQuery.matches ? duration.base : duration.settle,
				stagger: 0.1,
				ease: ease.out,
				paused: true,
				immediateRender: false,
			});
			const trigger = ScrollTrigger.create({
				trigger: root,
				start: "top 82%",
				onEnter: () => enterTween?.play(),
				onEnterBack: () => enterTween?.play(),
				onLeaveBack: () => enterTween?.reverse(),
			});
			if (trigger.progress > 0) enterTween?.play();
		}, root);

		if (hoverQuery.matches) {
			doors.forEach((door, index) => {
				const face = faces[index];
				if (face) bindTilt(door, face);
			});
		}

		doors.forEach((door) => {
			const onFocus = () => enterTween?.play();
			door.addEventListener("focus", onFocus);
			unlisten.push(() => door.removeEventListener("focus", onFocus));
		});
	}

	const rebuild = () => setup(prefersReducedMotion());
	const stopReduced = onReducedMotionChange(rebuild);
	hoverQuery.addEventListener("change", rebuild);
	rebuild();

	window.addEventListener(
		"pagehide",
		() => {
			clearMotion();
			stopReduced();
			hoverQuery.removeEventListener("change", rebuild);
		},
		{ once: true },
	);
}
