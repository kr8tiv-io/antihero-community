"""Design System v2 revision: open-sky imagery, the KR8TIV family, image cover, Open Ring retired.

python design_system_v2.py stage <dir>                       -> writes changed project files + upload copies + upload_plan_v2.json
python design_system_v2.py index <dir> <fresh_index.json> <ids.json>  -> merges new asset records into the freshly read index
"""
import base64
import datetime
import glob
import io
import json
import os
import shutil
import sys

from PIL import Image

from brand import C, KIT

TITLE = 'AntiHero'

README = """AntiHero is an AI and entrepreneurship brand: a free community that teaches AI tools, branding, and SEO, plus 1:1 consulting. Its sister studios, KR8TIV (design) and KR8TIV AI (automation), take on done-for-you work. The promise in four words: **be your own hero**.

## Content fundamentals

- Sound like the friend who has already done it and tells you the truth over coffee: direct, dry, useful, and fun. Plain words, specific numbers, real prompts.
- **No exclamation points.** Oxford comma. Numerals for numbers. "AI" always capitalised. Say *you*, never *users*; say *build*, never *hustle*.
- Headlines, labels, and eyebrows are UPPERCASE (Bebas Neue, Barlow Condensed). Body copy is sentence case.
- No emoji in brand graphics. At most one in a casual post caption.
- Big numbers need receipts: "I wrote 40 product descriptions before lunch" beats any multiplier.
- Words we use: build, ship, tools, test, learn, own, story, plain, real, crew, receipts. Words we avoid: hustle, passive income, guru, crush it, secret, game-changer, revolutionary.
- Lines to reuse:
  - Tagline: **BE YOUR OWN HERO.**
  - Creed: **NOBODY'S COMING TO SAVE YOU. YOU NEVER NEEDED SAVING.**
  - Surprise them: **THEY DIDN'T SEE YOU COMING.**
  - The way out: **HATE YOUR JOB? GOOD. THAT'S YOUR RUNWAY.**
  - Do it your way: **BREAK FORMATION.**
  - Tech is your friend: **AI LEVELED THE FIELD. NOW PLAY.**
  - Community: **WRITE YOUR OWN STORY.** Also: BUILD MORE. GRIND LESS. / REMEMBER WHERE YOU CAME FROM. THEN GO FURTHER.
  - Heritage (personal, travel, lifestyle posts only): LIFE IS SHORT. MAKE IT MAGICAL.
  - Descriptor: AI · BRANDING · SEO · ENTREPRENEURSHIP
  - One-liner: AntiHero is an AI and entrepreneurship community for people who would rather build than wait.

## Visual foundations

- **Open sky, dark type.** Put headlines on bright, inspiring imagery (the `Backgrounds` asset group) as black label boxes (`label-fill` / `on-label` in the light theme: black box, white text). Over dark grounds, the boxes flip to white. Paragraphs over photos sit on a dark panel (`void` at 80%).
- **One red thing.** `ignition` appears once per layout: one word, one label box, one button, or the *hero* in the wordmark. If the picture already carries red (the balloon, the red paper plane), one red tag may echo it; nothing else goes red. Never a full-page red wash. `ember` is only a pressed or hover state.
- Text on an `ignition` fill is `on-ignition`. `ignition` as text only at 24px and up. Captions use `ink-muted`.
- **Type**: `display-xl` and `headline` (Bebas Neue, uppercase) for headlines; `label-box` inside label boxes; `lead`, `body`, `small` (Barlow) for reading; `eyebrow` (Barlow Condensed, tracked 0.26em) for eyebrows and descriptors; `prompt` (JetBrains Mono) for anything AI, data, or code.
- **The label system** is the signature: see LabelStack. Pair it with FlankingRules. Mark AI content with PromptLine. Keep stacks clear of the picture's subject; left-align on covers and posts.
- **Shape**: everything is square (`radius-0`). Only the badge and avatars are round (`radius-disc`). No drop shadows in layouts.
- **Spacing**: `space-*` steps on a 4px base; social posts use a `space-20` outer margin at 1080px, with a dark wordmark bar along the bottom.
- **Imagery**: morning light and altitude. Rise Above (a red-and-white balloon over a sea of clouds), First Light (clean sunrise above the clouds), Launch (a paper plane), Break Formation (a flock of white planes, one red plane leaving), See Further (a drone: technology as a friend), Daybreak (soft sky for text-heavy layouts). All are original 3D renders made for AntiHero, not stock and not AI-generated. Skip dark "hacker" tech, glowing circuit brains, robots, stock smiles, supercars, and cash.
- **Textures** (asset group `Textures`): the logo in 15 materials for hero visuals, launches, and merch mockups. Never at small sizes or in UI.
- **Focus**: a solid 2px `focus-ring` offset 2px from the control.

## Logo

- Place logos from the `Logos` and `Lockups` asset groups; never redraw them or set *hero* in a font.
- Primary: `antihero-badge-carbon.svg`. On light grounds: `antihero-badge-black.svg`. Over photos: `antihero-badge-outline-white.svg`. One-colour production: `antihero-badge-knockout-*.svg`.
- Wordmark on dark: `antihero-wordmark-white-ignition.svg`; on light and bright skies: `antihero-wordmark-black-ignition.svg`; on `ignition`: `antihero-wordmark-white.svg`.
- Clear space: one quarter of the badge diameter. Minimum: badge 24px (10mm print), wordmark 18px tall.

## The family

AntiHero teaches it, KR8TIV designs it, KR8TIV AI automates it. Use the `Family` asset group for about slides and footers. Inside AntiHero layouts the sister logos are single-colour (white or black), never in their own accents. Give first: about nine posts of pure value for every post that points to the studios. See the family guideline section.

## Iconography

AntiHero has no icon set. Meaning is carried by type (label boxes, eyebrows) and two devices: the prompt caret `>` with a block cursor, and the flanking rules. If an interface needs icons, use a thin-stroke outline set at 1.5px in `ink`, square caps, never filled or multicolour, and keep `ignition` off icons.

## Formats

- Facebook page cover 1640 x 924 (all text inside the centre 1100 x 560); group cover 1640 x 856; profile picture 2048 x 2048 with the disc colour filling the square.
- Facebook group: one series card per day, same card every week (Mon AI tool of the week, Tue prompt swap, Wed live workshop, Thu get found, Fri wins and builds, Sat build day). The card stays fixed; the caption changes. Text and rules: the launch-copy guideline.
- Feed posts 1080 x 1350; stories 1080 x 1920; YouTube banner 2560 x 1440 (text inside 1546 x 423); LinkedIn 1584 x 396; X header 1500 x 500.
"""

FAMILY_MD = """# The family

**AntiHero teaches it. KR8TIV designs it. KR8TIV AI automates it.** One founder, three ways in.

| Brand | Role | What | Look |
| --- | --- | --- | --- |
| AntiHero | Learn it | The free community and school: AI tools, branding, SEO, entrepreneurship. Group, lives, workshops, 1:1 consulting. | Bebas Neue; black, white, one Ignition Red |
| KR8TIV (kr8tiv.io) | Design it | Cyber-renaissance design atelier: brand identity, websites, motion, video, AI solutions. Founder on every project. | Instrument Serif; dark ground, prism accents (#FF6AD5, #8E00FF, #FF2D4A, #FFD166) |
| KR8TIV AI (kr8tiv.ai) | Automate it | AI back-office systems: receipts, quoting, dispatch, morning digests, watchdog agents. Products: JARVIS, KIN. | Syne; deep navy #050510, one amber #D4A853 |

**The give-first ladder:** free posts, then the group (the product), then live workshops, then 1:1 consulting, then done-for-you work with KR8TIV or KR8TIV AI.

**Rules**

1. The community is the product. AntiHero gives real value away until people ask how to work with you.
2. Nine to one: about nine posts of pure value for every post that points to the studios. The ask is an invitation or a case study, never a pitch in someone's DMs.
3. Teach with real work: a build story is a lesson first and a case study second.
4. Inside AntiHero layouts, sister logos appear single-colour (white or black), so the one-red rule holds.
5. Each brand keeps its own look on its own site. Optional: the studios point back with the "Part of the AntiHero family" footer endorsement.
6. One founder voice: Matt signs the posts.
"""

GROUP_READMES = {
    'Backgrounds': 'Original 3D renders made for AntiHero (Blender, physically based sky and volumetric clouds), plus Daybreak, Concrete, and Bone Paper. Preview size here; 4K and phone originals are in the brand kit folder 04_Backgrounds. Rise Above is the default cover backdrop; First Light and Daybreak take text best. Rise Above and Break Formation carry their own red element: one red tag may echo it, nothing else goes red.',
    'Social': 'Finished social examples: the four Facebook cover concepts (Rise Above recommended), the profile picture as Facebook crops it, ten post and story templates, and Facebook Group Kit cards (group cover, Start Here, House Rules, four of the six weekly series cards, and a poll). Layout recipe: a bright scene, one black label stack, one red idea, and the dark wordmark bar.',
    'Family': 'AntiHero + KR8TIV + KR8TIV AI lockups (on-dark files are white ink; on-light files are black ink) and the optional footer endorsements for kr8tiv.io and kr8tiv.ai. Always single-colour inside AntiHero layouts.',
}


def cover_html(img_b64):
    return f"""<!-- @dsCard height=288 -->
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>AntiHero</title>
<style>
html,body{{margin:0;height:100%}}
body{{background:var(--surface);color:var(--ink);font-family:var(--font-body);overflow:hidden}}
.cover{{position:relative;height:288px;overflow:hidden;background:url(data:image/jpeg;base64,{img_b64}) center/cover}}
.words{{position:absolute;left:var(--space-8);bottom:var(--space-8);max-width:440px}}
.name{{margin:0;display:inline-block;font-family:var(--font-display);font-weight:400;font-size:84px;line-height:1;letter-spacing:.01em;
background:#0a0a0b;color:#ffffff;padding:10px 14px 6px 16px;text-box:trim-both cap alphabetic}}
.tag{{display:inline-block;margin:0;font-family:var(--font-display);font-size:18px;letter-spacing:.16em;line-height:1;background:var(--ignition);
color:var(--on-ignition);padding:8px 10px 6px 12px;text-box:trim-both cap alphabetic}}
</style></head><body>
<!--
  image       Rise Above: the brand's own render (red-and-white balloon over a sea of clouds at sunrise), cropped with the balloon right of centre
  name        AntiHero set as a black label box (label-fill of the light theme), bottom-left, clear of the balloon
  tagline     one ignition label: the one red idea besides the balloon
-->
<div class="cover" role="img" aria-label="A red and white hot-air balloon rising above a sea of clouds at sunrise">
<div class="words"><h1 class="name">AntiHero</h1><br><p class="tag">BE YOUR OWN HERO</p></div></div>
</body></html>
"""


def cover_image():
    src = os.path.join(KIT, '_build', 'scenes', 'out', 'final', 'rise-above.png')
    im = Image.open(src).convert('RGB')
    W, H = im.size
    # full width, from just above the balloon (envelope top y=312 of 1440) so the cloud sea fills the bottom quarter
    x0, y0 = 0, int(H * 0.197)
    cw = W
    ch = int(cw * 288 / 960)
    im = im.crop((x0, y0, x0 + cw, y0 + ch)).resize((1440, 432), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=78, optimize=True, progressive=True)
    return base64.b64encode(buf.getvalue()).decode('ascii')


def w(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def uploads():
    A = os.path.join(KIT, '01_Brand-Bible', 'assets')
    F = os.path.join(KIT, '02_Logos', '07_Family')
    G = os.path.join(KIT, '05_Social', 'Facebook', 'Group-Kit')
    return {
        'Backgrounds': [(os.path.join(A, f'bg-{n}.jpg'), f'antihero-background-{n}.jpg') for n in
                        ['rise-above', 'first-light', 'launch', 'break-formation', 'see-further', 'daybreak', 'concrete', 'paper-bone']],
        'Social': [(os.path.join(A, f'{src}.jpg'), dst) for src, dst in
                   [('fb-cover-rise', 'facebook-cover-rise.jpg'), ('fb-cover-launch', 'facebook-cover-launch.jpg'),
                    ('fb-cover-formation', 'facebook-cover-formation.jpg'), ('fb-cover-manifesto', 'facebook-cover-manifesto.jpg'),
                    ('fb-profile-preview', 'facebook-profile-crop.jpg'), ('post-01', 'post-welcome.jpg'), ('post-02', 'post-creed.jpg'),
                    ('post-03', 'post-ai-tool.jpg'), ('post-04', 'post-workshop.jpg'), ('post-05', 'post-seo-tip.jpg'),
                    ('post-07', 'post-runway.jpg'), ('post-08', 'post-break-formation.jpg'), ('post-09', 'post-work-with-us.jpg'),
                    ('post-06', 'post-now-open.jpg'), ('story-01', 'story-join.jpg')]] +
                  [(os.path.join(G, *src.split('/')), dst) for src, dst in
                   [('01_Cover/antihero-group-cover-write-your-story_1640x856.png', 'group-cover-write-your-story.jpg'),
                    ('02_Pinned/antihero-group-start-here_1080x1350.png', 'group-start-here.jpg'),
                    ('02_Pinned/antihero-group-house-rules_1080x1350.png', 'group-house-rules.jpg'),
                    ('03_Weekly-Series/antihero-series-mon-ai-tool_1080x1350.png', 'group-series-mon-ai-tool.jpg'),
                    ('03_Weekly-Series/antihero-series-tue-prompt-swap_1080x1350.png', 'group-series-tue-prompt-swap.jpg'),
                    ('03_Weekly-Series/antihero-series-thu-get-found_1080x1350.png', 'group-series-thu-get-found.jpg'),
                    ('03_Weekly-Series/antihero-series-sat-build-day_1080x1350.png', 'group-series-sat-build-day.jpg'),
                    ('04_Templates/antihero-group-poll_1080x1080.png', 'group-poll.jpg')]],
        'Family': [(p, os.path.basename(p)) for p in sorted(glob.glob(os.path.join(F, '*.svg')))],
    }


def launch_md():
    """Page and group text. The group half comes from group_kit.py, the same source as the Group Kit and the Brand Bible."""
    from group_kit import ABOUT, GROUP_URL, NAME, QUESTIONS, RULES, SERIES
    intro = "AI tools, branding, and SEO for people who'd rather build than wait. Be your own hero."
    import re

    def series_name(s):     # sentence case, but "AI" stays capitalised (brand voice rule)
        return re.sub(r'^Ai\b', 'AI', ' '.join(s['title']).replace('&amp;', 'and').capitalize())
    rows = '\n'.join(f"| {s['short'].title()} | {series_name(s)} | {s['line']} |" for s in SERIES)
    return f"""# Launch copy

Paste-ready text for the Facebook page and group. The brand kit's Group Kit (05_Social/Facebook/Group-Kit) holds the same group text plus the setup steps, the weekly series cards, and the first ten posts.

**Page intro ({len(intro)} characters, limit 101)**

{intro}

**Group name**

{NAME}, live at {GROUP_URL} (private, visible in search).

**Group description**

{ABOUT}

**House rules** (add each in the group's Rules section: bold line as the title, the rest as the description)

{chr(10).join(f'{i + 1}. **{t}** {d}' for i, (t, d) in enumerate(RULES))}

**Membership questions**

{chr(10).join(f'{i + 1}. {q}' for i, q in enumerate(QUESTIONS))}

Turn on "ask people to agree to the rules".

**The weekly rhythm**

| Day | Series | Card line |
| --- | --- | --- |
{rows}
| Sun | Off | Go outside. |

**Boilerplate**

AntiHero teaches everyday entrepreneurs to use AI tools, build a brand, and get found online. The free AntiHero group runs weekly tool breakdowns, live workshops, and build-in-public threads. AntiHero Consulting helps businesses with branding, SEO, and AI systems, done with them rather than to them. Be your own hero.
"""


def stage(d):
    P = os.path.join(d, 'project')
    from design_system import TOKENS
    w(d, 'project/tokens.json', json.dumps(TOKENS, indent=1, ensure_ascii=False))
    w(d, 'project/README.md', README)
    w(d, 'project/guidelines/30-family.md', FAMILY_MD)
    w(d, 'project/guidelines/20-launch-copy.md', launch_md())
    w(d, 'project/components/Cover/preview.html', cover_html(cover_image()))
    for g, txt in GROUP_READMES.items():
        w(d, f'project/assets/{g}/README.md', f'# {g}\n\n{txt}\n')
    U = os.path.join(d, 'upload_v2')
    if os.path.isdir(U):
        shutil.rmtree(U)
    plan = {}
    for g, items in uploads().items():
        os.makedirs(os.path.join(U, g), exist_ok=True)
        for src, name in items:
            dst = os.path.join(U, g, name)
            if src.lower().endswith('.png') and name.endswith('.jpg'):    # full-size kit renders -> light previews
                im = Image.open(src).convert('RGB')
                im.thumbnail((1080, 1080))
                im.save(dst, 'JPEG', quality=82, optimize=True, progressive=True)
            else:
                shutil.copy2(src, dst)
            plan.setdefault(g, []).append(dst)
    json.dump(plan, open(os.path.join(d, 'upload_plan_v2.json'), 'w'), indent=1)
    allf = [p for g in ('Backgrounds', 'Social', 'Family') for p in plan[g]]
    for i in range(0, len(allf), 25):
        print('CHUNK', i // 25, json.dumps(allf[i:i + 25]))
    cov = os.path.getsize(os.path.join(P, 'components', 'Cover', 'preview.html'))
    print('cover bytes', cov)


def index(d, fresh, ids_path):
    idx = json.load(open(fresh, encoding='utf-8'))
    ids = json.load(open(ids_path))
    plan = json.load(open(os.path.join(d, 'upload_plan_v2.json')))
    tiles = {'Backgrounds': 'l', 'Social': 'm', 'Family': 'l'}
    for g in ('Backgrounds', 'Social', 'Family'):
        files, order = {}, []
        for p in plan[g]:
            name = os.path.basename(p)
            ext = name.rsplit('.', 1)[-1].lower()
            files[name] = {'name': name, 'blob': ids[name], 'size': os.path.getsize(p),
                           'type': {'svg': 'image/svg+xml', 'jpg': 'image/jpeg', 'png': 'image/png'}[ext]}
            order.append(name)
        idx['assetGroups'][g] = {'name': g, 'tile': tiles[g], 'order': order, 'files': files}
    idx['groups'] = ['Logos', 'Lockups', 'Family', 'Social', 'Backgrounds', 'Textures']
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    idx['lastChange'] = {'by': 'Matt', 'at': now, 'via': 'Claude Code',
                         'note': 'v2: open-sky imagery (original 3D renders), KR8TIV family, Facebook Group Kit cards and launch copy, new lines, image cover; Open Ring retired'}
    w(d, 'project/design-system.json', json.dumps(idx, indent=1))
    print('index merged:', {g: len(v['files']) for g, v in idx['assetGroups'].items()})


if __name__ == '__main__':
    if sys.argv[1] == 'stage':
        stage(sys.argv[2])
    else:
        index(sys.argv[2], sys.argv[3], sys.argv[4])
