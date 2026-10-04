/**
 * Decides whether the starfield may exist, then loads Three.js.
 * This file does not import three, so content pages do not download it.
 */

import { normalizePath } from "../data/nav";
import { onReducedMotionChange, prefersReducedMotion } from "./motion";

const GATE = "(min-width: 1024px) and (hover: hover) and (pointer: fine)";
const ROUTES = new Set(["/", "/about", "/join"]);

type Field = { destroy: () => void; path: string };

let generation = 0;
let pendingPath: string | null = null;
let live: Field | null = null;
let listening = false;

export function bootStarfield(): void {
	ensureListeners();
	const path = normalizePath(window.location.pathname);
	if (!allowed(path)) {
		releaseStarfield();
		return;
	}
	if (live?.path === path || pendingPath === path) return;

	const gen = ++generation;
	pendingPath = path;
	document.documentElement.classList.add("ah-stars");

	void import("../three/starfield").then((mod) => {
		if (gen !== generation) return;
		live?.destroy();
		const field = mod.createStarfield(path);
		pendingPath = null;
		if (!field) {
			live = null;
			document.documentElement.classList.remove("ah-stars");
			return;
		}
		live = field;
	}).catch(() => {
		if (gen !== generation) return;
		pendingPath = null;
		document.documentElement.classList.remove("ah-stars");
	});
}

/** Drop the WebGL context before a view transition swaps the page. */
export function releaseStarfield(): void {
	generation++;
	pendingPath = null;
	live?.destroy();
	live = null;
	document.documentElement.classList.remove("ah-stars");
}

/** Same attributes as the renderer, so a software GL driver never downloads Three.js. */
function hasWebGL(): boolean {
	try {
		const canvas = document.createElement("canvas");
		const gl = canvas.getContext("webgl2", {
			alpha: true,
			depth: false,
			stencil: false,
			antialias: false,
			premultipliedAlpha: false,
			powerPreference: "high-performance",
			failIfMajorPerformanceCaveat: true,
		});
		if (!gl) return false;
		gl.getExtension("WEBGL_lose_context")?.loseContext();
		return true;
	} catch {
		return false;
	}
}

function allowed(path: string): boolean {
	if (!ROUTES.has(path)) return false;
	if (prefersReducedMotion()) return false;
	if (!window.matchMedia(GATE).matches) return false;
	if ((navigator.hardwareConcurrency ?? 0) < 4) return false;
	const connection = (navigator as Navigator & { connection?: { saveData?: boolean } }).connection;
	if (connection?.saveData) return false;
	if (!hasWebGL()) return false;
	return true;
}

function ensureListeners(): void {
	if (listening) return;
	listening = true;
	window.matchMedia(GATE).addEventListener("change", bootStarfield);
	onReducedMotionChange(bootStarfield);
	const connection = (navigator as Navigator & {
		connection?: { addEventListener?: (type: string, listener: () => void) => void };
	}).connection;
	connection?.addEventListener?.("change", bootStarfield);
}
