---
title: "5.10 Hover glow titles"
useItFor: "Warm a heading up under the cursor. Phones stay still."
category: Websites
source: websites-on-autopilot
order: 15
---

[RULES]

TASK: Title glow on hover
On desktop, headings (H1, H2 and card titles) get a soft glow that "heats up" behind them on hover: a blurred radial gradient in [accent color] at low opacity, easing in over about 1.2s and cooling out over about 2.4s. Build it in CSS first (a ::before pseudo-element, animating only opacity and transform). Optionally upgrade to one shared WebGL canvas with animated noise if it stays under 1ms per frame. Keyboard focus triggers it too. Touch devices and reduced motion get a static faint glow or nothing.
