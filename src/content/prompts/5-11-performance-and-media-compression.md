---
title: "5.11 Performance and media compression"
useItFor: "Shrink the pictures and video so the first screen shows up fast."
category: Websites
source: websites-on-autopilot
order: 16
---

[RULES]

TASK: Media and performance pass
Find every image and video on the site. Images: export AVIF and WebP at 1280, 1920 and 2560 widths and serve them through Astro's Picture component with sizes. Videos: encode a WebM (AV1) and an MP4 (H.264, crf 23, -movflags +faststart, no audio), each loop under about 4 MB where possible, with a poster frame. Video tags: muted, playsinline, loop, preload="metadata". Mobile and save-data users get the poster only. Keep originals in /_archive/originals. Preload the two brand fonts. Write scripts/optimize-media.mjs so I can rerun this on new files. Report a before and after size table and a Lighthouse estimate (target: LCP under 2.5s, no layout shift).
