ANTIHERO BRAND KIT - v2.0 - September 2026
===========================================

Open 00_START-HERE.html in a browser for a visual index of everything.
The rules live in 01_Brand-Bible/AntiHero-Brand-Bible.pdf (42 pages).

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
