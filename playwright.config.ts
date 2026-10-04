import { defineConfig, devices } from "@playwright/test";

const chrome = devices["Desktop Chrome"];
const firefox = devices["Desktop Firefox"];
const webkit = devices["Desktop Safari"];

/**
 * Preview is the built site. npm run qa builds first, then this server
 * starts on 4330. Port 4321 belongs to another project.
 */
export default defineConfig({
	testDir: "./tests",
	fullyParallel: true,
	forbidOnly: !!process.env.CI,
	retries: 0,
	workers: 3,
	timeout: 90_000,
	expect: { timeout: 15_000 },
	reporter: [["list"]],
	use: {
		baseURL: "http://localhost:4330",
		trace: "off",
		video: "off",
		screenshot: "off",
	},
	webServer: {
		command: "npx astro preview --port 4330 --host localhost",
		url: "http://localhost:4330",
		reuseExistingServer: false,
		timeout: 120_000,
	},
	projects: [
		{ name: "chromium", use: { ...chrome } },
		{ name: "firefox", use: { ...firefox } },
		{ name: "webkit", use: { ...webkit } },
		{
			name: "chromium-reduced",
			use: { ...chrome, reducedMotion: "reduce" },
		},
	],
});
