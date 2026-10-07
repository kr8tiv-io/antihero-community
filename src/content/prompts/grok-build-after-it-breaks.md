---
title: "Undo it without making it worse"
useItFor: "Roll back a bad change cleanly when the AI broke something."
category: Websites
goal: grok-build
order: 209
---

[RULES]

TASK: Something broke after the last change, find and undo it safely
Don't force push, don't reset anything that's already pushed, and don't delete files. Show me the last 5 commits and what each one changed. Find which commit broke [what I see].
Then propose the smallest fix: either a revert commit for that one change or a targeted patch. Tell me which you recommend and why, and wait for my OK before doing it.
