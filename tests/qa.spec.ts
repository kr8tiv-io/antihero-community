import { mkdirSync } from "node:fs";
import { expect, test, type Locator, type Page } from "@playwright/test";

/**
 * Published routes only. The one blog note is draft: true, so production
 * has no /blog/<slug> page. Guide ids are the slug field.
 */
const ROUTES = [
	{ path: "/", shot: "home" },
	{ path: "/guides", shot: "guides" },
	{ path: "/guides/websites-on-autopilot", shot: "guides-websites-on-autopilot" },
	{ path: "/guides/build-a-brand-from-scratch-with-ai", shot: "guides-build-a-brand-from-scratch-with-ai" },
	{ path: "/guides/antihero-website-masterclass", shot: "guides-antihero-website-masterclass" },
	{ path: "/guides/email-the-channel-nobody-can-take", shot: "guides-email-the-channel-nobody-can-take" },
	{ path: "/prompts", shot: "prompts" },
	{ path: "/videos", shot: "videos" },
	{ path: "/blog", shot: "blog" },
	{ path: "/about", shot: "about" },
	{ path: "/join", shot: "join" },
	{ path: "/credits", shot: "credits" },
] as const;

const WIDTHS = [375, 768, 1440, 1920] as const;

const HEIGHT: Record<(typeof WIDTHS)[number], number> = {
	375: 812,
	768: 1024,
	1440: 900,
	1920: 1080,
};

const GROUP = "https://www.facebook.com/groups/antiheroai";
const KR8TIV = "https://kr8tiv.io";

/**
 * Visible site voice. Prompt bodies are the text you copy, and several of
 * them are the rules that name these words on purpose. They are skipped.
 * Matt can say if those bodies should be in this check too.
 */
const BANNED = [
	"hustle",
	"passive income",
	"guru",
	"crush it",
	"secret",
	"game-changer",
	"revolutionary",
	"unlock",
	"elevate",
	"seamless",
	"revolutionize",
	"empower",
	"delve",
	"leverage",
	"cutting-edge",
	"journey",
	"free everything",
] as const;

mkdirSync("qa/screenshots", { recursive: true });

function shotPath(name: string, width: number): string {
	return `qa/screenshots/${name}-${width}.png`;
}

function findBanned(text: string): string[] {
	const hits: string[] = [];
	for (const phrase of BANNED) {
		const pattern = phrase.includes(" ")
			? new RegExp(phrase.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "i")
			: new RegExp(`(?:^|[^a-z0-9])${phrase.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}(?=$|[^a-z0-9])`, "i");
		if (pattern.test(text)) hits.push(phrase);
	}
	return hits;
}

async function allowClipboard(page: Page, browserName: string): Promise<void> {
	if (browserName === "chromium") {
		await page.context().grantPermissions(["clipboard-read", "clipboard-write"]);
		return;
	}
	// Firefox and WebKit do not grant clipboard-read or clipboard-write.
	// The page still calls navigator.clipboard.writeText. This makes that call resolve.
	await page.addInitScript(() => {
		let saved = "";
		Object.defineProperty(navigator, "clipboard", {
			configurable: true,
			value: {
				writeText: async (text: string) => {
					saved = text;
				},
				readText: async () => saved,
			},
		});
	});
}

/**
 * The email fallback sits in the footer and in the join band, so each
 * has two group links while Mailchimp is unset. Both should be visible.
 */
async function expectGroupLinks(root: Locator): Promise<void> {
	const links = root.locator(`a[href="${GROUP}"]`);
	const count = await links.count();
	expect(count, "group link").toBeGreaterThan(0);
	for (let index = 0; index < count; index += 1) {
		await expect(links.nth(index)).toBeVisible();
	}
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

async function visibleCopy(page: Page): Promise<string> {
	return page.evaluate(() => {
		const parts: string[] = [];
		const walk = (node: Node): void => {
			if (node.nodeType === Node.TEXT_NODE) {
				parts.push(node.textContent ?? "");
				return;
			}
			if (!(node instanceof HTMLElement)) return;
			if (node.matches("script, style, noscript, [data-prompt-body]")) return;
			if (node.classList.contains("visually-hidden")) return;
			const style = getComputedStyle(node);
			if (style.display === "none" || style.visibility === "hidden") return;
			for (const child of node.childNodes) walk(child);
		};
		walk(document.body);
		return parts.join(" ");
	});
}

test.beforeEach(async ({ page, browserName }) => {
	await allowClipboard(page, browserName);
});

for (const width of WIDTHS) {
	test.describe(`${width}px`, () => {
		test.use({ viewport: { width, height: HEIGHT[width] } });

		for (const route of ROUTES) {
			test(route.path, async ({ page }, testInfo) => {
				const consoleErrors: string[] = [];
				const failed: string[] = [];

				page.on("console", (msg) => {
					if (msg.type() === "error") consoleErrors.push(msg.text());
				});
				page.on("pageerror", (error) => {
					consoleErrors.push(error.message);
				});
				page.on("response", (response) => {
					if (response.status() >= 400) failed.push(`${response.status()} ${response.url()}`);
				});
				page.on("requestfailed", (request) => {
					const errorText = request.failure()?.errorText ?? "failed";
					if (/ERR_ABORTED|NS_BINDING_ABORTED|cancelled|canceled/i.test(errorText)) return;
					failed.push(`${errorText} ${request.url()}`);
				});

				await page.goto(route.path, { waitUntil: "domcontentloaded" });
				await expect.poll(() => headingIsShown(page), { timeout: 15_000 }).toBe(true);

				if (testInfo.project.name === "chromium") {
					await page.screenshot({ path: shotPath(route.shot, width), fullPage: true });
				}

				const hrefs = await page.locator("a[href]").evaluateAll((anchors) =>
					anchors.map((anchor) => anchor.getAttribute("href") ?? ""),
				);
				const seen = new Set<string>();
				const broken: string[] = [];
				const here = new URL(page.url());
				for (const href of hrefs) {
					if (!href || href.startsWith("#") || href.startsWith("mailto:") || href.startsWith("tel:")) continue;
					let url: URL;
					try {
						url = new URL(href, here);
					} catch {
						broken.push(`bad href ${href}`);
						continue;
					}
					if (url.origin !== here.origin) continue;
					url.hash = "";
					const key = url.toString();
					if (seen.has(key)) continue;
					seen.add(key);
					const response = await page.request.get(key, { failOnStatusCode: false });
					if (response.status() >= 400) broken.push(`${response.status()} ${key}`);
				}
				expect(broken, broken.join("\n")).toEqual([]);

				const images = page.locator("img");
				const imageCount = await images.count();
				for (let index = 0; index < imageCount; index += 1) {
					const alt = await images.nth(index).getAttribute("alt");
					expect(alt, `image ${index} is missing alt`).not.toBeNull();
				}

				const buttons = page.getByRole("button");
				const buttonCount = await buttons.count();
				for (let index = 0; index < buttonCount; index += 1) {
					await expect(buttons.nth(index)).toHaveAccessibleName(/.+/);
				}

				const copy = await visibleCopy(page);
				expect(copy, "visible text has an exclamation point").not.toMatch(/!/);
				expect(copy, "visible text has an em dash").not.toMatch(/\u2014/);
				const banned = findBanned(copy);
				expect(banned, `banned words: ${banned.join(", ")}`).toEqual([]);

				const footer = page.locator("footer");
				await expect(footer).toBeVisible();
				await expectGroupLinks(footer);
				await expect(footer.locator(`a[href="${KR8TIV}"]`)).toBeVisible();

				const band = page.locator("[data-join-band]");
				if (route.path === "/join") {
					await expect(band).toHaveCount(0);
					await expectGroupLinks(page.locator("main"));
				} else {
					await expect(band).toBeVisible();
					await expectGroupLinks(band);
				}

				const menu = page.locator("[data-menu-button]");
				if (width >= 1024) {
					await expect(menu).toBeHidden();
				} else {
					await menu.focus();
					await page.keyboard.press("Enter");
					await expect(menu).toHaveAttribute("aria-expanded", "true");
					await page.keyboard.press("Escape");
					await expect(menu).toHaveAttribute("aria-expanded", "false");
					await expect(menu).toBeFocused();
					await expect(page.locator("[data-menu]")).toBeHidden();
				}

				if (route.path === "/guides") {
					const websites = page.locator('[data-guide-card][data-category="websites"]');
					const brand = page.locator('[data-guide-card][data-category="brand"]');
					await expect(websites.first()).toBeVisible();
					await page.getByRole("button", { name: "Brand", exact: true }).click();
					await expect(page).toHaveURL(/[?&]c=brand(?:&|$)/);
					await expect(brand.first()).toBeVisible();
					await expect(websites.first()).toBeHidden();
				}

				if (route.path === "/prompts") {
					const copyButton = page.locator("[data-copy]").first();
					await copyButton.click();
					await expect(copyButton).toContainText("Stolen. Nice.");
				}

				expect(consoleErrors, consoleErrors.join("\n")).toEqual([]);
				expect(failed, failed.join("\n")).toEqual([]);
			});
		}
	});
}
