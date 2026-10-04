/**
 * Rebuild public media from assets-src/media.
 * Missing sources become labeled plates. npm run media
 */
import { execFile } from "node:child_process";
import { mkdir, copyFile, readdir, readFile, rm, stat, writeFile } from "node:fs/promises";
import path from "node:path";
import { promisify } from "node:util";
import sharp from "sharp";

const run = promisify(execFile);
const ROOT = path.resolve(import.meta.dirname, "..");
const ORIGINALS = path.join(ROOT, "assets-src", "media");
const PUBLIC_MEDIA = path.join(ROOT, "public", "media");
const ASSET_MEDIA = path.join(ROOT, "src", "assets", "media");
const FONT = path.join(ROOT, "_archive", "fonts-ttf", "JetBrainsMono-Regular.ttf");
const LIMIT = 25 * 1024 * 1024;
const TAIL =
	"No text, no logos, photoreal, brand palette of black, bone and one red accent.";
const MOVE = "One slow continuous camera move, no cuts, no shake.";

const written = [];

const STILLS = [
	{
		file: "promise.jpg",
		width: 2560,
		height: 1440,
		seeds: [path.join(ASSET_MEDIA, "promise.jpg")],
		copies: [path.join(ASSET_MEDIA, "promise.jpg")],
	},
	{
		file: "about.jpg",
		width: 2560,
		height: 1440,
		seeds: [],
		copies: [path.join(ASSET_MEDIA, "about.jpg"), path.join(PUBLIC_MEDIA, "about.jpg")],
	},
	{
		file: "join.jpg",
		width: 2560,
		height: 1440,
		seeds: [path.join(PUBLIC_MEDIA, "join.jpg")],
		copies: [path.join(ASSET_MEDIA, "join.jpg"), path.join(PUBLIC_MEDIA, "join.jpg")],
	},
	{
		file: "og.jpg",
		width: 1200,
		height: 630,
		seeds: [],
		copies: [
			path.join(ASSET_MEDIA, "og.jpg"),
			path.join(PUBLIC_MEDIA, "og.jpg"),
			path.join(ROOT, "public", "og", "og.jpg"),
		],
	},
];

const SCRUBS = [
	{
		file: "hero-desktop.mp4",
		width: 1920,
		height: 1080,
		frames: "desktop",
		seeds: [path.join(PUBLIC_MEDIA, "hero-desktop.mp4")],
	},
	{
		file: "hero-mobile.mp4",
		width: 1080,
		height: 1920,
		frames: "mobile",
		seeds: [path.join(PUBLIC_MEDIA, "hero-mobile.mp4")],
	},
];

const LOOPS = ["door-guides", "door-prompts", "door-videos", "door-blog"].map((name) => ({
	file: `${name}.mp4`,
	width: 1080,
	height: 1350,
	seeds: [path.join(PUBLIC_MEDIA, `${name}.mp4`)],
}));

function ffmpegEscape(filePath) {
	return filePath.replace(/\\/g, "/").replace(/:/g, "\\:").replace(/'/g, "\\'");
}

async function ffmpeg(args) {
	try {
		await run("ffmpeg", ["-hide_banner", "-loglevel", "error", "-y", ...args], {
			windowsHide: true,
			maxBuffer: 32 * 1024 * 1024,
		});
	} catch (error) {
		const stderr = error.stderr?.toString?.() ?? "";
		throw new Error(`ffmpeg failed\n${args.join(" ")}\n${stderr}`);
	}
}

async function ffprobe(file, entries) {
	const { stdout } = await run(
		"ffprobe",
		["-v", "error", "-show_entries", entries, "-of", "default=noprint_wrappers=1:nokey=1", file],
		{ windowsHide: true },
	);
	return stdout.trim().split(/\r?\n/).filter(Boolean);
}

async function exists(file) {
	try {
		await stat(file);
		return true;
	} catch {
		return false;
	}
}

function fit(width, height, maxWidth, maxHeight) {
	const scale = Math.min(1, maxWidth / width, maxHeight / height);
	const nextWidth = Math.max(2, Math.round((width * scale) / 2) * 2);
	const nextHeight = Math.max(2, Math.round((height * scale) / 2) * 2);
	return { width: nextWidth, height: nextHeight };
}

async function mark(file, kind) {
	const info = await stat(file);
	written.push({
		file: path.relative(ROOT, file).replaceAll("\\", "/"),
		bytes: info.size,
		kind,
	});
}

async function plate(width, height, label, outFile) {
	const pixels = Buffer.alloc(width * height * 3);
	const cx = Math.round(width * 0.72);
	const cy = Math.round(height * 0.38);
	const radius = Math.hypot(width, height) * 0.38;
	for (let y = 0; y < height; y += 1) {
		const t = height === 1 ? 0 : y / (height - 1);
		const baseR = 10 + (29 - 10) * t;
		const baseG = 10 + (33 - 10) * t;
		const baseB = 11 + (36 - 11) * t;
		for (let x = 0; x < width; x += 1) {
			const falloff = Math.max(0, 1 - Math.hypot(x - cx, y - cy) / radius);
			const glow = falloff * falloff * 0.22;
			const index = (y * width + x) * 3;
			pixels[index] = Math.min(255, Math.round(baseR + (224 - baseR) * glow));
			pixels[index + 1] = Math.min(255, Math.round(baseG + (38 - baseG) * glow));
			pixels[index + 2] = Math.min(255, Math.round(baseB + (30 - baseB) * glow));
		}
	}
	const raw = path.join(path.dirname(outFile), `.raw-${path.basename(outFile)}.png`);
	await sharp(pixels, { raw: { width, height, channels: 3 } }).png().toFile(raw);
	const size = Math.max(18, Math.round(width * 0.018));
	const font = ffmpegEscape(FONT);
	await ffmpeg([
		"-i",
		raw,
		"-vf",
		`drawtext=fontfile='${font}':text='${label}':fontsize=${size}:fontcolor=0x8A9096:x=48:y=h-th-48`,
		"-frames:v",
		"1",
		"-update",
		"1",
		outFile,
	]);
	await rm(raw, { force: true });
}

async function resolveSource(job) {
	const dest = path.join(ORIGINALS, job.file);
	if (await exists(dest)) return { file: dest, placeholder: false };
	for (const seed of job.seeds) {
		if (await exists(seed)) {
			await mkdir(path.dirname(dest), { recursive: true });
			await copyFile(seed, dest);
			return { file: dest, placeholder: false };
		}
	}
	return { file: null, placeholder: true };
}

async function writeOgDerivatives(jpg, width, kind) {
	const ogDir = path.join(ROOT, "public", "og");
	await mkdir(ogDir, { recursive: true });
	const widths = [640, 1200].filter((size) => size < width);
	for (const size of widths) {
		const resized = sharp(jpg).resize({ width: size, withoutEnlargement: true });
		const avif = path.join(ogDir, `og-${size}.avif`);
		const webp = path.join(ogDir, `og-${size}.webp`);
		await resized.clone().avif({ quality: 50 }).toFile(avif);
		await resized.clone().webp({ quality: 72 }).toFile(webp);
		await mark(avif, kind);
		await mark(webp, kind);
	}
	const fullAvif = path.join(ogDir, "og.avif");
	const fullWebp = path.join(ogDir, "og.webp");
	await sharp(jpg).avif({ quality: 50 }).toFile(fullAvif);
	await sharp(jpg).webp({ quality: 72 }).toFile(fullWebp);
	await mark(fullAvif, kind);
	await mark(fullWebp, kind);
}

async function writeStill(job) {
	const source = await resolveSource(job);
	if (!source.placeholder && source.file) {
		const bytes = await readFile(source.file);
		const meta = await sharp(bytes).metadata();
		for (const copy of job.copies) {
			await mkdir(path.dirname(copy), { recursive: true });
			if (path.resolve(copy) !== path.resolve(source.file)) await writeFile(copy, bytes);
			await mark(copy, "source");
		}
		if (job.file === "og.jpg") await writeOgDerivatives(bytes, meta.width ?? job.width, "source");
		return { width: meta.width ?? job.width, placeholder: false };
	}

	const master = path.join(ORIGINALS, `.plate-${job.file}.png`);
	await mkdir(ORIGINALS, { recursive: true });
	await plate(job.width, job.height, job.file, master);
	const jpg = await sharp(master).jpeg({ quality: 86, mozjpeg: true }).toBuffer();
	const meta = await sharp(jpg).metadata();
	for (const copy of job.copies) {
		await mkdir(path.dirname(copy), { recursive: true });
		await writeFile(copy, jpg);
		await mark(copy, "placeholder");
	}
	if (job.file === "og.jpg") await writeOgDerivatives(jpg, meta.width ?? job.width, "placeholder");
	await rm(master, { force: true });
	return { width: meta.width ?? job.width, placeholder: true };
}

const HERO_CAP = 6 * 1024 * 1024;
const POSTER_CAP = 250 * 1024;

async function encodeBuffer(source, format, quality) {
	const image = sharp(source);
	if (format === "jpeg") return image.jpeg({ quality, mozjpeg: true }).toBuffer();
	if (format === "webp") return image.webp({ quality }).toBuffer();
	return image.avif({ quality }).toBuffer();
}

async function underCap(source, format, quality, cap, step, floor) {
	let next = quality;
	let buffer = await encodeBuffer(source, format, next);
	while (buffer.length > cap && next - step >= floor) {
		next -= step;
		buffer = await encodeBuffer(source, format, next);
	}
	return { buffer, quality: next };
}

async function posterFrom(video, stem, kind, extras = {}) {
	const cap = extras.cap ?? Number.POSITIVE_INFINITY;
	const jpg = path.join(PUBLIC_MEDIA, `${stem}-poster.jpg`);
	const avif = path.join(PUBLIC_MEDIA, `${stem}-poster.avif`);
	const grabbed = path.join(PUBLIC_MEDIA, `.grab-${stem}.png`);
	await ffmpeg(["-i", video, "-frames:v", "1", grabbed]);
	const jpeg = await underCap(grabbed, "jpeg", 82, cap, 6, 46);
	const avifImage = await underCap(grabbed, "avif", 50, cap, 5, 30);
	await writeFile(jpg, jpeg.buffer);
	await writeFile(avif, avifImage.buffer);
	await mark(jpg, kind);
	await mark(avif, kind);
	if (extras.webp) {
		const webp = path.join(PUBLIC_MEDIA, `${stem}-poster.webp`);
		const webpImage = await underCap(grabbed, "webp", 72, cap, 6, 40);
		await writeFile(webp, webpImage.buffer);
		await mark(webp, kind);
		console.log(`${stem} poster webp q${webpImage.quality} ${webpImage.buffer.length}`);
	}
	await rm(grabbed, { force: true });
	console.log(
		`${stem} poster jpeg q${jpeg.quality} ${jpeg.buffer.length} avif q${avifImage.quality} ${avifImage.buffer.length}`,
	);
}

function heroAttempts(job) {
	const full = { width: job.width, height: job.height };
	const attempts = [
		{ crf: 24, g: 1, ...full },
		{ crf: 26, g: 1, ...full },
		{ crf: 28, g: 1, ...full },
		{ crf: 28, g: 4, ...full },
	];
	if (job.frames === "desktop") attempts.push({ crf: 28, g: 4, width: 1600, height: 900 });
	return attempts;
}

async function writeScrub(input, out, still, attempt) {
	const lead = still
		? ["-loop", "1", "-framerate", "24", "-t", "6", "-i", input]
		: ["-i", input, "-t", "10"];
	const interval = String(attempt.g);
	await ffmpeg([
		...lead,
		"-an",
		"-vf",
		`scale=${attempt.width}:${attempt.height}:flags=lanczos,fps=24`,
		"-c:v",
		"libx264",
		"-crf",
		String(attempt.crf),
		"-preset",
		"slow",
		"-g",
		interval,
		"-keyint_min",
		interval,
		"-sc_threshold",
		"0",
		"-pix_fmt",
		"yuv420p",
		"-movflags",
		"+faststart",
		out,
	]);
}

async function encodeScrub(job) {
	const source = await resolveSource(job);
	const out = path.join(PUBLIC_MEDIA, job.file);
	let input = source.file;
	let kind = "source";
	let still = false;
	if (source.placeholder) {
		input = path.join(ORIGINALS, `.plate-${job.file}.png`);
		await plate(job.width, job.height, job.file, input);
		kind = "placeholder";
		still = true;
	} else {
		const [durationText] = await ffprobe(input, "format=duration");
		const duration = Number(durationText);
		console.log(`${job.file} source ${duration.toFixed(3)}s`);
		if (duration > 10) console.log(`${job.file} trimmed to 10s`);
	}
	const attempts = still ? [{ crf: 24, g: 1, width: job.width, height: job.height }] : heroAttempts(job);
	let chosen = attempts[0];
	for (const attempt of attempts) {
		chosen = attempt;
		await writeScrub(input, out, still, attempt);
		const info = await stat(out);
		console.log(
			`${job.file} crf ${attempt.crf} g ${attempt.g} ${attempt.width}x${attempt.height} ${info.size}`,
		);
		if (still || info.size <= HERO_CAP) break;
	}
	const finalInfo = await stat(out);
	if (!still && finalInfo.size > HERO_CAP) {
		console.log(`${job.file} still over ${HERO_CAP} after ${chosen.crf}/${chosen.g}`);
	}
	await mark(out, kind);
	await posterFrom(out, job.file.replace(/\.mp4$/, ""), kind, { webp: true, cap: POSTER_CAP });
	await exportFrames(out, job.frames, kind);
	if (source.placeholder) await rm(input, { force: true });
}

async function exportFrames(video, folder, kind) {
	const [durationText] = await ffprobe(video, "format=duration");
	const duration = Number(durationText);
	const target = Math.min(180, Math.max(120, Math.round(duration * 24)));
	const dir = path.join(PUBLIC_MEDIA, "hero-frames", folder);
	await rm(dir, { recursive: true, force: true });
	await mkdir(dir, { recursive: true });
	await ffmpeg([
		"-i",
		video,
		"-an",
		"-vf",
		`fps=${target}/${duration}`,
		"-start_number",
		"1",
		"-c:v",
		"libwebp",
		"-quality",
		"72",
		path.join(dir, "%04d.webp"),
	]);
	const names = (await readdir(dir)).filter((name) => name.endsWith(".webp")).sort();
	const count = Math.min(names.length, 180);
	for (const extra of names.slice(count)) await rm(path.join(dir, extra));
	if (count < 120) {
		throw new Error(`${folder} exported ${count} frames, expected 120 to 180`);
	}
	const manifest = { count, first: 1, pad: 4, ext: "webp" };
	const manifestPath = path.join(dir, "manifest.json");
	await writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);
	for (const name of names.slice(0, count)) await mark(path.join(dir, name), kind);
	await mark(manifestPath, kind);
}

async function encodeLoop(job) {
	const source = await resolveSource(job);
	const stem = job.file.replace(/\.mp4$/, "");
	const mp4 = path.join(PUBLIC_MEDIA, job.file);
	const webm = path.join(PUBLIC_MEDIA, `${stem}.webm`);
	let input = source.file;
	let kind = "source";
	let still = false;
	let size = { width: job.width, height: job.height };
	if (source.placeholder) {
		input = path.join(ORIGINALS, `.plate-${job.file}.png`);
		await plate(job.width, job.height, job.file, input);
		kind = "placeholder";
		still = true;
	} else {
		const probe = await ffprobe(input, "stream=width,height");
		const width = Number(probe[0]);
		const height = Number(probe[1]);
		if (width > 0 && height > 0) size = fit(width, height, job.width, job.height);
	}
	const lead = still
		? ["-loop", "1", "-framerate", "24", "-t", "6", "-i", input]
		: ["-i", input];
	const scale = `scale=${size.width}:${size.height}:flags=lanczos,fps=24`;
	await ffmpeg([
		...lead,
		"-an",
		"-vf",
		scale,
		"-c:v",
		"libx264",
		"-crf",
		"24",
		"-preset",
		"slow",
		"-pix_fmt",
		"yuv420p",
		"-movflags",
		"+faststart",
		mp4,
	]);
	await ffmpeg([
		...lead,
		"-an",
		"-vf",
		scale,
		"-c:v",
		"libsvtav1",
		"-crf",
		"34",
		"-preset",
		"6",
		"-pix_fmt",
		"yuv420p",
		webm,
	]);
	await mark(mp4, kind);
	await mark(webm, kind);
	await posterFrom(mp4, stem, kind);
	if (source.placeholder) await rm(input, { force: true });
}

async function writeGitignore() {
	await mkdir(ORIGINALS, { recursive: true });
	const names = await readdir(ORIGINALS);
	const large = [];
	for (const name of names) {
		if (name === ".gitignore" || name.startsWith(".plate-")) continue;
		const info = await stat(path.join(ORIGINALS, name));
		if (info.isFile() && info.size > LIMIT) large.push(name);
	}
	const lines = [
		"# Originals over 25 MB stay on this machine.",
		"# scripts/optimize-media.mjs rewrites this list.",
		...large.sort(),
		"",
	];
	await writeFile(path.join(ORIGINALS, ".gitignore"), lines.join("\n"));
}

function table() {
	const rolled = new Map();
	for (const row of written) {
		const frame = row.file.match(/^(public\/media\/hero-frames\/[^/]+)\/\d+\.webp$/);
		const key = frame ? `${frame[1]}/*.webp` : row.file;
		const prev = rolled.get(key);
		if (prev) {
			prev.bytes += row.bytes;
			prev.count += 1;
		} else {
			rolled.set(key, { file: key, bytes: row.bytes, kind: row.kind, count: frame ? 1 : 0 });
		}
	}
	const rows = [...rolled.values()].sort((a, b) => a.file.localeCompare(b.file));
	const labels = rows.map((row) => (row.count > 0 ? `${row.file} (${row.count})` : row.file));
	const nameWidth = Math.max(4, ...labels.map((label) => label.length));
	const lines = [`${"file".padEnd(nameWidth)}  bytes      kind`];
	let total = 0;
	rows.forEach((row, index) => {
		total += row.bytes;
		lines.push(`${labels[index].padEnd(nameWidth)}  ${String(row.bytes).padStart(9)}  ${row.kind}`);
	});
	lines.push(`${"total".padEnd(nameWidth)}  ${String(total).padStart(9)}`);
	return lines.join("\n");
}

async function main() {
	await run("ffmpeg", ["-hide_banner", "-version"], { windowsHide: true });
	await stat(FONT);
	await mkdir(PUBLIC_MEDIA, { recursive: true });
	await mkdir(ASSET_MEDIA, { recursive: true });
	for (const job of STILLS) await writeStill(job);
	for (const job of SCRUBS) await encodeScrub(job);
	for (const job of LOOPS) await encodeLoop(job);
	await writeGitignore();
	console.log(table());
	console.log(`\nPrompts live in docs/MEDIA.md. ${TAIL} Videos also use: ${MOVE}`);
}

main().catch((error) => {
	console.error(error instanceof Error ? error.message : error);
	process.exitCode = 1;
});
