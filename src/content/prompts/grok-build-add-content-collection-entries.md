---
title: "Load a batch of content into the site"
useItFor: "Add a pile of new entries (prompts, posts, products) without breaking the build."
category: Websites
goal: grok-build
order: 204
---

[RULES]

TASK: Add new content entries from [file or folder]
Read the content schema in [src/content.config.ts or wherever it lives] and two existing entries first, so you match the format exactly. Then add each new entry as its own file in [folder]. Keep slugs lowercase and unique, don't overwrite existing files, and don't change the schema or any existing entry.
Run the build. If an entry fails validation, fix that entry, not the schema. Report how many you added, the slugs, and the build result. One commit: "Add [n] new [entries]".
