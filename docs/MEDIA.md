# Media

`npm run media` reads originals from `assets-src/media` and writes the files the site serves. A missing original becomes a labeled plate: Anti Black into Carbon, a faint red glow, and the filename in JetBrains Mono. Videos of that kind are 6 seconds. Drop the real file on the same name in `assets-src/media` and run the command again.

Originals over 25 MB are listed in `assets-src/media/.gitignore` by that command and stay off the repo. Smaller originals are committed.

Posters (`*-poster.jpg` and `*-poster.avif`) and `public/media/hero-frames/` are derived. They are not separate Imagine files. Scrub films are H.264 with a keyframe on every frame, plus 120 to 180 WebP frames for the canvas fallback. Door films are WebM AV1 and MP4 H.264, no audio, at most 1080 by 1350. Stills used on the page go through Astro's Picture component at 640, 1280, 1920, and 2560 where the original is that wide. `og.jpg` is the fixed 1200 by 630 social card at `public/og/og.jpg`.

Every Imagine prompt ends with: no text, no logos, photoreal, brand palette of black, bone and one red accent. Every video prompt also ends with: one slow continuous camera move, no cuts, no shake.

| File | Aspect | Where it is used | Grok Imagine prompt |
| --- | --- | --- | --- |
| hero-desktop.mp4 | 16:9 | Home hero scrub, laptop | Hyper-real macro of molten black glass folding into a vast mountain range, red light pulsing through the cracks, camera pushes through a gap into a starfield, one smooth move. One slow continuous camera move, no cuts, no shake. No text, no logos, photoreal, brand palette of black, bone and one red accent. |
| hero-mobile.mp4 | 9:16 | Home hero scrub, phone | Hyper-real macro of molten black glass folding into a vast mountain range, red light pulsing through the cracks, camera pushes through a gap into a starfield, one smooth move. One slow continuous camera move, no cuts, no shake. No text, no logos, photoreal, brand palette of black, bone and one red accent. |
| promise.jpg | 16:9 | Home promise section | Chrome spheres at a red sunrise. No text, no logos, photoreal, brand palette of black, bone and one red accent. |
| door-guides.mp4 | 4:5 | Library door, Guides | Paper sheets in zero gravity orbiting a red core. One slow continuous camera move, no cuts, no shake. No text, no logos, photoreal, brand palette of black, bone and one red accent. |
| door-prompts.mp4 | 4:5 | Library door, Prompts | Liquid mercury letters dissolving into smoke. One slow continuous camera move, no cuts, no shake. No text, no logos, photoreal, brand palette of black, bone and one red accent. |
| door-videos.mp4 | 4:5 | Library door, Videos | A waterfall flowing upward into a storm with red lightning. One slow continuous camera move, no cuts, no shake. No text, no logos, photoreal, brand palette of black, bone and one red accent. |
| door-blog.mp4 | 4:5 | Library door, Blog | Topographic light lines rising into mountains at dusk. One slow continuous camera move, no cuts, no shake. No text, no logos, photoreal, brand palette of black, bone and one red accent. |
| about.jpg | 16:9 | About hero | A lone figure on a cliff above the clouds with a giant red planet. No text, no logos, photoreal, brand palette of black, bone and one red accent. |
| join.jpg | 16:9 | Join page hero, and the home Join band | A pine forest at blue hour with red neon veins. No text, no logos, photoreal, brand palette of black, bone and one red accent. |
| og.jpg | 1200x630 | Default social image, also copied to public/og/og.jpg | An obsidian monolith in a misty meadow at sunrise. No text, no logos, photoreal, brand palette of black, bone and one red accent. |
