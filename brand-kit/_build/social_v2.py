"""Social assets v2: bright, inspiring scenes (Blender renders) with the black-box label system on top."""
import os
import shutil
import sys

from brand import C, KIT
from family import KR_D, KR_VB
from render import Renderer
import social as S
from social import (BASE_CSS, DESC, badge_inline, circle_hint, guide_overlay, job, mark_inline, page_html, wordmark_svg)

OUT = S.OUT
BG = S.BG
PHONE = {'rise-above', 'launch', 'first-light', 'daybreak', 'concrete', 'paper-bone'}


def bg(name, phone=False):
    if phone and name in PHONE:
        return S.bg_url(name, 'phone-1290x2796')
    return S.bg_url(name)


EXTRA_CSS = """
.panel{background:rgba(10,10,11,.80);color:#fff}
.bar{position:absolute;left:0;right:0;bottom:0;padding:26px 80px 30px;background:rgba(10,10,11,.86);display:flex;align-items:center;justify-content:space-between}
.bar .h{font-family:'Barlow Condensed';font-weight:700;font-size:24px;letter-spacing:.26em;color:#fff;margin-right:-.26em}
"""


def kr8tiv_svg(height, fill='#fff'):
    s = height / KR_VB[3]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{KR_VB[0]} {KR_VB[1]} {KR_VB[2]} {KR_VB[3]}" '
            f'style="height:{height}px;width:{KR_VB[2] * s:.1f}px;display:block"><path fill="{fill}" fill-rule="evenodd" d="{KR_D}"/></svg>')


# ---------------------------------------------------------------------------
# Cover blocks (reference 1100 x 560, scaled into each platform's safe zone)
# ---------------------------------------------------------------------------
def block_rise(align='flex-start'):
    return 1100, 560, f"""<style>.r{{width:1100px;height:560px;display:flex;flex-direction:column;justify-content:center;align-items:{align};padding-left:6px}}
.r .l1{{font-size:214px;letter-spacing:.015em;padding:22px 28px 22px 32px}}
.r .l2{{font-size:52px;letter-spacing:.045em;padding:14px 22px 14px 26px}}
.r .l3{{font-size:34px;letter-spacing:.16em;padding:12px 18px 12px 23px;margin-top:26px}}</style>
<div class="r"><span class="lbl blk l1">ANTIHERO</span><span class="lbl blk l2">{DESC}</span><span class="lbl red l3">BE YOUR OWN HERO</span></div>"""


def block_launch():
    return 1100, 560, f"""<style>.q{{width:1100px;height:560px;display:flex;flex-direction:column;justify-content:center;align-items:flex-start;padding-left:6px}}
.q .l1{{font-size:132px;letter-spacing:.012em;padding:18px 24px 18px 27px}}
.q .l2{{font-size:132px;letter-spacing:.012em;padding:18px 24px 18px 27px}}
.q .row{{display:flex;align-items:center;gap:26px;margin-top:30px}}
.q .l3{{font-size:32px;letter-spacing:.16em;padding:12px 18px 12px 22px}}</style>
<div class="q"><span class="lbl blk l1">THEY DIDN&rsquo;T</span><span class="lbl blk l2">SEE YOU COMING.</span>
<div class="row"><span class="lbl red l3">BE YOUR OWN HERO</span></div></div>"""


def block_formation():
    return 1100, 560, f"""<style>.f{{width:1100px;height:560px;display:flex;flex-direction:column;justify-content:flex-end;align-items:flex-end;padding-bottom:4px}}
.f .l1{{font-size:150px;letter-spacing:.012em;padding:18px 24px 18px 27px}}
.f .l3{{font-size:32px;letter-spacing:.16em;padding:12px 18px 12px 22px;margin-top:22px}}</style>
<div class="f"><span class="lbl blk l1">BREAK</span><span class="lbl blk l1">FORMATION.</span><span class="lbl red l3">BE YOUR OWN HERO</span></div>"""


def block_manifesto():
    return 1100, 560, f"""<style>.m{{width:1100px;height:560px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:var(--void)}}
.m .big{{font-family:'Bebas Neue';font-size:236px;line-height:.84;text-box:trim-both cap alphabetic}}
.m .big + .big{{margin-top:24px}}.m .big em{{font-style:normal;color:var(--red)}}
.m .sub{{margin-top:40px;display:flex;align-items:center;gap:22px}}
.m .sub span{{font-family:'Barlow Condensed';font-weight:700;font-size:30px;letter-spacing:.3em;margin-right:-.3em}}
.m .dot{{width:9px;height:9px;border-radius:50%;background:var(--red)}}</style>
<div class="m"><div class="big">BE YOUR OWN</div><div class="big"><em>HERO.</em></div>
<div class="sub">{wordmark_svg(C['void'], C['ignition'], 44)}<i class="dot"></i><span>AI &amp; ENTREPRENEURSHIP</span></div></div>"""


COVERS = {
    'rise': (block_rise, 'rise-above', 'center 55%'),
    'launch': (block_launch, 'launch', 'center 50%'),
    'formation': (block_formation, 'break-formation', '22% 38%;background-size:122% auto'),
    'manifesto': (block_manifesto, 'daybreak', 'center'),
}


def css_page(html):
    return html.replace('</style>', EXTRA_CSS + '</style>', 1)


def facebook():
    for concept, (fn, bgname, pos) in COVERS.items():
        blk = fn()
        u = bg(bgname)
        W, H = 1640, 924
        safe = ((W - 1100) / 2, (H - 560) / 2, 1100, 560)
        zones = [(0, (H - 624) // 2, W, 624, 'desktop 2.63:1 band (820x312 @2x)', '#1e88ff'),
                 (0, (H - 683) // 2, W, 683, 'mobile 2.4:1 band', '#12a150'),
                 ((W - 1100) // 2, (H - 560) // 2, 1100, 560, 'KEEP TEXT HERE - universal safe zone', '#e0261e')]
        g = page_html(W, H, u, blk, safe, bg_pos=pos, overlay=guide_overlay(W, H, zones) + circle_hint(150, H - 40, 110, 'profile pic<br>overlap'))
        job(f'Facebook/Page-Cover/antihero-fb-page-cover-{concept}_1640x924.png', W, H, page_html(W, H, u, blk, safe, bg_pos=pos), g)
        W, H = 1640, 624
        safe = ((W - 1060) / 2, (H - 520) / 2, 1060, 520)
        job(f'Facebook/Page-Cover/antihero-fb-page-cover-{concept}_1640x624.png', W, H, page_html(W, H, u, blk, safe, bg_pos=pos),
            page_html(W, H, u, blk, safe, bg_pos=pos, overlay=guide_overlay(W, H, [((W - 1109) // 2, 0, 1109, H, 'visible if shown 16:9', '#12a150'),
                                                                                     ((W - 1060) // 2, (H - 520) // 2, 1060, 520, 'KEEP TEXT HERE', '#e0261e')])))
        W, H = 1640, 856
        safe = ((W - 1100) / 2, (H - 540) / 2, 1100, 540)
        job(f'Facebook/Group-Cover/antihero-fb-group-cover-{concept}_1640x856.png', W, H, page_html(W, H, u, blk, safe, bg_pos=pos),
            page_html(W, H, u, blk, safe, bg_pos=pos, overlay=guide_overlay(W, H, [(0, (H - 662) // 2, W, 662, 'desktop crop band', '#1e88ff'),
                                                                                     ((W - 1100) // 2, (H - 540) // 2, 1100, 540, 'KEEP TEXT HERE', '#e0261e')])))
        W, H = 1920, 1005
        safe = ((W - 1300) / 2, (H - 640) / 2, 1300, 640)
        job(f'Facebook/Event-Cover/antihero-fb-event-cover-{concept}_1920x1005.png', W, H, page_html(W, H, u, blk, safe, bg_pos=pos))


# ---------------------------------------------------------------------------
# Posts
# ---------------------------------------------------------------------------
def shell(W, H, u, inner, pos='center', foot='bar'):
    footer = {
        'bar': f'<div class="bar">{wordmark_svg("#fff", C["ignition"], 40)}<span class="h">BE YOUR OWN HERO</span></div>',
        'light': f'<div class="bar" style="background:transparent;padding-bottom:70px">{wordmark_svg(C["void"], C["ignition"], 40)}'
                 f'<span class="h" style="color:var(--void)">BE YOUR OWN HERO</span></div>',
        'none': '',
    }[foot]
    return css_page(f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}
body{{width:{W}px;height:{H}px}}
.frame{{position:absolute;inset:0;padding:84px 80px 150px;display:flex;flex-direction:column}}</style></head><body>
<div class="bg" style="background-image:url('{u}');background-position:{pos}"></div>
<div class="frame">{inner}</div>{footer}</body></html>""")


def posts():
    W, H = 1080, 1350
    # 1 welcome
    inner = """<style>.w .lbl{font-size:118px;padding:14px 20px 14px 22px;letter-spacing:.015em}
.w .hero{font-size:320px;padding:24px 30px 24px 34px;letter-spacing:.01em}
.w .p{font-size:32px;line-height:1.4;font-weight:500;padding:26px 30px;margin-top:40px;max-width:900px}
.w .p b{font-weight:700}</style>
<div class="w" style="display:flex;flex-direction:column;align-items:flex-start;margin-top:10px">
<span class="lbl blk">YOU ARE THE</span><span class="lbl red hero">HERO</span><span class="lbl blk">OF YOUR OWN STORY.</span>
<p class="p panel"><b>Welcome to AntiHero.</b> AI tools, branding, SEO, and real-world entrepreneurship for people who would rather build than wait.</p></div>"""
    job('Posts/antihero-post-01-welcome_1080x1350.png', W, H, shell(W, H, bg('rise-above', True), inner, 'center 30%'))

    # 2 quote (daybreak, light)
    inner = f"""<style>.q h1{{font-family:'Bebas Neue';font-weight:400;font-size:158px;line-height:.9;color:var(--void)}}
.q h1 em{{font-style:normal;color:var(--red)}}
.q .by{{margin-top:44px;font-family:'Barlow Condensed';font-weight:700;font-size:30px;letter-spacing:.24em;color:var(--void)}}</style>
<div class="q" style="margin-top:20px"><div style="margin-bottom:64px">{mark_inline(150, C['void'], C['ignition'])}</div>
<h1>NOBODY&rsquo;S COMING<br>TO SAVE YOU.<br><em>YOU NEVER<br>NEEDED SAVING.</em></h1><div class="by">THE ANTIHERO CREED</div></div>"""
    job('Posts/antihero-post-02-quote_1080x1350.png', W, H, shell(W, H, bg('daybreak', True), inner, foot='light'))

    # 3 AI tool of the week (drone, tech as a friend)
    inner = """<style>.t .kick{font-size:44px;letter-spacing:.12em;padding:12px 18px 12px 22px}
.t .name{font-size:210px;margin-top:22px;padding:22px 28px 22px 30px;letter-spacing:.01em}
.t .what{font-size:34px;font-weight:600;padding:18px 24px;margin-top:0}
.t .box{margin-top:auto;padding:28px 32px 32px;max-width:920px}
.t .box .k{font-family:'JetBrains Mono';font-weight:700;font-size:22px;color:#ff5a4f;letter-spacing:.08em}
.t .box p{font-family:'JetBrains Mono';font-size:26px;line-height:1.55;margin-top:14px;color:#f1f1f1}</style>
<div class="t" style="display:flex;flex-direction:column;align-items:flex-start;height:100%"><span class="lbl red kick">AI TOOL OF THE WEEK</span>
<span class="lbl blk name">CLAUDE</span><span class="what panel">Your always-on marketing department.</span>
<div class="box panel"><div class="k">&gt; TRY THIS PROMPT</div><p>Act as a local SEO strategist. Write 5 Google Business Profile posts for my [business] in [city]. Each under 250 words, one clear call to action, no hype.</p></div></div>"""
    job('Posts/antihero-post-03-ai-tool_1080x1350.png', W, H, shell(W, H, bg('see-further'), inner, '74% center'))

    # 4 live workshop (launch)
    inner = """<style>.e .kick{font-size:50px;letter-spacing:.14em;padding:14px 20px 14px 24px}
.e .h{font-size:132px;padding:16px 22px 16px 24px;letter-spacing:.01em}
.e .meta{display:flex;gap:14px;margin-top:40px;flex-wrap:wrap}
.e .meta span{font-size:50px;letter-spacing:.06em;padding:12px 18px 12px 20px}
.e .note{margin-top:30px;font-size:30px;font-weight:600;padding:18px 24px}</style>
<div class="e" style="display:flex;flex-direction:column;align-items:flex-start"><span class="lbl red kick">LIVE WORKSHOP</span>
<span class="lbl blk h" style="margin-top:36px">BUILD YOUR BRAND</span><span class="lbl blk h">WITH AI IN</span><span class="lbl blk h">60 MINUTES</span>
<div class="meta"><span class="lbl">THU OCT 2</span><span class="lbl">7 PM MT</span><span class="lbl red">FREE</span></div>
<div class="note panel">Link in the comments. Bring your laptop and one business idea.</div></div>"""
    job('Posts/antihero-post-04-workshop_1080x1350.png', W, H, shell(W, H, bg('launch', True), inner, 'center 40%'))

    # 5 SEO tip (bone paper) - light layout kept
    inner = """<style>.s .kick{font-size:46px;letter-spacing:.12em;padding:12px 18px 12px 22px}
.s h1{font-family:'Bebas Neue';font-weight:400;font-size:150px;line-height:.9;margin-top:46px;color:var(--void)}
.s h1 em{font-style:normal;color:var(--red)}
.s p{font-size:34px;line-height:1.42;margin-top:40px;color:#2a2d31;max-width:860px;font-weight:500}
.s .swipe{margin-top:44px;font-family:'Barlow Condensed';font-weight:800;font-size:30px;letter-spacing:.24em;color:var(--red)}</style>
<div class="s" style="margin-top:10px"><span class="lbl blk kick">SEO TIP 01</span>
<h1>YOUR GOOGLE BUSINESS PROFILE IS YOUR <em>NEW HOMEPAGE.</em></h1>
<p>Most local customers decide before they ever reach your website. Photos, reviews, and weekly posts do the selling.</p>
<div class="swipe">SWIPE FOR THE 5-MINUTE FIX &rarr;</div></div>"""
    job('Posts/antihero-post-05-seo-tip_1080x1350.png', W, H, shell(W, H, bg('paper-bone', True), inner, foot='light'))

    # 6 now open (square, balloon)
    S2 = 1080
    inner = f"""<style>.n{{display:flex;flex-direction:column;align-items:flex-start;justify-content:center;height:100%}}
.n .l1{{font-size:150px;padding:18px 24px 18px 28px}}.n .l2{{font-size:56px;letter-spacing:.05em;padding:14px 20px 14px 24px}}
.n .l3{{font-size:34px;letter-spacing:.16em;padding:11px 16px 11px 21px;margin-top:26px}}</style>
<div class="n">{badge_inline(170)}<span class="lbl blk l1" style="margin-top:40px">NOW OPEN</span><span class="lbl blk l2">THE ANTIHERO GROUP</span>
<span class="lbl red l3">BE YOUR OWN HERO</span></div>"""
    job('Posts/antihero-post-06-now-open_1080x1080.png', S2, S2, shell(S2, S2, bg('rise-above'), inner, '76% center', foot='none'))

    # 7 story (join)
    W2, H2 = 1080, 1920
    inner = f"""<style>.st{{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;text-align:center;padding-bottom:40px}}
.st .l1{{font-size:170px;padding:20px 26px 20px 30px}}.st .l2{{font-size:52px;letter-spacing:.05em;padding:14px 20px 14px 24px}}
.st .cta{{margin-top:60px;font-size:60px;letter-spacing:.12em;padding:18px 28px 18px 34px}}
.st .badge{{margin-bottom:50px}}</style>
<div class="st"><div class="badge">{badge_inline(300)}</div><span class="lbl blk l1">ANTIHERO</span><span class="lbl blk l2">AI &middot; BRANDING &middot; SEO</span>
<span class="lbl red cta">JOIN THE GROUP</span></div>"""
    job('Posts/antihero-story-01-join_1080x1920.png', W2, H2, shell(W2, H2, bg('rise-above', True), inner, 'center 20%', foot='none'))

    # 8 runway (new)
    inner = """<style>.rw .l{font-size:128px;padding:16px 22px 16px 24px;letter-spacing:.01em}
.rw .good{font-size:300px;padding:26px 30px 26px 34px}
.rw .p{font-size:32px;line-height:1.4;font-weight:500;padding:24px 28px;margin-top:40px;max-width:900px}</style>
<div class="rw" style="display:flex;flex-direction:column;align-items:flex-start;margin-top:10px">
<span class="lbl blk l">HATE YOUR JOB?</span><span class="lbl red good">GOOD.</span><span class="lbl blk l">THAT&rsquo;S YOUR RUNWAY.</span>
<p class="p panel">Every skill we teach in the group is a way out: AI tools, branding, and getting found online. Start on a Saturday. Leave when you are ready.</p></div>"""
    job('Posts/antihero-post-07-runway_1080x1350.png', W, H, shell(W, H, bg('launch', True), inner, 'center 40%'))

    # 9 break formation (new)
    inner = """<style>.bf .l{font-size:170px;padding:20px 26px 20px 28px;letter-spacing:.012em}
.bf .p{font-size:32px;line-height:1.4;font-weight:500;padding:24px 28px;margin-top:36px;max-width:880px}</style>
<div class="bf" style="display:flex;flex-direction:column;align-items:flex-start;justify-content:flex-end;height:100%">
<span class="lbl blk l">BREAK</span><span class="lbl blk l">FORMATION.</span>
<p class="p panel">Everyone else is flying the same route. You are allowed to take a different one.</p></div>"""
    job('Posts/antihero-post-08-break-formation_1080x1350.png', W, H, shell(W, H, bg('break-formation'), inner, '62% center'))

    # 10 work with us (the family) - the occasional ask
    inner = f"""<style>.ww .l{{font-size:120px;padding:16px 22px 16px 24px;letter-spacing:.01em}}
.ww .card{{margin-top:34px;padding:30px 34px;width:100%}}
.ww .row{{display:flex;align-items:center;justify-content:space-between;gap:24px;padding:22px 0;border-top:1px solid rgba(255,255,255,.18)}}
.ww .row:first-of-type{{border-top:0;padding-top:4px}}
.ww .t{{font-size:27px;line-height:1.35;color:#e9e9e9;font-weight:500;max-width:420px}}
.ww .u{{font-family:'JetBrains Mono';font-size:24px;color:#fff}}
.ww .cap{{font-family:'Barlow Condensed';font-weight:700;font-size:22px;letter-spacing:.26em;color:#bfc3c7;margin-bottom:10px}}</style>
<div class="ww" style="display:flex;flex-direction:column;align-items:flex-start">
<span class="lbl blk l">WANT IT</span><span class="lbl red l">DONE FOR YOU?</span>
<div class="card panel"><div class="cap">THE ANTIHERO FAMILY</div>
<div class="row"><div>{kr8tiv_svg(44)}<div class="t" style="margin-top:12px">Brand, web, motion, and video. The studio.</div></div><div class="u">kr8tiv.io</div></div>
<div class="row"><div style="display:flex;align-items:flex-start;gap:10px">{kr8tiv_svg(44)}<span class="mono" style="font-weight:700;font-size:24px">AI</span></div>
<div class="u">kr8tiv.ai</div></div><div class="t" style="margin-top:-8px">AI systems that run your back office.</div></div></div>"""
    job('Posts/antihero-post-09-work-with-us_1080x1350.png', W, H, shell(W, H, bg('first-light', True), inner, 'center 30%'))


# ---------------------------------------------------------------------------
# Platforms
# ---------------------------------------------------------------------------
def platforms():
    blk = block_rise()
    W, H = 2560, 1440
    safe = ((W - 1546) / 2, (H - 423) / 2, 1546, 423)
    zones = [((W - 1546) // 2, (H - 423) // 2, 1546, 423, 'safe on all devices 1546x423', '#e0261e'),
             ((W - 2560) // 2, (H - 423) // 2, 2560, 423, 'desktop max 2560x423', '#1e88ff'),
             ((W - 1855) // 2, (H - 423) // 2, 1855, 423, 'tablet 1855x423', '#12a150')]
    job('YouTube/antihero-youtube-banner_2560x1440.png', W, H, page_html(W, H, bg('rise-above'), blk, safe, bg_pos='center 55%'),
        page_html(W, H, bg('rise-above'), blk, safe, bg_pos='center 55%', overlay=guide_overlay(W, H, zones)))
    thumb = f"""<style>.yt{{position:absolute;inset:0}}
.yt .t1{{position:absolute;left:70px;top:110px;font-size:170px;padding:18px 24px 18px 28px}}
.yt .t2{{position:absolute;left:70px;top:330px;font-size:170px;padding:18px 24px 18px 28px}}
.yt .t3{{position:absolute;left:74px;top:548px;font-family:'Barlow Condensed';font-weight:800;font-size:40px;letter-spacing:.2em;padding:10px 18px;background:rgba(10,10,11,.8)}}
.yt .face{{position:absolute;right:60px;top:60px;width:420px;height:600px;border:4px dashed rgba(10,10,11,.45);
display:grid;place-items:center;font:700 24px 'JetBrains Mono';color:rgba(10,10,11,.6);text-align:center}}</style>
<div class="yt"><span class="lbl blk t1">AI BUILT MY</span><span class="lbl red t2">WHOLE BRAND</span>
<div class="t3">IN ONE AFTERNOON</div><div class="face">YOUR PHOTO<br>(cut-out)</div></div>"""
    job('YouTube/antihero-youtube-thumbnail-template_1280x720.png', 1280, 720,
        f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}body{{width:1280px;height:720px}}</style></head>
<body><div class="bg" style="background-image:url('{bg('first-light')}')"></div>{thumb}</body></html>""")
    W, H = 1584, 396
    job('LinkedIn/antihero-linkedin-banner_1584x396.png', W, H, page_html(W, H, bg('rise-above'), blk, (470, 40, 1060, 316), bg_pos='center 52%'))
    W, H = 1128, 191
    job('LinkedIn/antihero-linkedin-company-cover_1128x191.png', W, H, page_html(W, H, bg('rise-above'), blk, (150, 14, 828, 163), bg_pos='center 52%'))
    W, H = 1500, 500
    job('X-Twitter/antihero-x-header_1500x500.png', W, H, page_html(W, H, bg('first-light'), blk, (330, 70, 1000, 360), bg_pos='center 45%'))
    for name, b, pos in [('first-light', 'first-light', 'center 48%'), ('rise-above', 'rise-above', 'center 55%')]:
        html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}body{{width:1920px;height:1080px}}
.wm{{position:absolute;right:90px;top:80px}}.tg{{position:absolute;right:92px;top:186px;font-family:'Barlow Condensed';font-weight:700;
font-size:24px;letter-spacing:.3em;color:var(--void);margin-right:-.3em}}</style></head><body>
<div class="bg" style="background-image:url('{bg(b)}');background-position:{pos}"></div>
<div class="wm">{wordmark_svg(C['void'], C['ignition'], 84)}</div><div class="tg">BE YOUR OWN HERO</div></body></html>"""
        job(f'Video-Call/antihero-zoom-background-{name}_1920x1080.png', 1920, 1080, html)
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}body{{width:1200px;height:300px}}
.row{{position:absolute;inset:0;display:flex;align-items:center;gap:44px;padding:0 60px}}
.col{{display:flex;flex-direction:column;gap:22px}}
.d{{font-family:'Barlow Condensed';font-weight:700;font-size:30px;letter-spacing:.24em;color:var(--void)}}</style></head><body>
<div class="bg" style="background-image:url('{bg('daybreak')}');background-position:center 70%"></div>
<div class="row">{badge_inline(200)}<div class="col">{wordmark_svg(C['void'], C['ignition'], 92)}<div class="d">{DESC}</div></div></div></body></html>"""
    job('Email/antihero-email-signature_1200x300.png', 1200, 300, html)
    job('Web/antihero-og-share_1200x630.png', 1200, 630, page_html(1200, 630, bg('rise-above'), blk, (70, 50, 1060, 530), bg_pos='center 55%'))


def archive_old():
    """Move the v1 dark concepts out of the way (kept, not deleted)."""
    arch = os.path.join(OUT, '_previous-dark-set')
    for sub in ['Facebook/Page-Cover', 'Facebook/Group-Cover', 'Facebook/Event-Cover', 'Facebook/Page-Cover/_safe-zone-guides',
                'Facebook/Group-Cover/_safe-zone-guides']:
        d = os.path.join(OUT, sub)
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if any(c in fn for c in ('-label_', '-signal_', '-manifesto_')) and fn.endswith('.png'):
                dst = os.path.join(arch, sub)
                os.makedirs(dst, exist_ok=True)
                shutil.move(os.path.join(d, fn), os.path.join(dst, fn))


if __name__ == '__main__':
    which = sys.argv[1:] or ['archive_old', 'facebook', 'posts', 'platforms']
    for w in which:
        globals()[w]()
    with Renderer() as r:
        for hp, png, W, H in S.JOBS:
            r.png(hp, png, W, H, wait_ms=80)
    print('rendered', len(S.JOBS))
