import { defineCollection, reference } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const category = z.enum(["Brand", "Websites", "Video", "Prompts"]);

const slug = z
  .string()
  .regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/, "Use a lowercase slug.");

const guidePdf = z
  .string()
  .regex(/^\/guides\/[a-z0-9]+(?:-[a-z0-9]+)*\.pdf$/, "PDF paths live under /guides/.");

/** Guide ids follow the slug field. Other collections use the filename. */
function entryId({
  entry,
  data,
}: {
  entry: string;
  base: URL;
  data: Record<string, unknown>;
}): string {
  if (typeof data.slug === "string" && data.slug.length > 0) return data.slug;
  return entry.replace(/\\/g, "/").replace(/\.(md|mdx)$/i, "");
}

const summary = z.tuple([z.string().min(1), z.string().min(1), z.string().min(1)]);

const guides = defineCollection({
  loader: glob({
    pattern: "**/*.{md,mdx}",
    base: "./src/content/guides",
    generateId: entryId,
  }),
  schema: z.object({
    title: z.string().min(1),
    slug,
    summary,
    category,
    date: z.coerce.date(),
    cover: z.string().min(1),
    pdf: guidePdf,
    replay: z.optional(reference("videos")),
    featured: z.boolean(),
    draft: z.boolean(),
  }),
});

const prompts = defineCollection({
  loader: glob({
    pattern: "**/*.{md,mdx}",
    base: "./src/content/prompts",
  }),
  schema: z.object({
    title: z.string().min(1),
    useItFor: z.string().min(1),
    category,
    source: z.optional(reference("guides")),
    order: z.number().int().positive(),
  }),
});

const videos = defineCollection({
  loader: glob({
    pattern: "**/*.{md,mdx}",
    base: "./src/content/videos",
  }),
  schema: z.object({
    title: z.string().min(1),
    date: z.coerce.date(),
    duration: z.string().min(1).optional(),
    youtubeId: z.string().min(1).optional(),
    videoUrl: z.string().url().optional(),
    poster: z.string().min(1),
    preview: z.string().min(1).optional(),
    guide: z.optional(reference("guides")),
    placeholder: z.boolean(),
  }),
});

const blog = defineCollection({
  loader: glob({
    pattern: "**/*.{md,mdx}",
    base: "./src/content/blog",
  }),
  schema: z.object({
    title: z.string().min(1),
    description: z.string().min(1),
    date: z.coerce.date(),
    draft: z.boolean(),
    relatedGuide: z.optional(reference("guides")),
    relatedPrompt: z.optional(reference("prompts")),
    ogImage: z.string().min(1).optional(),
  }),
});

export const collections = { guides, prompts, videos, blog };
