"""00_START-HERE.html (visual index of the kit) + README.txt."""
import glob
import os

from brand import C, KIT, mark_group

FONT = '06_Fonts'


def rel(p):
    return os.path.relpath(p, KIT).replace(os.sep, '/')


def thumbs(pattern, n=None, h=120, bg='#1D2124'):
    fs = sorted(glob.glob(os.path.join(KIT, pattern)))
    if n:
        fs = fs[:n]
    return ''.join(f'<a class="th" href="{rel(f)}" title="{os.path.basename(f)}" style="background:{bg}"><img loading="lazy" src="{rel(f)}" style="height:{h}px"></a>' for f in fs)


badge = f'<svg viewBox="0 0 1000 1000" width="120" height="120"><circle cx="500" cy="500" r="500" fill="{C["carbon"]}"/>{mark_group("#fff")}</svg>'

html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AntiHero Brand Kit</title><style>
@font-face{{font-family:'Bebas Neue';src:url('{FONT}/Bebas Neue (display)/BebasNeue-Regular.ttf')}}
@font-face{{font-family:'Barlow';src:url('{FONT}/Barlow (body)/Barlow-Regular.ttf')}}
@font-face{{font-family:'Barlow';font-weight:700;src:url('{FONT}/Barlow (body)/Barlow-Bold.ttf')}}
@font-face{{font-family:'Barlow Condensed';font-weight:700;src:url('{FONT}/Barlow Condensed (labels)/BarlowCondensed-Bold.ttf')}}
@font-face{{font-family:'JetBrains Mono';src:url('{FONT}/JetBrains Mono (prompts + data)/JetBrainsMono-Regular.ttf')}}
:root{{--void:{C['void']};--carbon:{C['carbon']};--red:{C['ignition']};--ash:{C['ash']};--bone:{C['bone']}}}
*{{box-sizing:border-box;margin:0}}body{{background:var(--void);color:#fff;font-family:'Barlow',sans-serif;padding:48px 20px 80px}}
.wrap{{max-width:1180px;margin:0 auto}}
.lbl{{font-family:'Bebas Neue';display:inline-block;background:#fff;color:var(--void);line-height:1;padding:.12em .2em .08em;text-box:trim-both cap alphabetic}}
.r{{background:var(--red);color:#fff}}
h2{{font-family:'Bebas Neue';font-weight:400;font-size:44px;letter-spacing:.01em;margin:54px 0 6px}}h2 em{{font-style:normal;color:var(--red)}}
p{{color:#cfd2d5;max-width:70ch;line-height:1.5}}
.eyebrow{{font-family:'Barlow Condensed';font-weight:700;letter-spacing:.26em;font-size:13px;color:var(--red)}}
.row{{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}}
.th{{display:grid;place-items:center;padding:10px;border:1px solid rgba(255,255,255,.1);text-decoration:none}}
.th:hover{{outline:2px solid var(--red)}}
.th img{{display:block;max-width:100%;width:auto}}
.fb{{display:grid;grid-template-columns:1.6fr 1fr;gap:20px;margin-top:18px}}
.fb a{{display:block}}.fb img{{width:100%;display:block;border:1px solid rgba(255,255,255,.12)}}
.mono{{font-family:'JetBrains Mono',monospace;font-size:13px;color:#e6e6e6}}
.steps li{{margin:6px 0;color:#cfd2d5}}
a{{color:#fff}}
@media (max-width:700px){{.fb{{grid-template-columns:1fr}}}}
</style></head><body><div class="wrap">
<div style="display:flex;gap:28px;align-items:center;flex-wrap:wrap">{badge}<div><div class="eyebrow">BRAND KIT &middot; V2.0 &middot; SEPTEMBER 2026</div>
<div style="margin-top:12px"><span class="lbl" style="font-size:72px">ANTIHERO</span></div>
<div><span class="lbl" style="font-size:24px;letter-spacing:.05em">AI &middot; BRANDING &middot; SEO &middot; ENTREPRENEURSHIP</span></div></div></div>
<p style="margin-top:26px">Everything for the AntiHero rebrand in one folder. The <a href="01_Brand-Bible/AntiHero-Brand-Bible.pdf">Brand Bible (PDF)</a> explains the rules; the folders below hold the files. Click any thumbnail to open it full size.</p>

<h2>FACEBOOK: <em>DO THIS FIRST</em></h2>
<div class="fb"><a href="05_Social/Facebook/Page-Cover/antihero-fb-page-cover-rise_1640x924.png"><img src="05_Social/Facebook/Page-Cover/antihero-fb-page-cover-rise_1640x924.png"></a>
<a href="05_Social/Facebook/Profile-Picture/antihero-fb-profile-carbon_2048px.png"><img src="05_Social/Facebook/Profile-Picture/_preview-circle-crop.png"></a></div>
<ol class="steps" style="margin:14px 0 0 20px"><li>Profile picture: <span class="mono">05_Social/Facebook/Profile-Picture/antihero-fb-profile-carbon_2048px.png</span></li>
<li>Page cover: <span class="mono">05_Social/Facebook/Page-Cover/antihero-fb-page-cover-rise_1640x924.png</span></li>
<li>Starting the group: open the <a href="05_Social/Facebook/Group-Kit/AntiHero-Facebook-Group-Kit.pdf">Group Kit playbook (PDF)</a>. Setup, house rules, the weekly rhythm, and the first ten posts, with paste-ready text in <span class="mono">Group-Kit/antihero-group-copy.txt</span>.</li>
<li>Page intro: page 14 of the Brand Bible (copy and paste).</li></ol>
<div class="row">{thumbs('05_Social/Facebook/Page-Cover/*.png', h=90)}{thumbs('05_Social/Facebook/Group-Cover/*.png', h=90)}{thumbs('05_Social/Facebook/Event-Cover/*.png', h=90)}</div>

<h2>FACEBOOK <em>GROUP KIT</em></h2><p>Group cover, Start Here, Welcome, and House Rules posts, six weekly series cards (Monday tools through Saturday build day), a member spotlight, a poll, and a live-workshop event cover. The playbook says when to post each one.</p>
<div class="row">{thumbs('05_Social/Facebook/Group-Kit/01_Cover/*.png', h=120)}{thumbs('05_Social/Facebook/Group-Kit/05_Event/*.png', h=120)}{thumbs('05_Social/Facebook/Group-Kit/02_Pinned/*.png', h=200)}</div>
<div class="row">{''.join(thumbs(f'05_Social/Facebook/Group-Kit/03_Weekly-Series/antihero-series-{d}-*.png', h=200) for d in ('mon', 'tue', 'wed', 'thu', 'fri', 'sat'))}{thumbs('05_Social/Facebook/Group-Kit/04_Templates/*.png', h=200)}</div>

<h2>LOGOS <em>(02_Logos)</em></h2><p>SVG files are the masters (they scale to any size and open in Canva, Illustrator, Figma, and sign-shop software). PNGs go up to 8192 px.</p>
<div class="row">{thumbs('02_Logos/01_Badge/*_512px.png', h=96, bg='#3a3e43')}</div>
<div class="row">{thumbs('02_Logos/02_Mark/*_512px.png', h=96, bg='#3a3e43')}</div>
<div class="row">{thumbs('02_Logos/03_Wordmark/*_1024px.png', h=60, bg='#3a3e43')}</div>
<div class="row">{thumbs('02_Logos/04_Lockups/*_1024px.png', h=70, bg='#3a3e43')}{thumbs('02_Logos/04_Lockups/*_1500px.png', h=70, bg='#3a3e43')}</div>
<div class="row">{thumbs('02_Logos/05_Icons/*_512px.png', h=80, bg='#3a3e43')}{thumbs('02_Logos/06_Construction/*.png', h=160)}</div>
<h2>THE <em>FAMILY</em></h2><p>AntiHero teaches it. KR8TIV designs it. KR8TIV AI automates it. Lockups for about slides, plus optional footer endorsements for kr8tiv.io and kr8tiv.ai.</p>
<div class="row">{thumbs('02_Logos/07_Family/*on-dark*.png', h=70, bg='#1D2124')}</div>

<h2>TEXTURES + <em>BACKGROUNDS</em></h2><p>The logo in 15 materials, the logo on every brand background (square, 4K wallpaper, phone), and the backgrounds on their own: five original 3D skies (Rise Above, First Light, Launch, Break Formation, See Further) plus Daybreak, Concrete, and Bone Paper. The old dark set is archived in <span class="mono">04_Backgrounds/_previous-dark-set</span>.</p>
<div class="row">{thumbs('03_Logo-Textures/*.jpg', h=150)}</div>
<div class="row">{thumbs('03_Logo-Textures/On-Backgrounds/*square*.jpg', h=120)}{thumbs('03_Logo-Textures/On-Backgrounds/*wallpaper*.jpg', h=120)}</div>
<div class="row">{thumbs('04_Backgrounds/*desktop*.jpg', h=100)}</div>

<h2>SOCIAL <em>TEMPLATES</em></h2>
<div class="row">{thumbs('05_Social/Posts/*.png', h=200)}</div>
<div class="row">{thumbs('05_Social/YouTube/*.png', h=90)}{thumbs('05_Social/LinkedIn/*.png', h=70)}{thumbs('05_Social/X-Twitter/*.png', h=70)}{thumbs('05_Social/Video-Call/*.png', h=90)}{thumbs('05_Social/Email/*.png', h=50)}{thumbs('05_Social/Web/*.png', h=90)}</div>

<h2>COLOR + <em>TYPE</em></h2>
<div class="row">{thumbs('07_Color/*.png', h=200)}{thumbs('06_Fonts/*.png', h=200)}</div>
<p style="margin-top:14px">Install the fonts from <span class="mono">06_Fonts</span> (right-click a .ttf &rarr; Install). Colors for design apps: <span class="mono">07_Color/antihero-palette.ase</span>. For the web: <span class="mono">antihero-palette.css</span>.</p>
<p style="margin-top:40px;font-family:'JetBrains Mono';font-size:12px;color:var(--ash)">Regenerate anything with the scripts in _build (see README.txt). Be your own hero.</p>
</div></body></html>"""

with open(os.path.join(KIT, '00_START-HERE.html'), 'w', encoding='utf-8') as f:
    f.write(html)

import fitz
PAGES = fitz.open(os.path.join(KIT, "01_Brand-Bible", "AntiHero-Brand-Bible.pdf")).page_count
readme = f"""ANTIHERO BRAND KIT - v2.0 - September 2026
===========================================

Open 00_START-HERE.html in a browser for a visual index of everything.
The rules live in 01_Brand-Bible/AntiHero-Brand-Bible.pdf ({PAGES} pages).

FACEBOOK, RIGHT NOW
  Profile picture : 05_Social/Facebook/Profile-Picture/antihero-fb-profile-carbon_2048px.png
  Page cover      : 05_Social/Facebook/Page-Cover/antihero-fb-page-cover-rise_1640x924.png
  Group           : 05_Social/Facebook/Group-Kit/AntiHero-Facebook-Group-Kit.pdf (setup, rules, weekly
                    rhythm, first ten posts) + antihero-group-copy.txt (all of the text, ready to paste)
  Group cover     : 05_Social/Facebook/Group-Kit/01_Cover/antihero-group-cover-write-your-story_1640x856.png
  Page intro      : Brand Bible page 14
  Safe zones      : every cover keeps its text in the centre 1100 x 560 px, so desktop and mobile
                    crops and the profile-picture overlap never cut it. See _safe-zone-guides.

WHAT'S INSIDE
  01_Brand-Bible     PDF + HTML brand bible (story, positioning, voice, logo, color, type, imagery, applications)
  02_Logos           badge (11 colorways), mark, wordmarks, lockups, icons + favicon.ico, construction drawings,
                     07_Family: AntiHero + KR8TIV + KR8TIV AI lockups and footer endorsements
                     SVG = master (text already outlined). PNG up to 8192 px.
  03_Logo-Textures   15 material studies + the logo on every background (square / 4K / phone)
  04_Backgrounds     original 3D skies: Rise Above, First Light, Launch, Break Formation, See Further
                     + Daybreak, Concrete, Bone Paper (4K + phone). Old dark set in _previous-dark-set
  05_Social          Facebook (page/group/event covers, profile pictures), 9 post templates + 1 story,
                     Facebook/Group-Kit (13 group graphics + playbook PDF + paste-ready copy),
                     YouTube, LinkedIn, X, Zoom backgrounds, email signature, web share image
  06_Fonts           Bebas Neue, Barlow, Barlow Condensed, JetBrains Mono + licenses (all SIL OFL, free for commercial use)
  07_Color           .ase (Adobe/Affinity), .css, .json tokens, .gpl, palette card, palette.txt (RGB/CMYK/Pantone)
  _build             the Python scripts that generated all of it

THE SYSTEM IN ONE BREATH
  Open sky, dark type, one red (Ignition Red #E0261E). Black Bebas Neue label boxes over bright,
  first-light imagery. The circle-A badge where the word "hero" completes the ring.
  Tagline: BE YOUR OWN HERO. Voice: straight talk, no hype, no exclamation points, fun.
  Family: AntiHero teaches it, KR8TIV designs it, KR8TIV AI automates it (give first, ask rarely).

DECISIONS WORTH A SECOND LOOK
  - Accent red #E0261E (Pantone 485 C nearest). Chosen to carry the old kit's "blood red" direction
    and to pass WCAG AA with white text on it (4.7:1).
  - Descriptor "AI - BRANDING - SEO - ENTREPRENEURSHIP" and supporting lines ("Nobody's coming to save
    you. You never needed saving.", "Hate your job? Good. That's your runway.", "Write your own story.")
    are proposals: change them in _build/social_v2.py, group_kit.py, and bible.py.
  - Business card uses [email] [phone] [website] placeholders until the domain is settled.
  - Pantone values are nearest matches: confirm against a physical swatch book before printing.

REGENERATE (Python 3.12 + Playwright/Chromium, numpy, opencv, Pillow, fontTools)
  cd _build
  python vectorize.py        # rebuild the master paths from the source screenshot
  python logos.py            # all logo SVG/PNG
  python backgrounds.py      # procedural grounds (Daybreak, Concrete, Bone Paper)
  cd scenes && python heightmaps.py && python batch_final.py && cd ..   # Blender 5.2 skies (GPU, ~1 h)
  python backgrounds_v2.py   # promote the renders to 4K / phone backgrounds
  python family.py           # KR8TIV family lockups
  python logo_textures.py    # 15 material studies
  python logo_scenes.py      # logo on every background
  python social_v2.py        # Facebook + posts + platforms (editable HTML in _build/templates)
  python group_kit.py        # Facebook Group Kit: group graphics, playbook PDF, paste-ready copy
  python brand_files.py      # colors, fonts, construction drawings
  python bible_assets.py && python bible.py    # Brand Bible HTML + PDF
  python start_here.py       # this index
"""
with open(os.path.join(KIT, 'README.txt'), 'w', encoding='utf-8') as f:
    f.write(readme)
print('ok')
