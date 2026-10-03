"""Write the AntiHero Design System artifact files (project/...) into a staging folder.

Usage:  python design_system.py stage <dir>          -> writes project/* (not the index) + upload/ copies
        python design_system.py index <dir> <ids.json> -> writes project/design-system.json from upload results
"""
import datetime
import glob
import json
import os
import shutil
import sys

from brand import (A_PATH, C, FONTS, HERO_PATH, HERO_UP, HERO_UP_W, KIT, FontOutline, hero_upright_group,
                   mark_group, text_path)

TITLE = 'AntiHero'
NS = 'AntiHero'


def w(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


# ---------------------------------------------------------------------------
TOKENS = {
    'name': TITLE, 'version': 1,
    'meta': {'source': 'AntiHero Brand Kit v1.0 (Sept 2026): brand bible + rebuilt logo files'},
    'color': {
        'themes': [{'id': 'dark', 'name': 'Dark'}, {'id': 'light', 'name': 'Light'}],
        'tokens': [
            {'name': 'void', 'value': C['void'], 'usage': 'Anti Black. The primary ground of every dark layout.'},
            {'name': 'carbon', 'value': C['carbon'], 'usage': 'The badge disc (sampled from the original logo); panels and cards on void.'},
            {'name': 'graphite', 'value': C['graphite'], 'usage': 'Raised surfaces and dividers on dark layouts.'},
            {'name': 'ash', 'value': C['ash'], 'usage': 'Captions and metadata on void (6.1:1) and carbon (5.0:1). Never on bone for text.'},
            {'name': 'bone', 'value': C['bone'], 'usage': 'Warm paper white: the ground of light layouts, quote cards, and print.'},
            {'name': 'white', 'value': '#ffffff', 'usage': 'Hero White: the mark, label boxes, headlines on void.'},
            {'name': 'ignition', 'value': C['ignition'], 'usage': 'Ignition Red, the one accent: one red idea per layout (a word, a label, a button, the hero in the wordmark). As text only at 24px and up on void (4.2:1) or bone (3.9:1).'},
            {'name': 'ember', 'value': C['ember'], 'usage': 'Pressed and hover state of ignition. Never a fill on its own.'},
            {'name': 'dusk', 'value': C['dusk'], 'usage': 'Photo duotone midtone (void -> dusk -> bone). Secondary text on bone (6.5:1).'},
            {'name': 'surface', 'value': {'dark': C['void'], 'light': C['bone']}, 'usage': 'Page ground.'},
            {'name': 'surface-raised', 'value': {'dark': C['carbon'], 'light': '#ffffff'}, 'usage': 'Cards, panels, code and prompt boxes on surface.'},
            {'name': 'ink', 'value': {'dark': '#ffffff', 'light': C['void']}, 'usage': 'Headlines and body copy on surface and surface-raised (16:1 and up in both themes).'},
            {'name': 'ink-muted', 'value': {'dark': C['ash'], 'light': C['dusk']}, 'usage': 'Secondary text on surface and surface-raised (5.0:1 or better in both themes).'},
            {'name': 'line', 'value': {'dark': '#ffffff24', 'light': '#0a0a0b1f'}, 'usage': 'Hairlines, table rules, card borders.'},
            {'name': 'label-fill', 'value': {'dark': '#ffffff', 'light': C['void']}, 'usage': 'The label box fill: white boxes on dark grounds, black boxes on light grounds.'},
            {'name': 'on-label', 'value': {'dark': C['void'], 'light': '#ffffff'}, 'usage': 'Text inside a label-fill box.'},
            {'name': 'on-ignition', 'value': '#ffffff', 'usage': 'Text and marks on an ignition fill (4.7:1, WCAG AA). The wordmark on red is all on-ignition.'},
            {'name': 'focus-ring', 'value': {'dark': '#ffffff', 'light': C['void']}, 'usage': 'Keyboard focus: a solid 2px ring in ink, offset 2px from the control.'},
        ]},
    'type': {
        'fonts': [
            {'family': 'Bebas Neue', 'file': 'fonts/BebasNeue-Regular.ttf', 'weight': '400'},
            {'family': 'Barlow', 'file': 'fonts/Barlow-Regular.ttf', 'weight': '400'},
            {'family': 'Barlow', 'file': 'fonts/Barlow-Medium.ttf', 'weight': '500'},
            {'family': 'Barlow', 'file': 'fonts/Barlow-SemiBold.ttf', 'weight': '600'},
            {'family': 'Barlow', 'file': 'fonts/Barlow-Bold.ttf', 'weight': '700'},
            {'family': 'Barlow Condensed', 'file': 'fonts/BarlowCondensed-SemiBold.ttf', 'weight': '600'},
            {'family': 'Barlow Condensed', 'file': 'fonts/BarlowCondensed-Bold.ttf', 'weight': '700'},
            {'family': 'Barlow Condensed', 'file': 'fonts/BarlowCondensed-ExtraBold.ttf', 'weight': '800'},
            {'family': 'JetBrains Mono', 'file': 'fonts/JetBrainsMono-Regular.ttf', 'weight': '400'},
            {'family': 'JetBrains Mono', 'file': 'fonts/JetBrainsMono-Bold.ttf', 'weight': '700'},
        ],
        'families': {
            'display': "'Bebas Neue', 'Oswald', 'Arial Narrow', sans-serif",
            'body': "Barlow, 'Helvetica Neue', Arial, sans-serif",
            'condensed': "'Barlow Condensed', 'Arial Narrow', sans-serif",
            'mono': "'JetBrains Mono', Consolas, monospace",
        },
        'groups': [
            {'name': 'Display', 'family': 'display', 'styles': [
                {'name': 'display-xl', 'fontSize': '120px', 'lineHeight': 0.88, 'fontWeight': 400, 'letterSpacing': '0', 'sample': 'BE YOUR OWN HERO', 'usage': 'Covers and posters. Always uppercase.'},
                {'name': 'headline', 'fontSize': '56px', 'lineHeight': 0.92, 'fontWeight': 400, 'letterSpacing': '0.005em', 'sample': 'BREAK FORMATION.', 'usage': 'Page and slide headlines. Always uppercase.'},
                {'name': 'label-box', 'fontSize': '38px', 'lineHeight': 1, 'fontWeight': 400, 'letterSpacing': '0.02em', 'sample': 'ANTIHERO', 'usage': 'Text set inside label boxes (label-fill / on-label, or ignition / on-ignition).'},
                {'name': 'title', 'fontSize': '26px', 'lineHeight': 0.95, 'fontWeight': 400, 'letterSpacing': '0.02em', 'sample': 'TOOLS OVER TALK', 'usage': 'Card and section titles.'},
            ]},
            {'name': 'Text', 'family': 'body', 'styles': [
                {'name': 'lead', 'fontSize': '20px', 'lineHeight': 1.45, 'fontWeight': 500, 'sample': "Nobody's coming to save you. You never needed saving.", 'usage': 'Intro paragraphs.'},
                {'name': 'body', 'fontSize': '15px', 'lineHeight': 1.5, 'fontWeight': 400, 'sample': 'AI gives one person the reach of a small team, if they learn the tools.', 'usage': 'Running text, 65 characters wide at most.'},
                {'name': 'small', 'fontSize': '12px', 'lineHeight': 1.5, 'fontWeight': 400, 'sample': 'Link in the comments.', 'usage': 'Captions and footnotes, in ink-muted.'},
            ]},
            {'name': 'Labels', 'family': 'condensed', 'styles': [
                {'name': 'eyebrow', 'fontSize': '12px', 'lineHeight': 1.2, 'fontWeight': 700, 'letterSpacing': '0.26em', 'sample': 'AI · BRANDING · SEO', 'usage': 'Eyebrows, descriptors, footers. Uppercase, tracked.'},
            ]},
            {'name': 'Mono', 'family': 'mono', 'styles': [
                {'name': 'prompt', 'fontSize': '14px', 'lineHeight': 1.55, 'fontWeight': 400, 'sample': '> Write 5 posts for my shop in Edmonton.', 'usage': 'AI prompts, tool names, numbers, data.'},
            ]},
        ]},
    'spacing': {'tokens': [
        {'name': 'space-1', 'value': '4px', 'usage': 'Hairline gaps, icon nudges.'},
        {'name': 'space-2', 'value': '8px', 'usage': 'Tight gaps inside components.'},
        {'name': 'space-3', 'value': '12px', 'usage': 'Label box horizontal padding at 38px type.'},
        {'name': 'space-4', 'value': '16px', 'usage': 'Default gap between related items.'},
        {'name': 'space-6', 'value': '24px', 'usage': 'Card padding; flanking-rule gap.'},
        {'name': 'space-8', 'value': '32px', 'usage': 'Gap between groups.'},
        {'name': 'space-12', 'value': '48px', 'usage': 'Section spacing.'},
        {'name': 'space-20', 'value': '80px', 'usage': 'Outer margin of 1080px social posts.'},
    ]},
    'radius': {'tokens': [
        {'name': 'radius-0', 'value': '0px', 'usage': 'Everything: label boxes, cards, buttons, images. The system is square.'},
        {'name': 'radius-disc', 'value': '50%', 'usage': 'The badge and avatars only.'},
    ]},
}


def badge_svg(size=None, cls_disc='disc', cls_mark='mk'):
    s = f' width="{size}" height="{size}"' if size else ''
    return (f'<svg viewBox="0 0 1000 1000"{s} role="img" aria-label="AntiHero"><circle class="{cls_disc}" cx="500" cy="500" r="500"/>'
            f'<path class="{cls_mark}" fill-rule="evenodd" d="{A_PATH}"/><path class="{cls_mark}" fill-rule="evenodd" d="{HERO_PATH}"/></svg>')


def wordmark_svg(height, cls_anti='wa', cls_hero='wh'):
    asc = HERO_UP['ascender']
    fo = FontOutline('bebas')
    size = asc * 0.86 / (fo.cap / fo.upm)
    anti, wdt = text_path('bebas', 'ANTI', size, 0, 0, '#000', tracking=0.01)
    anti = anti.replace('fill="#000"', f'class="{cls_anti}"')
    hero = hero_upright_group('#000', wdt + 40, 0).replace('fill="#000"', f'class="{cls_hero}"')
    tw = wdt + 40 + HERO_UP_W
    top, bot = -asc - 4, 16
    sc = height / asc
    return (f'<svg viewBox="0 {top:.1f} {tw:.1f} {bot - top:.1f}" style="height:{(bot - top) * sc:.1f}px;width:{tw * sc:.1f}px" role="img" aria-label="AntiHero">'
            f'{anti}{hero}</svg>')


BASE = ("html,body{margin:0}body{background:var(--surface);color:var(--ink);font-family:var(--font-body);padding:24px}"
        ".lbl{font-family:var(--font-display);line-height:1;display:inline-block;background:var(--label-fill);color:var(--on-label);"
        "padding:.14em .2em .1em .22em;white-space:nowrap;text-box:trim-both cap alphabetic}"
        ".lbl.red{background:var(--ignition);color:var(--on-ignition)}")

COMPONENTS = {}

COMPONENTS['Logo'] = ('Brand', 230, f"""<style>{BASE}
.row{{display:flex;align-items:center;gap:40px;flex-wrap:wrap}}
.disc{{fill:var(--carbon)}}.mk{{fill:#ffffff}}.wa{{fill:var(--ink)}}.wh{{fill:var(--ignition)}}
.cap{{font-family:var(--font-condensed);font-weight:700;font-size:11px;letter-spacing:.24em;color:var(--ink-muted);margin-top:10px}}</style>
<div class="row"><div>{badge_svg(150)}<div class="cap">BADGE</div></div>
<div>{wordmark_svg(64)}<div class="cap">WORDMARK &middot; ANTI + HERO</div></div></div>""",
"""The AntiHero logo: the circle-A badge where the hand-lettered word *hero* completes the ring, plus the ANTI + hero wordmark.

**Use the files, never redraw.** Place logos from the `Logos` asset group (SVG masters, text already outlined). The lettering is custom; no font matches it.

- **Badge** (`antihero-badge-carbon.svg`): the primary logo. Avatars, stamps, merch, anything where the logo stands alone. `carbon` disc with a `white` mark.
- **On light grounds** use `antihero-badge-black.svg` or keep the carbon badge; over photography use `antihero-badge-outline-white.svg`; for one-colour print, vinyl and laser use the `knockout` files (the letters are real holes).
- **Wordmark** (`antihero-wordmark-white-ignition.svg` on dark, `antihero-wordmark-black-ignition.svg` on light): headers, sign-offs, post footers. On an `ignition` ground use the all-white wordmark.
- **Clear space**: one quarter of the badge diameter on every side. **Minimum**: badge 24px on screen (10mm in print); wordmark 18px tall.

Don't: stretch, rotate the badge to straighten "hero", retype "hero" in a font, add glows or bevels, recolour outside the palette, crop the ring, or put the red wordmark on red.""")

COMPONENTS['LabelStack'] = ('Brand devices', 250, f"""<style>{BASE}
.stack{{display:flex;flex-direction:column;align-items:flex-start}}
.a{{font-size:72px}}.b{{font-size:26px;letter-spacing:.05em}}.c{{font-size:18px;letter-spacing:.16em;padding:.3em .5em .26em .66em}}</style>
<div class="stack"><span class="lbl a">ANTIHERO</span><span class="lbl b">AI &middot; BRANDING &middot; SEO &middot; ENTREPRENEURSHIP</span>
<span class="lbl red c" style="margin-top:16px">BE YOUR OWN HERO</span></div>""",
"""The label stack: Bebas Neue set on solid boxes and stacked flush like a warning label, straight from the original AntiHero channel art.

The consumer provides one to three short uppercase lines (2 to 6 words each).

- Boxes use `label-fill` with `on-label` text, or `ignition` with `on-ignition` for the ONE red box in a layout.
- Type: `label-box` (Bebas Neue). Padding 0.14em top and bottom, 0.2em left and right, trimmed to the cap height.
- Stack boxes flush with no gap and let their widths step (a narrow line over a wider one). Centre stacks on covers; left-align them on posts.
- Pair with FlankingRules for a short tagline under the stack.

Don't: round the corners, add shadows, set lowercase, or use more than one red box.""")

COMPONENTS['FlankingRules'] = ('Brand devices', 110, f"""<style>{BASE}
.t{{display:flex;align-items:center;gap:24px;justify-content:center;padding-top:20px}}
.r{{width:120px;height:2px;background:var(--ink)}}.lbl{{font-size:20px;letter-spacing:.16em;padding:.3em .5em .26em .66em}}</style>
<div class="t"><span class="r"></span><span class="lbl red">BE YOUR OWN HERO</span><span class="r"></span></div>""",
"""Flanking rules: two short hairlines either side of a one-line tagline, carried over from the original channel art.

The consumer provides one short line (the tagline or a date).

- Rules are 2px (3px above 1600px wide) in `ink`, as long as 1.5 to 3 times the line's cap height times 4, with a `space-6` gap.
- The line itself is a label box (usually the ignition box) or plain `eyebrow` text.
- Use once per layout, under a LabelStack or at the foot of a cover.""")

COMPONENTS['PromptLine'] = ('Brand devices', 120, f"""<style>{BASE}
.box{{background:var(--surface-raised);border:1px solid var(--line);padding:18px 22px;font-family:var(--font-mono);font-size:14px;line-height:1.55;max-width:560px}}
.k{{color:var(--ignition);font-weight:700}}.cur{{display:inline-block;width:8px;height:16px;background:var(--ignition);vertical-align:-3px;margin-left:4px}}
.lab{{font-family:var(--font-mono);font-weight:700;font-size:11px;letter-spacing:.08em;color:var(--ignition);margin-bottom:8px}}</style>
<div class="box"><div class="lab">&gt; TRY THIS PROMPT</div>Act as a local SEO strategist. Write 5 Google Business Profile posts for my [business] in [city].<span class="cur"></span></div>""",
"""The prompt line marks anything AI: JetBrains Mono text with a red caret and a block cursor.

The consumer provides the prompt text (real, copy-pasteable prompts only; square-bracket the parts the reader fills in).

- Type: `prompt` in `ink` on `surface-raised`, bordered with `line`; the caret, kicker and cursor in `ignition`.
- Use in AI tool posts, workshop slides, and consulting docs. One prompt box per post.
- Keep prompts under 300 characters on social; longer ones belong in the comments or a document.""")

COMPONENTS['OpenRing'] = ('Brand devices', 220, f"""<style>{BASE}
.wrap{{position:relative;height:180px;overflow:hidden;background:var(--surface-raised)}}
.ring{{position:absolute;right:-110px;top:-40px;width:260px;height:260px;border-radius:50%;border:40px solid var(--ink);border-right-color:transparent;border-top-color:transparent;transform:rotate(45deg)}}
.h{{position:absolute;left:24px;bottom:22px;font-family:var(--font-display);font-size:48px;line-height:.9}}.h em{{font-style:normal;color:var(--ignition)}}</style>
<div class="wrap"><div class="ring"></div><div class="h">WRITE YOUR<br><em>OWN STORY.</em></div></div>""",
"""The open ring: the left half of the badge's ring, used big and cropped off an edge as a framing device.

The consumer provides the layout it sits in (a cover, slide, or poster) and a headline or photo to frame.

- Stroke weight is 0.158 of the ring's radius, like the logo. Colour `ink` (or `white` on photos).
- Crop it off the right or bottom edge; never show a full circle (a full ring reads as a different symbol).
- One ring per layout, behind the content, never touching text.""")

COVER = f"""<!-- @dsCard height=288 -->
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>AntiHero</title>
<style>
html,body{{margin:0;height:100%}}
body{{background:var(--surface);color:var(--ink);font-family:var(--font-body);overflow:hidden}}
.cover{{position:relative;height:288px;overflow:hidden}}
.art{{position:absolute;top:0;left:480px;width:480px;height:288px;overflow:hidden}}
.art svg{{display:block;width:480px;height:288px}}
.slab{{fill:var(--label-fill)}}.red{{fill:var(--ignition)}}.ash{{fill:var(--ash)}}.ringc{{fill:none;stroke:var(--white);stroke-width:24}}
.rule{{fill:var(--ink)}}
.words{{position:absolute;left:var(--space-8);bottom:var(--space-8);max-width:440px}}
.name{{margin:0;font-family:var(--font-display);font-weight:400;font-size:88px;line-height:.92;letter-spacing:.01em;color:var(--ink)}}
.tag{{margin:var(--space-2) 0 0 2px;font-size:14px;line-height:20px;color:var(--ink-muted)}}
</style></head><body>
<div class="cover"><div class="art" aria-hidden="true">
<svg viewBox="0 0 480 288" width="480" height="288">
<!--
  blocks      label-fill slabs 168x48 over 256x32 (the heritage label stack), ignition disc r=152 bleeding off the right edge (badge-ignition), ash 64x16 tag, about 38% of 960x288
  arrangement the original channel-art stack: a narrow slab flush over a wider one, stepped, stacked above flanking rules; one big red disc bleeding off the right
  pattern     arcs, from "the open ring": the white half-ring inside the disc (stroke = 0.158 r), plus two ink hairlines flanking the ash tag
  scales      sides in space-2 multiples; gutters space-4; corners radius-0 (the system is square); disc radius-disc
-->
<circle class="red" cx="440" cy="136" r="152"/>
<path class="ringc" d="M440 23.5 A112.5 112.5 0 0 0 440 248.5"/>
<rect class="slab" x="24" y="72" width="168" height="48"/>
<rect class="slab" x="24" y="120" width="256" height="32"/>
<rect class="rule" x="24" y="190" width="56" height="2"/>
<rect class="ash" x="96" y="183" width="64" height="16"/>
<rect class="rule" x="176" y="190" width="56" height="2"/>
</svg></div>
<div class="words"><h1 class="name">AntiHero</h1><p class="tag">Be your own hero. No capes, just tools.</p></div></div>
</body></html>
"""

README = """AntiHero is an AI and entrepreneurship brand: a free community that teaches AI tools, branding, and SEO, plus hands-on consulting for small businesses. It grew out of the AntiHero fitness and travel channel, and keeps that channel's badge, label boxes, and attitude. The promise in four words: **be your own hero**.

## Content fundamentals

- Sound like the friend who has already done it and tells you the truth over coffee: direct, dry, useful. Plain words, specific numbers, real prompts.
- **No exclamation points.** Oxford comma. Numerals for numbers. "AI" always capitalised. Say *you*, never *users*; say *build*, never *hustle*.
- Headlines, labels, and eyebrows are UPPERCASE (Bebas Neue, Barlow Condensed). Body copy is sentence case.
- No emoji in brand graphics. At most one in a casual post caption.
- Words we use: build, ship, tools, test, learn, own, story, plain, real, crew, receipts. Words we avoid: hustle, grind, passive income, guru, crush it, secret, game-changer, 10x, revolutionary.
- Real copy to reuse:
  - Tagline: **BE YOUR OWN HERO.**
  - AI line: **NO CAPES. JUST TOOLS.**
  - Creed: **NOBODY'S COMING TO SAVE YOU. GOOD.**
  - Community: **WRITE YOUR OWN STORY.**
  - Heritage (personal, travel, lifestyle posts only): **LIFE IS SHORT. MAKE IT MAGICAL.**
  - Descriptor: AI · BRANDING · SEO · ENTREPRENEURSHIP
  - One-liner: AntiHero is an AI and entrepreneurship community for people who would rather build than wait.
- Do: "Here's the exact prompt I used. Steal it." Don't: "Unlock the secret AI hack 99% of people don't know!!!"

## Visual foundations

- **Start dark.** Put layouts on `surface` (Anti Black `void` in the dark theme) with `ink` text; use the light theme (`bone` ground) for quote cards, print, and documents.
- **One red thing.** `ignition` appears once per layout: one word, one label box, one button, or the *hero* in the wordmark. Two red things compete; zero is fine. `ember` is only a pressed or hover state.
- Text on an `ignition` fill is `on-ignition`. `ignition` as text only at 24px and up. Captions use `ink-muted`.
- **Type**: `display-xl` and `headline` (Bebas Neue, uppercase) for headlines; `label-box` inside label boxes; `lead`, `body`, `small` (Barlow) for reading; `eyebrow` (Barlow Condensed, tracked 0.26em) for eyebrows and descriptors; `prompt` (JetBrains Mono) for anything AI, data, or code.
- **The label system** is the signature: see the LabelStack component. Pair it with FlankingRules. Mark AI content with PromptLine.
- **Shape**: everything is square (`radius-0`). Only the badge, avatars, and the open ring are round (`radius-disc`). No drop shadows in layouts; borders are `line` hairlines.
- **Spacing**: `space-*` steps on a 4px base; social posts use a `space-20` outer margin at 1080px.
- **Imagery**: dark, cinematic, real work in low light (hands on keyboards at night, whiteboards, job sites, storefronts, horizons). Treat photos as a duotone from `void` through `dusk` to `bone` with fine grain, then let one red element carry the colour. Skip stock smiles, handshakes, luxury cars, and cash.
- **Backgrounds** (asset group `Backgrounds`): First Light (a red horizon glow, the default), Concrete, Smoke, Grid (AI and tech), Ignition Grain (bold announcements), Bone Paper (light).
- **Textures** (asset group `Textures`): the logo in 15 materials for hero visuals, launch posts, and merch mockups. Never at small sizes or in UI.
- **Focus**: a solid 2px `focus-ring` offset 2px from the control.

## Logo

- Place logos from the `Logos` and `Lockups` asset groups; never redraw them or set *hero* in a font.
- Primary: `antihero-badge-carbon.svg`. On light grounds: `antihero-badge-black.svg`. Over photos: `antihero-badge-outline-white.svg`. One-colour production: `antihero-badge-knockout-*.svg`.
- Wordmark on dark: `antihero-wordmark-white-ignition.svg`; on light: `antihero-wordmark-black-ignition.svg`; on `ignition`: `antihero-wordmark-white.svg`.
- Clear space: one quarter of the badge diameter. Minimum: badge 24px (10mm print), wordmark 18px tall.

## Iconography

AntiHero has no icon set. Meaning is carried by type (label boxes, eyebrows) and three devices: the prompt caret `>` with a block cursor, the flanking rules, and the open ring. If an interface needs icons, use a thin-stroke outline set at 1.5px in `ink`, square caps, never filled or multicolour, and keep `ignition` off icons.

## Formats

- Facebook page cover 1640 x 924 (all text inside the centre 1100 x 560); group cover 1640 x 856; profile picture 2048 x 2048 with the disc colour filling the square.
- Feed posts 1080 x 1350; stories 1080 x 1920; YouTube banner 2560 x 1440 (text inside 1546 x 423); LinkedIn 1584 x 396; X header 1500 x 500.
"""

VOICE_MD = """# Launch copy

Paste-ready text for the Facebook page and group.

**Page intro (98 characters, limit 101)**

AI tools, branding, SEO, and real-world entrepreneurship. No capes. Just tools. Be your own hero.

**Group description**

Welcome to AntiHero. This is a group for people who would rather build than wait: solo founders, side-hustlers, trades, creators, and small-business owners.

Every week: one AI tool broken down with real prompts, a live workshop, and a thread where you share what you are building. No gurus, no pitches, no hype. Just tools, straight talk, and a crew that helps.

Be your own hero.

**Group rules**

1. **Give before you ask.** Share something that worked before you ask for help.
2. **No guru pitches.** No MLMs, course funnels, or cold DMs. Instant removal.
3. **Show your work.** Real prompts, real screenshots, real numbers.
4. **Be straight, not cruel.** Honest feedback is the point. Dunking on beginners is not.
5. **Build in public.** Post progress and mistakes, not only wins.

**Membership questions**

1. What are you building, or want to build?
2. Which AI tools do you use today, if any?
3. Do you agree to the group rules? (Yes / No)

**Boilerplate**

AntiHero teaches everyday entrepreneurs to use AI tools, build a brand, and get found online. The free AntiHero group runs weekly tool breakdowns, live workshops, and build-in-public threads. AntiHero Consulting helps businesses with branding, SEO, and AI systems, done with them rather than to them. Be your own hero.
"""

POSITIONING_MD = """# Positioning

**Mission.** Give ordinary people the tools, the skills, and the nerve to build on their own terms.

**What AntiHero does.** The AntiHero group: a free Facebook community with weekly AI tool breakdowns, live workshops, prompt swaps, and build-in-public threads. AntiHero Consulting: hands-on branding, SEO and Google Business Profile, AI systems and automations, and getting the basics set up properly.

**Who it is for.** Solo founders, side-hustlers, tradespeople going out on their own, creators, and small-business owners who are tired of paying for hype. Beginner-friendly. Allergic to gurus.

**The anti-hero idea.** Heroes wait for the call; anti-heroes answer their own. Nobody here is coming to save you, and that is the good news. You are the main character; the group is the crew; AI is the new gear. The badge says it without words: half the circle is missing, and the word *hero* completes it.

**Pillars.**

| Pillar | What it means |
| --- | --- |
| Own your story | Agency over everything. Every post ends with something the reader can do today. |
| Tools over talk | Show the prompt, the workflow, and the result. Practical beats inspirational. |
| Straight talk | No hype, no fake screenshots, no overnight promises. If something is hard or slow, say so. |
| Build in public | Share the work, the numbers, and the mistakes. The group learns faster that way. |
"""

GROUP_READMES = {
    'Logos': 'The AntiHero logo masters (SVG, text outlined). Badges: carbon is primary, black for light grounds, outline-white over photos, knockout (letters are holes) for one-colour print, vinyl, and laser. Marks drop the disc. Wordmarks: ANTI + hero; white-ignition on dark, black-ignition on light, all-white on ignition. Every file is fixed-colour: pick the file whose name matches the ground.',
    'Lockups': 'Badge + wordmark lockups (horizontal for headers and footers, stacked for posters and title slides), the BE YOUR OWN HERO tagline bar, and square app icons. Fixed-colour SVGs: on-dark files for dark grounds, on-light for light.',
    'Backgrounds': 'Brand backgrounds (preview size; the 4K and phone originals live in the brand kit folder 04_Backgrounds). First Light is the default cover backdrop; Grid signals AI and tech; Ignition Grain is for bold announcements; Bone Paper for light layouts.',
    'Textures': 'The logo rendered in 15 materials (preview size; 2400px originals in the brand kit). For hero visuals, launch posts, merch mockups, and slide openers only.',
    'Social': 'Finished social examples: the three Facebook cover concepts, the profile picture as Facebook crops it, and the post and story templates. Use them as the reference for layout: one label stack, one red idea, the wordmark footer.',
}

UPLOADS = {
    'Logos': sorted(glob.glob(os.path.join(KIT, '02_Logos', '01_Badge', '*.svg'))) + sorted(glob.glob(os.path.join(KIT, '02_Logos', '02_Mark', '*.svg'))) +
             sorted(glob.glob(os.path.join(KIT, '02_Logos', '03_Wordmark', '*.svg'))),
    'Lockups': sorted(glob.glob(os.path.join(KIT, '02_Logos', '04_Lockups', '*.svg'))) + sorted(glob.glob(os.path.join(KIT, '02_Logos', '05_Icons', '*.svg'))),
    'Backgrounds': sorted(glob.glob(os.path.join(KIT, '01_Brand-Bible', 'assets', 'bg-*.jpg'))),
    'Textures': sorted(glob.glob(os.path.join(KIT, '01_Brand-Bible', 'assets', 'tex-*.jpg'))),
    'Social': [os.path.join(KIT, '01_Brand-Bible', 'assets', f) for f in
               ['fb-cover-label.jpg', 'fb-cover-manifesto.jpg', 'fb-cover-signal.jpg', 'fb-profile-preview.jpg', 'post-01.jpg', 'post-02.jpg',
                'post-03.jpg', 'post-04.jpg', 'post-05.jpg', 'post-06.jpg', 'story-01.jpg']],
}
NICE = {'fb-cover-label.jpg': 'facebook-cover-label.jpg', 'fb-cover-manifesto.jpg': 'facebook-cover-manifesto.jpg',
        'fb-cover-signal.jpg': 'facebook-cover-signal.jpg', 'fb-profile-preview.jpg': 'facebook-profile-crop.jpg',
        'post-01.jpg': 'post-welcome.jpg', 'post-02.jpg': 'post-quote.jpg', 'post-03.jpg': 'post-ai-tool.jpg', 'post-04.jpg': 'post-workshop.jpg',
        'post-05.jpg': 'post-seo-tip.jpg', 'post-06.jpg': 'post-now-open.jpg', 'story-01.jpg': 'story-join.jpg'}


def stage(d):
    P = os.path.join(d, 'project')
    if os.path.isdir(P):
        shutil.rmtree(P)
    w(d, 'project/tokens.json', json.dumps(TOKENS, indent=1, ensure_ascii=False))
    w(d, 'project/README.md', README)
    w(d, 'project/guidelines/10-positioning.md', POSITIONING_MD)
    w(d, 'project/guidelines/20-launch-copy.md', VOICE_MD)
    for name, (group, height, html, guide) in COMPONENTS.items():
        w(d, f'project/components/{name}/preview.html',
          f'<!-- @dsCard group="{group}" height={height} -->\n<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{name}</title></head><body>\n{html}\n</body></html>\n')
        w(d, f'project/components/{name}/README.md', f'# {name}\n\n{guide}\n')
    w(d, 'project/components/Cover/preview.html', COVER)
    for g, txt in GROUP_READMES.items():
        w(d, f'project/assets/{g}/README.md', f'# {g}\n\n{txt}\n')
    fdir = os.path.join(P, 'fonts')
    os.makedirs(fdir, exist_ok=True)
    for src, dst in [('bebasneue__BebasNeue-Regular.ttf', 'BebasNeue-Regular.ttf'), ('barlow__Barlow-Regular.ttf', 'Barlow-Regular.ttf'),
                     ('barlow__Barlow-Medium.ttf', 'Barlow-Medium.ttf'), ('barlow__Barlow-SemiBold.ttf', 'Barlow-SemiBold.ttf'),
                     ('barlow__Barlow-Bold.ttf', 'Barlow-Bold.ttf'), ('barlowcondensed__BarlowCondensed-SemiBold.ttf', 'BarlowCondensed-SemiBold.ttf'),
                     ('barlowcondensed__BarlowCondensed-Bold.ttf', 'BarlowCondensed-Bold.ttf'),
                     ('barlowcondensed__BarlowCondensed-ExtraBold.ttf', 'BarlowCondensed-ExtraBold.ttf'),
                     ('JetBrainsMono-Regular.ttf', 'JetBrainsMono-Regular.ttf'), ('JetBrainsMono-Bold.ttf', 'JetBrainsMono-Bold.ttf')]:
        shutil.copy2(os.path.join(FONTS, src), os.path.join(fdir, dst))
    # upload staging copies with their final names
    U = os.path.join(d, 'upload')
    if os.path.isdir(U):
        shutil.rmtree(U)
    plan = {}
    for g, files in UPLOADS.items():
        os.makedirs(os.path.join(U, g), exist_ok=True)
        for f in files:
            base = os.path.basename(f)
            name = NICE.get(base, base)
            if g in ('Backgrounds', 'Textures'):
                name = 'antihero-' + base.replace('bg-', 'background-').replace('tex-', 'texture-')
            dst = os.path.join(U, g, name)
            shutil.copy2(f, dst)
            plan.setdefault(g, []).append(dst)
    with open(os.path.join(d, 'upload_plan.json'), 'w') as f:
        json.dump(plan, f, indent=1)
    files = []
    for root, _, fs in os.walk(P):
        for fn in fs:
            files.append(os.path.relpath(os.path.join(root, fn), d).replace(os.sep, '/'))
    print(json.dumps({'project_files': sorted(files), 'uploads': {g: len(v) for g, v in plan.items()}}, indent=1))


def index(d, ids_path):
    ids = json.load(open(ids_path))          # {"<abs upload path>": {"id": "...", ...}}
    plan = json.load(open(os.path.join(d, 'upload_plan.json')))
    tiles = {'Logos': 'm', 'Lockups': 'l', 'Backgrounds': 'l', 'Textures': 'm', 'Social': 'm'}
    groups = ['Logos', 'Lockups', 'Social', 'Backgrounds', 'Textures']
    ag = {}
    for g in groups:
        files, order = {}, []
        for p in plan[g]:
            name = os.path.basename(p)
            rec = {'id': ids[name]}
            ext = name.rsplit('.', 1)[-1].lower()
            files[name] = {'name': name, 'blob': rec['id'], 'size': os.path.getsize(p),
                           'type': {'svg': 'image/svg+xml', 'jpg': 'image/jpeg', 'png': 'image/png'}[ext]}
            order.append(name)
        ag[g] = {'name': g, 'tile': tiles[g], 'order': order, 'files': files}
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    idx = {'v': 3, 'layout': 'files', 'createdOnFiles': {'v': 1, 'at': now}, 'title': TITLE, 'namespace': NS, 'libraries': [],
           'sections': {}, 'groups': groups, 'assetGroups': ag, 'blobs': {}, 'docs': {'readme': 'project/README.md', 'sections': []},
           'lastChange': {'by': 'Matt', 'at': now, 'via': 'Claude Code', 'note': 'Created the AntiHero design system from the v1.0 brand kit'}}
    w(d, 'project/design-system.json', json.dumps(idx, indent=1))
    print('index written with', sum(len(v['files']) for v in ag.values()), 'asset records')


if __name__ == '__main__':
    if sys.argv[1] == 'stage':
        stage(sys.argv[2])
    else:
        index(sys.argv[2], sys.argv[3])
