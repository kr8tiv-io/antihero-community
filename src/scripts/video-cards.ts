/**
 * The modal builds a YouTube iframe or a native player only after a click.
 * Card hover films live in the shared hover player.
 */

const YOUTUBE_ID = /^[A-Za-z0-9_-]{6,20}$/;
const FOCUSABLE = "a[href], button:not([disabled]), iframe, video, [tabindex]:not([tabindex='-1'])";

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

export function releaseVideoCards(): void {
	// Hover films are released with the shared player.
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
	releaseVideoCards();
	root.dataset.videosReady = "true";
	bootModal(root);
}
