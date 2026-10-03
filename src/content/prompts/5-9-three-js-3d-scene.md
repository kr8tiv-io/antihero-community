---
title: "5.9 Three.js 3D scene"
useItFor: "Put one 3D scene on a big screen, and a still image on a phone."
category: Websites
source: websites-on-autopilot
order: 14
---

[RULES]

TASK: 3D scene in [section]
Install three. Build src/three/scene.ts and mount it in [section] on desktop only (1024px and up, fine pointer). Scene: [describe it, e.g. a slow camera drift over a meadow at golden hour with a glass cube catching the light]. Light it with a free HDRI from Poly Haven (polyhaven.com, CC0) for real reflections, ACES or AgX tone mapping, soft shadows. The camera moves with scroll progress through the section using GSAP ScrollTrigger. One renderer only, pixel ratio capped at 2, rendering paused when the section is offscreen or the tab is hidden. Mobile, low-power devices and reduced motion get a still image rendered from the same scene. Load models through one shared GLTFLoader with Draco and Meshopt support, and leave a drop-in folder /public/models/custom/ so I can replace the model later without code changes. Add every model, texture and HDRI to the credits data.
