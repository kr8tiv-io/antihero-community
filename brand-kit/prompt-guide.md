# Websites on Autopilot: the prompt guide

AntiHero AI · Facebook Live · Friday, October 2, 2026
Group: https://www.facebook.com/groups/antiheroai

This is the exact workflow we used to build the Aura Homes site, cleaned up so you can copy it. Tonight's demo brand is AntiHero. Later we use the same playbook for an AntiHero site that lists every guide in the group.

How to read this: every grey box is a prompt. Copy the whole box. Text in [square brackets] is yours to fill in. Everything else stays as is.

---

## The words, explained once

- **Grok Bot**: the AI teammate on a cloud computer. It interviews you, writes the plan, writes the prompts and checks the work. https://www.x.ai/bot
- **Grok Build**: xAI's coding agent. It runs in a terminal window on your computer, inside your project folder, and actually writes the files. Install from https://x.ai/cli, docs at https://docs.x.ai/build/overview. Type `/model` inside it to switch models (we use Grok 4.7 Fast for speed).
- **Grok Imagine**: xAI's image and video generator. Use it at https://grok.com/imagine, or through the API (https://x.ai/api/imagine) if you like code.
- **Astro**: the website framework. It builds fast pages that ship very little JavaScript unless you ask for it. https://astro.build
- **GSAP**: the animation library most award-winning sites use. Moves things smoothly and on time. Free, including the plugins. https://gsap.com
- **ScrollTrigger**: a GSAP plugin that ties an animation to your scroll position. Scroll down, the thing happens. Scroll back, it un-happens. https://gsap.com/docs/v3/Plugins/ScrollTrigger/
- **Lenis**: a small library that makes scrolling feel smooth and weighted instead of jumpy. https://lenis.darkroom.engineering
- **Three.js**: the library for real 3D in the browser. Meadows, glass, steam, models you can spin. https://threejs.org
- **Awwwards**: the website that hands out awards for web design. The best free mood board on the internet. https://www.awwwards.com
- **RULES paragraph**: one paragraph of non-negotiables (brand, voice, what never gets touched) pasted at the top of every build prompt, so the coding agent never forgets them.
- **TASK block**: one job for the coding agent. One prompt, one job, one commit.
- **Commit**: a saved checkpoint in git. If a prompt breaks something, you roll back to the last commit and lose nothing.
- **localhost**: your site running privately on your own computer (usually http://localhost:4321 for Astro). Nobody else can see it.

---

## Stage 0. The pre-checklist (do not skip)

Before any of this works you need:

- [ ] **Brand voice** written down (three traits, banned words)
- [ ] **Logo** done, ideally as an SVG
- [ ] **Colors** with hex codes and **two fonts**
- [ ] **Tagline**
- [ ] A **brand brain** doc your AI reads first

Not done yet? Go through *Build a Brand From Scratch With AI* (the Oct 1 guide in the group) first. A website without a brand is a very fast way to look like everyone else.

Tools on your computer:

- [ ] Node.js (LTS) from https://nodejs.org
- [ ] Git from https://git-scm.com
- [ ] Grok Build:
  - Mac or Linux: `curl -fsSL https://x.ai/cli/install.sh | bash`
  - Windows PowerShell: `irm https://x.ai/cli/install.ps1 | iex`
  - Then `cd` into your project folder and type `grok`. It opens a browser to log in the first time.
- [ ] A folder for the project, and a second folder called `assets` for your logo, fonts and images

---

## Stage 1. The interview (Grok Bot or any chat AI)

Run this first, in one long chat, so the AI remembers everything.

```
You are a senior web designer and art director who has built sites that won Awwwards Site of the Day. Interview me to plan a website. Read my brand brain first: [paste it or attach it].

Ask me one question at a time. Wait for my answer before the next one. Push back if an answer is vague. Cover:
1. What the site is for, in one sentence, and the one action a visitor should take.
2. Who the visitor is: a specific person, what they want, what they're afraid of, what device they're on.
3. The offer: what I sell or give away, and why anyone should care.
4. The pages and sections I think I need (you'll fix this list later).
5. The vibe in three words, and three words it must never feel like.
6. Three to five reference sites I love (Awwwards, Godly, anything) and exactly what I love about each.
7. What I already have: logo, photos, video, copy, fonts, an old site.
8. What must never change (an existing page, a video, legal wording).
9. Motion appetite from 1 to 10: 1 is a calm brochure, 10 is a 3D scroll movie.
10. Hard limits: deadline, budget, hosting, things I legally can't say.

When you have enough, write a one-page Site Brief: goal, visitor, offer, vibe, references and what to steal from each (the thinking, not the look), what exists, what's protected, motion level, limits. Then ask me what you got wrong.
```

**Tip:** answer with voice typing. You'll say better stuff than you'd type.

**Finding references:** go to https://www.awwwards.com, open "Websites", filter by Sites of the Day, and screenshot three you'd steal from. Paste the links into the interview. The Aura Homes references were Lando Norris, Igloo Inc, Cozy Lake Cabin, Edelschwarz and The Floating Forest.

---

## Stage 2. The section plan

```
Using the Site Brief, write the section plan for the site.

For each page: the URL, its one job, and its sections in order. For each section: a name, what it says (draft headline and one line of copy in my brand voice), what the visitor sees (image, video, 3D, plain), and the one effect that earns its place there (or "none"). Mark which sections are protected and must never be changed once built.

Rules: the homepage hero gets the most attention. No more than one "wow" effect per section. Every page ends with the one action from the brief. Keep the first version small enough to ship in a weekend, and put everything else in a "Version 2" list at the bottom.

Then list every image and video I need, with a short Grok Imagine prompt for each, the aspect ratio, and where it goes.
```

---

## Stage 3. The meta-prompt: "write me all the build prompts"

This is the trick. You don't write the build prompts. You make the AI write them, all of them, in order, each one able to stand on its own.

```
Now write the complete build package for Grok Build, the coding agent that will build this site in my project folder.

Format:
1. Start with one RULES paragraph that every prompt repeats word for word. It must include: the project type (Astro site, or tell me if something else fits better), my brand name spelled correctly, fonts and colors with hex codes, my voice rules and banned words, everything that must never be touched, "do not deploy", "do not delete files, move unused ones to /_archive", motion rules (calm or energetic, respect prefers-reduced-motion, animate only transform and opacity), and "commit to git when done with a short message".
2. Then numbered prompts, one job each, in build order: setup and backup, site map and navigation, each page and section, imagery, then the motion and effects pass, then performance, credits page and QA.
3. Every prompt is one copy-paste block: the full RULES paragraph, then "TASK: [name]", then exact instructions. Name files, components and routes. Say what "done" looks like and what to report back.
4. Each prompt must work on its own. Never write "as before" or "see above".
5. Anything borrowed (code, models, fonts, textures) must get a credits entry in the same commit.
6. Elevated by default: every prompt aims for an Awwwards Site of the Day result, not a regular website. Each section gets one bold idea, real copy in my voice and a specific detail nobody else would think of.
7. Put my NO SLOP RULES inside the RULES paragraph, word for word: [paste the NO SLOP RULES].

Write them all. Don't summarize. Save it as a file I can download.
```

---

## Stage 4. The RULES paragraph template

Fill this in once. It goes at the top of every prompt. This is what keeps an autopilot from flying into a mountain.

```
RULES: This is the [Brand] [Astro] site. Do NOT change [the protected page, video or section] in any way. Do not deploy. Do not delete files; move unused ones to /_archive. Fonts: [display font] for headlines, [body font] for text. Colors: [name #hex], [name #hex], [accent name #hex] (accent used sparingly). Use the logo in /src/assets/logo wherever a logo is needed. Brand name is "[Brand]" everywhere. Never say: [banned words or claims, e.g. prices, guarantees, competitor names]. Tone: [three voice traits]. No em dashes, no exclamation points. Motion must feel [calm, slow and expensive / quick and playful]: [long eases, nothing bouncy], respect prefers-reduced-motion, animate only transform and opacity. Elevated by default: aim for an Awwwards Site of the Day result, not a regular website; one bold idea per section, real copy, specific details. Follow the NO SLOP RULES: [paste them]. Commit to git when done with a short message.
```

**AntiHero example** (fill with your real kit):

```
RULES: This is the AntiHero Astro site. Do NOT change the homepage hero video or its scroll logic once it is approved. Do not deploy. Do not delete files; move unused ones to /_archive. Fonts: [Bebas Neue] for headlines, [Barlow] for text. Colors: [Anti Black #0A0A0B] 60 percent, [Bone #ECE8E1] 30 percent, [accent #hex] 10 percent. Use the AntiHero logo in /src/assets/logo wherever a logo is needed. Brand name is "AntiHero" everywhere. Never say: delve, unlock, elevate, seamless, game-changer, empower, journey. Tone: direct, funny, human. No em dashes, no exclamation points. Motion must feel confident and quick but never bouncy: short eases, respect prefers-reduced-motion, animate only transform and opacity. Elevated by default: aim for an Awwwards Site of the Day result, not a regular website. Follow the NO SLOP RULES (Stage 9). Commit to git when done with a short message.
```

In every TASK prompt below, `[RULES]` means "paste your full RULES paragraph here".

---

## Stage 5. Example TASK prompts (copy, swap the brackets)

### 5.1 Setup and backup

```
[RULES]

TASK: Project setup and backup
Create a new Astro project in this folder (latest stable, TypeScript strict, no UI framework yet). Add Tailwind only if I said so in the brief. Set up git, a .gitignore for node_modules and .env, and make a first commit called "Fresh start". Create /src/assets/logo, /src/assets/img, /public/media and /_archive. Copy my logo files from [path to assets folder] into /src/assets/logo and my fonts into /public/fonts with @font-face rules in a global CSS file. Add CSS variables for every brand color. Tell me the command to run the site locally and the URL.
```

### 5.2 Hero

```
[RULES]

TASK: Homepage hero
Build the homepage hero as src/components/Hero.astro. Full viewport height. Background: [image or looping muted video] from /public/media/[file], with a poster image so something shows instantly. Headline "[headline]" in the display font, very large, low-left, with generous empty space. One line under it: "[subline]". One button: "[CTA text]" linking to [URL]. Text must pass contrast over the image (add a soft dark gradient behind it if needed). On mobile, use the still image, not the video. Show me a screenshot description of desktop and mobile.
```

### 5.3 Navigation

```
[RULES]

TASK: Navigation and menu
Build a slim top bar (about 56px): logo left, text links [Page 1, Page 2, Page 3], and an outlined "[CTA]" button right. Transparent over the hero, soft frosted background after 80px of scroll, hides on scroll down and comes back on scroll up. Under 1024px show only the logo and a "Menu" button that opens a full-screen menu with big links. Menu button: 44px minimum tap target, aria-expanded, Escape closes, focus stays inside the open menu and returns to the button on close. Add the same links to the footer.
```

### 5.4 Sections (one prompt per section)

```
[RULES]

TASK: [Section name] section
Build src/components/[SectionName].astro and add it to [page] after [previous section]. Purpose: [one job of this section]. Content: headline "[headline]", copy "[copy]", [cards / image grid / testimonial / FAQ list]. Layout: [describe it, or "steal the structure of [reference site]'s [section], not the look"]. Use only brand fonts and colors. Mobile first, then desktop. No effects yet; motion comes in a later prompt.
```

### 5.5 Lenis smooth scroll

```
[RULES]

TASK: Smooth scroll foundation
Install Lenis and GSAP. Wire Lenis to GSAP ScrollTrigger site-wide (lenis.on('scroll', ScrollTrigger.update) and drive Lenis from gsap.ticker). [Except the protected page; leave its scroll logic exactly as is.] Create src/scripts/motion.ts with shared eases, durations and a prefers-reduced-motion check, so every later effect uses the same feel. With reduced motion on, Lenis is disabled and scrolling is native. Anchor links must still land in the right place.
```

### 5.6 GSAP ScrollTrigger reveals

```
[RULES]

TASK: Scroll reveals
Create a reusable reveal system using GSAP ScrollTrigger and the shared settings in src/scripts/motion.ts. (1) Headings: a <RevealHeading> component that splits text into lines (GSAP SplitText), each line masked and rising from below with a 0.06s stagger when it enters the viewport. (2) Images: a clip-path "window opening" from the center outward while the image inside scales from 1.1 to 1. (3) Cards in grids stagger by 0.1s. Each animation plays once. Use on every H1 and H2 [outside the protected page]. Reduced motion: everything is simply visible.
```

### 5.7 Scroll-scrubbed video

This is the "the video plays as you scroll" effect. Make the video in Grok Imagine first (Stage 6).

```
[RULES]

TASK: Scroll-scrubbed hero video
Build src/components/ScrollFilm.astro: a section about [400vh] tall with a sticky full-screen stage. As the visitor scrolls through it, the video /public/media/[file].mp4 plays forward frame by frame, and backwards when they scroll up, using GSAP ScrollTrigger with scrub: true. First, re-encode the video for smooth seeking with ffmpeg: H.264, keyframe every frame (-g 1), no audio (-an), 1920px wide, -movflags +faststart, and keep the original in /_archive. If seeking still stutters, extract frames to WebP (about 120 to 180 frames) and draw them to a canvas instead. Overlay three lines of copy that fade in at 20, 50 and 80 percent progress: "[line 1]", "[line 2]", "[line 3]". Poster image first. Mobile and reduced motion get the poster and the copy, no scrubbing.
```

### 5.8 Page transitions

```
[RULES]

TASK: Page transitions
Add Astro View Transitions (ClientRouter) with a custom transition: [a thin line in the accent color sweeps across the screen, the old page fades and lifts 20px, the new page rises in], about 700ms total. The logo and nav persist without flicker. Re-initialize GSAP, ScrollTrigger and Lenis correctly after each navigation (kill old triggers, then refresh). Reduced motion: a plain quick fade.
```

### 5.9 Three.js 3D scene

```
[RULES]

TASK: 3D scene in [section]
Install three. Build src/three/scene.ts and mount it in [section] on desktop only (1024px and up, fine pointer). Scene: [describe it, e.g. a slow camera drift over a meadow at golden hour with a glass cube catching the light]. Light it with a free HDRI from Poly Haven (polyhaven.com, CC0) for real reflections, ACES or AgX tone mapping, soft shadows. The camera moves with scroll progress through the section using GSAP ScrollTrigger. One renderer only, pixel ratio capped at 2, rendering paused when the section is offscreen or the tab is hidden. Mobile, low-power devices and reduced motion get a still image rendered from the same scene. Load models through one shared GLTFLoader with Draco and Meshopt support, and leave a drop-in folder /public/models/custom/ so I can replace the model later without code changes. Add every model, texture and HDRI to the credits data.
```

The Aura Homes site went much further (hyper-real grass, trees, polycarbonate glass, a steaming cedar hot tub). The big lesson from that research: **what makes 3D look real is light, not more polygons.** An outdoor HDRI, good tone mapping, ambient occlusion and fog do more than a million extra triangles.

### 5.10 Hover glow titles

```
[RULES]

TASK: Title glow on hover
On desktop, headings (H1, H2 and card titles) get a soft glow that "heats up" behind them on hover: a blurred radial gradient in [accent color] at low opacity, easing in over about 1.2s and cooling out over about 2.4s. Build it in CSS first (a ::before pseudo-element, animating only opacity and transform). Optionally upgrade to one shared WebGL canvas with animated noise if it stays under 1ms per frame. Keyboard focus triggers it too. Touch devices and reduced motion get a static faint glow or nothing.
```

### 5.11 Performance and media compression

```
[RULES]

TASK: Media and performance pass
Find every image and video on the site. Images: export AVIF and WebP at 1280, 1920 and 2560 widths and serve them through Astro's Picture component with sizes. Videos: encode a WebM (AV1) and an MP4 (H.264, crf 23, -movflags +faststart, no audio), each loop under about 4 MB where possible, with a poster frame. Video tags: muted, playsinline, loop, preload="metadata". Mobile and save-data users get the poster only. Keep originals in /_archive/originals. Preload the two brand fonts. Write scripts/optimize-media.mjs so I can rerun this on new files. Report a before and after size table and a Lighthouse estimate (target: LCP under 2.5s, no layout shift).
```

### 5.12 Credits page

Borrowing open-source code is normal. Not saying thank you is rude, and sometimes it's a license violation.

```
[RULES]

TASK: Credits page
Create src/data/credits.ts: a typed list of { name, author, license, link, usedFor, category }, with categories "Code and libraries", "3D models", "Textures and HDRIs", "Fonts", "Inspiration". Build /credits from it: a calm page with one intro line ("[Brand] stands on the generosity of open-source makers. Thank you."), then each category as a clean list with the name linked to the source and the license linked. Seed it with everything that ships to the browser (read each package's license in node_modules), plus Astro, GSAP (Standard no-charge license, https://gsap.com/standard-license), Lenis, three.js and the fonts. Add a small "Credits" link in the footer. Add a comment at the top of credits.ts: anything borrowed gets an entry in the same commit.
```

### 5.13 QA with Playwright

Playwright is a free tool that opens your site in a real browser by itself and checks it. https://playwright.dev

```
[RULES]

TASK: QA pass
Install Playwright as a dev dependency. Write tests/qa.spec.ts that, for every page at 375px, 768px, 1440px and 1920px: loads the page, fails on any console error or 404, takes a full-page screenshot into /qa/screenshots, checks every internal link resolves, checks every image has alt text, and checks the menu opens and closes with the keyboard. Also run it once with reduced motion on. Run npm run build, then the tests. Fix anything you broke. Report what you fixed and anything you need me to decide. Confirm with git diff that the protected files are unchanged.
```

---

## Stage 6. Visuals with Grok Imagine

Use https://grok.com/imagine (easiest) or the API (https://docs.x.ai/developers/model-capabilities/imagine). Make the still first, approve it, then animate it.

**Hero still:**
```
[Scene in one sentence], shot like a premium brand campaign, [time of day and light], [your palette] color grade, calm empty space on the [left] third for a headline, no text, no logos, photoreal, 16:9.
```

**Scroll video (from your approved still):**
```
Animate this image. Slow, steady camera [push-in / dolly right / rise], no cuts, no shake, no zoom pulses, subjects move gently, light stays constant, ends on a calm composed frame. [10] seconds.
```

Why "no cuts, no shake": a scroll-scrubbed video gets played backwards and forwards by your thumb. Any jump looks like a glitch. Smooth, single-move shots scrub beautifully.

**Rules:** make them in the brand's world (AntiHero's might be [its world here]); keep the same light across every image; never put text in the image, the site adds it.

---

## Stage 7. Autopilot: feeding Grok Build while Grok Bot watches

The loop, one prompt at a time:

1. Paste prompt N into Grok Build. Let it work.
2. It commits.
3. Grok Bot checks the commit: did it do the task, did it touch anything protected, did it follow the RULES.
4. You look at localhost, hard refresh (Ctrl+Shift+R, or Cmd+Shift+R on Mac).
5. Good? Next prompt. Bad? Paste the fix into Grok Build, or roll back.

**The watcher prompt (give this to Grok Bot):**

```
You're my build supervisor. Here is the full build package: [attach it]. Grok Build is running these prompts one at a time in my project. After each one I'll paste its final report and the output of `git show --stat HEAD` (and the diff if it's small).

For each step tell me:
1. Done or not done, against the TASK's own definition of done.
2. Did it touch anything the RULES protect? Name the file.
3. Any RULES broken (banned words, em dashes, wrong colors, missing credits entry, deploys, deleted files).
4. What to look at on localhost before moving on.
5. If something is wrong: the exact fix prompt to paste back into Grok Build, with the RULES paragraph on top.
Then give me the next prompt number. Keep it short.
```

If your Grok Bot can see the project directly (a shared repo or folder), tell it to run `git log` and `git diff` itself after every step. That's the full autopilot: you approve, it checks, Grok Build builds.

**Switching models:** inside Grok Build type `/model` and pick Grok 4.7 Fast for quick, simple prompts (copy changes, sections). Switch back to the bigger model for 3D, transitions and anything with "refactor" in it.

**Rolling back:** `git log --oneline` to find the last good commit, then ask Grok Build: "Revert the last commit, keep a backup branch called backup-[date]."

---

## Stage 8. Review and the fix list

```
Here are screenshots of my site on desktop and mobile: [attach]. Here is my Site Brief and brand brain: [attach]. Act as an Awwwards juror and my brand director. Give me a numbered fix list, most important first. Each fix must be specific ("headline is 14 words, cut to 6", not "make it pop") and written as a ready-to-paste Grok Build TASK with my RULES paragraph on top. Also tell me what to keep so I don't break the good stuff.
```

Last checks before you call it done:
- Hard refresh every page. Then open it on your actual phone.
- Turn on reduced motion (your OS accessibility settings) and scroll the whole site.
- Run your homepage through https://pagespeed.web.dev once it's live.
- /credits lists everything you borrowed.

## Stage 9. Make It Stand Out

A working website is the floor. Nobody remembers the floor. This stage is how you get from "nice site" to "wait, who made this".

### 9.1 The NO SLOP RULES (written for the AI, not for you)

Paste this into your RULES paragraph, right before "Commit to git". Every build prompt carries it. This is what stops the AI from handing you the same website it handed everyone else this morning.

```
NO SLOP RULES. Never use: purple-to-blue or rainbow gradients; a centered hero with a floating stock blob or abstract 3D shape; the generic row of 3 feature cards with icons; emoji as icons; the words unlock, elevate, seamless, revolutionize, empower, game-changer, delve, leverage, cutting-edge, journey, "in today's fast-paced world" or "it's not just X, it's Y"; lorem ipsum or placeholder copy; stock photos of smiling people pointing at laptops; the default Tailwind look (gray-50 backgrounds, rounded-xl cards, indigo buttons, everything centered); every section with the same rhythm (headline, subline, grid, repeat); invented testimonials, fake logos or made-up numbers. Instead, always: one bold idea per section, and say what it is in your report; real copy in the brand voice, specific and human; asymmetric layouts with intentional empty space; a deliberate type scale with big contrast between display and body; motion with a purpose (it guides the eye, reveals the story or gives feedback, never decoration); specific details only this brand would have; brand colors and fonts only. If you're about to do something you've seen on a thousand sites, stop and do the more interesting version. If something isn't real yet, mark it TODO instead of faking it.
```

### 9.2 The Visual Interview

Run this right after the site interview, in the same chat.

```
You're an award-winning art director. Read my brand brain and Site Brief: [paste or attach]. Interview me about the look and feel of the site, one question at a time, and wait for each answer. Show me examples or options when I'm stuck. Cover:
1. Five mood words, and three words it must never feel like.
2. Three to five Awwwards sites I love (awwwards.com, Sites of the Day), and exactly which part of each: the type, the scroll, the layout, the color, the motion.
3. Type pairing: how loud the headlines should be, and how big the contrast between headline and body.
4. Color temperature: warm, cool or neutral, light or dark, and how often the accent color shows up.
5. Motion personality: calm and expensive, snappy and playful, heavy and cinematic, or something else. Give me a real-world comparison for each.
6. Texture: clean and flat, film grain, paper, glass, noise, or something physical from my world.
7. Imagery style: photo, illustration, 3D or video, light and time of day, real people or no people, and what never shows up.
8. The signature moment: the one thing people will screenshot and send to a friend.
Then write a one-page Visual Direction brief: mood, references and what to steal from each, type scale with sizes, color usage with hex codes, motion rules (eases, durations, what moves and what never moves), texture, imagery rules, the signature moment, and a "never do" list. Ask me what you got wrong.
```

### 9.3 The Standout Features Interview

```
You're the creative technologist on an agency team that wins Awwwards. Read my Site Brief and Visual Direction brief: [paste or attach]. Propose features that would make this site memorable, then interview me about them one at a time. Consider at least: a signature hero interaction, scroll storytelling, a cursor effect, a 3D moment, micro-interactions (buttons, links, forms), an optional sound toggle (off by default), page transitions, and a playful easter egg. For each one, explain in plain English what the visitor sees and feels, why it fits my brand (or why it doesn't), how heavy it is for phones, and a version for people who turn motion off. Ask me which ones excite me. Then pick the 3 to 5 best for my brand, rank them, and for each write: the plain-English description, where on the site it lives, and a ready-to-paste Grok Build TASK with my RULES paragraph on top. Cut anything that's a trick without a reason.
```

### 9.4 Elevation prompts (upgrade a section or the whole site)

Use these after something works but feels ordinary. Point each one at a section or at the whole site.

```
[RULES]

TASK: Typography and spacing pass on [section or whole site]
Audit and upgrade the type and spacing. Define one type scale (display, h1, h2, h3, body, small, caption) with real contrast between display and body, using only the brand fonts, and use it everywhere. Tighten letter spacing on big display type, loosen it on small caps. Set body text at 16 to 18px with a line length of 45 to 75 characters and line height around 1.5. Create one spacing scale and use it for every gap. Break the identical section rhythm: vary alignment, widths and empty space so each section has its own shape. Report before and after for each section in one line.
```

```
[RULES]

TASK: Motion pass on [section or whole site]
Audit every animation. Remove anything that moves just because it can. For what's left, give each one a job (guide the eye, reveal the story, or give feedback) and say which job in your report. Use one shared set of eases and durations from src/scripts/motion.ts. Add the one motion moment from the Visual Direction brief if it's missing. Stagger related elements, never animate everything at once, animate only transform and opacity, and make sure reduced motion gets a calm, complete version. Report what you removed, what you kept and what you added.
```

```
[RULES]

TASK: Imagery pass on [section or whole site]
Audit every image and video against the Visual Direction brief (light, color grade, subject, what never shows up). List anything off-brand, generic or stock-looking. For each, write a Grok Imagine prompt for a replacement in the brand's world and leave a clearly named placeholder slot. Crop for intent: make sure every image leaves calm space where text sits, and that the hero image reads at phone size. Apply one consistent color treatment (grade, grain or duotone) so the whole site feels like one world. Report the list and the prompts.
```

```
[RULES]

TASK: Copy pass on [section or whole site]
Rewrite every headline, subline, button and caption in the brand voice from the brand brain. Kill every banned word and every generic line ("Welcome to our website", "We are passionate about", "Learn more"). Headlines: short, specific, a little surprising. Buttons: say exactly what happens ("Book a call", not "Submit"). Mark anything that needs a real fact (a number, a name, a quote) as TODO instead of inventing it. Report a before and after table.
```

```
Act as a jury of three Awwwards judges: a designer, a developer and a brand strategist. Review my site: [live URL, or attach screenshots of every page on desktop and mobile]. Here is my Site Brief and Visual Direction brief: [attach]. Score it out of 10 on Design, Usability, Creativity and Content, the way Awwwards does, with two lines of honest reasoning for each score. Then tell me: the first impression in 3 seconds, the single thing holding it back the most, anything that looks like AI slop or a template, and what's already good enough to keep. Finish with a numbered fix list, most important first, each fix specific enough that a developer could do it without asking a question. No flattery. If it's a 6, say 6.
```

```
Turn this fix list into Grok Build prompts: [paste the jury's fix list]. Group related fixes so each prompt is one job and one commit, and order them by impact. Every prompt is a single copy-paste block that starts with my full RULES paragraph (including the NO SLOP RULES and the elevated-by-default line), then "TASK: [name]", then exact instructions, files to touch, what done looks like and what to report. Each prompt must work on its own. Finish with the order to run them in and what to check on localhost after each.
```

### 9.5 The Post-launch Quality Upgrade Interview

Run this when the site is finished and live. A week later is even better. You'll see it with fresh, slightly annoyed eyes.

```
My site is finished and live at [URL]. Read my Site Brief, Visual Direction brief and brand brain: [attach]. First, review the live site yourself (open it, or use these screenshots: [attach]) on desktop and mobile, and write down what feels flat, generic, slow or confusing, before I tell you anything. Then interview me one question at a time: which pages I avoid showing people, where visitors drop off or get confused (if I have analytics, ask for them), what people have said about it, what feels flat to me, what I'd be proudest of if it were better, and what I've been too scared to try. Then write an upgrade plan with no more than 8 upgrades, ranked by impact versus effort, each explained in one plain-English sentence. Then write every upgrade as a ready-to-paste Grok Build prompt with my full RULES paragraph on top (including the NO SLOP RULES and elevated by default). Protect everything that already works.
```

---

## How to pick what you need

You don't need all of this. Most sites shouldn't use all of this.

| Your site | Use | Skip |
|---|---|---|
| Local business, 3 to 5 pages | Stages 1 to 4, hero, nav, sections, Lenis, reveals, media pass, QA | 3D, scroll video, glow |
| Personal brand or creator (AntiHero) | All of the above plus one scroll-scrubbed video, page transitions, hover glow | Heavy 3D |
| Product launch or "wow" landing page | Everything, including one 3D scene | More than one 3D scene per page |
| Guides library (the AntiHero site) | Hero, nav, a card grid of guides with filters, reveals, transitions, credits, QA | Scroll video, 3D |

Rules of thumb:
- **One wow per section.** Three effects fighting is not three times the wow.
- **Motion appetite 1 to 4:** reveals and smooth scroll. **5 to 7:** add scroll video and transitions. **8 to 10:** add 3D. Respect your own answer from the interview.
- **Mobile is half your visitors.** Every heavy effect needs a calm phone version.
- **Effects come last.** Content and structure first, then motion. Decorating a house before the walls are up is how you get a pretty tent.

---

## All the links

- Grok: https://grok.com
- Grok Imagine: https://grok.com/imagine
- Grok Imagine API: https://x.ai/api/imagine
- Grok Build (install): https://x.ai/cli
- Grok Build docs: https://docs.x.ai/build/overview
- Grok Build CLI reference: https://docs.x.ai/build/cli/reference
- Grok Bot: https://www.x.ai/bot
- xAI console (API keys): https://console.x.ai
- GSAP: https://gsap.com
- ScrollTrigger docs: https://gsap.com/docs/v3/Plugins/ScrollTrigger/
- Lenis: https://lenis.darkroom.engineering
- Three.js: https://threejs.org
- Poly Haven (free HDRIs, textures, models): https://polyhaven.com
- Awwwards: https://www.awwwards.com
- Astro: https://astro.build
- Astro view transitions: https://docs.astro.build/en/guides/view-transitions/
- Node.js: https://nodejs.org
- Git: https://git-scm.com
- Playwright: https://playwright.dev
- PageSpeed Insights: https://pagespeed.web.dev
- AntiHero AI group: https://www.facebook.com/groups/antiheroai

All links checked October 2, 2026.

BE YOUR OWN HERO.
