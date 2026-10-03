// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';
import mdx from '@astrojs/mdx';
import { SITE_URL } from './src/data/site.ts';

// https://astro.build/config
export default defineConfig({
  // TODO: confirm the real domain. SITE_URL in src/data/site.ts is the only copy.
  site: SITE_URL,
  output: 'static',
  trailingSlash: 'ignore',
  build: {
    format: 'directory',
  },
  integrations: [sitemap(), mdx()],
  vite: {
    plugins: [tailwindcss()],
  },
});
