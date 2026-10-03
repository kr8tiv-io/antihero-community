/**
 * Desktop hover previews load on the first hover. Phones stay on the poster.
 * The modal builds a YouTube iframe or a native player only after a click.
 */

import { isMobile, onReducedMotionChange, prefersReducedMotion } from "./motion";

const YOUTUBE_ID = /^[A-Za-z0-9_-]{6,20}$/;
const FOCUSABLE = "a[href], button:not([disabled]), iframe, video, [tabindex]:not([tabindex='-1'])";

function previewsAllowed(): boolean {
	return !isMobile() && !prefersReducedMotion();
}

function safePlayableUrl(value: string): string | null {
	if (value.startsWith("/") && !value.startsWith("//") && !value.includes("\\")) return value;
	try {
		const url = new URL(value);
		if (url.protocol === "https:" || url.protocol === "http:") return url.href;
	} catch {
		return null;
	}
	return null;
}

function ensurePreview(media: HTMLElement, src: string): HTMLVideoElement {
	const existing = media.querySelector<HTMLVideoElement>(".video-preview");
	if (existing) return existing;
	const video = document.createElement("video");
	video.className = "video-preview";
	video.muted = true;
	video.defaultMuted = true;
	video.loop = true;
	video.playsInline = true;
	video.preload = "none";
	video.tabIndex = -1;
	video.setAttribute("playsinline", "");
	video.setAttribute("aria-hidden", "true");
	video.src = src;
	media.appendChild(video);
	return video;
}

function stopPreview(media: HTMLElement): void {
	const video = media.querySelector<HTMLVideoElement>(".video-preview");
	media.classList.remove("is-playing");
	if (!video) return;
	video.pause();
	try {
		video.currentTime = 0;
	} catch {
		// The file may not have a timeline yet.
	}
}

function playPreview(media: HTMLElement): void {
	if (!previewsAllowed()) return;
	const src = media.dataset.preview;
	if (!src) return;
	const video = ensurePreview(media, src);
	media.classList.add("is-playing");
	void video.play().catch(() => {
		media.classList.remove("is-playing");
	});
}

function bootPreviews(root: HTMLElement): void {
	const medias = [...root.querySelectorAll<HTMLElement>("[data-video-media][data-preview]")];

	for (const media of medias) {
		const card = media.closest<HTMLElement>("[data-video-card]");
		if (!card) continue;

		card.addEventListener("pointerenter", () => playPreview(media));
		card.addEventListener("pointerleave", () => stopPreview(media));
		card.addEventListener("focusin", () => playPreview(media));
		card.addEventListener("focusout", (event) => {
			const next = event.relatedTarget;
			if (next instanceof Node && card.contains(next)) return;
			stopPreview(media);
		});
	}

	const halt = (): void => {
		for (const media of medias) stopPreview(media);
	};

	const watch = (query: string): void => {
		window.matchMedia(query).addEventListener("change", halt);
	};
	watch("(width < 768px)");
	watch("(pointer: coarse)");
	onReducedMotionChange((reduced) => {
		if (reduced) halt();
	});
}

function focusable(dialog: HTMLElement): HTMLElement[] {
	return [...dialog.querySelectorAll<HTMLElement>(FOCUSABLE)].filter((el) => {
		if (el.hasAttribute("disabled")) return false;
		return el.getClientRects().length > 0;
	});
}

function bootModal(root: HTMLElement): void {
	const dialog = root.querySelector<HTMLDialogElement>("[data-video-modal]");
	const stage = root.querySelector<HTMLElement>("[data-video-stage]");
	const title = root.querySelector<HTMLElement>("[data-video-title]");
	const closeButton = root.querySelector<HTMLButtonElement>("[data-video-close]");
	if (!dialog || !stage || !title || !closeButton) return;

	let opener: HTMLElement | null = null;

	const clearStage = (): void => {
		stage.replaceChildren();
	};

	const close = (): void => {
		if (dialog.open) dialog.close();
	};

	const onKeydown = (event: KeyboardEvent): void => {
		if (event.key !== "Tab") return;
		const items = focusable(dialog);
		if (items.length === 0) return;
		const first = items[0];
		const last = items[items.length - 1];
		if (!first || !last) return;
		if (event.shiftKey && document.activeElement === first) {
			event.preventDefault();
			last.focus();
		} else if (!event.shiftKey && document.activeElement === last) {
			event.preventDefault();
			first.focus();
		}
	};

	const open = (button: HTMLButtonElement): void => {
		const name = button.dataset.videoTitle || "Replay";
		const youtubeId = button.dataset.youtubeId ?? "";
		const fileUrl = button.dataset.videoUrl ? safePlayableUrl(button.dataset.videoUrl) : null;
		clearStage();
		title.textContent = name;

		if (YOUTUBE_ID.test(youtubeId)) {
			const frame = document.createElement("iframe");
			const id = encodeURIComponent(youtubeId);
			frame.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`;
			frame.title = name;
			frame.allow =
				"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
			frame.allowFullscreen = true;
			frame.referrerPolicy = "strict-origin-when-cross-origin";
			stage.appendChild(frame);
		} else if (fileUrl) {
			const video = document.createElement("video");
			video.controls = true;
			video.playsInline = true;
			video.preload = "metadata";
			video.src = fileUrl;
			const poster = button.dataset.videoPoster;
			if (poster) video.poster = poster;
			video.setAttribute("aria-label", name);
			stage.appendChild(video);
			void video.play().catch(() => undefined);
		} else {
			return;
		}

		opener = button;
		if (!dialog.open) dialog.showModal();
		closeButton.focus();
	};

	root.addEventListener("click", (event) => {
		const target = event.target;
		if (!(target instanceof Element)) return;
		const button = target.closest<HTMLButtonElement>("[data-video-open]");
		if (!button || !root.contains(button)) return;
		open(button);
	});

	closeButton.addEventListener("click", close);

	dialog.addEventListener("click", (event) => {
		if (event.target === dialog) close();
	});

	dialog.addEventListener("close", () => {
		clearStage();
		dialog.removeEventListener("keydown", onKeydown);
		opener?.focus();
		opener = null;
	});

	dialog.addEventListener("cancel", () => {
		clearStage();
	});

	const armKeys = (): void => {
		dialog.addEventListener("keydown", onKeydown);
	};
	dialog.addEventListener("toggle", () => {
		if (dialog.open) armKeys();
	});
}

export function bootVideoCards(): void {
	const root = document.querySelector<HTMLElement>("[data-videos]");
	if (!root || root.dataset.videosReady === "true") return;
	root.dataset.videosReady = "true";
	bootPreviews(root);
	bootModal(root);
}
