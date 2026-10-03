"""Social assets: Facebook (page/group/event covers, profile pics, posts), YouTube, LinkedIn, X, Zoom, email."""
import os
import sys

from brand import C, KIT, HERO_UP, HERO_UP_W, FontOutline, font_face_css, hero_upright_group, mark_group, text_path
from render import Renderer, file_url

HERE = os.path.dirname(os.path.abspath(__file__))
HTML_DIR = os.path.join(HERE, 'templates')          # editable HTML sources (kept in the kit)
OUT = os.path.join(KIT, '05_Social')
BG = os.path.join(KIT, '04_Backgrounds')
os.makedirs(HTML_DIR, exist_ok=True)


def bg_url(name, kind='desktop-3840x2160'):
    return file_url(os.path.join(BG, f'antihero-bg-{name}_{kind}.jpg'))


def rel_fonts():
    return os.path.relpath(os.path.join(HERE, 'fonts'), HTML_DIR).replace('\\', '/')


BASE_CSS = f"""
{font_face_css(rel_fonts())}
:root{{--void:{C['void']};--carbon:{C['carbon']};--graphite:{C['graphite']};--ash:{C['ash']};--bone:{C['bone']};
--white:#fff;--red:{C['ignition']};--ember:{C['ember']};}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:var(--void)}}
body{{position:relative;overflow:hidden;-webkit-font-smoothing:antialiased;font-family:'Barlow',sans-serif;color:#fff}}
.bg{{position:absolute;inset:0;background-size:cover;background-position:center}}
.block{{position:absolute;transform-origin:0 0}}
.lbl{{font-family:'Bebas Neue',sans-serif;font-weight:400;line-height:1;text-box:trim-both cap alphabetic;
      display:inline-block;background:#fff;color:var(--void);white-space:nowrap}}
.red{{background:var(--red);color:#fff}}
.blk{{background:var(--void);color:#fff}}
.mono{{font-family:'JetBrains Mono',monospace}}
.cond{{font-family:'Barlow Condensed',sans-serif}}
"""


def wordmark_svg(col_anti='#fff', col_hero=None, height=100):
    """Inline ANTI+hero wordmark, `height` = px from ascender top to baseline."""
    col_hero = col_hero or col_anti
    asc = HERO_UP['ascender']
    fo = FontOutline('bebas')
    cap = asc * 0.86
    size = cap / (fo.cap / fo.upm)
    anti, w = text_path('bebas', 'ANTI', size, 0, 0, col_anti, tracking=0.01)
    hero = hero_upright_group(col_hero, w + 40, 0)
    total_w = w + 40 + HERO_UP_W
    top, bot = -asc - 4, 16
    s = height / asc
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {top:.1f} {total_w:.1f} {bot - top:.1f}" '
            f'style="height:{(bot - top) * s:.1f}px;width:{total_w * s:.1f}px;display:block">{anti}{hero}</svg>')


def badge_inline(size, disc=C['carbon'], mark='#fff'):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" style="width:{size}px;height:{size}px;display:block">'
            f'<circle cx="500" cy="500" r="500" fill="{disc}"/>{mark_group(mark)}</svg>')


def mark_inline(width, col='#fff', col_hero=None):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="114 113 785 773" style="width:{width}px;display:block">'
            f'{mark_group(col, col_hero)}</svg>')


# ---------------------------------------------------------------------------
# Content blocks, each designed at a reference size and scaled into a safe zone
# ---------------------------------------------------------------------------
DESC = 'AI &middot; BRANDING &middot; SEO &middot; ENTREPRENEURSHIP'


def block_label(stack_gap=0):
    """Concept A - the original channel-art label stack, rebuilt. Ref 1100x560."""
    return 1100, 560, f"""
<style>
.a{{width:1100px;height:560px;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.a .l1{{font-size:228px;letter-spacing:.015em;padding:22px 30px 22px 34px}}
.a .l2{{font-size:62px;letter-spacing:.045em;padding:15px 26px 15px 30px;margin-top:{stack_gap}px}}
.a .tag{{display:flex;align-items:center;gap:26px;margin-top:40px}}
.a .rule{{width:150px;height:3px;background:#fff;opacity:.9}}
.a .l3{{font-size:38px;letter-spacing:.16em;padding:12px 20px 12px 26px}}
</style>
<div class="a"><span class="lbl l1">ANTIHERO</span><span class="lbl l2">{DESC}</span>
<div class="tag"><span class="rule"></span><span class="lbl red l3">BE YOUR OWN HERO</span><span class="rule"></span></div></div>"""


def block_manifesto():
    """Concept B - type-led manifesto. Ref 1100x560."""
    return 1100, 560, f"""
<style>
.b{{width:1100px;height:560px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
.b .big{{font-family:'Bebas Neue';font-size:246px;line-height:.84;letter-spacing:.01em;color:#fff;text-box:trim-both cap alphabetic}}
.b .big + .big{{margin-top:26px}}
.b .big em{{font-style:normal;color:var(--red)}}
.b .sub{{margin-top:40px;display:flex;align-items:center;gap:22px}}
.b .sub span{{font-family:'Barlow Condensed';font-weight:700;font-size:30px;letter-spacing:.3em;color:#fff;opacity:.92;margin-right:-.3em}}
.b .dot{{width:9px;height:9px;border-radius:50%;background:var(--red)}}
</style>
<div class="b"><div class="big">BE YOUR OWN</div><div class="big"><em>HERO.</em></div>
<div class="sub">{wordmark_svg('#fff', C['ignition'], 44)}<i class="dot"></i><span>AI &amp; ENTREPRENEURSHIP</span></div></div>"""


def block_signal():
    """Concept C - 'No capes. Just tools.' AI angle. Ref 1100x560."""
    return 1100, 560, f"""
<style>
.c{{width:1100px;height:560px;display:flex;align-items:center;justify-content:center;gap:64px}}
.c .left{{flex:none}}
.c .right{{display:flex;flex-direction:column;align-items:flex-start}}
.c .l1{{font-size:150px;letter-spacing:.02em;padding:16px 22px 16px 24px}}
.c .l2{{font-size:150px;letter-spacing:.02em;padding:16px 22px 16px 24px}}
.c .prompt{{margin-top:34px;font-family:'JetBrains Mono';font-size:25px;color:#e8e8e8;letter-spacing:.01em}}
.c .prompt b{{color:var(--red);font-weight:700}}
.c .cursor{{display:inline-block;width:14px;height:26px;background:var(--red);vertical-align:-4px;margin-left:6px}}
</style>
<div class="c"><div class="left">{badge_inline(360)}</div>
<div class="right"><span class="lbl l1">NO CAPES.</span><span class="lbl red l2">JUST TOOLS.</span>
<div class="prompt"><b>&gt;</b> ai &middot; branding &middot; seo &middot; entrepreneurship<span class="cursor"></span></div></div></div>"""


BLOCKS = {'label': block_label, 'manifesto': block_manifesto, 'signal': block_signal}
BGS = {'label': 'first-light', 'manifesto': 'concrete', 'signal': 'grid'}


def page_html(W, H, bg, block, safe, extra='', bg_pos='center', overlay=''):
    bw, bh, html = block
    sx, sy, sw, sh = safe
    s = min(sw / bw, sh / bh)
    left = sx + (sw - bw * s) / 2
    top = sy + (sh - bh * s) / 2
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}
body{{width:{W}px;height:{H}px}}</style></head><body>
<div class="bg" style="background-image:url('{bg}');background-position:{bg_pos}"></div>{extra}
<div class="block" style="left:{left:.1f}px;top:{top:.1f}px;width:{bw}px;height:{bh}px;transform:scale({s:.4f})">{html}</div>
{overlay}</body></html>"""


def guide_overlay(W, H, zones):
    """Dashed guide rectangles: [(x,y,w,h,label,color)]."""
    out = []
    for i, (x, y, w, h, label, col) in enumerate(zones):
        side = 'left:8px' if i % 2 == 0 else 'right:8px'     # alternate so stacked labels never collide
        out.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border:3px dashed {col};'
                   f'pointer-events:none"><span style="position:absolute;{side};top:6px;font:700 20px \'JetBrains Mono\';'
                   f'color:{col};background:rgba(0,0,0,.6);padding:2px 6px">{label}</span></div>')
    return ''.join(out)


def circle_hint(cx, cy, r, label):
    return (f'<div style="position:absolute;left:{cx - r}px;top:{cy - r}px;width:{2 * r}px;height:{2 * r}px;border-radius:50%;'
            f'border:3px dashed #ffd400;background:rgba(255,212,0,.08)"><span style="position:absolute;left:50%;top:50%;'
            f'transform:translate(-50%,-50%);font:700 18px \'JetBrains Mono\';color:#ffd400;text-align:center;width:{2 * r}px">{label}</span></div>')


JOBS = []


def job(rel_png, W, H, html, guide_html=None):
    name = os.path.splitext(os.path.basename(rel_png))[0]
    hp = os.path.join(HTML_DIR, name + '.html')
    with open(hp, 'w', encoding='utf-8') as f:
        f.write(html)
    JOBS.append((hp, os.path.join(OUT, rel_png), W, H))
    if guide_html:
        gp = os.path.join(HTML_DIR, name + '__GUIDE.html')
        with open(gp, 'w', encoding='utf-8') as f:
            f.write(guide_html)
        JOBS.append((gp, os.path.join(OUT, os.path.dirname(rel_png), '_safe-zone-guides', name + '__GUIDE.png'), W, H))


# ---------------------------------------------------------------------------
# FACEBOOK
# ---------------------------------------------------------------------------
def facebook():
    # universal safe zone: centre 1100 x 560 survives 16:9, 2.63:1 and 2.4:1 crops on desktop + mobile
    for concept in BLOCKS:
        blk = BLOCKS[concept]()
        bg = bg_url(BGS[concept])
        # Page cover, 16:9 master (recommended upload)
        W, H = 1640, 924
        safe = ((W - 1100) / 2, (H - 560) / 2, 1100, 560)
        zones = [(0, (H - 624) // 2, W, 624, 'desktop 2.63:1 band (820x312 @2x)', '#39c6ff'),
                 (0, (H - 683) // 2, W, 683, 'mobile 2.4:1 band', '#7CFF6B'),
                 ((W - 1100) // 2, (H - 560) // 2, 1100, 560, 'KEEP TEXT HERE - universal safe zone', '#ff4d4d')]
        g = page_html(W, H, bg, blk, safe, overlay=guide_overlay(W, H, zones) + circle_hint(150, H - 40, 110, 'profile pic<br>overlap'))
        job(f'Facebook/Page-Cover/antihero-fb-page-cover-{concept}_1640x924.png', W, H, page_html(W, H, bg, blk, safe), g)
        # Page cover, classic 2.63:1 (820x312 @2x)
        W, H = 1640, 624
        safe = ((W - 1060) / 2, (H - 520) / 2, 1060, 520)
        zones = [((W - 1109) // 2, 0, 1109, H, 'visible if shown 16:9', '#7CFF6B'),
                 ((W - 1060) // 2, (H - 520) // 2, 1060, 520, 'KEEP TEXT HERE', '#ff4d4d')]
        g = page_html(W, H, bg, blk, safe, overlay=guide_overlay(W, H, zones))
        job(f'Facebook/Page-Cover/antihero-fb-page-cover-{concept}_1640x624.png', W, H, page_html(W, H, bg, blk, safe), g)
        # Group cover 1640x856 (1.91:1)
        W, H = 1640, 856
        safe = ((W - 1100) / 2, (H - 540) / 2, 1100, 540)
        zones = [(0, (H - 662) // 2, W, 662, 'desktop crop band', '#39c6ff'),
                 ((W - 1100) // 2, (H - 540) // 2, 1100, 540, 'KEEP TEXT HERE', '#ff4d4d')]
        g = page_html(W, H, bg, blk, safe, overlay=guide_overlay(W, H, zones))
        job(f'Facebook/Group-Cover/antihero-fb-group-cover-{concept}_1640x856.png', W, H, page_html(W, H, bg, blk, safe), g)
        # Event cover 1920x1005
        W, H = 1920, 1005
        safe = ((W - 1300) / 2, (H - 640) / 2, 1300, 640)
        job(f'Facebook/Event-Cover/antihero-fb-event-cover-{concept}_1920x1005.png', W, H, page_html(W, H, bg, blk, safe))

    # Profile pictures: disc colour fills the square so Facebook's circle crop == the badge
    for name, disc, mark in [('carbon', C['carbon'], '#fff'), ('black', C['void'], '#fff'),
                             ('ignition', C['ignition'], '#fff'), ('white', '#ffffff', C['void'])]:
        for S in (2048, 1080, 720, 320):
            html = f"""<!doctype html><html><head><style>*{{margin:0}}body{{width:{S}px;height:{S}px;background:{disc}}}</style></head>
<body>{badge_inline(S, disc, mark)}</body></html>"""
            job(f'Facebook/Profile-Picture/antihero-fb-profile-{name}_{S}px.png', S, S, html)
    # a circle-crop preview so you can see exactly what Facebook shows
    S = 1080
    prev = f"""<!doctype html><html><head><style>*{{margin:0}}body{{width:{S}px;height:{S}px;background:#f0f2f5;display:grid;place-items:center}}
.ring{{width:720px;height:720px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 12px #fff,0 8px 40px rgba(0,0,0,.25)}}</style></head>
<body><div class="ring">{badge_inline(720)}</div></body></html>"""
    job('Facebook/Profile-Picture/_preview-circle-crop.png', S, S, prev)


# ---------------------------------------------------------------------------
# FEED POSTS (Facebook + Instagram, 1080x1350 portrait / 1080x1080 square) and STORY 1080x1920
# ---------------------------------------------------------------------------
def post_shell(W, H, bg, inner, bg_pos='center'):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}
body{{width:{W}px;height:{H}px}}
.frame{{position:absolute;inset:0;padding:84px 80px;display:flex;flex-direction:column}}
.foot{{margin-top:auto;display:flex;align-items:center;justify-content:space-between}}
.foot .h{{font-family:'Barlow Condensed';font-weight:700;font-size:24px;letter-spacing:.26em;opacity:.85}}
</style></head><body><div class="bg" style="background-image:url('{bg}');background-position:{bg_pos}"></div>
<div class="frame">{inner}</div></body></html>"""


def posts():
    W, H = 1080, 1350
    foot_dark = f'<div class="foot">{wordmark_svg("#fff", C["ignition"], 40)}<span class="h">BE YOUR OWN HERO</span></div>'
    foot_light = f'<div class="foot" style="color:var(--void)">{wordmark_svg(C["void"], C["ignition"], 40)}<span class="h">BE YOUR OWN HERO</span></div>'
    # on Ignition red the wordmark is always all-white (red-on-red disappears)
    foot_on_red = f'<div class="foot">{wordmark_svg("#fff", "#fff", 40)}<span class="h">BE YOUR OWN HERO</span></div>'

    # 1. Welcome / manifesto
    inner = f"""<style>.w .lbl{{font-size:122px;padding:14px 20px 14px 22px;letter-spacing:.015em}}
.w .hero{{font-size:330px;padding:24px 30px 24px 34px;letter-spacing:.01em}}
.w p{{font-size:34px;line-height:1.38;font-weight:500;max-width:860px;margin-top:56px;color:#e9e9e9}}
.w p b{{color:#fff;font-weight:700}}</style>
<div class="w" style="display:flex;flex-direction:column;align-items:flex-start;margin-top:40px">
<span class="lbl">YOU ARE THE</span><span class="lbl red hero">HERO</span><span class="lbl">OF YOUR OWN STORY.</span>
<p><b>Welcome to AntiHero.</b> AI tools, branding, SEO, and real-world entrepreneurship for people who would rather build than wait.</p></div>{foot_dark}"""
    job('Posts/antihero-post-01-welcome_1080x1350.png', W, H, post_shell(W, H, bg_url('concrete', 'phone-1290x2796'), inner))

    # 2. Quote card (light)
    inner = f"""<style>.q .mk{{margin-bottom:70px}}
.q h1{{font-family:'Bebas Neue';font-weight:400;font-size:176px;line-height:.9;color:var(--void);letter-spacing:.005em}}
.q h1 em{{font-style:normal;color:var(--red)}}
.q .by{{margin-top:44px;font-family:'Barlow Condensed';font-weight:700;font-size:30px;letter-spacing:.24em;color:var(--void)}}</style>
<div class="q" style="margin-top:30px"><div class="mk">{mark_inline(150, C['void'], C['ignition'])}</div>
<h1>NOBODY&rsquo;S COMING<br>TO SAVE YOU.<br><em>GOOD.</em></h1><div class="by">&mdash; THE ANTIHERO CREED</div></div>{foot_light}"""
    job('Posts/antihero-post-02-quote_1080x1350.png', W, H, post_shell(W, H, bg_url('paper-bone', 'phone-1290x2796'), inner))

    # 3. AI tool of the week
    inner = f"""<style>.t .kick{{font-size:46px;letter-spacing:.12em;padding:12px 18px 12px 22px}}
.t h1{{font-family:'Bebas Neue';font-weight:400;font-size:230px;line-height:.86;margin-top:40px;letter-spacing:.01em}}
.t .what{{font-size:36px;font-weight:600;margin-top:22px;color:#f1f1f1}}
.t .box{{margin-top:48px;border:2px solid rgba(255,255,255,.22);background:rgba(10,10,11,.72);padding:30px 34px 34px}}
.t .box .k{{font-family:'JetBrains Mono';font-weight:700;font-size:22px;color:var(--red);letter-spacing:.08em}}
.t .box p{{font-family:'JetBrains Mono';font-size:26px;line-height:1.55;margin-top:16px;color:#ededed}}</style>
<div class="t" style="margin-top:10px"><span class="lbl red kick">AI TOOL OF THE WEEK</span>
<h1>CLAUDE</h1><div class="what">Your always-on marketing department.</div>
<div class="box"><div class="k">&gt; TRY THIS PROMPT</div><p>Act as a local SEO strategist. Write 5 Google Business Profile posts for my [business] in [city]. Each under 250 words, one clear call to action, no hype.</p></div></div>{foot_dark}"""
    job('Posts/antihero-post-03-ai-tool_1080x1350.png', W, H, post_shell(W, H, bg_url('grid', 'phone-1290x2796'), inner))

    # 4. Live workshop
    inner = f"""<style>.e .kick{{font-size:52px;letter-spacing:.14em;padding:14px 20px 14px 24px}}
.e h1{{font-family:'Bebas Neue';font-weight:400;font-size:168px;line-height:.9;margin-top:52px;color:#fff}}
.e .meta{{display:flex;gap:14px;margin-top:56px;flex-wrap:wrap}}
.e .meta span{{font-size:52px;letter-spacing:.06em;padding:12px 18px 12px 20px}}
.e .note{{margin-top:40px;font-size:32px;font-weight:600}}</style>
<div class="e" style="margin-top:10px"><span class="lbl blk kick">LIVE WORKSHOP</span>
<h1>BUILD YOUR BRAND<br>WITH AI IN<br>60 MINUTES</h1>
<div class="meta"><span class="lbl">THU OCT 2</span><span class="lbl">7 PM MT</span><span class="lbl blk">FREE</span></div>
<div class="note">Link in the comments. Bring your laptop and one business idea.</div></div>{foot_on_red}"""
    job('Posts/antihero-post-04-workshop_1080x1350.png', W, H, post_shell(W, H, bg_url('ignition-grain', 'phone-1290x2796'), inner))

    # 5. SEO tip (carousel cover)
    inner = f"""<style>.s .kick{{font-size:46px;letter-spacing:.12em;padding:12px 18px 12px 22px}}
.s h1{{font-family:'Bebas Neue';font-weight:400;font-size:150px;line-height:.9;margin-top:46px;color:var(--void)}}
.s h1 em{{font-style:normal;color:var(--red)}}
.s p{{font-size:34px;line-height:1.42;margin-top:40px;color:#2a2d31;max-width:860px;font-weight:500}}
.s .swipe{{margin-top:44px;font-family:'Barlow Condensed';font-weight:800;font-size:30px;letter-spacing:.24em;color:var(--red)}}</style>
<div class="s" style="margin-top:10px"><span class="lbl blk kick">SEO TIP 01</span>
<h1>YOUR GOOGLE BUSINESS PROFILE IS YOUR <em>NEW HOMEPAGE.</em></h1>
<p>Most local customers decide before they ever reach your website. Photos, reviews, and weekly posts do the selling.</p>
<div class="swipe">SWIPE FOR THE 5-MINUTE FIX &rarr;</div></div>{foot_light}"""
    job('Posts/antihero-post-05-seo-tip_1080x1350.png', W, H, post_shell(W, H, bg_url('paper-bone', 'phone-1290x2796'), inner))

    # 6. Square announcement (1080x1080)
    S = 1080
    inner = f"""<style>.n{{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;text-align:center}}
.n .l1{{font-size:150px;padding:18px 24px 18px 28px}}
.n .l2{{font-size:56px;letter-spacing:.05em;padding:14px 20px 14px 24px}}
.n .tag{{display:flex;align-items:center;gap:22px;margin-top:40px}}
.n .rule{{width:110px;height:3px;background:#fff}}
.n .l3{{font-size:34px;letter-spacing:.16em;padding:11px 16px 11px 21px}}
.n .badge{{margin-bottom:54px}}</style>
<div class="n"><div class="badge">{badge_inline(250)}</div><span class="lbl l1">NOW OPEN</span><span class="lbl l2">THE ANTIHERO GROUP</span>
<div class="tag"><span class="rule"></span><span class="lbl red l3">BE YOUR OWN HERO</span><span class="rule"></span></div></div>"""
    job('Posts/antihero-post-06-now-open_1080x1080.png', S, S, post_shell(S, S, bg_url('first-light', 'phone-1290x2796'), inner, 'center 62%'))

    # 7. Story 1080x1920
    W2, H2 = 1080, 1920
    inner = f"""<style>.st{{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;text-align:center}}
.st .l1{{font-size:170px;padding:20px 26px 20px 30px}}
.st .l2{{font-size:52px;letter-spacing:.05em;padding:14px 20px 14px 24px}}
.st .cta{{margin-top:80px;font-size:60px;letter-spacing:.12em;padding:18px 28px 18px 34px}}
.st .small{{margin-top:26px;font-family:'Barlow Condensed';font-weight:700;font-size:30px;letter-spacing:.26em}}
.st .badge{{margin-bottom:80px}}</style>
<div class="st"><div class="badge">{badge_inline(330)}</div><span class="lbl l1">ANTIHERO</span><span class="lbl l2">AI &middot; BRANDING &middot; SEO</span>
<span class="lbl red cta">JOIN THE GROUP</span><div class="small">BE YOUR OWN HERO</div></div>"""
    job('Posts/antihero-story-01-join_1080x1920.png', W2, H2, post_shell(W2, H2, bg_url('first-light', 'phone-1290x2796'), inner, 'center 55%'))


# ---------------------------------------------------------------------------
# OTHER PLATFORMS
# ---------------------------------------------------------------------------
def platforms():
    blk = BLOCKS['label']()
    # YouTube channel banner 2560x1440, text-safe 1546x423 centre
    W, H = 2560, 1440
    safe = ((W - 1546) / 2, (H - 423) / 2, 1546, 423)
    zones = [((W - 1546) // 2, (H - 423) // 2, 1546, 423, 'safe on all devices 1546x423', '#ff4d4d'),
             ((W - 2560) // 2, (H - 423) // 2, 2560, 423, 'desktop max 2560x423', '#39c6ff'),
             ((W - 1855) // 2, (H - 423) // 2, 1855, 423, 'tablet 1855x423', '#7CFF6B')]
    job('YouTube/antihero-youtube-banner_2560x1440.png', W, H, page_html(W, H, bg_url('first-light'), blk, safe),
        page_html(W, H, bg_url('first-light'), blk, safe, overlay=guide_overlay(W, H, zones)))
    job('YouTube/antihero-youtube-profile_800x800.png', 800, 800,
        f'<!doctype html><html><head><style>*{{margin:0}}body{{width:800px;height:800px;background:{C["carbon"]}}}</style></head><body>{badge_inline(800)}</body></html>')
    job('YouTube/antihero-youtube-watermark_150x150.png', 150, 150,
        f'<!doctype html><html><head><style>*{{margin:0}}body{{width:150px;height:150px;background:transparent}}</style></head><body>{badge_inline(150)}</body></html>')
    # YouTube thumbnail template
    thumb = f"""<style>.yt{{position:absolute;inset:0}}
.yt .t1{{position:absolute;left:70px;top:110px;font-size:170px;padding:18px 24px 18px 28px}}
.yt .t2{{position:absolute;left:70px;top:330px;font-size:170px;padding:18px 24px 18px 28px}}
.yt .t3{{position:absolute;left:74px;top:560px;font-family:'Barlow Condensed';font-weight:800;font-size:40px;letter-spacing:.2em}}
.yt .face{{position:absolute;right:60px;top:60px;width:420px;height:600px;border:4px dashed rgba(255,255,255,.35);
display:grid;place-items:center;font:700 24px 'JetBrains Mono';color:rgba(255,255,255,.55);text-align:center}}
.yt .bd{{position:absolute;right:40px;bottom:40px}}</style>
<div class="yt"><span class="lbl t1">AI BUILT MY</span><span class="lbl red t2">WHOLE BRAND</span>
<div class="t3">IN ONE AFTERNOON</div><div class="face">YOUR PHOTO<br>(cut-out)</div></div>"""
    job('YouTube/antihero-youtube-thumbnail-template_1280x720.png', 1280, 720,
        f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}body{{width:1280px;height:720px}}</style></head>
<body><div class="bg" style="background-image:url('{bg_url('smoke')}')"></div>{thumb}</body></html>""")

    # LinkedIn personal banner 1584x396 - avatar overlaps bottom-left, keep content right of ~420px
    W, H = 1584, 396
    job('LinkedIn/antihero-linkedin-banner_1584x396.png', W, H, page_html(W, H, bg_url('first-light'), blk, (470, 40, 1060, 316), bg_pos='center 58%'))
    W, H = 1128, 191
    job('LinkedIn/antihero-linkedin-company-cover_1128x191.png', W, H, page_html(W, H, bg_url('first-light'), blk, (150, 14, 828, 163), bg_pos='center 58%'))
    job('LinkedIn/antihero-linkedin-logo_400x400.png', 400, 400,
        f'<!doctype html><html><head><style>*{{margin:0}}body{{width:400px;height:400px;background:{C["carbon"]}}}</style></head><body>{badge_inline(400)}</body></html>')
    # X / Twitter header 1500x500 - avatar bottom-left; top/bottom ~60px can crop
    W, H = 1500, 500
    job('X-Twitter/antihero-x-header_1500x500.png', W, H, page_html(W, H, bg_url('first-light'), blk, (330, 70, 1000, 360), bg_pos='center 58%'))
    job('X-Twitter/antihero-x-profile_400x400.png', 400, 400,
        f'<!doctype html><html><head><style>*{{margin:0}}body{{width:400px;height:400px;background:{C["carbon"]}}}</style></head><body>{badge_inline(400)}</body></html>')

    # Zoom / Teams / Meet virtual background 1920x1080 - keep the centre clear for you
    for name, bg in [('concrete', 'concrete'), ('first-light', 'first-light')]:
        html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}body{{width:1920px;height:1080px}}
.wm{{position:absolute;right:90px;top:80px}}.tg{{position:absolute;right:92px;top:186px;font-family:'Barlow Condensed';font-weight:700;
font-size:24px;letter-spacing:.3em;opacity:.8;margin-right:-.3em}}</style></head><body>
<div class="bg" style="background-image:url('{bg_url(bg)}');background-position:center 64%"></div>
<div class="wm">{wordmark_svg('#fff', C['ignition'], 84)}</div><div class="tg">BE YOUR OWN HERO</div></body></html>"""
        job(f'Video-Call/antihero-zoom-background-{name}_1920x1080.png', 1920, 1080, html)

    # Email signature banner (600x150 display, rendered @2x)
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}body{{width:1200px;height:300px;background:var(--carbon)}}
.row{{position:absolute;inset:0;display:flex;align-items:center;gap:44px;padding:0 60px}}
.col{{display:flex;flex-direction:column;gap:22px}}
.d{{font-family:'Barlow Condensed';font-weight:700;font-size:30px;letter-spacing:.24em;color:#d9dcdf}}</style></head><body>
<div class="bg" style="background-image:url('{bg_url('concrete')}');opacity:.9"></div>
<div class="row">{badge_inline(200)}<div class="col">{wordmark_svg('#fff', C['ignition'], 92)}<div class="d">{DESC}</div></div></div></body></html>"""
    job('Email/antihero-email-signature_1200x300.png', 1200, 300, html)
    # Link-share / Open Graph image 1200x630
    job('Web/antihero-og-share_1200x630.png', 1200, 630, page_html(1200, 630, bg_url('first-light'), blk, (80, 50, 1040, 530), bg_pos='center 60%'))


if __name__ == '__main__':
    which = sys.argv[1:] or ['facebook', 'posts', 'platforms']
    for w in which:
        globals()[w]()
    with Renderer() as r:
        for hp, png, W, H in JOBS:
            r.png(hp, png, W, H, transparent=png.endswith('watermark_150x150.png'), wait_ms=60)
    print('rendered', len(JOBS))
