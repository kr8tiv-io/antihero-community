---
title: "5.7 Scroll-scrubbed video"
useItFor: "Play a video forward and back with the scroll."
category: Websites
source: websites-on-autopilot
order: 12
---

[RULES]

TASK: Scroll-scrubbed hero video
Build src/components/ScrollFilm.astro: a section about [400vh] tall with a sticky full-screen stage. As the visitor scrolls through it, the video /public/media/[file].mp4 plays forward frame by frame, and backwards when they scroll up, using GSAP ScrollTrigger with scrub: true. First, re-encode the video for smooth seeking with ffmpeg: H.264, keyframe every frame (-g 1), no audio (-an), 1920px wide, -movflags +faststart, and keep the original in /_archive. If seeking still stutters, extract frames to WebP (about 120 to 180 frames) and draw them to a canvas instead. Overlay three lines of copy that fade in at 20, 50 and 80 percent progress: "[line 1]", "[line 2]", "[line 3]". Poster image first. Mobile and reduced motion get the poster and the copy, no scrubbing.
