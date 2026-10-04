import { gsap, ScrollTrigger, onReducedMotionChange, prefersReducedMotion } from "./motion";

export function bootDoors(): void {
	

	const root = document.querySelector<HTMLElement>("[data-doors]");
	if (root && root.dataset.doorsReady !== "true") {
		root.dataset.doorsReady = "true";

		const doors = [...root.querySelectorAll<HTMLElement>("[data-door]")];
		const faces = [...root.querySelectorAll<HTMLElement>("[data-door-face]")];
		const hoverQuery = window.matchMedia(
			"(min-width: 768px) and (hover: hover) and (pointer: fine)",
		);
		const playGen = new WeakMap<HTMLVideoElement, number>();
		let ctx: gsap.Context | undefined;
		let io: IntersectionObserver | undefined;
		let enterTween: gsap.core.Tween | undefined;
		const unlisten: Array<() => void> = [];

		function clearMotion(): void {
			unlisten.splice(0).forEach((stop) => stop());
			io?.disconnect();
			io = undefined;
			ctx?.revert();
			ctx = undefined;
			enterTween = undefined;
		}

		function saveDataOn(): boolean {
			const connection = (navigator as Navigator & { connection?: { saveData?: boolean } }).connection;
			return Boolean(connection?.saveData);
		}

		function setPlaying(video: HTMLVideoElement, playing: boolean): void {
			video.classList.toggle("is-playing", playing);
		}

		function showPoster(video: HTMLVideoElement): void {
			setPlaying(video, false);
			video.pause();
			video.querySelectorAll("source").forEach((source) => source.removeAttribute("src"));
			video.removeAttribute("src");
			video.load();
		}

		/** Attach WebM, then MP4, the first time this door should play. */
		function armSources(video: HTMLVideoElement): void {
			const sources = [...video.querySelectorAll("source")];
			if (sources.some((source) => source.getAttribute("src"))) return;
			sources.forEach((source) => {
				const src = source.dataset.src;
				if (src) source.src = src;
			});
			video.load();
		}

		/** Phones and save-data play once the door is in view. Desktop waits for hover too. */
		function sync(door: HTMLElement, reduced: boolean): void {
			const video = door.querySelector("video");
			if (!video) return;
			const generation = (playGen.get(video) ?? 0) + 1;
			playGen.set(video, generation);
			const inView = door.dataset.inview === "true";
			const hot = door.matches(":hover") || door.matches(":focus-visible");
			const light = !hoverQuery.matches || saveDataOn();
			const shouldPlay = !reduced && inView && (light ? true : hot);

			if (!shouldPlay) {
				video.pause();
				setPlaying(video, false);
				return;
			}

			armSources(video);
			video.muted = true;
			void video.play().then(
				() => {
					if (playGen.get(video) !== generation) {
						video.pause();
						setPlaying(video, false);
						return;
					}
					setPlaying(video, true);
				},
				() => {
					setPlaying(video, false);
				},
			);
		}

		function bindTilt(door: HTMLElement, face: HTMLElement): void {
			const rotX = gsap.quickTo(face, "rotationX", { duration: 0.6, ease: "power3.out" });
			const rotY = gsap.quickTo(face, "rotationY", { duration: 0.6, ease: "power3.out" });
			const lift = gsap.quickTo(face, "y", { duration: 0.45, ease: "power3.out" });

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
			doors.forEach((door) => {
				const video = door.querySelector("video");
				if (!video) return;
				video.pause();
				if (reduced) showPoster(video);
			});

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
					duration: hoverQuery.matches ? 0.8 : 0.55,
					stagger: 0.1,
					ease: "power3.out",
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

			io = new IntersectionObserver(
				(entries) => {
					entries.forEach((entry) => {
						const door = entry.target as HTMLElement;
						door.dataset.inview = entry.isIntersecting ? "true" : "false";
						sync(door, false);
					});
				},
				{ threshold: 0.6 },
			);
			doors.forEach((door) => {
				io?.observe(door);
				const onHot = () => sync(door, false);
				const onFocus = () => {
					enterTween?.play();
					sync(door, false);
				};
				door.addEventListener("pointerenter", onHot);
				door.addEventListener("pointerleave", onHot);
				door.addEventListener("focus", onFocus);
				door.addEventListener("blur", onHot);
				unlisten.push(() => {
					door.removeEventListener("pointerenter", onHot);
					door.removeEventListener("pointerleave", onHot);
					door.removeEventListener("focus", onFocus);
					door.removeEventListener("blur", onHot);
				});
			});
		}

		const rebuild = () => setup(prefersReducedMotion());
		const stopReduced = onReducedMotionChange(rebuild);
		hoverQuery.addEventListener("change", rebuild);
		rebuild();

		window.addEventListener("pagehide", () => {
			clearMotion();
			stopReduced();
			hoverQuery.removeEventListener("change", rebuild);
		}, { once: true });
	}
}
