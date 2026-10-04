/**
 * Rule: anything borrowed gets an entry here in the same commit.
 */

export const creditCategories = [
  "Code and libraries",
  "Fonts",
  "Images and video",
  "3D and textures",
  "Techniques and inspiration",
] as const;

export type CreditCategory = (typeof creditCategories)[number];

export interface Credit {
  name: string;
  author: string;
  license: string;
  link: string;
  licenseLink?: string;
  usedFor: string;
  category: CreditCategory;
  files?: string[];
}

export const credits: Credit[] = [
  {
    name: "Astro",
    author: "withastro",
    license: "MIT",
    link: "https://astro.build",
    licenseLink: "https://github.com/withastro/astro/blob/main/LICENSE",
    usedFor: "Static site framework, including ClientRouter view transitions",
    category: "Code and libraries",
  },
  {
    name: "Tailwind CSS",
    author: "Tailwind Labs",
    license: "MIT",
    link: "https://tailwindcss.com",
    licenseLink: "https://github.com/tailwindlabs/tailwindcss/blob/main/LICENSE",
    usedFor: "Utility styling, through the Tailwind CSS Vite plugin",
    category: "Code and libraries",
  },
  {
    name: "GSAP",
    author: "GreenSock",
    license: "GreenSock Standard no-charge license",
    link: "https://gsap.com",
    licenseLink: "https://gsap.com/standard-license",
    usedFor: "Motion, including ScrollTrigger and Flip",
    category: "Code and libraries",
  },
  {
    name: "Lenis",
    author: "darkroom.engineering",
    license: "MIT",
    link: "https://github.com/darkroomengineering/lenis",
    licenseLink: "https://github.com/darkroomengineering/lenis/blob/main/LICENSE",
    usedFor: "Smooth scrolling",
    category: "Code and libraries",
  },
  {
    name: "three.js",
    author: "mrdoob and contributors",
    license: "MIT",
    link: "https://threejs.org",
    licenseLink: "https://github.com/mrdoob/three.js/blob/dev/LICENSE",
    usedFor: "The starfield on the home, about, and join pages",
    files: ["src/three/starfield.ts"],
    category: "Code and libraries",
  },
  {
    name: "igloo.inc",
    author: "Igloo Inc, built by Abeto with Bureaux",
    license: "Inspiration only. No code, models, or shaders copied.",
    link: "https://www.igloo.inc",
    usedFor: "The idea of moving through one space. The starfield shader is original.",
    category: "Techniques and inspiration",
  },
  {
    name: "@astrojs/sitemap",
    author: "withastro",
    license: "MIT",
    link: "https://docs.astro.build/en/guides/integrations-guide/sitemap/",
    licenseLink: "https://github.com/withastro/astro/blob/main/LICENSE",
    usedFor: "Sitemap generation",
    category: "Code and libraries",
  },
  {
    name: "@astrojs/rss",
    author: "withastro",
    license: "MIT",
    link: "https://docs.astro.build/en/guides/rss/",
    licenseLink: "https://github.com/withastro/astro/blob/main/LICENSE",
    usedFor: "RSS feeds",
    category: "Code and libraries",
  },
  {
    name: "@astrojs/mdx",
    author: "withastro",
    license: "MIT",
    link: "https://docs.astro.build/en/guides/integrations-guide/mdx/",
    licenseLink: "https://github.com/withastro/astro/blob/main/LICENSE",
    usedFor: "MDX pages and content",
    category: "Code and libraries",
  },
  {
    name: "wawoff2",
    author: "fontello",
    license: "MIT",
    link: "https://github.com/fontello/wawoff2",
    usedFor: "Converted the brand TTFs to WOFF2",
    category: "Code and libraries",
  },
  {
    name: "Bebas Neue",
    author: "Dharma Type",
    license: "SIL Open Font License 1.1",
    link: "https://fonts.google.com/specimen/Bebas+Neue",
    licenseLink: "https://scripts.sil.org/OFL",
    usedFor: "Display headlines",
    category: "Fonts",
    files: [
      "public/fonts/BebasNeue-Regular.woff2",
      "public/fonts/OFL-BebasNeue.txt",
    ],
  },
  {
    name: "Barlow",
    author: "Jeremy Tribby",
    license: "SIL Open Font License 1.1",
    link: "https://fonts.google.com/specimen/Barlow",
    licenseLink: "https://scripts.sil.org/OFL",
    usedFor: "Body text",
    category: "Fonts",
    files: [
      "public/fonts/Barlow-Regular.woff2",
      "public/fonts/Barlow-Medium.woff2",
      "public/fonts/Barlow-SemiBold.woff2",
      "public/fonts/Barlow-Bold.woff2",
      "public/fonts/Barlow-Italic.woff2",
      "public/fonts/OFL-Barlow.txt",
    ],
  },
  {
    name: "Barlow Condensed",
    author: "Jeremy Tribby",
    license: "SIL Open Font License 1.1",
    link: "https://fonts.google.com/specimen/Barlow+Condensed",
    licenseLink: "https://scripts.sil.org/OFL",
    usedFor: "Labels and buttons",
    category: "Fonts",
    files: [
      "public/fonts/BarlowCondensed-SemiBold.woff2",
      "public/fonts/BarlowCondensed-Bold.woff2",
      "public/fonts/OFL-BarlowCondensed.txt",
    ],
  },
  {
    name: "sharp",
    author: "Lovell Fuller and contributors",
    license: "Apache-2.0",
    link: "https://sharp.pixelplumbing.com",
    licenseLink: "https://github.com/lovell/sharp/blob/main/LICENSE",
    usedFor: "Image resize and AVIF, WebP, and JPEG encoding in scripts/optimize-media.mjs",
    category: "Code and libraries",
  },
  {
    name: "Grok Imagine",
    author: "xAI",
    license: "Generated for AntiHero AI",
    link: "https://grok.com",
    usedFor: "Prompts for the site stills and films. Labeled plates stand in until those frames exist.",
    category: "Images and video",
    files: [
      "public/media/hero-desktop.mp4",
      "public/media/hero-mobile.mp4",
      "src/assets/media/promise.jpg",
      "public/media/door-guides.mp4",
      "public/media/door-prompts.mp4",
      "public/media/door-videos.mp4",
      "public/media/door-blog.mp4",
      "src/assets/media/about.jpg",
      "public/media/join.jpg",
      "public/og/og.jpg",
    ],
  },
  {
    name: "JetBrains Mono",
    author: "JetBrains",
    license: "SIL Open Font License 1.1",
    link: "https://github.com/JetBrains/JetBrainsMono",
    licenseLink: "https://scripts.sil.org/OFL",
    usedFor: "Prompts and data",
    category: "Fonts",
    files: [
      "public/fonts/JetBrainsMono-Regular.woff2",
      "public/fonts/JetBrainsMono-Bold.woff2",
      "public/fonts/OFL-JetBrainsMono.txt",
    ],
  },
];
