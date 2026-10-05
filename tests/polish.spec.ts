import { mkdirSync, readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { expect, test, type Page } from "@playwright/test";

/**
 * Prompt 38. Every built page at phone and desktop widths, plus one
 * reduced-motion pass. Shots land in qa/prompt-38. Do not hover a card
 * and do not start a player. A hover plays a loop. Play would fetch a replay.
 */

const WIDTHS = [
	{ width: 375, height: 667, deep: true },
	{ width: 393, height: 852, deep: false },
	{ width: 430, height: 932, deep: false },
	{ width: 1440, height: 900, deep: true },
] as const;

const HOST = "https://antihero.community";

mkdirSync("qa/prompt-38", { recursive: true });

test.beforeEach(({ browserName }, testInfo) => {
	test.skip(
		browserName !== "chromium" ||
			(testInfo.project.name !== "chromium" && testInfo.project.name !== "chromium-reduced"),
		"Polish runs in Chromium, including reduced motion.",
	);
});

function field(text: string, key: string): string | null {
	const match = text.match(new RegExp(`^${key}:\\s*"?([^"\\n]+)"?\\s*$`, "m"));
	return match?.[1]?.trim() ?? null;
}

function contentRoutes(): string[] {
	const root = process.cwd();
	const guides = readdirSync(join(root, "src/content/guides"))
		.filter((name) => name.endsWith(".md"))
		.flatMap((name) => {
			const text = readFileSync(join(root, "src/content/guides", name), "utf8");
			if (/^draft:\s*true/m.test(text)) return [];
			const slug = field(text, "slug") ?? name.replace(/\.md$/, "");
			return [`/guides/${slug}`];
		});
	const videos = readdirSync(join(root, "src/content/videos"))
		.filter((name) => name.endsWith(".md"))
		.map((name) => `/videos/${name.replace(/\.md$/, "")}`);
	return [...guides, ...videos];
}

const PAGES = [
	"/",
	"/guides",
	"/prompts",
	"/videos",
	"/blog",
	"/about",
	"/join",
	"/credits",
	"/404",
	...contentRoutes(),
];

function shotName(path: string): string {
	if (path === "/") return "home";
	return path.replace(/^\//, "").replaceAll("/", "-");
}

async function hideChrome(page: Page): Promise<void> {
	await page.addStyleTag({
		content: ".route-band, astro-dev-toolbar, .ah-cursor{visibility:hidden!important}",
	});
}

async function settle(page: Page): Promise<void> {
	await page.locator("main h1").first().waitFor({ state: "visible" });
	await expect
		.poll(async () =>
			page.locator("main h1").first().evaluate((el) => {
				const nodes = [el, ...el.querySelectorAll<HTMLElement>("*")];
				return nodes.every((node) => {
					const style = getComputedStyle(node);
					if (style.display === "none" || style.visibility === "hidden") return false;
					return Number(style.opacity) > 0.9;
				});
			}),
		)
		.toBe(true);
	await page.waitForTimeout(800);
}

async function overflow(page: Page): Promise<number> {
	return page.evaluate(
		() => document.documentElement.scrollWidth - document.documentElement.clientWidth,
	);
}

async function shot(page: Page, name: string): Promise<void> {
	await page.screenshot({
		path: join("qa/prompt-38", `${name}.png`),
		animations: "disabled",
	});
}

test("every page has one h1, a real origin, and its own card", async ({ page }, testInfo) => {
	test.skip(testInfo.project.name !== "chromium", "Meta is checked once.");
	test.setTimeout(180_000);
	await page.setViewportSize({ width: 1440, height: 900 });

	const titles = new Map<string, string>();
	const descriptions = new Map<string, string>();
	const images = new Map<string, string>();

	for (const path of PAGES) {
		const response = await page.goto(path, { waitUntil: "domcontentloaded" });
		expect(response?.status(), path).toBeLessThan(400);
		await settle(page);

		const h1 = await page.locator("h1").count();
		expect(h1, path).toBe(1);

		const title = await page.title();
		const description = await page.locator('meta[name="description"]').getAttribute("content");
		const canonical = await page.locator('link[rel="canonical"]').getAttribute("href");
		const og = await page.locator('meta[property="og:image"]').getAttribute("content");
		expect(title.length, path).toBeGreaterThan(0);
		expect(description?.length ?? 0, path).toBeGreaterThan(0);
		const bare = (value: string) => value.replace(/\/$/, "");
		expect(bare(canonical ?? ""), path).toBe(bare(new URL(path, HOST).href));
		expect(og, path).toContain(`${HOST}/`);
		expect(titles.has(title), `${path} repeats ${title}`).toBe(false);
		expect(descriptions.has(description ?? ""), `${path} repeats a description`).toBe(false);
		expect(images.has(og ?? ""), `${path} repeats ${og}`).toBe(false);
		titles.set(title, path);
		descriptions.set(description ?? "", path);
		images.set(og ?? "", path);

		const missingAlt = await page.locator("img:not([alt])").count();
		expect(missingAlt, path).toBe(0);

		const replayHits = await page.evaluate(() =>
			performance
				.getEntriesByType("resource")
				.map((entry) => entry.name)
				.filter((name) => name.includes("/media/replays/")),
		);
		expect(replayHits, path).toEqual([]);
	}
});

test("internal links, anchors, the missing page, and the redirect targets", async ({ page }, testInfo) => {
	test.skip(testInfo.project.name !== "chromium", "Links are checked once.");
	test.setTimeout(180_000);
	const seen = new Set<string>();
	const anchors = new Map<string, Set<string>>();

	for (const path of PAGES) {
		await page.goto(path, { waitUntil: "domcontentloaded" });
		const found = await page.locator("a[href]").evaluateAll((nodes) =>
			nodes.map((node) => (node as HTMLAnchorElement).getAttribute("href") ?? ""),
		);
		for (const href of found) {
			if (!href.startsWith("/") || href.startsWith("//")) continue;
			const url = new URL(href, "http://localhost:4330");
			const target = url.pathname.replace(/\/$/, "") || "/";
			seen.add(target);
			if (url.hash.length > 1) {
				const ids = anchors.get(target) ?? new Set<string>();
				ids.add(decodeURIComponent(url.hash.slice(1)));
				anchors.set(target, ids);
			}
		}
	}

	for (const target of seen) {
		if (target.endsWith(".pdf") || target.endsWith(".xml")) {
			const response = await page.request.get(target);
			expect(response.status(), target).toBeLessThan(400);
			continue;
		}
		const response = await page.goto(target, { waitUntil: "domcontentloaded" });
		expect(response?.status(), target).toBeLessThan(400);
	}

	for (const [target, ids] of anchors) {
		await page.goto(target, { waitUntil: "domcontentloaded" });
		for (const id of ids) {
			const count = await page.locator(`[id="${id.replaceAll("\\", "\\\\").replaceAll('"', '\\"')}"]`).count();
			expect(count, `${target}#${id}`).toBeGreaterThan(0);
		}
	}

	const missing = await page.goto("/this-page-is-not-real", { waitUntil: "domcontentloaded" });
	expect(missing?.status()).toBe(404);
	await expect(page.locator("h1")).toContainText("This page went to be its own hero somewhere else.");
	await expect(page.locator(".missing-home")).toHaveCount(1);
	await expect(page.locator('.missing-links a[href="/guides"]')).toHaveCount(1);

	const htaccess = readFileSync(join(process.cwd(), "public/.htaccess"), "utf8");
	const redirects = [
		["/guides/todo-older-live-1", "/guides/antihero-website-masterclass"],
		["/guides/todo-older-live-2", "/guides/email-the-channel-nobody-can-take"],
		["/guides/todo-older-live-1.pdf", "/guides/antihero-website-masterclass.pdf"],
		["/guides/todo-older-live-2.pdf", "/guides/email-the-channel-nobody-can-take.pdf"],
	] as const;
	for (const [from, to] of redirects) {
		expect(htaccess).toContain(`Redirect 301 ${from} ${to}`);
		const response = await page.request.get(to);
		expect(response.status(), to).toBeLessThan(400);
	}
});

test("keyboard can open the menu and reach the player", async ({ page }, testInfo) => {
	test.skip(testInfo.project.name !== "chromium", "Keyboard is checked once.");
	await page.setViewportSize({ width: 375, height: 667 });
	await page.goto("/", { waitUntil: "domcontentloaded" });
	await settle(page);
	await page.keyboard.press("Tab");
	await expect(page.locator(".skip-link")).toBeFocused();
	const skipBox = await page.locator(".skip-link").boundingBox();
	expect(skipBox?.height ?? 0).toBeGreaterThan(20);

	const menu = page.locator("[data-menu-button]");
	await menu.focus();
	await page.keyboard.press("Enter");
	await expect(page.locator("#site-menu")).toBeVisible();
	await page.keyboard.press("Escape");
	await expect(page.locator("#site-menu")).toBeHidden();

	await page.goto("/videos/websites-on-autopilot-live", { waitUntil: "domcontentloaded" });
	const player = page.locator("video.watch-player");
	await expect(player).toHaveAttribute("controls", "");
	await expect(player).toHaveAttribute("preload", "none");
	await expect(player).not.toHaveAttribute("autoplay", "");
	await player.focus();
	await expect(player).toBeFocused();
	await expect(page.locator('label[for="footer-email"]')).toHaveCount(1);
});

test("phone and desktop frames stay inside the viewport", async ({ page }, testInfo) => {
	test.skip(testInfo.project.name !== "chromium", "Shots are taken once, with motion on.");
	test.setTimeout(420_000);
	const overflows: string[] = [];
	const tiny: string[] = [];

	for (const size of WIDTHS) {
		await page.setViewportSize({ width: size.width, height: size.height });
		for (const path of PAGES) {
			const response = await page.goto(path, { waitUntil: "domcontentloaded" });
			expect(response?.status(), path).toBeLessThan(400);
			await hideChrome(page);
			await settle(page);
			const name = `${shotName(path)}-${size.width}`;
			await shot(page, name);

			const delta = await overflow(page);
			if (delta !== 0) overflows.push(`${name} ${delta}`);

			if (path === "/") {
				const wordmark = await page.locator(".hero-wordmark img").evaluate((img) => {
					const box = img.getBoundingClientRect();
					return {
						left: box.left,
						right: box.right,
						top: box.top,
						bottom: box.bottom,
						width: box.width,
						height: box.height,
						view: window.innerWidth,
					};
				});
				expect(wordmark.width, name).toBeGreaterThan(120);
				expect(wordmark.height, name).toBeGreaterThan(24);
				expect(wordmark.left, name).toBeGreaterThanOrEqual(12);
				expect(wordmark.right, name).toBeLessThanOrEqual(wordmark.view - 12);
				expect(wordmark.top, name).toBeGreaterThanOrEqual(0);
				expect(wordmark.bottom, name).toBeLessThanOrEqual(size.height);
			}

			const tinyType = await page.evaluate(() => {
				const skip = (el: Element) =>
					el.closest(".caption, .label, .join-band, .mono, .hero-scroll, .ah-cursor") ||
					el.matches(
						".mono, .label, .caption, .goal-count, .guide-num, .watch-kicker, .watch-meta, .prompt-card__cat, .notes-rss",
					);
				return [...document.querySelectorAll("main p")]
					.filter((el) => {
						if (skip(el)) return false;
						const style = getComputedStyle(el);
						if (style.display === "none" || style.visibility === "hidden") return false;
						return Number.parseFloat(style.fontSize) < 16;
					})
					.slice(0, 6)
					.map((el) => `${el.className} ${getComputedStyle(el).fontSize} ${(el.textContent ?? "").trim().slice(0, 48)}`);
			});
			if (tinyType.length > 0) tiny.push(`${name}: ${tinyType.join(" | ")}`);

			if (!size.deep) continue;
			const landmark = page
				.locator(".about-portrait, .promise-copy, .prompt-copy, .watch-player, .guide-card, .video-card, .credits-group")
				.first();
			if ((await landmark.count()) === 0) continue;
			await landmark.scrollIntoViewIfNeeded();
			await page.waitForTimeout(200);
			await shot(page, `${name}-rest`);
			const restDelta = await overflow(page);
			if (restDelta !== 0) overflows.push(`${name}-rest ${restDelta}`);
		}
	}

	expect(tiny).toEqual([]);
	expect(overflows).toEqual([]);
});

test("reduced motion leaves the page visible", async ({ page }, testInfo) => {
	test.skip(testInfo.project.name !== "chromium-reduced", "Reduced motion project only.");
	test.setTimeout(240_000);
	await page.setViewportSize({ width: 375, height: 667 });

	for (const path of PAGES) {
		await page.goto(path, { waitUntil: "domcontentloaded" });
		await hideChrome(page);
		await settle(page);
		const hidden = await page.evaluate(() => {
			const nodes = [
				...document.querySelectorAll<HTMLElement>(
					"main h1, main h2, main p, .promise-word, .about-note, .about-portrait img, .watch-player, .prompt-card, .guide-card",
				),
			];
			return nodes
				.filter((el) => {
					const style = getComputedStyle(el);
					if (style.display === "none" || style.visibility === "hidden") return false;
					const box = el.getBoundingClientRect();
					if (box.width < 2 && box.height < 2) return false;
					return Number(style.opacity) < 0.05;
				})
				.slice(0, 8)
				.map((el) => `${el.tagName} ${el.className} ${(el.textContent ?? "").trim().slice(0, 40)}`);
		});
		expect(hidden, path).toEqual([]);
		if (path === "/" || path === "/about" || path === "/videos" || path === "/prompts") {
			await shot(page, `${shotName(path)}-375-reduced`);
		}
	}
});
