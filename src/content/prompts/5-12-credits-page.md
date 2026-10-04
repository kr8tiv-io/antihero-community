---
title: "5.12 Credits page"
useItFor: "Name everything you borrowed, with the person, the license, and the link."
category: Websites
goal: grok-build
source: websites-on-autopilot
order: 17
---

[RULES]

TASK: Credits page
Create src/data/credits.ts: a typed list of { name, author, license, link, usedFor, category }, with categories "Code and libraries", "3D models", "Textures and HDRIs", "Fonts", "Inspiration". Build /credits from it: a calm page with one intro line ("[Brand] stands on the generosity of open-source makers. Thank you."), then each category as a clean list with the name linked to the source and the license linked. Seed it with everything that ships to the browser (read each package's license in node_modules), plus Astro, GSAP (Standard no-charge license, https://gsap.com/standard-license), Lenis, three.js and the fonts. Add a small "Credits" link in the footer. Add a comment at the top of credits.ts: anything borrowed gets an entry in the same commit.
