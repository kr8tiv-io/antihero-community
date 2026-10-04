import type { ImageMetadata } from "astro";

/**
 * Public JPGs the media pipeline already wrote. Picture turns the ones
 * a page actually renders into AVIF and WebP. Hero stills stay out of
 * this map. The hero file is protected and preloads its own posters.
 */
const covers = import.meta.glob<ImageMetadata>(
	"../../public/media/covers/*.{jpg,jpeg,png,webp}",
	{ eager: true, import: "default" },
);

const doorPosters = import.meta.glob<ImageMetadata>(
	"../../public/media/door-*-poster.jpg",
	{ eager: true, import: "default" },
);

const byUrl = new Map<string, ImageMetadata>();

for (const [spec, image] of Object.entries({ ...covers, ...doorPosters })) {
	const normalized = spec.replaceAll("\\", "/");
	const marker = "/public/";
	const index = normalized.lastIndexOf(marker);
	if (index === -1) continue;
	byUrl.set(`/${normalized.slice(index + marker.length)}`, image);
}

/** Image metadata for a public URL, or null when this map does not own it. */
export function rasterFrom(url: string | null | undefined): ImageMetadata | null {
	if (!url || !url.startsWith("/")) return null;
	const clean = url.split("?")[0] ?? url;
	return byUrl.get(clean) ?? null;
}

/** Candidate widths that exist, plus the file's own width. */
export function rasterWidths(image: ImageMetadata, caps: number[]): number[] {
	const widths = caps.filter((size) => size > 0 && size < image.width);
	if (!widths.includes(image.width)) widths.push(image.width);
	widths.sort((a, b) => a - b);
	return widths.length > 0 ? widths : [image.width];
}
