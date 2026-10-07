---
title: "The pre-deploy checklist"
useItFor: "Run one last check before anything goes live."
category: Websites
goal: grok-build
order: 208
---

[RULES]

TASK: Pre-deploy check, read-only
Don't change or commit anything. Run a clean production build and report: build errors or warnings, broken internal links, missing images or media, pages without titles, console errors on the home page, total page weight of the home page, and any secrets, API keys or .env values that ended up in the output folder.
Finish with GO or NO-GO and the exact list of what has to be fixed first.
