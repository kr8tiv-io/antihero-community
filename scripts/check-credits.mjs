/**
 * Warn when a file in public/fonts, public/media, or public/models
 * is missing from src/data/credits.ts.
 * A files entry covers that path and anything inside it.
 * Dotfiles are skipped. Warnings do not fail the build.
 */
import { readdir, readFile } from "node:fs/promises";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const creditsPath = path.join(root, "src", "data", "credits.ts");
const watched = ["public/fonts", "public/media", "public/models"];

const source = await readFile(creditsPath, "utf8");
const mentioned = [];
for (const match of source.matchAll(/files\s*:\s*\[([\s\S]*?)\]/g)) {
	for (const pathMatch of match[1].matchAll(/["'`]([^"'`]+)["'`]/g)) {
		mentioned.push(pathMatch[1].replaceAll("\\", "/").replace(/^\.?\//, "").replace(/\/$/, ""));
	}
}

async function walk(dir) {
	let entries;
	try {
		entries = await readdir(dir, { withFileTypes: true });
	} catch (error) {
		if (error && error.code === "ENOENT") return [];
		throw error;
	}
	const files = [];
	for (const entry of entries) {
		if (entry.name.startsWith(".")) continue;
		const full = path.join(dir, entry.name);
		if (entry.isDirectory()) files.push(...(await walk(full)));
		else files.push(full);
	}
	return files;
}

function covers(filePosix, entry) {
	return filePosix === entry || filePosix.startsWith(`${entry}/`);
}

const missing = [];
for (const rel of watched) {
	const files = await walk(path.join(root, rel));
	for (const file of files) {
		const posix = path.relative(root, file).split(path.sep).join("/");
		if (!mentioned.some((entry) => covers(posix, entry))) missing.push(posix);
	}
}

if (missing.length === 0) {
	console.log("credits: fonts, media, and models are covered");
} else {
	console.warn(`credits: ${missing.length} file(s) have no credit entry`);
	for (const file of missing) console.warn(`  ${file}`);
}
