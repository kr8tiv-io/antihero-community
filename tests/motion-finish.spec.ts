import { mkdirSync } from "node:fs";
import { expect, test, type Page } from "@playwright/test";

/**
 * Prompt 35. Overflow and settled motion at the four phone and laptop sizes.
 * The draft blog note is absent from the production build, so that route is
 * checked on the dev server when this preview answers 404.
 */

const ROUTES = [
	{ path: "/", shot: "home" },
	{ path: "/guides", shot: "guides" },
	{ path: "/guides/build-a-brand-from-scratch-with-ai", shot: "guide" },
	{ path: "/prompts", shot: "prompts" },
	{ path: "/videos", shot: "videos" },
	{ path: "/blog", shot: "blog" },
	{ path: "/blog/why-we-built-this-site-live", shot: "post" },
	{ path: "/about", shot: "about" },
	{ path: "/join", shot: "join" },
	{ path: "/credits", shot: "credits" },
	{ path: "/404", shot: "missing" },
] as const;

const SIZES = [
	{ width: 375, height: 667 },
	{ width: 393, height: 852 },
	{ width: 430, height: 932 },
	{ width: 1440, height: 900 },
] as const;

mkdirSync("qa/prompt-35", { recursive: true });

test.beforeEach(({ browserName }, testInfo) => {
	test.skip(
		browserName !== "chromium" || testInfo.project.name !== "chromium",
		"Motion shots run once, in the default Chromium project.",
	);
});

async function scrollThrough(page: Page, width: number): Promise<void> {
	if (width < 768) {
		await page.evaluate(async () => {
			const step = Math.round(window.innerHeight * 0.65);
			const max = () => document.documentElement.scrollHeight - window.innerHeight;
			for (let y = 0; y < max(); y += step) {
				window.scrollTo(0, y);
				await new Promise((resolve) => setTimeout(resolve, 70));
			}
			window.scrollTo(0, Math.max(0, max()));
		});
		await page.waitForTimeout(1100);
		return;
	}

	for (let i = 0; i < 50; i += 1) {
		const done = await page.evaluate(() => {
			const max = document.documentElement.scrollHeight - window.innerHeight;
			return max <= 2 || window.scrollY >= max - 8;
		});
		if (done) break;
		await page.mouse.wheel(0, 1100);
		await page.waitForTimeout(90);
	}
	await page.waitForTimeout(1400);
}

async function audit(page: Page): Promise<{ overflow: number; stuck: string[] }> {
	return page.evaluate(() => {
		const root = document.documentElement;
		const stuck: string[] = [];
		const skip = "[hidden], .is-gone, dialog:not([open])";

		document.querySelectorAll<HTMLElement>("[data-reveal]").forEach((el) => {
			if (el.closest(skip)) return;
			const style = getComputedStyle(el);
			if (style.display === "none" || style.visibility === "hidden") return;
			const opacity = Number(style.opacity);
			if (opacity < 0.95) {
				stuck.push(`${el.getAttribute("data-reveal")} ${el.className} opacity ${opacity.toFixed(2)}`);
			}
			if (el.getAttribute("data-reveal") === "rule" && el.getBoundingClientRect().width < 2) {
				stuck.push(`rule ${el.className} not drawn`);
			}
		});

		document.querySelectorAll<HTMLElement>(".reveal-heading__text").forEach((el) => {
			if (el.closest(skip)) return;
			const line = el.parentElement;
			if (!line) return;
			const text = el.getBoundingClientRect();
			const box = line.getBoundingClientRect();
			if (box.height < 2) return;
			if (text.bottom < box.top + 1 || text.top > box.bottom - 1) {
				stuck.push(`heading clipped ${el.textContent?.trim().slice(0, 32) ?? ""}`);
			}
		});

		document.querySelectorAll<HTMLElement>(".reveal-heading__line").forEach((el) => {
			if (el.closest(skip)) return;
			if (el.getBoundingClientRect().width < 2) stuck.push("heading line not drawn");
		});

		document.querySelectorAll<HTMLElement>("[data-promise-word], [data-promise-sub], [data-promise-line]").forEach((el) => {
			const opacity = Number(getComputedStyle(el).opacity);
			if (opacity < 0.95) stuck.push(`promise opacity ${opacity.toFixed(2)}`);
		});

		return {
			overflow: root.scrollWidth - root.clientWidth,
			stuck: stuck.slice(0, 16),
		};
	});
}

for (const size of SIZES) {
	for (const route of ROUTES) {
		test(`${route.shot} ${size.width}x${size.height}`, async ({ page }) => {
			test.setTimeout(120_000);
			await page.setViewportSize({ width: size.width, height: size.height });
			const response = await page.goto(route.path, { waitUntil: "load" });
			let status = response?.status() ?? 0;
			if (route.shot === "post" && status === 404) {
				const dev = await page
					.goto("http://localhost:4321/blog/why-we-built-this-site-live", { waitUntil: "load" })
					.catch(() => null);
				const devStatus = dev?.status() ?? 0;
				const title = devStatus > 0 && devStatus < 400 ? await page.title() : "";
				if (devStatus >= 400 || devStatus === 0 || !/antihero/i.test(title)) {
					test.info().annotations.push({
						type: "note",
						description: "Draft post is not in the production build.",
					});
					return;
				}
				status = devStatus;
			}
			if (route.shot === "missing") expect([200, 404]).toContain(status);
			else expect(status, route.path).toBeLessThan(400);

			await page.mouse.move(size.width / 2, size.height / 2);
			await page.waitForTimeout(300);
			await scrollThrough(page, size.width);
			await expect.poll(async () => (await audit(page)).stuck, { timeout: 8_000 }).toEqual([]);
			const result = await audit(page);
			expect(result.overflow, `${route.path} overflow`).toBe(0);

			await shoot(page, route.shot, size.width, size.height);
		});
	}
}

/** Desktop full-page shots stitch wrong while Lenis owns the scroll. Viewport frames do not. */
async function wheelTo(page: Page, target: number, width: number, height: number): Promise<void> {
	await page.mouse.move(width / 2, height / 2);
	for (let i = 0; i < 70; i += 1) {
		const y = await page.evaluate(() => window.scrollY);
		if (Math.abs(y - target) <= 24) break;
		const delta = Math.max(-1400, Math.min(1400, (target - y) * 1.2));
		await page.mouse.wheel(0, delta);
		await page.waitForTimeout(80);
	}
	await page.waitForTimeout(700);
}

async function shoot(page: Page, name: string, width: number, height: number): Promise<void> {
	const base = `qa/prompt-35/${name}-${width}`;
	// Full-page captures paint fixed layers into the page image: the route band
	// parked below the viewport, the dev toolbar on the draft post, and the
	// test cursor. None of those sit on the page a person is reading.
	await page.addStyleTag({
		content: ".route-band, astro-dev-toolbar, .ah-cursor{visibility:hidden!important}",
	});
	if (width < 768) {
		await page.evaluate(() => window.scrollTo(0, 0));
		await page.waitForTimeout(350);
		await page.screenshot({ path: `${base}.png`, fullPage: true });
		return;
	}

	await page.screenshot({ path: `${base}-bottom.png` });
	const max = await page.evaluate(() =>
		Math.max(0, document.documentElement.scrollHeight - window.innerHeight),
	);
	if (max > 80) {
		await wheelTo(page, Math.round(max * 0.42), width, height);
		await page.screenshot({ path: `${base}-mid.png` });
	}
	await wheelTo(page, 0, width, height);
	await page.waitForTimeout(500);
	await page.screenshot({ path: `${base}-top.png` });
}
