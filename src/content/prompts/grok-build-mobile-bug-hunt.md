---
title: "Mobile bug hunt with Playwright"
useItFor: "Find what's broken on phones before your visitors do."
category: Websites
goal: grok-build
order: 205
---

[RULES]

TASK: Mobile bug hunt, report first
Start the dev server and use Playwright to load every page at 375x812 and 390x844, in portrait. For each page, screenshot it and check: horizontal scroll, text overflow, tap targets under 44px, overlapping elements, images that don't load, console errors, and anything heavy that should be desktop-only.
Don't fix anything yet. Save screenshots to [qa/mobile] and give me a list ranked by how bad it looks, with the file and line for each cause. Then write the fixes as separate TASKs I can paste one at a time.
