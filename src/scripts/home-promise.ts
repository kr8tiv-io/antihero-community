import { ease, gsap, onReducedMotionChange, prefersReducedMotion } from "./motion";

/**
 * Promise scroll story.
 * The first 0.08 of the scrub is the hero dissolve: the film fades in
 * while the hero mask opens. Leave that window where it is.
 * Scrubbed tweens use ease.linear. Words keep their data-rot angles.
 * The film plays only near the viewport, and never under reduced motion
 * or Save-Data.
 */

type FilmVideo = HTMLVideoElement & { dataset: DOMStringMap };

function saveDataOn(): boolean {
	const nav = navigator as Navigator & { connection?: { saveData?: boolean } };
	return Boolean(nav.connection?.saveData);
}

function phoneNow(): boolean {
	return window.matchMedia("(max-width: 767px)").matches;
}

function filmStem(phone: boolean): string {
	return phone ? "/media/promise-loop-mobile" : "/media/promise-loop";
}

function disarm(video: HTMLVideoElement): void {
	video.pause();
	video.querySelectorAll("source").forEach((source) => source.remove());
	video.removeAttribute("src");
	video.classList.remove("is-playing");
	delete video.dataset.armed;
	delete video.dataset.base;
	try {
		video.load();
	} catch {
		// The element is already going away.
	}
}

function arm(video: HTMLVideoElement, phone: boolean): void {
	const stem = filmStem(phone);
	if (video.dataset.armed === "1" && video.dataset.base === stem) return;
	disarm(video);
	video.dataset.base = stem;
	video.poster = `${stem}-poster.jpg`;
	video.muted = true;
	video.defaultMuted = true;
	video.loop = true;
	video.playsInline = true;
	video.preload = "none";
	const webm = document.createElement("source");
	webm.src = `${stem}.webm`;
	webm.type = "video/webm";
	const mp4 = document.createElement("source");
	mp4.src = `${stem}.mp4`;
	mp4.type = "video/mp4";
	video.append(webm, mp4);
	video.dataset.armed = "1";
	video.load();
}

export function bootPromise(): void {
	const root = document.querySelector<HTMLElement>("[data-promise]");
	if (!root || root.dataset.promiseReady === "true") return;
	root.dataset.promiseReady = "true";

	const film = root.querySelector<HTMLElement>("[data-promise-film]");
	const shade = root.querySelector<HTMLElement>("[data-promise-shade]");
	const copy = root.querySelector<HTMLElement>("[data-promise-copy]");
	const video = root.querySelector<FilmVideo>("[data-promise-video]");
	const words = [...root.querySelectorAll<HTMLElement>("[data-promise-word]")];
	const sub = root.querySelector<HTMLElement>("[data-promise-sub]");
	const lines = [...root.querySelectorAll<HTMLElement>("[data-promise-line]")];
	const mobileQuery = window.matchMedia("(max-width: 767px)");
	let ctx: gsap.Context | undefined;
	let observer: IntersectionObserver | null = null;
	let saveWatcher: (() => void) | null = null;

	const tilt = (_index: number, element: Element) => Number((element as HTMLElement).dataset.rot ?? 0);

	function travel(): number {
		if (mobileQuery.matches) return window.innerHeight * 0.035;
		return ((root?.offsetHeight ?? 0) + window.innerHeight) * 0.07;
	}

	function allowed(): boolean {
		return !prefersReducedMotion() && !saveDataOn();
	}

	function stopFilm(): void {
		observer?.disconnect();
		observer = null;
		if (video) disarm(video);
	}

	function watchFilm(): void {
		stopFilm();
		if (!video || !allowed()) return;
		observer = new IntersectionObserver(
			(entries) => {
				const hit = entries.some((entry) => entry.isIntersecting);
				if (!allowed()) {
					stopFilm();
					return;
				}
				if (hit) {
					arm(video, mobileQuery.matches);
					video
						.play()
						.then(() => video.classList.add("is-playing"))
						.catch(() => undefined);
					return;
				}
				video.pause();
			},
			{ rootMargin: "18% 0px", threshold: 0.01 },
		);
		observer.observe(root!);
	}

	function setup(reduced: boolean): void {
		ctx?.revert();
		ctx = undefined;
		if (!film || !shade || !copy || !sub || words.length === 0) return;

		if (reduced) {
			root!.classList.add("is-still");
			gsap.set([film, shade, copy, sub, ...words, ...lines], { clearProps: "transform,opacity" });
			film.style.willChange = "auto";
			stopFilm();
			return;
		}

		root!.classList.remove("is-still");
		const phone = mobileQuery.matches;
		// Stamps finish while the sticky stage is on screen, before the handoff.
		const wordStagger = phone ? 0.012 : 0.018;
		const wordDur = phone ? 0.03 : 0.04;
		const wordsAt = phone ? 0.28 : 0.3;
		const wordsEnd = wordsAt + wordStagger * Math.max(0, words.length - 1) + wordDur;

		ctx = gsap.context(() => {
			gsap.set(film, {
				scale: 1.15,
				opacity: 0,
				y: () => travel(),
				transformOrigin: "center center",
			});
			gsap.set(shade, { opacity: phone ? 0.45 : 0.36 });
			gsap.set(words, {
				y: phone ? 16 : 26,
				scale: phone ? 1.04 : 1.08,
				opacity: 0,
				rotation: tilt,
				transformOrigin: "left center",
			});
			gsap.set(sub, { y: phone ? 10 : 16, opacity: 0 });
			gsap.set(lines, { y: phone ? 8 : 12, opacity: 0 });
			gsap.set(copy, { opacity: 1, y: 0 });

			const flight = gsap.timeline({
				defaults: { ease: ease.linear },
				scrollTrigger: {
					trigger: root,
					start: "top bottom",
					end: "bottom top",
					scrub: true,
					invalidateOnRefresh: true,
					onToggle: (self) => {
						film.style.willChange = self.isActive ? "transform, opacity" : "auto";
					},
				},
			});

			// Dissolve window. Matches the hero mask. Do not lengthen it.
			flight.to(film, { opacity: 1, duration: 0.08, immediateRender: false }, 0);
			flight.fromTo(
				film,
				{ y: () => travel() },
				{ y: () => travel() * 0.35, duration: 0.08, immediateRender: false },
				0,
			);
			// The 0.92 weight is the slow parallax after the dissolve. Leave that span.
			flight.to(film, { y: () => -travel() * (phone ? 0.28 : 0.45), duration: 0.92, immediateRender: false }, 0.08);
			flight.to(film, { scale: 1, duration: phone ? 0.28 : 0.4, immediateRender: false }, 0);

			flight.to(shade, { opacity: 1, duration: phone ? 0.16 : 0.2, immediateRender: false }, 0.26);

			flight.to(
				words,
				{
					y: 0,
					scale: 1,
					opacity: 1,
					rotation: tilt,
					duration: wordDur,
					stagger: wordStagger,
					immediateRender: false,
				},
				wordsAt,
			);
			flight.to(sub, { y: 0, opacity: 1, duration: phone ? 0.03 : 0.035, immediateRender: false }, wordsEnd);
			flight.to(
				lines,
				{
					y: 0,
					opacity: 1,
					duration: phone ? 0.028 : 0.03,
					stagger: 0.008,
					immediateRender: false,
				},
				wordsEnd + 0.02,
			);

			// Soft handoff while the sticky stage is still in view, after the copy has landed.
			flight.to(
				film,
				{ scale: phone ? 0.985 : 0.97, opacity: phone ? 0.78 : 0.55, duration: 0.1, immediateRender: false },
				0.56,
			);
			flight.to(copy, { y: phone ? -8 : -16, opacity: 0, duration: 0.1, immediateRender: false }, 0.56);
		}, root);

		watchFilm();
	}

	const rebuild = () => setup(prefersReducedMotion());
	const stopReduced = onReducedMotionChange(rebuild);
	mobileQuery.addEventListener("change", rebuild);

	const connection = (navigator as Navigator & { connection?: EventTarget }).connection;
	if (connection && "addEventListener" in connection) {
		const onSave = () => rebuild();
		connection.addEventListener("change", onSave);
		saveWatcher = () => connection.removeEventListener("change", onSave);
	}

	rebuild();

	window.addEventListener(
		"pagehide",
		() => {
			ctx?.revert();
			stopFilm();
			stopReduced();
			saveWatcher?.();
			mobileQuery.removeEventListener("change", rebuild);
			delete root.dataset.promiseReady;
		},
		{ once: true },
	);
}
