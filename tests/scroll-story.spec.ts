import { mkdirSync } from "node:fs";
import { expect, test, type Page } from "@playwright/test";

/**
 * Prompt 36. Overflow, the promise film, and the scroll story.
 * Shots are viewport frames. Desktop full-page stitches break under Lenis,
 * and full-page paints the parked route band into the picture.
 */

const ROUTES = [
	"/",
	"/guides",
	"/guides/build-a-brand-from-scratch-with-ai",
	"/prompts",
	"/videos",
	"/blog",
	"/about",
	"/join",
	"/credits",
	"/404",
] as const;

const SIZES = [
	{ width: 375, height: 667 },
	{ width: 393, height: 852 },
	{ width: 430, height: 932 },
	{ width: 1440, height: 900 },
] as const;

mkdirSync("qa/prompt-36", { recursive: true });

test.beforeEach(({ browserName }, testInfo) => {
	test.skip(
		browserName !== "chromium" ||
			(testInfo.project.name !== "chromium" && testInfo.project.name !== "chromium-reduced"),
		"Scroll story runs in Chromium, including reduced motion.",
	);
});

async function hideChrome(page: Page): Promise<void> {
	await page.addStyleTag({
		content: ".route-band, astro-dev-toolbar, .ah-cursor{visibility:hidden!important}",
	});
}

async function wheelTo(page: Page, target: number): Promise<void> {
	const size = page.viewportSize();
	await page.mouse.move((size?.width ?? 800) / 2, (size?.height ?? 600) / 2);
	for (let i = 0; i < 80; i += 1) {
		const y = await page.evaluate(() => window.scrollY);
		if (Math.abs(y - target) <= 28) break;
		const delta = Math.max(-1200, Math.min(1200, (target - y) * 1.15));
		await page.mouse.wheel(0, delta);
		await page.waitForTimeout(70);
	}
	await page.waitForTimeout(400);
}

async function scrollTo(page: Page, target: number, phone: boolean): Promise<void> {
	if (phone) {
		await page.evaluate((y) => window.scrollTo(0, y), target);
		await page.waitForTimeout(250);
		return;
	}
	await wheelTo(page, target);
}

async function scrollThrough(page: Page, phone: boolean): Promise<void> {
	if (phone) {
		await page.evaluate(async () => {
			const step = Math.round(window.innerHeight * 0.7);
			const max = () => document.documentElement.scrollHeight - window.innerHeight;
			for (let y = 0; y < max(); y += step) {
				window.scrollTo(0, y);
				await new Promise((resolve) => setTimeout(resolve, 40));
			}
			window.scrollTo(0, Math.max(0, max()));
		});
		await page.waitForTimeout(600);
		return;
	}
	for (let i = 0; i < 46; i += 1) {
		const done = await page.evaluate(() => {
			const max = document.documentElement.scrollHeight - window.innerHeight;
			return max <= 2 || window.scrollY >= max - 8;
		});
		if (done) break;
		await page.mouse.wheel(0, 1100);
		await page.waitForTimeout(60);
	}
	await page.waitForTimeout(700);
}

async function stuck(page: Page): Promise<string[]> {
	return page.evaluate(() => {
		const problems: string[] = [];
		const skip = "[hidden], .is-gone, dialog:not([open])";
		document.querySelectorAll<HTMLElement>(".reveal-heading__text").forEach((el) => {
			if (el.closest(skip)) return;
			const line = el.parentElement;
			if (!line) return;
			const text = el.getBoundingClientRect();
			const box = line.getBoundingClientRect();
			if (box.height < 2 || box.bottom < 0) return;
			if (text.bottom < box.top + 1 || text.top > box.bottom - 1) {
				problems.push(`heading clipped ${el.textContent?.trim().slice(0, 32) ?? ""}`);
			}
		});
		document.querySelectorAll<HTMLElement>("[data-promise-word], [data-promise-sub], [data-promise-line]").forEach(
			(el) => {
				const opacity = Number(getComputedStyle(el).opacity);
				if (opacity < 0.95) problems.push(`promise ${opacity.toFixed(2)}`);
			},
		);
		document.querySelectorAll<HTMLElement>("[data-drop-in]").forEach((el) => {
			const opacity = Number(getComputedStyle(el).opacity);
			if (opacity < 0.95) problems.push(`drop ${opacity.toFixed(2)}`);
		});
		return problems.slice(0, 12);
	});
}

for (const size of SIZES) {
	for (const route of ROUTES) {
		test(`overflow ${route} ${size.width}x${size.height}`, async ({ page }) => {
			test.setTimeout(120_000);
			const phone = size.width < 768;
			await page.setViewportSize({ width: size.width, height: size.height });
			const response = await page.goto(route === "/404" ? "/404" : route, { waitUntil: "load" });
			if (route === "/404") expect([200, 404]).toContain(response?.status() ?? 0);
			else expect(response?.status() ?? 0, route).toBeLessThan(400);
			await page.mouse.move(size.width / 2, size.height / 2);
			await scrollThrough(page, phone);
			await expect.poll(async () => stuck(page), { timeout: 8_000 }).toEqual([]);
			const overflow = await page.evaluate(
				() => document.documentElement.scrollWidth - document.documentElement.clientWidth,
			);
			expect(overflow, route).toBe(0);
		});
	}
}

test("promise film plays in view and pauses offscreen", async ({ page }, testInfo) => {
	test.skip(testInfo.project.name !== "chromium", "Playback is checked with motion on.");
	test.setTimeout(90_000);
	await page.setViewportSize({ width: 1440, height: 900 });
	await page.goto("/", { waitUntil: "load" });
	await page.mouse.move(720, 400);
	const place = await page.evaluate(() => {
		const section = document.querySelector("[data-promise]");
		if (!section) return 0;
		const top = section.getBoundingClientRect().top + window.scrollY;
		return Math.max(0, top - window.innerHeight * 0.15);
	});
	await scrollTo(page, place, false);
	const video = page.locator("[data-promise-video]");
	await expect
		.poll(async () => {
			return video.evaluate((node) => {
				const film = node as HTMLVideoElement;
				return !film.paused && film.querySelectorAll("source").length >= 2 && film.readyState >= 2;
			});
		})
		.toBe(true);
	const max = await page.evaluate(() => document.documentElement.scrollHeight - window.innerHeight);
	await scrollTo(page, max, false);
	await expect.poll(async () => video.evaluate((node) => (node as HTMLVideoElement).paused)).toBe(true);
});

test("phones play the phone loop", async ({ page }, testInfo) => {
	test.skip(testInfo.project.name !== "chromium", "Playback is checked with motion on.");
	await page.setViewportSize({ width: 393, height: 852 });
	await page.goto("/", { waitUntil: "load" });
	const place = await page.evaluate(() => {
		const section = document.querySelector("[data-promise]");
		if (!section) return 0;
		return Math.max(0, section.getBoundingClientRect().top + window.scrollY - window.innerHeight * 0.1);
	});
	await scrollTo(page, place, true);
	const src = page.locator("[data-promise-video] source");
	await expect.poll(async () => src.first().getAttribute("src")).toContain("promise-loop-mobile");
	await expect
		.poll(async () => page.locator("[data-promise-video]").evaluate((node) => (node as HTMLVideoElement).paused))
		.toBe(false);
});

test("reduced motion keeps the promise visible and silent", async ({ page }, testInfo) => {
	test.skip(testInfo.project.name !== "chromium-reduced", "Reduced motion project only.");
	await page.setViewportSize({ width: 1440, height: 900 });
	await page.goto("/", { waitUntil: "load" });
	const video = page.locator("[data-promise-video]");
	await expect.poll(async () => video.evaluate((node) => (node as HTMLVideoElement).querySelectorAll("source").length)).toBe(0);
	await expect.poll(async () => video.evaluate((node) => (node as HTMLVideoElement).paused)).toBe(true);
	const opacity = await page.locator("[data-promise-word]").first().evaluate((node) => getComputedStyle(node).opacity);
	expect(Number(opacity)).toBeGreaterThan(0.95);
	const requests = await page.evaluate(() =>
		performance.getEntriesByType("resource").some((entry) => entry.name.includes("promise-loop.mp4") || entry.name.includes("promise-loop.webm")),
	);
	expect(requests).toBe(false);
});

test("screenshots of the scroll story", async ({ page }, testInfo) => {
	test.skip(testInfo.project.name !== "chromium", "Shots are taken once, with motion on.");
	test.setTimeout(180_000);
	for (const size of SIZES) {
		const phone = size.width < 768;
		await page.setViewportSize({ width: size.width, height: size.height });
		await page.goto("/", { waitUntil: "load" });
		await page.mouse.move(size.width / 2, size.height / 2);
		await hideChrome(page);
		await page.waitForTimeout(300);
		await page.screenshot({ path: `qa/prompt-36/hero-${size.width}.png` });

		const meltTarget = await page.evaluate(() => {
			const hero = document.querySelector("[data-hero]");
			if (!hero) return 0;
			// Midpoint of the hero mask, not the middle of the whole hero.
			return Math.round(hero.getBoundingClientRect().height * 0.54);
		});
		await scrollTo(page, meltTarget, phone);
		await page.waitForTimeout(250);
		await page.screenshot({ path: `qa/prompt-36/dissolve-${size.width}.png` });

		const promiseAt = await page.evaluate(() => {
			const section = document.querySelector("[data-promise]");
			if (!section) return 0;
			const top = section.getBoundingClientRect().top + window.scrollY;
			return Math.max(0, Math.round(top + window.innerHeight * 0.35));
		});
		await scrollTo(page, promiseAt, phone);
		await page.waitForTimeout(350);
		await page.screenshot({ path: `qa/prompt-36/promise-${size.width}.png` });

		await page.goto("/guides/build-a-brand-from-scratch-with-ai", { waitUntil: "load" });
		await hideChrome(page);
		await page.mouse.move(size.width / 2, size.height / 2);
		await scrollTo(page, 0, phone);
		await page.waitForTimeout(300);
		await page.screenshot({ path: `qa/prompt-36/guide-${size.width}.png` });
	}
});
