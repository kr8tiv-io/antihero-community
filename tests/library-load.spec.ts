import { mkdirSync } from "node:fs";
import { expect, test, type Page } from "@playwright/test";

/**
 * Prompt 37. The loaded library: videos, one replay, one clip, the
 * placeholder live, guides, one guide, prompts, and the home doors.
 * Chromium only. WebKit cannot launch on this machine.
 * Shots are the top of the page. Do not hover a card. Hover would play a
 * loop, and a replay page must not be asked to download the full file.
 */

const SIZES = [
	{ width: 393, height: 852 },
	{ width: 1440, height: 900 },
] as const;

const NEW_PROMPTS = [
	"masterclass-ambient-sound",
	"masterclass-glb-3d-model",
	"masterclass-hero-video",
	"masterclass-hostinger-deploy",
	"masterclass-mcp-safety-check",
	"masterclass-mobile-pass",
	"masterclass-notebooklm-research",
	"masterclass-reference-folder",
	"masterclass-seo-blog",
	"masterclass-stack-loader",
	"3d-masterclass-tripo3d-landing-page",
] as const;

mkdirSync("qa/prompt-37", { recursive: true });

test.beforeEach(({ browserName }, testInfo) => {
	test.skip(
		browserName !== "chromium" ||
			(testInfo.project.name !== "chromium" && testInfo.project.name !== "chromium-reduced"),
		"Library load runs in Chromium, including reduced motion.",
	);
});

async function hideChrome(page: Page): Promise<void> {
	await page.addStyleTag({
		content: ".route-band, astro-dev-toolbar, .ah-cursor{visibility:hidden!important}",
	});
}

function trackFailures(page: Page): string[] {
	const failed: string[] = [];
	page.on("response", (response) => {
		const url = response.url();
		if (response.status() < 400) return;
		if (url.includes("favicon")) return;
		failed.push(`${response.status()} ${url}`);
	});
	return failed;
}

function trackReplayHits(page: Page): string[] {
	const hits: string[] = [];
	page.on("request", (request) => {
		if (request.url().includes("/media/replays/")) hits.push(request.url());
	});
	return hits;
}

async function overflow(page: Page): Promise<number> {
	return page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
}

async function clippedText(page: Page, selector: string): Promise<string[]> {
	return page.locator(selector).evaluateAll((nodes) =>
		nodes
			.filter((node) => node.scrollWidth > node.clientWidth + 1)
			.map((node) => `${node.textContent ?? ""} ${node.scrollWidth}/${node.clientWidth}`),
	);
}

async function titleOverlapsPlayer(page: Page): Promise<number> {
	return page.evaluate(() => {
		const title = document.querySelector(".watch-title");
		const stage = document.querySelector(".watch-stage");
		if (!title || !stage) return 0;
		const a = title.getBoundingClientRect();
		const b = stage.getBoundingClientRect();
		const x = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left));
		const y = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
		return Math.round(x * y);
	});
}

async function headingIsShown(page: Page): Promise<boolean> {
	return page.locator("main h1").first().evaluate((el) => {
		const nodes = [el, ...el.querySelectorAll<HTMLElement>("*")];
		return nodes.every((node) => {
			const style = getComputedStyle(node);
			if (style.display === "none" || style.visibility === "hidden") return false;
			return Number(style.opacity) > 0.05;
		});
	});
}

async function brokenImages(page: Page): Promise<string[]> {
	return page.evaluate(async () => {
		const imgs = [...document.querySelectorAll<HTMLImageElement>("main img")];
		await Promise.all(
			imgs.map(
				(img) =>
					new Promise<void>((resolve) => {
						if (img.complete) {
							resolve();
							return;
						}
						const timer = window.setTimeout(resolve, 4000);
						img.addEventListener(
							"load",
							() => {
								window.clearTimeout(timer);
								resolve();
							},
							{ once: true },
						);
						img.addEventListener(
							"error",
							() => {
								window.clearTimeout(timer);
								resolve();
							},
							{ once: true },
						);
					}),
			),
		);
		return imgs
			.filter((img) => img.complete && (img.currentSrc || img.src) && img.naturalWidth === 0)
			.map((img) => img.currentSrc || img.src);
	});
}

async function openAndSettle(page: Page, path: string): Promise<void> {
	await page.goto(path, { waitUntil: "domcontentloaded" });
	await expect.poll(() => headingIsShown(page), { timeout: 8_000 }).toBe(true);
}

async function shot(page: Page, name: string, width: number): Promise<void> {
	await hideChrome(page);
	await page.evaluate(() => window.scrollTo(0, 0));
	await page.screenshot({ path: `qa/prompt-37/${name}-${width}.png` });
}

for (const size of SIZES) {
	test.describe(`${size.width}x${size.height}`, () => {
		test.use({ viewport: { width: size.width, height: size.height } });

		test("videos library", async ({ page }, testInfo) => {
			const failed = trackFailures(page);
			const replays = trackReplayHits(page);
			await openAndSettle(page, "/videos");

			await expect(page.locator("[data-video-card]")).toHaveCount(16);
			await expect(page.locator(".video-lead [data-video-card]")).toHaveAttribute("id", "websites-on-autopilot-live");
			await expect(page.locator("#videos-live")).toHaveText("Live replays");
			await expect(page.locator("#videos-clips")).toHaveText("Clips");
			await expect(page.locator("#videos-promos")).toHaveText("Promos");
			await expect(page.locator("main")).not.toContainText(/coming soon/i);

			const placeholder = page.locator("#ai-tooling-101-live");
			await expect(placeholder).toHaveAttribute("data-placeholder", "true");
			const facebook = placeholder.locator("a.video-hit");
			await expect(facebook).toHaveAttribute("href", /facebook\.com/);
			await expect(facebook).toContainText("Watch on Facebook");
			await expect(placeholder.locator("a.video-card__title")).toHaveAttribute("href", "/videos/ai-tooling-101-live");

			const real = page.locator("#site-walkthrough a.video-hit");
			await expect(real).toHaveAttribute("href", "/videos/site-walkthrough");

			expect(await clippedText(page, ".video-lead .reveal-heading__text"), "lead title is clipped").toEqual([]);

			expect(await overflow(page)).toBeLessThanOrEqual(1);
			expect(await brokenImages(page)).toEqual([]);
			expect(replays, "the index must not request a full replay").toEqual([]);
			expect(failed, failed.join("\n")).toEqual([]);

			if (testInfo.project.name === "chromium") await shot(page, "videos", size.width);
		});

		test("replay page", async ({ page }, testInfo) => {
			const failed = trackFailures(page);
			const replays = trackReplayHits(page);
			await openAndSettle(page, "/videos/websites-on-autopilot-live");

			const player = page.locator("[data-watch-player]");
			await expect(player).toHaveCount(1);
			await expect(player).toHaveAttribute("preload", "none");
			await expect(player).toHaveAttribute("playsinline", "");
			await expect(player).toHaveAttribute("controls", "");
			expect(await player.getAttribute("autoplay")).toBeNull();
			await expect(player).not.toHaveAttribute("muted", "");
			const sources = player.locator("source");
			await expect(sources).toHaveCount(1);
			await expect(sources).toHaveAttribute("type", "video/mp4");
			await expect(sources).toHaveAttribute("src", "/media/replays/websites-on-autopilot-live.mp4");
			await expect(player).toHaveAttribute("poster", /video-websites-on-autopilot-live-poster\.jpg$/);

			await expect(page.getByRole("link", { name: "Watch on Facebook" })).toHaveAttribute("href", /facebook\.com/);
			await expect(page.locator("a.watch-guide")).toHaveAttribute("href", "/guides/websites-on-autopilot");
			await expect(page.locator("main")).not.toContainText(/^TODO/m);
			const ld = await page.locator('script[type="application/ld+json"]').evaluate((el) => el.textContent ?? "");
			expect(ld).toContain("VideoObject");
			expect(ld).toContain("websites-on-autopilot-live.mp4");

			expect(await clippedText(page, ".watch-title .reveal-heading__text"), "watch title is clipped").toEqual([]);
			expect(await titleOverlapsPlayer(page), "title overlaps the player").toBe(0);

			expect(await overflow(page)).toBeLessThanOrEqual(1);
			expect(await brokenImages(page)).toEqual([]);
			expect(replays, "preload none must not fetch the replay").toEqual([]);
			expect(failed, failed.join("\n")).toEqual([]);

			if (testInfo.project.name === "chromium") await shot(page, "videos-websites-on-autopilot-live", size.width);
		});

		test("clip page", async ({ page }, testInfo) => {
			const failed = trackFailures(page);
			await openAndSettle(page, "/videos/site-walkthrough");

			const player = page.locator("[data-watch-player]");
			const sources = player.locator("source");
			await expect(sources).toHaveCount(2);
			await expect(sources.nth(0)).toHaveAttribute("src", "/media/clips/site-walkthrough.webm");
			await expect(sources.nth(0)).toHaveAttribute("type", "video/webm");
			await expect(sources.nth(1)).toHaveAttribute("src", "/media/clips/site-walkthrough.mp4");
			await expect(sources.nth(1)).toHaveAttribute("type", "video/mp4");
			await expect(player).toHaveAttribute("preload", "none");
			expect(await player.getAttribute("autoplay")).toBeNull();
			await expect(page.locator("main")).toContainText("Clip");

			expect(await clippedText(page, ".watch-title .reveal-heading__text"), "watch title is clipped").toEqual([]);
			expect(await titleOverlapsPlayer(page), "title overlaps the player").toBe(0);

			expect(await overflow(page)).toBeLessThanOrEqual(1);
			expect(await brokenImages(page)).toEqual([]);
			expect(failed, failed.join("\n")).toEqual([]);

			if (testInfo.project.name === "chromium") await shot(page, "videos-site-walkthrough", size.width);
		});

		test("placeholder live", async ({ page }, testInfo) => {
			const failed = trackFailures(page);
			const replays = trackReplayHits(page);
			await openAndSettle(page, "/videos/ai-tooling-101-live");

			await expect(page.locator("video")).toHaveCount(0);
			await expect(page.locator(".watch-still img")).toBeVisible();
			await expect(page.getByRole("link", { name: "Watch on Facebook" })).toHaveAttribute(
				"href",
				"https://www.facebook.com/mattchaynes/videos/2198989667344012/",
			);
			await expect(page.locator("main")).not.toContainText(/coming soon/i);
			await expect(page.locator("main")).not.toContainText("TODO");
			const ld = await page.locator('script[type="application/ld+json"]').evaluate((el) => el.textContent ?? "");
			expect(ld).toContain("VideoObject");
			expect(ld).not.toContain("contentUrl");

			expect(await clippedText(page, ".watch-title .reveal-heading__text"), "watch title is clipped").toEqual([]);
			expect(await titleOverlapsPlayer(page), "title overlaps the still").toBe(0);

			expect(await overflow(page)).toBeLessThanOrEqual(1);
			expect(await brokenImages(page)).toEqual([]);
			expect(replays).toEqual([]);
			expect(failed, failed.join("\n")).toEqual([]);

			if (testInfo.project.name === "chromium") await shot(page, "videos-ai-tooling-101-live", size.width);
		});

		test("guides library", async ({ page }, testInfo) => {
			const failed = trackFailures(page);
			await openAndSettle(page, "/guides");

			await expect(page.locator("[data-guide-card]")).toHaveCount(5);
			const pdfs = page.locator("[data-guide-card] a[href$='.pdf']");
			await expect(pdfs).toHaveCount(5);
			const covers = page.locator("[data-guide-card] img");
			await expect(covers).toHaveCount(5);

			expect(await overflow(page)).toBeLessThanOrEqual(1);
			expect(await brokenImages(page)).toEqual([]);
			expect(failed, failed.join("\n")).toEqual([]);

			if (testInfo.project.name === "chromium") await shot(page, "guides", size.width);
		});

		test("masterclass guide", async ({ page }, testInfo) => {
			const failed = trackFailures(page);
			await openAndSettle(page, "/guides/antihero-website-masterclass");

			await expect(page.locator("a[href='/guides/antihero-website-masterclass.pdf']").first()).toBeVisible();
			await expect(page.locator("a.guide-replay__link")).toHaveAttribute("href", "/videos/website-masterclass-live");
			await expect(page.locator("a.guide-replay__link")).toContainText("Watch the replay");
			await expect(page.locator("a[href='/prompts#masterclass-hero-video']")).toBeAttached();
			await expect(page.locator(".guide-prompt")).toHaveCount(10);

			expect(await overflow(page)).toBeLessThanOrEqual(1);
			expect(await brokenImages(page)).toEqual([]);
			expect(failed, failed.join("\n")).toEqual([]);

			if (testInfo.project.name === "chromium") await shot(page, "guides-antihero-website-masterclass", size.width);
		});

		test("prompts library", async ({ page }, testInfo) => {
			const failed = trackFailures(page);
			await openAndSettle(page, "/prompts");

			await expect(page.locator("[data-prompt-card]")).toHaveCount(89);
			for (const id of NEW_PROMPTS) {
				const card = page.locator(`[id="${id}"]`);
				await expect(card).toBeAttached();
				await expect(card.locator("[data-copy]")).toBeAttached();
			}
			await expect(page.locator('[id="masterclass-hero-video"] a[href="/guides/antihero-website-masterclass"]')).toBeAttached();
			await expect(page.locator('[id="3d-masterclass-tripo3d-landing-page"]')).toBeAttached();

			const sections = page.locator("[data-goal-section]");
			const count = await sections.count();
			let total = 0;
			for (let index = 0; index < count; index += 1) {
				const section = sections.nth(index);
				const id = await section.getAttribute("data-goal");
				const cards = await section.locator("[data-prompt-card]").count();
				total += cards;
				const label = cards === 1 ? "1 prompt" : `${cards} prompts`;
				await expect(page.locator(`[data-goal-link][data-goal="${id}"] .goal-link__count`)).toHaveText(label);
				await expect(section.locator(".goal-count")).toHaveText(label);
			}
			expect(total).toBe(89);

			if (size.width === 1440 && testInfo.project.name === "chromium") {
				await page.context().grantPermissions(["clipboard-read", "clipboard-write"]);
				const copy = page.locator("#masterclass-hero-video [data-copy]");
				await copy.scrollIntoViewIfNeeded();
				await copy.click();
				await expect(copy).toContainText("Stolen. Nice.");
				const copied = await page.evaluate(() => navigator.clipboard.readText());
				expect(copied).toContain("looping background");
			}

			expect(await overflow(page)).toBeLessThanOrEqual(1);
			expect(failed, failed.join("\n")).toEqual([]);

			if (testInfo.project.name === "chromium") await shot(page, "prompts", size.width);
		});

		test("home drop and doors", async ({ page }, testInfo) => {
			const failed = trackFailures(page);
			const replays = trackReplayHits(page);
			await openAndSettle(page, "/");

			await expect(page.locator("[data-drop] a[href='/guides/websites-on-autopilot']").first()).toBeAttached();
			await expect(page.locator("[data-drop] a[href='/videos/websites-on-autopilot-live']")).toBeAttached();
			await expect(page.locator("[data-drop]")).toContainText("Play");

			const doors = page.locator("[data-door]");
			await expect(doors).toHaveCount(4);
			await expect(doors.nth(0)).toHaveAttribute("href", "/guides/websites-on-autopilot");
			await expect(doors.nth(0)).toContainText("5 guides");
			await expect(doors.nth(1)).toHaveAttribute("href", /^\/prompts#/);
			await expect(doors.nth(1)).toContainText("89 prompts");
			await expect(doors.nth(2)).toHaveAttribute("href", "/videos/site-walkthrough");
			await expect(doors.nth(2)).toContainText("16 videos");
			await expect(doors.nth(3)).toHaveAttribute("href", "/blog");
			await expect(doors.nth(3)).toContainText("0 notes");

			const promptDoor = await doors.nth(1).getAttribute("href");
			expect(promptDoor).toBeTruthy();

			expect(await overflow(page)).toBeLessThanOrEqual(1);
			expect(replays).toEqual([]);
			expect(failed, failed.join("\n")).toEqual([]);

			if (testInfo.project.name === "chromium") await shot(page, "home", size.width);
		});
	});
}
