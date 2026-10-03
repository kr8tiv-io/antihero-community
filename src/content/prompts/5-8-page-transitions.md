---
title: "5.8 Page transitions"
useItFor: "Move between pages without a hard cut, and keep the nav steady."
category: Websites
source: websites-on-autopilot
order: 13
---

[RULES]

TASK: Page transitions
Add Astro View Transitions (ClientRouter) with a custom transition: [a thin line in the accent color sweeps across the screen, the old page fades and lifts 20px, the new page rises in], about 700ms total. The logo and nav persist without flicker. Re-initialize GSAP, ScrollTrigger and Lenis correctly after each navigation (kill old triggers, then refresh). Reduced motion: a plain quick fade.
