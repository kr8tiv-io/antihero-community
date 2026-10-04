---
title: "5.6 GSAP ScrollTrigger reveals"
useItFor: "Bring headings, images, and cards in as they reach the screen."
category: Websites
goal: grok-build
source: websites-on-autopilot
order: 11
---

[RULES]

TASK: Scroll reveals
Create a reusable reveal system using GSAP ScrollTrigger and the shared settings in src/scripts/motion.ts. (1) Headings: a <RevealHeading> component that splits text into lines (GSAP SplitText), each line masked and rising from below with a 0.06s stagger when it enters the viewport. (2) Images: a clip-path "window opening" from the center outward while the image inside scales from 1.1 to 1. (3) Cards in grids stagger by 0.1s. Each animation plays once. Use on every H1 and H2 [outside the protected page]. Reduced motion: everything is simply visible.
