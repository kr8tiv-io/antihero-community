# AntiHero AI

**A free AI community hub with no gatekeeping.** Guides, prompts, live replays and how-tos for the AntiHero AI Facebook group. The content is free forever.

**Live site: [antihero.community](https://antihero.community)**

---

## What it is

AntiHero AI is the home base for the [AntiHero AI Facebook group](https://www.facebook.com/groups/antiheroai). The site gives you one place to:

- **Join the group.** Every page has a clear path into the Facebook community.
- **Get on the email list** through an embedded Mailchimp sign-up form.
- **Grab the guides.** It's a library of downloadable PDF guides from the lives, filterable by category (Brand, Websites, Video, Prompts).
- **Steal the prompts.** The prompt library is sorted by goal: Websites, Grok Build, Grok Bot, Brand, Images and video, Content and social, and Business. A pop-up goal menu takes you straight to what you need, and you can copy, paste, done.
- **Watch the replays** of the lives, linked to their guides.
- **Read the blog** for notes from the trenches. It has an RSS feed.

There are also About, Join and Credits pages, a custom 404, a sitemap, and per-page SEO and Open Graph images.

## The vibe

It's approachable, fun and a little edgy. The look is spacey high-tech: deep blacks, bone, and one Ignition Red accent.

The motion is meant to be a 10/10:

- A scroll-scrubbed hero film, with separate desktop and phone cuts
- A Three.js starfield
- GSAP ScrollTrigger reveals and Lenis smooth scrolling
- Page transitions
- Hover films on every library door and card
- A custom cursor, plus an easter egg for those who look

**Mobile gets a lighter version.** Phones and touch devices skip the heavy effects. The starfield only runs on capable desktop machines, hover films and the cursor are desktop-only, the hero falls back for Save-Data connections, and everything respects `prefers-reduced-motion`.

## How it was built

The site was prompted live, in public. The build was fed to **Grok Build** as a series of focused prompts, one job and one commit at a time: setup, hero, navigation, sections, smooth scroll, reveals, scroll-scrubbed video, transitions, the 3D scene, hover titles, media compression, credits, and Playwright QA. Those exact prompts are in the site's own prompt library under the **Grok Build** goal.

The visuals, including the hero films, library-door loops, card loops and stills, were generated with **Grok Imagine (xAI)** and then encoded for the web by a local media script. The prompt behind each file is in [`docs/MEDIA.md`](docs/MEDIA.md).

## Tech stack

| | |
| --- | --- |
| Framework | [Astro](https://astro.build) 7, static output, with MDX and content collections (Zod schemas) |
| Styling | [Tailwind CSS](https://tailwindcss.com) 4 (via `@tailwindcss/vite`) and custom CSS |
| Motion | [GSAP](https://gsap.com) and ScrollTrigger, [Lenis](https://lenis.darkroom.engineering) smooth scroll |
| 3D | [Three.js](https://threejs.org) starfield |
| Feeds and SEO | `@astrojs/rss`, `@astrojs/sitemap` |
| Media tooling | `sharp`, `wawoff2`, and `ffmpeg` (for `npm run media`) |
| QA | [Playwright](https://playwright.dev) |
| Hosting | Static build on Hostinger (see [`docs/DEPLOY.md`](docs/DEPLOY.md)) |

## Run it locally

You need Node.js **22.12 or newer**.

```sh
npm install
npm run dev       # http://localhost:4321
npm run build     # checks credits, then writes the static site to dist/
npm run preview   # serves the dist/ build locally
```

Other scripts:

```sh
npm run media     # re-encode originals in assets-src/media into public/media (needs ffmpeg)
npm run qa        # build, then run the Playwright test suite
```

Optional environment variables (copy `.env.example` to `.env`):

- `MAILCHIMP_FORM_ACTION` is the embedded Mailchimp form action URL.
- `SITE_URL` is a placeholder. The build reads the site origin from `src/data/site.ts`.

## Project structure

```
src/
  pages/          routes: home, guides, prompts, videos, blog, about, join, credits, 404, rss.xml
  content/        content collections: guides, prompts (sorted by goal), videos, blog
  content.config.ts  collection schemas
  components/     Header, Footer, MenuOverlay, cards, EmailForm, PromptGoalMenu, ...
    home/         Hero, Promise, LibraryDoors, LatestDrop
  layouts/        BaseLayout, PostLayout
  scripts/        motion: hero scrub, reveals, smooth scroll, transitions, starfield, cursor, ...
  three/          Three.js starfield scene
  data/           site URL, nav and Facebook group link, prompt goals, credits, hover media
  styles/         global styles and brand palette
  assets/         logo SVGs, icons and images processed by Astro
public/
  guides/         downloadable PDF guides
  media/          hero films, frames, hover loops and posters
  fonts/          self-hosted WOFF2 fonts
  og/             social share images
  .htaccess       Hostinger cache, 404 and redirect rules
assets-src/media/ media originals for `npm run media`
brand-kit/        source brand kit (brand bible, logos, backgrounds, fonts, color)
docs/             DEPLOY.md, MEDIA.md, VERSION-2.md
scripts/          check-credits.mjs, optimize-media.mjs
tests/            Playwright QA spec
_archive/         retired assets kept for reference
```

## Adding content

Content is Markdown in `src/content/`, validated by the schemas in `src/content.config.ts`:

- **Guides:** `src/content/guides/*.md`, with the PDF in `public/guides/`
- **Prompts:** `src/content/prompts/*.md`. Set `goal` to one of the IDs in `src/data/prompt-goals.ts`.
- **Videos:** `src/content/videos/*.md` (YouTube ID or video URL, plus a poster)
- **Blog:** `src/content/blog/*.md`

Every file in `public/fonts` and `public/media` should be credited in `src/data/credits.ts`. The build warns if one isn't.

## Roadmap

Ideas parked for version 2 are in [`docs/VERSION-2.md`](docs/VERSION-2.md).

---

Join the community: **[antihero.community](https://antihero.community)**
