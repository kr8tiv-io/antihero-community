# AntiHero AI

Static site for AntiHero AI. Astro, Tailwind CSS, GSAP, Lenis, and Three.js.

Do not deploy from this repo until Matt says so.

## Run it

```sh
npm install
npm run dev
```

Open http://localhost:4321.

`npm run build` writes the static site to `dist/`. `npm run preview` serves that build on your machine.

## Where things live

- `src/pages/` for routes
- `src/content/` for content collections, when they exist
- `src/components/` and `src/layouts/` for the interface
- `src/data/` for typed data, including `credits.ts` and the site URL
- `src/assets/brand/` for the logo SVGs and app icons. Use the SVG wordmark. Do not retype the logo.
- `public/fonts/` for the self-hosted WOFF2 files. The original TTFs are in `_archive/fonts-ttf`.
- `public/media/`, `public/guides/`, and `public/og/` for static files
- `brand-kit/` for the source kit. Copy what a page needs into `src/` or `public/`. Leave the kit itself alone.
- `docs/VERSION-2.md` for what version 1 does not build

## Domain

The public origin is `SITE_URL` in `src/data/site.ts` (`https://antiheroai.com`). TODO: confirm the real domain. That constant is the only copy the build uses.

Mailchimp is not wired yet. `MAILCHIMP_FORM_ACTION` in `.env` stays empty until the form exists. Copy `.env.example` to `.env` if you do not have one.
