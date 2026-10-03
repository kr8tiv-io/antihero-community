/**
 * Copy the exact prompt text, including line breaks.
 * Clipboard API first. Fallback selects that text and uses execCommand.
 * Success label holds for 1.6s. The scale bump is transform only.
 */

const SUCCESS = "Stolen. Nice.";
const FAILURE = "Couldn't copy. Select it and copy by hand.";
const COPY = "Copy";

const timers = new WeakMap<HTMLButtonElement, number>();

export function bootPromptCards(): void {
	const root = document.querySelector<HTMLElement>("[data-prompts]");
	if (!root || root.dataset.cardsReady === "true") return;
	root.dataset.cardsReady = "true";

	const fitToggles = (): void => {
		for (const card of root.querySelectorAll<HTMLElement>("[data-prompt-card]")) {
			const body = card.querySelector<HTMLElement>("[data-prompt-body]");
			const toggle = card.querySelector<HTMLButtonElement>("[data-prompt-toggle]");
			if (!body || !toggle || toggle.getAttribute("aria-expanded") === "true") continue;
			if (card.classList.contains("is-gone") || body.clientWidth === 0) continue;
			const probe = body.cloneNode(true) as HTMLElement;
			probe.style.setProperty("display", "block");
			probe.style.setProperty("-webkit-line-clamp", "unset");
			probe.style.setProperty("position", "absolute");
			probe.style.setProperty("visibility", "hidden");
			probe.style.setProperty("pointer-events", "none");
			probe.style.setProperty("width", `${body.clientWidth}px`);
			body.insertAdjacentElement("afterend", probe);
			const line = parseFloat(getComputedStyle(body).lineHeight) || 20;
			const needs = probe.scrollHeight > line * 8 + 2;
			probe.remove();
			toggle.hidden = !needs;
			body.classList.toggle("is-clamped", needs);
		}
	};

	fitToggles();
	window.addEventListener("resize", fitToggles);
	document.fonts?.ready.then(fitToggles).catch(() => undefined);
	root.addEventListener("filtershelf:change", fitToggles);

	root.addEventListener("click", (event) => {
		const target = event.target as Element | null;
		if (!target) return;

		const toggle = target.closest<HTMLButtonElement>("[data-prompt-toggle]");
		if (toggle && root.contains(toggle)) {
			const card = toggle.closest<HTMLElement>("[data-prompt-card]");
			const body = card?.querySelector<HTMLElement>("[data-prompt-body]");
			const open = toggle.getAttribute("aria-expanded") === "true";
			const next = !open;
			toggle.setAttribute("aria-expanded", next ? "true" : "false");
			toggle.textContent = next ? "Show less" : "Show the whole thing";
			body?.classList.toggle("is-clamped", !next);
			return;
		}

		const button = target.closest<HTMLButtonElement>("[data-copy]");
		if (!button || !root.contains(button)) return;
		const card = button.closest<HTMLElement>("[data-prompt-card]");
		const body = card?.querySelector<HTMLElement>("[data-prompt-body]");
		const label = button.querySelector<HTMLElement>("[data-copy-label]");
		const live = card?.querySelector<HTMLElement>("[data-copy-live]");
		if (!body || !label || !live) return;
		const text = body.textContent ?? "";
		void copyExact(text).then((ok) => showResult(button, label, live, ok));
	});
}

async function copyExact(text: string): Promise<boolean> {
	try {
		if (navigator.clipboard?.writeText) {
			await navigator.clipboard.writeText(text);
			return true;
		}
	} catch {
		// Fall through to the selection fallback.
	}
	return selectAndCopy(text);
}

function selectAndCopy(text: string): boolean {
	const area = document.createElement("textarea");
	area.value = text;
	area.setAttribute("readonly", "");
	area.style.position = "fixed";
	area.style.top = "0";
	area.style.left = "0";
	area.style.opacity = "0";
	document.body.appendChild(area);
	area.focus();
	area.select();
	let ok = false;
	try {
		ok = document.execCommand("copy");
	} catch {
		ok = false;
	}
	area.remove();
	return ok;
}

function showResult(
	button: HTMLButtonElement,
	label: HTMLElement,
	live: HTMLElement,
	ok: boolean,
): void {
	const pending = timers.get(button);
	if (pending) window.clearTimeout(pending);
	timers.delete(button);

	button.classList.remove("is-stolen", "is-failed");
	label.textContent = ok ? SUCCESS : FAILURE;
	live.textContent = "";
	window.requestAnimationFrame(() => {
		live.textContent = ok ? SUCCESS : FAILURE;
	});

	if (!ok) {
		button.classList.add("is-failed");
		return;
	}

	void button.offsetWidth;
	button.classList.add("is-stolen");
	const timeout = window.setTimeout(() => {
		button.classList.remove("is-stolen");
		label.textContent = COPY;
		live.textContent = "";
		timers.delete(button);
	}, 1600);
	timers.set(button, timeout);
}
