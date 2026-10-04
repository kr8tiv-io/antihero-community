---
title: "5.5 Lenis smooth scroll"
useItFor: "Make scrolling feel weighted, and switch it off when someone wants less motion."
category: Websites
goal: grok-build
source: websites-on-autopilot
order: 10
---

[RULES]

TASK: Smooth scroll foundation
Install Lenis and GSAP. Wire Lenis to GSAP ScrollTrigger site-wide (lenis.on('scroll', ScrollTrigger.update) and drive Lenis from gsap.ticker). [Except the protected page; leave its scroll logic exactly as is.] Create src/scripts/motion.ts with shared eases, durations and a prefers-reduced-motion check, so every later effect uses the same feel. With reduced motion on, Lenis is disabled and scrolling is native. Anchor links must still land in the right place.
