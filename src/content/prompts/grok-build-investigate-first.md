---
title: "Investigate before you fix"
useItFor: "Find out why something is broken without letting the AI change a thing."
category: Websites
goal: grok-build
source: websites-on-autopilot
order: 201
---

[RULES]

TASK: Investigate [the problem], read-only
Don't change, stage or commit anything. Problem: [what you see, for example "the hero is just black"]. Find the cause: read the files involved, list the media they load, check those files exist and aren't placeholders, and run the dev server or a build if you need to. Report the root cause in 2 sentences, the exact files and lines, and the smallest fix written as a TASK I can paste next.
