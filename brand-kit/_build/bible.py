"""AntiHero Brand Bible: designed HTML pages (11 x 8.5 in landscape) -> PDF + page PNGs."""
import os
import sys

from brand import C, KIT, FONTS, font_face_css, mark_group, HERO_PATH, A_PATH
from family import KR_D, KR_VB

HERE = os.path.dirname(os.path.abspath(__file__))
BD = os.path.join(KIT, '01_Brand-Bible')
FONT_REL = os.path.relpath(FONTS, BD).replace(os.sep, '/')
WEB = '--web' in sys.argv            # web build: Google Fonts instead of local files (for publishing)

RED, VOID, CARBON, BONE, ASH, GRAPHITE, EMBER, DUSK = (C['ignition'], C['void'], C['carbon'], C['bone'], C['ash'],
                                                         C['graphite'], C['ember'], C['dusk'])


def badge(size, disc=CARBON, mark='#fff'):
    return (f'<svg viewBox="0 0 1000 1000" width="{size}" height="{size}" aria-hidden="true">'
            f'<circle cx="500" cy="500" r="500" fill="{disc}"/>{mark_group(mark)}</svg>')


def mark(width, col='#fff', hero=None, extra=''):
    return f'<svg viewBox="114 113 785 773" width="{width}" aria-hidden="true" {extra}>{mark_group(col, hero)}</svg>'


FONTS_CSS = ("@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400"
             "&family=Barlow+Condensed:wght@500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');"
             if WEB else font_face_css(FONT_REL))

CSS = FONTS_CSS + """
:root{--void:%(VOID)s;--carbon:%(CARBON)s;--graphite:%(GRAPHITE)s;--ash:%(ASH)s;--bone:%(BONE)s;--red:%(RED)s;--ember:%(EMBER)s;--dusk:%(DUSK)s}
@page{size:11in 8.5in;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html{background:#141517}
body{font-family:'Barlow',system-ui,sans-serif;color:#fff;-webkit-font-smoothing:antialiased;font-size:13.5px;line-height:1.5}
.page{width:1056px;height:816px;position:relative;overflow:hidden;background:var(--void);padding:74px 72px 60px;break-after:page;page-break-after:always}
.page.light{background:var(--bone);color:var(--void)}
.page.red{background:var(--red)}
@media screen{body{padding:32px 0}.page{margin:0 auto 32px;box-shadow:0 20px 60px rgba(0,0,0,.5)}}
.hdr{position:absolute;top:30px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center;
     font-family:'Barlow Condensed';font-weight:700;font-size:11px;letter-spacing:.26em;opacity:.62}
.hdr .pn{font-family:'JetBrains Mono';font-weight:400;letter-spacing:.06em}
.lbl{font-family:'Bebas Neue';font-weight:400;line-height:1;text-box:trim-both cap alphabetic;display:inline-block;
     background:#fff;color:var(--void);white-space:nowrap;padding:.14em .2em .14em .22em}
.lbl.r{background:var(--red);color:#fff}.lbl.k{background:var(--void);color:#fff}
.eyebrow{font-family:'Barlow Condensed';font-weight:700;font-size:12px;letter-spacing:.28em;color:var(--red);text-transform:uppercase}
h1,h2,h3{font-family:'Bebas Neue';font-weight:400;line-height:.92;letter-spacing:.005em}
h1{font-size:92px}h2{font-size:58px}h3{font-size:26px;letter-spacing:.02em}
h1 em,h2 em,h3 em{font-style:normal;color:var(--red)}
p{max-width:62ch;text-wrap:pretty}
.lead{font-size:18px;line-height:1.45;font-weight:500;max-width:52ch}
.muted{opacity:.72}
.mono{font-family:'JetBrains Mono',monospace}
.small{font-size:11.5px;line-height:1.5}
.grid{display:grid;gap:22px}
.rule{height:1px;background:currentColor;opacity:.16}
.cap{font-family:'Barlow Condensed';font-weight:700;font-size:11px;letter-spacing:.2em;text-transform:uppercase;opacity:.75;margin-top:8px}
img{display:block;max-width:100%}
.sec-num{font-family:'JetBrains Mono';font-size:13px;color:var(--red);letter-spacing:.08em}
.chip{display:inline-block;font-family:'JetBrains Mono';font-size:10.5px;padding:3px 7px;border:1px solid currentColor;opacity:.8}
.do,.dont{padding:14px 16px;border-left:3px solid}
.do{border-color:#7fd08a}.dont{border-color:var(--red)}
.do b,.dont b{font-family:'Barlow Condensed';letter-spacing:.2em;font-size:11px;display:block;margin-bottom:4px}
table{border-collapse:collapse;width:100%}
td,th{text-align:left;padding:7px 10px 7px 0;border-bottom:1px solid rgba(255,255,255,.12);font-size:12.5px;vertical-align:top}
.light td,.light th{border-color:rgba(0,0,0,.12)}
th{font-family:'Barlow Condensed';font-weight:700;letter-spacing:.18em;font-size:10.5px;text-transform:uppercase;opacity:.7}
.tile{background:var(--carbon);display:grid;place-items:center;position:relative}
.checker{background-color:#d9d6cf;background-image:linear-gradient(45deg,#c9c5bd 25%%,transparent 25%%,transparent 75%%,#c9c5bd 75%%),
         linear-gradient(45deg,#c9c5bd 25%%,transparent 25%%,transparent 75%%,#c9c5bd 75%%);background-size:16px 16px;background-position:0 0,8px 8px}
.x{position:absolute;top:8px;right:8px;width:22px;height:22px;border-radius:50%%;background:var(--red);color:#fff;display:grid;place-items:center;
   font:700 13px 'Barlow'}
.ok{position:absolute;top:8px;right:8px;width:22px;height:22px;border-radius:50%%;background:#2f8f45;color:#fff;display:grid;place-items:center;font:700 13px 'Barlow'}
"""
for _k, _v in dict(VOID=VOID, CARBON=CARBON, GRAPHITE=GRAPHITE, ASH=ASH, BONE=BONE, RED=RED, EMBER=EMBER, DUSK=DUSK).items():
    CSS = CSS.replace('%(' + _k + ')s', _v)
CSS = CSS.replace('%%', '%')

PAGES = []


def page(body, cls='', title=''):
    PAGES.append((cls, title, body))


def hdr(title):
    return f'<div class="hdr"><span>ANTIHERO / BRAND BIBLE</span><span>{title}</span><span class="pn">{{PN}}</span></div>'


def section_opener(num, title, sub, bg='bg-rise-above.jpg', pos='center 55%'):
    """v2: bright scene, title set as black label boxes (dark type over an inspiring image)."""
    page(f"""<div style="position:absolute;inset:0;background:url(assets/{bg}) {pos}/cover"></div>
<div style="position:relative;height:100%;display:flex;flex-direction:column;justify-content:flex-end;align-items:flex-start;padding-bottom:34px">
<span class="lbl r" style="font-size:17px;letter-spacing:.22em;padding:.4em .6em .35em .8em">SECTION {num}</span>
<span class="lbl k" style="font-size:150px;margin-top:10px">{title}</span>
<p class="lead" style="margin-top:12px;background:rgba(10,10,11,.82);padding:14px 18px;color:#fff;max-width:60ch">{sub}</p></div>""",
         title=title)


# ---------------------------------------------------------------------------
# COVER
page(f"""<div style="position:absolute;inset:0;background:url(assets/bg-rise-above.jpg) 62% 50%/cover"></div>
<div style="position:relative;height:100%;display:flex;flex-direction:column;align-items:flex-start;justify-content:center">
<div style="margin-bottom:30px">{badge(180)}</div>
<span class="lbl k" style="font-size:118px">ANTIHERO</span>
<span class="lbl k" style="font-size:34px;letter-spacing:.06em">AI &middot; BRANDING &middot; SEO &middot; ENTREPRENEURSHIP</span>
<span class="lbl r" style="font-size:22px;letter-spacing:.18em;padding:.3em .5em .3em .66em;margin-top:24px">BRAND BIBLE</span>
<div class="mono" style="position:absolute;bottom:30px;left:0;font-size:11px;letter-spacing:.14em;color:var(--void);background:rgba(236,232,225,.85);padding:6px 10px">VERSION 2.0 &middot; SEPTEMBER 2026 &middot; BE YOUR OWN HERO</div></div>""",
     title='Cover')

# CONTENTS
toc = [('01', 'Story', 'Where AntiHero came from, and the rebuild'), ('02', 'Positioning', 'Mission, audience, pillars, the anti-hero idea'),
       ('03', 'Voice', 'How we sound, words we use, messaging, launch copy'), ('04', 'Logo', 'Badge, construction, versions, clear space, misuse'),
       ('05', 'Color', 'Palette, proportions, contrast'), ('06', 'Type', 'Fonts, hierarchy, the label system'),
       ('07', 'Imagery', 'Graphic devices, open-sky imagery, backgrounds, textures'), ('08', 'In the wild', 'Facebook, templates, platforms, merch'),
       ('09', 'The family', 'KR8TIV, KR8TIV AI, and the give-first ladder')]
rows = ''.join(f"""<div style="display:grid;grid-template-columns:70px 1fr 1.4fr;align-items:baseline;padding:13px 0;border-bottom:1px solid rgba(255,255,255,.12)">
<span class="sec-num">{n}</span><span style="font-family:'Bebas Neue';font-size:40px;line-height:1">{t}</span><span class="muted">{d}</span></div>""" for n, t, d in toc)
page(f"""{hdr('Contents')}<div class="grid" style="grid-template-columns:300px 1fr;gap:70px;height:100%;align-items:center">
<div><h1>WHAT&rsquo;S<br><em>INSIDE</em></h1><p class="muted" style="margin-top:22px">Everything needed to make AntiHero look and sound like itself: on Facebook, in a slide deck, on a shirt, or in a client proposal.</p></div>
<div>{rows}</div></div>""", title='Contents')

# ONE-PAGE SUMMARY
page(f"""{hdr('The short version')}<div class="eyebrow">If you read one page</div><h1 style="margin-top:12px">THE SHORT <em>VERSION</em></h1>
<div class="grid" style="grid-template-columns:repeat(4,1fr);margin-top:44px;gap:26px">
<div><div class="sec-num">WHAT</div><h3 style="margin:10px 0 8px">AN AI + ENTREPRENEURSHIP CREW</h3><p class="small muted">A free community that teaches AI tools, branding, and SEO, plus hands-on consulting for businesses that want it done with them.</p></div>
<div><div class="sec-num">WHY</div><h3 style="margin:10px 0 8px">BE YOUR OWN HERO</h3><p class="small muted">Nobody is coming to build your business for you. With the right tools, one person can do what used to take a team.</p></div>
<div><div class="sec-num">LOOK</div><h3 style="margin:10px 0 8px">OPEN SKY, DARK TYPE, ONE RED</h3><p class="small muted">The circle-A badge. Black label boxes over bright, first-light skies. Ignition Red for exactly one idea per layout.</p></div>
<div><div class="sec-num">SOUND</div><h3 style="margin:10px 0 8px">STRAIGHT TALK</h3><p class="small muted">Plain words, dry humor, receipts over hype. No exclamation points. No gurus.</p></div></div>
<div style="display:flex;gap:18px;margin-top:56px;align-items:center">{badge(120)}<img src="assets/wordmark-white-ignition_2048px.png" style="height:74px">
<div style="margin-left:auto;display:flex;gap:0">{''.join(f'<span style="width:58px;height:74px;background:{c}"></span>' for c in [VOID, CARBON, GRAPHITE, ASH, BONE, '#fff', RED])}</div></div>""",
     title='Summary')

# ---------------------------------------------------------------------------
section_opener('01', 'STORY', 'AntiHero started as a fitness, travel, and lifestyle channel. The badge was always bigger than the niche.', 'bg-rise-above.jpg', '65% 50%')

page(f"""{hdr('01 Story')}<div class="grid" style="grid-template-columns:1fr 1fr;gap:56px;height:100%">
<div><div class="eyebrow">Where this came from</div><h2 style="margin:12px 0 22px">LIFE IS SHORT.<br><em>MAKE IT MAGICAL.</em></h2>
<p>That was the line on the original AntiHero channel art: white label boxes stacked over a dark, sun-bleached beach. It covered fitness, travel, lifestyle, and drones.</p>
<p style="margin-top:12px">The badge did the real work. A circle-A that trades half its ring for the word <i>hero</i>. It said: you don&rsquo;t have to wait for one. You can be one, on your own terms.</p>
<p style="margin-top:12px">AntiHero now trains a different muscle: AI tools, branding, search, and the unglamorous work of building a business. Same attitude. New weights.</p></div>
<div style="display:flex;flex-direction:column;justify-content:center;gap:14px"><img src="assets/heritage-channel.jpg" style="width:100%;border:1px solid rgba(255,255,255,.15)">
<div class="cap">The original channel art: the label-box system starts here</div>
<div style="display:flex;gap:14px;align-items:center;margin-top:18px"><img src="assets/heritage-logo-original.png" style="width:120px;border-radius:50%">
<p class="small muted">The original badge, recovered from a 337&thinsp;px screenshot. Every visual in this bible grows from these two pieces.</p></div></div></div>""", title='01 Story')

page(f"""{hdr('01 Story')}<div class="eyebrow">The rebuild</div><h2 style="margin:12px 0 10px">FROM A BLURRY SCREENSHOT <em>TO CLEAN VECTOR</em></h2>
<p class="muted">The only surviving copy of the logo was a small, compressed avatar. It has been rebuilt: the circle-A from measured geometry, the lettering traced and redrawn as smooth curves. It now scales from a 16&thinsp;px favicon to a billboard.</p>
<div class="grid" style="grid-template-columns:1fr 1fr 1fr;gap:22px;margin-top:30px">
<div><img src="assets/heritage-logo-original-zoom.png" style="width:100%;aspect-ratio:1;object-fit:cover;image-rendering:auto"><div class="cap">Before: original, enlarged</div></div>
<div><img src="assets/rebuild-zoom.png" style="width:100%;aspect-ratio:1;object-fit:cover"><div class="cap">After: rebuilt vector, same crop</div></div>
<div style="background:var(--carbon);display:grid;place-items:center">{badge(250)}<div class="cap" style="position:absolute;margin-top:290px"></div></div></div>
<div class="grid" style="grid-template-columns:repeat(3,1fr);gap:22px;margin-top:18px">
<p class="small muted"><b style="color:#fff">Faithful.</b> The rebuilt mark matches the original within 0.6% of its pixels, so it reads as the same logo.</p>
<p class="small muted"><b style="color:#fff">Systematic.</b> One stroke weight everywhere (0.158 of the radius), and a diagonal fixed at 24.7&deg;.</p>
<p class="small muted"><b style="color:#fff">Master files.</b> SVG in <span class="mono">02_Logos</span>, plus PNGs up to 8192&thinsp;px for print and signage.</p></div>""", title='01 Story')

# ---------------------------------------------------------------------------
section_opener('02', 'POSITIONING', 'What AntiHero is, who it is for, and what it refuses to become.', 'bg-first-light.jpg', 'center 40%')

page(f"""{hdr('02 Positioning')}<div class="grid" style="grid-template-columns:1.1fr 1fr;gap:60px">
<div><div class="eyebrow">Mission</div><h2 style="margin:12px 0 20px">GIVE ORDINARY PEOPLE THE TOOLS, THE SKILLS, AND THE NERVE TO BUILD <em>ON THEIR OWN TERMS.</em></h2>
<div class="rule" style="margin:26px 0"></div>
<div class="grid" style="grid-template-columns:1fr 1fr;gap:26px">
<div><h3>THE GROUP</h3><p class="small muted" style="margin-top:6px">A free community on Facebook. Weekly AI tool breakdowns, live workshops, prompt swaps, and build-in-public threads. Beginners welcome.</p></div>
<div><h3>CONSULTING</h3><p class="small muted" style="margin-top:6px">Hands-on help for businesses: branding, SEO and Google Business Profile, AI systems and automations, and getting the basics set up properly. Done-for-you builds go to the sister studios, KR8TIV and KR8TIV AI (section 09).</p></div></div></div>
<div><div class="eyebrow">Who it is for</div>
<p class="lead" style="margin:12px 0 18px">Solo founders, side-hustlers, tradespeople going out on their own, creators, and small-business owners who are tired of paying for hype.</p>
<table><tr><th>We are for</th><th>We are against</th></tr>
<tr><td>Doing it yourself, with better tools</td><td>Waiting for permission</td></tr>
<tr><td>Showing the prompt, the steps, the numbers</td><td>Guru culture and screenshot flexing</td></tr>
<tr><td>Free basics, shared in the open</td><td>Paywalled common sense</td></tr>
<tr><td>Slow, honest growth</td><td>&ldquo;Passive income&rdquo; fairy tales</td></tr>
<tr><td>Beginners asking questions</td><td>Gatekeeping and dunking</td></tr></table></div></div>""", title='02 Positioning')

page(f"""{hdr('02 Positioning')}<div class="grid" style="grid-template-columns:420px 1fr;gap:64px;height:100%;align-items:center">
<div><div class="eyebrow">The anti-hero idea</div><h1 style="margin-top:12px">HEROES WAIT FOR THE CALL. <em>ANTI-HEROES ANSWER THEIR OWN.</em></h1></div>
<div><p class="lead">The internet is full of people selling you a savior: the course, the guru, the secret. AntiHero is the opposite. Nobody here is going to save you, and that is the good news.</p>
<p style="margin-top:16px" class="muted">You are the main character. The group is the crew: people learning in public, sharing what works, and pulling the next person up. AI is the new gear: it gives one person the reach of a small team, if they learn to use it.</p>
<p style="margin-top:16px" class="muted">The badge says it without words. The circle-A is the old sign for going your own way. Half the circle is missing, and the word <i>hero</i> completes it. The story isn&rsquo;t finished until you write yourself into it.</p>
<div style="display:flex;gap:26px;align-items:center;margin-top:28px">{mark(120, '#fff', RED)}<span class="lbl" style="font-size:40px">YOU COMPLETE THE CIRCLE.</span></div></div></div>""", title='02 Positioning')

pillars = [('OWN YOUR STORY', 'Agency over everything. Nobody is coming. Good. Every post ends with something the reader can do today.'),
           ('TOOLS OVER TALK', 'Show the prompt, the workflow, and the result. Practical beats inspirational, every time.'),
           ('STRAIGHT TALK', 'No hype, no fake screenshots, no overnight promises. If something is hard or slow, say so.'),
           ('BUILD IN PUBLIC', 'Share the work, the numbers, and the mistakes. The whole group learns faster that way.')]
page(f"""{hdr('02 Positioning')}<div class="eyebrow">Brand pillars</div><h2 style="margin:12px 0 34px">FOUR THINGS WE <em>ALWAYS</em> DO</h2>
<div class="grid" style="grid-template-columns:repeat(4,1fr);gap:0">{''.join(f'''<div style="padding:26px 22px 30px;border-left:1px solid rgba(255,255,255,.14);min-height:360px;display:flex;flex-direction:column">
<span class="sec-num">0{i + 1}</span><h2 style="font-size:46px;margin:16px 0 14px">{t}</h2><p class="muted">{d}</p>
</div>''' for i, (t, d) in enumerate(pillars))}</div>
<p class="small muted" style="margin-top:22px">When in doubt, test a post against the pillars. If it doesn&rsquo;t hand the reader agency, a tool, the truth, or the real work behind it, cut it.</p>""", title='02 Positioning')

# ---------------------------------------------------------------------------
section_opener('03', 'VOICE', 'The friend who has already done it, telling you the truth over coffee.', 'bg-launch.jpg', '70% 40%')

page(f"""{hdr('03 Voice')}<div class="grid" style="grid-template-columns:1fr 1.25fr;gap:56px">
<div><div class="eyebrow">How we sound</div><h2 style="margin:12px 0 22px">DIRECT. DRY. <em>USEFUL.</em></h2>
<table><tr><th>We are</th><th>We are not</th></tr>
<tr><td><b>Direct</b></td><td>Harsh</td></tr><tr><td><b>Dry humor</b></td><td>Snark at beginners</td></tr>
<tr><td><b>Plain words</b></td><td>Jargon and buzzwords</td></tr><tr><td><b>Confident</b></td><td>Cocky or salesy</td></tr>
<tr><td><b>Specific</b></td><td>Vague and motivational</td></tr></table>
<h3 style="margin-top:26px">MECHANICS</h3>
<p class="small muted" style="margin-top:8px">No exclamation points. Oxford comma. Numbers as numerals. Headlines in caps (Bebas Neue), body in sentence case. &ldquo;AI&rdquo; is always capitalized. Say <i>you</i>, not <i>users</i>. Say <i>build</i>, not <i>hustle</i>.</p></div>
<div class="grid" style="gap:12px;align-content:start">
<div class="do"><b>DO</b>Here&rsquo;s the exact prompt I used. Steal it.</div>
<div class="dont"><b>DON&rsquo;T</b>Unlock the secret AI hack 99% of people don&rsquo;t know about!!!</div>
<div class="do"><b>DO</b>This took me three weekends. Here&rsquo;s what broke.</div>
<div class="dont"><b>DON&rsquo;T</b>Make $10K a month on autopilot with this one tool.</div>
<div class="do"><b>DO</b>SEO is slow. Start today anyway.</div>
<div class="dont"><b>DON&rsquo;T</b>Rank #1 on Google overnight, guaranteed.</div>
<div class="grid" style="grid-template-columns:1fr 1fr;gap:18px;margin-top:10px">
<div><h3 style="color:#7fd08a">WORDS WE USE</h3><p class="mono small" style="margin-top:6px">build, ship, tools, test, learn, own, story, plain, real, crew, receipts</p></div>
<div><h3 style="color:var(--red)">WORDS WE AVOID</h3><p class="mono small" style="margin-top:6px">hustle, passive income, guru, crush it, secret, game-changer, revolutionary</p></div></div>
<p class="small muted" style="margin-top:10px">Big numbers need receipts. &ldquo;I wrote 40 product descriptions before lunch&rdquo; beats any multiplier. Keep it fun: the work is serious, the tone doesn&rsquo;t have to be.</p></div></div>""",
     title='03 Voice')

page(f"""{hdr('03 Voice')}<div class="eyebrow">Messaging</div><h2 style="margin:12px 0 26px">TAGLINES + <em>LINES WE OWN</em></h2>
<div class="grid" style="grid-template-columns:1.1fr 1fr;gap:50px">
<div class="grid" style="gap:14px;align-content:start">
<div><span class="lbl r" style="font-size:50px">BE YOUR OWN HERO.</span><div class="cap">Primary tagline &middot; everywhere</div></div>
<div><span class="lbl" style="font-size:32px">NOBODY&rsquo;S COMING TO SAVE YOU. YOU NEVER NEEDED SAVING.</span><div class="cap">The creed &middot; manifesto posts</div></div>
<div><span class="lbl" style="font-size:32px">THEY DIDN&rsquo;T SEE YOU COMING.</span><div class="cap">Surprise them &middot; launches, member wins</div></div>
<div><span class="lbl" style="font-size:32px">HATE YOUR JOB? GOOD. THAT&rsquo;S YOUR RUNWAY.</span><div class="cap">The way out &middot; career-change posts</div></div>
<div><span class="lbl" style="font-size:32px">BREAK FORMATION.</span><div class="cap">Do it your way &middot; manifesto posts</div></div>
<div><span class="lbl" style="font-size:32px">AI LEVELED THE FIELD. NOW PLAY.</span><div class="cap">Tech is your friend &middot; tool posts, workshops</div></div>
<div><span class="lbl" style="font-size:32px">WRITE YOUR OWN STORY.</span><div class="cap">Community &middot; member wins</div></div>
<div style="display:flex;gap:8px;flex-wrap:wrap"><span class="lbl k" style="font-size:24px;border:1px solid rgba(255,255,255,.3)">BUILD MORE. GRIND LESS.</span><span class="lbl k" style="font-size:24px;border:1px solid rgba(255,255,255,.3)">REMEMBER WHERE YOU CAME FROM. THEN GO FURTHER.</span><span class="lbl k" style="font-size:24px;border:1px solid rgba(255,255,255,.3)">LIFE IS SHORT. MAKE IT MAGICAL.</span></div></div>
<div><h3>DESCRIPTOR</h3><p class="mono small" style="margin:6px 0 18px">AI &middot; BRANDING &middot; SEO &middot; ENTREPRENEURSHIP</p>
<h3>ONE-LINER</h3><p class="small muted" style="margin:6px 0 18px">AntiHero is an AI and entrepreneurship community for people who would rather build than wait.</p>
<h3>BOILERPLATE</h3><p class="small muted" style="margin-top:6px">AntiHero teaches everyday entrepreneurs to use AI tools, build a brand, and get found online. The free AntiHero group runs weekly tool breakdowns, live workshops, and build-in-public threads. AntiHero Consulting helps businesses with branding, SEO, and AI systems, done with them rather than to them. Be your own hero.</p></div></div>""",
     title='03 Voice')

INTRO = 'AI tools, branding, and SEO for people who&rsquo;d rather build than wait. Be your own hero.'
# the group copy has one home (group_kit.py) so the bible and the Group Kit can never disagree
from group_kit import ABOUT as G_ABOUT, QUESTIONS as G_QUESTIONS, RULES as G_RULES  # noqa: E402
G_ABOUT_SHORT = '<br><br>'.join(G_ABOUT.split('\n\n')[:3])
page(f"""{hdr('03 Voice')}<div class="eyebrow">Launch copy &middot; paste-ready</div><h2 style="margin:12px 0 22px">FACEBOOK <em>SETUP TEXT</em></h2>
<div class="grid" style="grid-template-columns:1fr 1fr;gap:44px">
<div><h3>PAGE INTRO <span class="chip" style="margin-left:6px">{len(INTRO.replace('&rsquo;', chr(39)))} / 101 CHARACTERS</span></h3>
<p class="mono small" style="margin:8px 0 20px;padding:12px 14px;background:var(--carbon)">{INTRO}</p>
<h3>GROUP DESCRIPTION</h3>
<p class="small" style="margin:8px 0 0;padding:12px 14px;background:var(--carbon);line-height:1.55">{G_ABOUT_SHORT}</p>
<p class="small muted" style="margin-top:10px">The full version, with the weekly rhythm, is in the Group Kit.</p></div>
<div><h3>GROUP RULES</h3>
<ol style="margin:10px 0 0 18px;display:grid;gap:10px" class="small">
{''.join(f'<li><b>{t}</b> ' + d.split('. ')[0].rstrip('.') + '.</li>' for t, d in G_RULES)}</ol>
<h3 style="margin-top:22px">MEMBERSHIP QUESTIONS</h3>
<ol style="margin:8px 0 0 18px;display:grid;gap:6px" class="small muted">{''.join(f'<li>{q}</li>' for q in G_QUESTIONS)}</ol>
<p class="small" style="margin-top:18px;padding:10px 12px;border-left:3px solid var(--red)">Setup steps, the weekly series, and the first ten posts: <span class="mono">05_Social/Facebook/Group-Kit</span>.</p></div></div>""",
     title='03 Voice')

# ---------------------------------------------------------------------------
section_opener('04', 'LOGO', 'The badge, the mark, the wordmark, and the rules that keep them sharp.', 'bg-daybreak.jpg', 'center')

callouts = [((186, 614), (-95, 614), '1'), ((388, 427), (150, -85), '2'), ((760, 205), (905, -85), '3'), ((850, 820), (1095, 930), '4')]
anatomy = (f'<svg viewBox="-160 -150 1320 1300" width="470" aria-hidden="true"><circle cx="500" cy="500" r="500" fill="{CARBON}"/>{mark_group("#fff")}'
           + ''.join(f'<line x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}" stroke="{RED}" stroke-width="4"/><circle cx="{p[0]}" cy="{p[1]}" r="14" fill="{RED}" stroke="#fff" stroke-width="4"/>'
                     f'<circle cx="{q[0]}" cy="{q[1]}" r="40" fill="{RED}"/><text x="{q[0]}" y="{q[1] + 17}" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="48" fill="#fff">{n}</text>'
                     for p, q, n in callouts) + '</svg>')
page(f"""{hdr('04 Logo')}<div class="grid" style="grid-template-columns:1fr 1fr;gap:50px;height:100%;align-items:center">
<div style="display:grid;place-items:center">{anatomy}</div>
<div><div class="eyebrow">The badge &middot; primary logo</div><h2 style="margin:12px 0 22px">A CIRCLE <em>YOU FINISH</em></h2>
<div class="grid" style="gap:16px">
<div style="display:grid;grid-template-columns:34px 1fr"><span class="sec-num">1</span><p class="small"><b>The open ring.</b> Half a circle. It is waiting for the other half.</p></div>
<div style="display:grid;grid-template-columns:34px 1fr"><span class="sec-num">2</span><p class="small"><b>The A.</b> The circle-A, the old sign for going your own way. The <i>anti</i> in AntiHero.</p></div>
<div style="display:grid;grid-template-columns:34px 1fr"><span class="sec-num">3</span><p class="small"><b>hero.</b> Hand-lettered, human, a little rough. It closes the circle, rotated along the edge like a signature.</p></div>
<div style="display:grid;grid-template-columns:34px 1fr"><span class="sec-num">4</span><p class="small"><b>The disc.</b> Carbon #1D2124, sampled from the original badge. On light grounds it keeps the white mark legible.</p></div></div></div></div>""",
     title='04 Logo')

page(f"""{hdr('04 Logo')}<div class="grid" style="grid-template-columns:560px 1fr;gap:46px;height:100%;align-items:center">
<img src="assets/construction_2400px.png" style="width:560px">
<div><div class="eyebrow">Construction</div><h2 style="margin:12px 0 18px">BUILT ON <em>ONE STROKE</em></h2>
<table><tr><td>Disc radius</td><td class="mono">R</td></tr><tr><td>Every stroke (ring, diagonal, bar)</td><td class="mono">t = 0.158 R</td></tr>
<tr><td>Ring outer / inner radius</td><td class="mono">0.747 R / 0.589 R</td></tr><tr><td>Vertical cut</td><td class="mono">x = &minus;0.014 R</td></tr>
<tr><td>Diagonal</td><td class="mono">24.7&deg; from vertical</td></tr><tr><td>Diagonal axis</td><td class="mono">meets the cut at the inner ring</td></tr>
<tr><td>Crossbar</td><td class="mono">top on the centre line</td></tr><tr><td>Lettering</td><td class="mono">custom, traced + rebuilt</td></tr></table>
<p class="small muted" style="margin-top:16px">Always place the logo from the master files. Never redraw it, and never set <i>hero</i> in a font: no typeface matches it.</p></div></div>""",
     title='04 Logo')

versions = [('badge-carbon_1024px.png', 'Badge', 'Primary. Avatars, stamps, merch, anywhere it stands alone.', CARBON),
            ('mark-white_1024px.png', 'Mark', 'No disc. For dark photos and textures, embossing, engraving.', '#2a2d31'),
            ('wordmark-white-ignition_2048px.png', 'Wordmark', 'ANTI + hero. Headers, sign-offs, footers.', VOID),
            ('wordmark-caps-white_2048px.png', 'Caps wordmark', 'When the script would be too small (under 24 px tall).', VOID),
            ('wordmark-label-white_2048px.png', 'Label', 'The heritage label box. Covers, thumbnails, stickers.', '#2a2d31'),
            ('lockup-horizontal-on-dark-ignition_2048px.png', 'Horizontal lockup', 'Websites, email headers, slide footers.', VOID),
            ('lockup-stacked-on-dark-ignition_1500px.png', 'Stacked lockup', 'Posters, title slides, merch backs.', VOID),
            ('app-icon-rounded_512px.png', 'App icon', 'Square containers: app, PWA, favicon masters.', '#2a2d31')]
page(f"""{hdr('04 Logo')}<div class="eyebrow">The family</div><h2 style="margin:12px 0 20px">ONE MARK, <em>EIGHT JOBS</em></h2>
<div class="grid" style="grid-template-columns:repeat(4,1fr);gap:14px">{''.join(f'''<div><div class="tile" style="height:150px;background:{bgc}"><img src="assets/{f}" style="max-height:108px;max-width:82%"></div>
<h3 style="margin-top:10px;font-size:22px">{t}</h3><p class="small muted">{d}</p></div>''' for f, t, d, bgc in versions)}</div>""", title='04 Logo')

cw = [('badge-carbon_1024px.png', VOID, 'Carbon', 'Default on dark'), ('badge-black_1024px.png', BONE, 'Black', 'Default on light'),
      ('badge-white_1024px.png', CARBON, 'White', 'Reversed, dark UI'), ('badge-ignition_1024px.png', VOID, 'Ignition', 'Launches, CTAs, merch'),
      ('badge-bone_1024px.png', GRAPHITE, 'Bone', 'Print, warm layouts'), ('badge-outline-white_1024px.png', 'url(assets/bg-first-light.jpg) center/cover', 'Outline', 'Over photography'),
      ('badge-knockout-white_1024px.png', 'url(assets/tex-08-screen-print-tee.jpg) center/cover', 'Knockout', 'Screen print, vinyl, stencil'),
      ('mark-duo-white-ignition_1024px.png', VOID, 'Duo mark', 'Accent moments only')]
page(f"""{hdr('04 Logo')}<div class="eyebrow">Color versions</div><h2 style="margin:12px 0 20px">PICK THE ONE THAT <em>CONTRASTS</em></h2>
<div class="grid" style="grid-template-columns:repeat(4,1fr);gap:14px">{''.join(f'''<div><div class="tile" style="height:170px;background:{bgc}"><img src="assets/{f}" style="max-height:132px"></div>
<h3 style="margin-top:10px;font-size:22px">{t}</h3><p class="small muted">{d}</p></div>''' for f, bgc, t, d in cw)}</div>
<p class="small muted" style="margin-top:14px">Knockout versions are one compound shape: the letters are real holes, so the surface shows through. Use them for single-color printing, vinyl cutting, and laser work.</p>""",
     title='04 Logo')

page(f"""{hdr('04 Logo')}<div class="grid" style="grid-template-columns:470px 1fr;gap:54px;height:100%;align-items:center">
<img src="assets/clearspace_2400px.png" style="width:470px">
<div><div class="eyebrow">Clear space + minimum size</div><h2 style="margin:12px 0 18px">GIVE IT <em>A QUARTER</em></h2>
<p>Keep a clear margin of one quarter of the badge&rsquo;s diameter on every side. No text, edges, or other logos inside it.</p>
<div class="grid" style="grid-template-columns:repeat(3,1fr);gap:18px;margin-top:26px;align-items:end">
<div>{badge(96)}<div class="cap">Badge &ge; 24 px / 10 mm</div></div>
<div><img src="assets/wordmark-white-ignition_2048px.png" style="height:38px"><div class="cap">Wordmark &ge; 18 px tall</div></div>
<div style="display:flex;gap:10px;align-items:end"><img src="assets/favicon-32.png" style="width:32px"><img src="assets/favicon-64.png" style="width:64px"><div class="cap" style="margin:0">Favicons</div></div></div>
<p class="small muted" style="margin-top:22px">Under 32 px, use the files in <span class="mono">02_Logos/05_Icons</span>. They are rendered at native size so the lettering stays readable.</p></div></div>""",
     title='04 Logo')

# misuse
K = 'https://fonts.googleapis.com'
def mis(inner, label, bg=CARBON):
    return f'<div><div class="tile" style="height:150px;background:{bg};overflow:hidden">{inner}<span class="x">&times;</span></div><p class="small" style="margin-top:8px"><b>{label}</b></p></div>'


mis_tiles = [
    mis(f'<div style="transform:scaleX(1.55)">{badge(104)}</div>', "Don't stretch or squash it."),
    mis(f'<div style="transform:rotate(90deg)">{badge(104)}</div>', "Don't rotate it to straighten &ldquo;hero&rdquo;."),
    mis(f'''<svg viewBox="0 0 1000 1000" width="104" height="104"><circle cx="500" cy="500" r="500" fill="{CARBON}"/><path fill="#fff" fill-rule="evenodd" d="{A_PATH}"/>
<text x="560" y="140" transform="rotate(90 560 140)" font-family="Georgia,serif" font-style="italic" font-size="240" fill="#fff">hero</text></svg>''',
        "Don't retype &ldquo;hero&rdquo; in a font."),
    mis(f'<div style="filter:drop-shadow(0 0 14px #39ff14) drop-shadow(6px 8px 0 #ffd400)">{badge(104)}</div>', "Don't add glows, bevels, or shadows."),
    mis(f'''<svg viewBox="0 0 1000 1000" width="104" height="104"><circle cx="500" cy="500" r="500" fill="#2d5bff"/>{mark_group('#ffd400', '#39ff14')}</svg>''',
        "Don't use colors outside the palette."),
    mis(f'<div style="opacity:.9">{mark(110, "#8A9096")}</div>', "Don't place it on busy, low-contrast images.", 'url(assets/tex-01-concrete-stencil.jpg) center/cover'),
    mis('<img src="assets/wordmark-white-ignition_2048px.png" style="width:78%">', "Don't put the red wordmark on red.", RED),
    mis(f'<div style="width:104px;height:104px;overflow:hidden;border-radius:4px"><div style="margin:-34px 0 0 -40px">{badge(190)}</div></div>',
        "Don't crop the badge or clip the ring."),
]
page(f"""{hdr('04 Logo')}<div class="eyebrow">Misuse</div><h2 style="margin:12px 0 20px">EIGHT WAYS <em>TO BREAK IT</em></h2>
<div class="grid" style="grid-template-columns:repeat(4,1fr);gap:16px 14px">{''.join(mis_tiles)}</div>""", title='04 Logo')

# ---------------------------------------------------------------------------
section_opener('05', 'COLOR', 'Black and white do the talking. Red makes one point, once.', 'bg-break-formation.jpg', '60% 40%')

pal = [('ANTI BLACK', VOID, '#0A0A0B', '10 10 11', 'Black 6 C', 'Primary ground'), ('CARBON', CARBON, '#1D2124', '29 33 36', '419 C', 'Badge disc, panels'),
       ('GRAPHITE', GRAPHITE, '#2B3035', '43 48 53', '432 C', 'Raised surfaces'), ('ASH', ASH, '#8A9096', '138 144 150', 'Cool Gray 8 C', 'Secondary text, lines'),
       ('BONE', BONE, '#ECE8E1', '236 232 225', 'Warm Gray 1 C tint', 'Light grounds, print'), ('HERO WHITE', '#FFFFFF', '#FFFFFF', '255 255 255', '-', 'Mark, labels, headlines'),
       ('IGNITION RED', RED, '#E0261E', '224 38 30', '485 C', 'The one accent'), ('EMBER', EMBER, '#A3160F', '163 22 15', '7621 C', 'Pressed state only'),
       ('DUSK', DUSK, '#5B4F48', '91 79 72', '7531 C', 'Photo duotone mid')]
page(f"""{hdr('05 Color')}<div class="eyebrow">Palette</div><h2 style="margin:12px 0 18px">NINE COLORS. <em>ONE ACCENT.</em></h2>
<div class="grid" style="grid-template-columns:repeat(9,1fr);gap:0;height:380px">{''.join(f'''<div style="background:{bg};color:{'#0A0A0B' if n in ('BONE', 'HERO WHITE', 'ASH') else '#fff'};padding:14px 11px;display:flex;flex-direction:column;justify-content:space-between;outline:1px solid rgba(255,255,255,.08)">
<div style="font-family:'Bebas Neue';font-size:25px;line-height:.95">{n}</div><div class="mono" style="font-size:9.5px;line-height:1.55">{hx}<br>RGB {rgbv}<br>PMS {pms}<br><span style="opacity:.8">{role}</span></div></div>''' for n, bg, hx, rgbv, pms, role in pal)}</div>
<div style="margin-top:26px"><div class="cap" style="margin-bottom:8px">Proportion &middot; a typical layout</div>
<div style="display:flex;height:34px"><div style="flex:62;background:{VOID};outline:1px solid rgba(255,255,255,.15)"></div><div style="flex:16;background:{CARBON}"></div>
<div style="flex:12;background:#fff"></div><div style="flex:6;background:{ASH}"></div><div style="flex:4;background:{RED}"></div></div>
<div class="grid" style="grid-template-columns:62fr 16fr 12fr 6fr 4fr;gap:0" ><span class="mono small">62% black</span><span class="mono small">16% carbon</span><span class="mono small">12% white</span><span class="mono small">6%</span><span class="mono small" style="color:var(--red)">4%</span></div></div>
<p class="small muted" style="margin-top:12px">Files: <span class="mono">07_Color</span> has the Adobe swatch file (.ase), CSS variables, JSON tokens, and a GIMP palette. Pantone values are nearest matches: check them against a swatch book before printing.</p>""",
     title='05 Color')

pairs = [('#FFFFFF', RED, 'White on Ignition', '4.7 : 1', 'AA', 'Label boxes, buttons'),
         (RED, VOID, 'Ignition on Anti Black', '4.2 : 1', 'AA large', 'Headlines 24 px and up'),
         ('#FFFFFF', VOID, 'White on Anti Black', '19.8 : 1', 'AAA', 'Everything'),
         (ASH, VOID, 'Ash on Anti Black', '6.1 : 1', 'AA', 'Captions, meta'),
         (VOID, BONE, 'Anti Black on Bone', '16.2 : 1', 'AAA', 'Print body copy'),
         (RED, BONE, 'Ignition on Bone', '3.9 : 1', 'AA large', 'Big accents only'),
         (RED, CARBON, 'Ignition on Carbon', '3.4 : 1', 'Large only', 'Accents, not text')]
page(f"""{hdr('05 Color')}<div class="grid" style="grid-template-columns:1fr 1.25fr;gap:56px">
<div><div class="eyebrow">Rules</div><h2 style="margin:12px 0 20px">THE <em>ONE RED THING</em> RULE</h2>
<p>Every layout gets one red idea: a word, a button, a label, or the <i>hero</i> in the wordmark. Two red things compete. Zero is fine.</p>
<ul style="margin:18px 0 0 18px;display:grid;gap:8px" class="small">
<li>Pair a bright, open scene with dark type: black label boxes and panels over light imagery, white boxes over dark grounds.</li>
<li>Red is never a background for long text, and never a full-page wash.</li>
<li>On red, everything is white: the wordmark too.</li><li>Keep photography bright and natural. If the picture already carries red (the balloon, the red plane), the red tag may echo it; nothing else goes red.</li>
<li>Ember only appears as a pressed or hover state.</li></ul></div>
<div><div class="eyebrow">Contrast (WCAG 2.1)</div><table style="margin-top:12px">{''.join(f'''<tr><td style="width:64px"><span style="display:inline-grid;place-items:center;width:52px;height:30px;background:{bg};color:{fg};font-family:'Bebas Neue';font-size:18px;outline:1px solid rgba(255,255,255,.15)">AH</span></td>
<td>{name}</td><td class="mono" style="white-space:nowrap">{ratio}</td><td style="white-space:nowrap"><span class="chip">{lvl}</span></td><td class="muted">{use}</td></tr>''' for fg, bg, name, ratio, lvl, use in pairs)}</table></div></div>""",
     title='05 Color')

# ---------------------------------------------------------------------------
section_opener('06', 'TYPE', 'A condensed shout, a friendly workhorse, and a terminal for the robots.', 'bg-see-further.jpg', '70% 45%')

page(f"""{hdr('06 Type')}<div class="eyebrow">Typefaces &middot; all free, all in 06_Fonts</div><h2 style="margin:12px 0 22px">FOUR FACES, <em>FOUR JOBS</em></h2>
<div class="grid" style="grid-template-columns:repeat(4,minmax(0,1fr));gap:18px">
<div style="background:var(--carbon);padding:22px;min-height:430px;display:flex;flex-direction:column"><div style="font-family:'Bebas Neue';font-size:130px;line-height:.85">AA</div><div style="font-family:'Bebas Neue';font-size:22px;letter-spacing:.04em;margin-top:14px;opacity:.85;overflow-wrap:anywhere">ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789</div><h3 style="margin-top:auto">BEBAS NEUE</h3><p class="small muted">Display. Headlines, labels, covers. Always uppercase. The same family as the original channel art.</p></div>
<div style="background:var(--carbon);padding:22px;min-height:430px;display:flex;flex-direction:column"><div style="font-size:120px;line-height:.9;font-weight:600">Aa</div><div style="font-size:16px;margin-top:14px;opacity:.85;overflow-wrap:anywhere">Abcdefghijklm nopqrstuvwxyz<br><b>Bold 700</b> &middot; <i>Italic</i> &middot; 0123456789</div><h3 style="margin-top:auto">BARLOW</h3><p class="small muted">Body. Paragraphs, captions, UI. 400 for reading, 600/700 for emphasis.</p></div>
<div style="background:var(--carbon);padding:22px;min-height:430px;display:flex;flex-direction:column"><div style="font-family:'Barlow Condensed';font-weight:800;font-size:120px;line-height:.9">Aa</div><div style="font-family:'Barlow Condensed';font-weight:700;font-size:15px;letter-spacing:.24em;margin-top:14px;opacity:.85;overflow-wrap:anywhere">ABCDEFGHIJKLMNOPQRSTUVWXYZ</div><h3 style="margin-top:auto">BARLOW CONDENSED</h3><p class="small muted">Labels and eyebrows. Bold, uppercase, tracked +20 to 30%.</p></div>
<div style="background:var(--carbon);padding:22px;min-height:430px;display:flex;flex-direction:column"><div style="font-family:'JetBrains Mono';font-size:100px;line-height:1">Aa</div><div class="mono" style="font-size:14px;margin-top:14px;opacity:.85"><b style="color:var(--red)">&gt;</b> abc_ABC {{ }} 0123 =&gt;</div><h3 style="margin-top:auto">JETBRAINS MONO</h3><p class="small muted">Prompts, tool names, numbers, data. The AI voice of the brand.</p></div></div>
<p class="small muted" style="margin-top:18px">Fallbacks when a font can&rsquo;t load: Oswald or Arial Narrow for Bebas Neue, Helvetica or Arial for Barlow, Consolas for JetBrains Mono. In Canva, all four are in the font menu by name.</p>""",
     title='06 Type')

scale = [("Display XL", "Bebas Neue 400", "120 / 0.88", "0", "font-family:'Bebas Neue';font-size:96px;line-height:.88", 'BE YOUR OWN HERO'),
         ("Headline", "Bebas Neue 400", "56 / 0.92", "+0.5%", "font-family:'Bebas Neue';font-size:56px;line-height:.92", 'BREAK FORMATION.'),
         ("Label", "Barlow Condensed 700", "12 / 1.2", "+26%", "font-family:'Barlow Condensed';font-weight:700;font-size:13px;letter-spacing:.26em", 'AI &middot; BRANDING &middot; SEO'),
         ("Lead", "Barlow 500", "20 / 1.45", "0", "font-size:20px;font-weight:500;line-height:1.45", 'Nobody is coming to save your business. Good.'),
         ("Body", "Barlow 400", "15 / 1.5", "0", "font-size:15px;line-height:1.5", 'AI gives one person the reach of a small team, if they learn the tools.'),
         ("Prompt", "JetBrains Mono 400", "14 / 1.55", "0", "font-family:'JetBrains Mono';font-size:14px", '<b style="color:var(--red)">&gt;</b> Write 5 posts for my shop in Edmonton.')]
page(f"""{hdr('06 Type')}<div class="eyebrow">Hierarchy</div><h2 style="margin:12px 0 14px">THE <em>SCALE</em></h2>
<div>{''.join(f'''<div style="display:grid;grid-template-columns:190px 1fr;gap:26px;align-items:center;padding:12px 0;border-bottom:1px solid rgba(255,255,255,.12)">
<div class="mono small"><b style="color:#fff">{n}</b><br><span class="muted">{f}<br>{s} &middot; track {t}</span></div><div style="{css};white-space:nowrap;overflow:hidden">{sample}</div></div>''' for n, f, s, t, css, sample in scale)}</div>""",
     title='06 Type')

page(f"""{hdr('06 Type')}<div class="grid" style="grid-template-columns:1fr 1fr;gap:56px;height:100%;align-items:center">
<div><div class="eyebrow">The signature device</div><h2 style="margin:12px 0 18px">THE <em>LABEL</em> SYSTEM</h2>
<p>Straight from the original channel art: Bebas Neue set on solid boxes and stacked like a warning label. It is the fastest way to make anything look like AntiHero.</p>
<ul style="margin:16px 0 0 18px;display:grid;gap:8px" class="small"><li>Over bright imagery: black boxes with white text. Over dark grounds: white boxes with black text. One red box per layout.</li>
<li>Padding: 0.14 &times; the font size top and bottom, 0.2 left and right.</li><li>Stack boxes flush, with no gap. Let the widths step.</li>
<li>Keep the stack clear of the picture&rsquo;s subject (the balloon, the plane). Left-align on covers and posts.</li><li>Pair with the flanking rules: two hairlines either side of a short line.</li></ul></div>
<div style="background:url(assets/bg-rise-above.jpg) 70% 50%/cover;height:560px;display:flex;flex-direction:column;align-items:flex-start;justify-content:center;padding-left:28px">
<span class="lbl k" style="font-size:92px">ANTIHERO</span><span class="lbl k" style="font-size:24px;letter-spacing:.05em">AI &middot; BRANDING &middot; SEO &middot; ENTREPRENEURSHIP</span>
<span class="lbl r" style="font-size:17px;letter-spacing:.16em;padding:.3em .5em .3em .66em;margin-top:18px">BE YOUR OWN HERO</span>
<div style="display:flex;flex-direction:column;align-items:flex-start;margin-top:46px"><span class="lbl k" style="font-size:32px">YOU ARE THE</span><span class="lbl r" style="font-size:74px">HERO</span><span class="lbl k" style="font-size:32px">OF YOUR OWN STORY.</span></div></div></div>""",
     title='06 Type')

# ---------------------------------------------------------------------------
section_opener('07', 'IMAGERY', 'Open sky, first light, and a little altitude. Dark type does the talking on top.', 'bg-first-light.jpg', 'center 45%')

page(f"""{hdr('07 Imagery')}<div class="eyebrow">Graphic devices</div><h2 style="margin:12px 0 20px">THE <em>TOOLKIT</em></h2>
<div class="grid" style="grid-template-columns:repeat(4,1fr);gap:18px">
<div><div class="tile" style="height:360px;background:url(assets/bg-break-formation.jpg) 76% 22%/260% auto"></div><h3 style="margin-top:10px">THE RED ONE</h3><p class="small muted">One red thing inside the picture (a balloon, a plane, a tag) carries the accent. Everything else stays sky, white, and black.</p></div>
<div><div class="tile" style="height:360px"><div style="display:flex;align-items:center;gap:10px"><span style="width:44px;height:2px;background:#fff"></span><span class="lbl" style="font-size:18px;letter-spacing:.16em">SHORT LINE</span><span style="width:44px;height:2px;background:#fff"></span></div></div><h3 style="margin-top:10px">FLANKING RULES</h3><p class="small muted">Two hairlines either side of a short line, from the original banner.</p></div>
<div><div class="tile" style="height:360px"><div class="mono" style="font-size:15px"><b style="color:var(--red)">&gt;</b> build your own<span style="display:inline-block;width:9px;height:17px;background:var(--red);vertical-align:-3px;margin-left:4px"></span></div></div><h3 style="margin-top:10px">THE PROMPT LINE</h3><p class="small muted">Mono text, a red caret, and a block cursor. Marks anything AI.</p></div>
<div><div class="tile" style="height:360px;background:url(assets/bg-first-light.jpg) center 45%/cover"></div><h3 style="margin-top:10px">FIRST LIGHT</h3><p class="small muted">Sunrise above the clouds: the old sunset banner, reborn as a morning. The brand&rsquo;s signature backdrop.</p></div></div>""",
     title='07 Imagery')

page(f"""{hdr('07 Imagery')}<div class="grid" style="grid-template-columns:1fr 1.35fr;gap:44px">
<div><div class="eyebrow">Imagery direction</div><h2 style="margin:12px 0 16px">RISE ABOVE, <em>LIGHT FIRST</em></h2>
<p class="small">Every picture should feel like a morning: open sky, altitude, and a sense of getting out. The metaphors are flight and freedom: rising, launching, leaving the formation, seeing further.</p>
<div class="grid" style="gap:10px;margin-top:14px">
<div class="do"><b>SHOOT + USE</b>Sunrise skies, cloud seas, balloons, paper planes, drones, open roads, summits, real people building real things in daylight. Technology that looks friendly and useful.</div>
<div class="dont"><b>SKIP</b>Dark &ldquo;hacker&rdquo; tech, glowing circuit brains, robots, stock smiles, handshakes, rented supercars, cash fans, and anything that sells a lifestyle instead of a skill.</div></div>
<h3 style="margin-top:16px">TREATMENT</h3><p class="small muted" style="margin-top:6px">Keep it bright and natural, a touch warm. Fine grain is fine; heavy filters are not. Dark comes from the type: black label boxes and panels on top of the light. One red element carries the colour.</p></div>
<div><div class="eyebrow">Backgrounds &middot; 04_Backgrounds &middot; original 3D renders</div><div class="grid" style="grid-template-columns:1fr 1fr;gap:10px;margin-top:12px">
{''.join(f'<div><img src="assets/bg-{b}.jpg" style="width:100%;height:132px;object-fit:cover;object-position:{p}"><div class="cap">{t}</div></div>' for b, t, p in [('rise-above', 'Rise Above', '65% 50%'), ('first-light', 'First Light', 'center 45%'), ('launch', 'Launch', '65% 40%'), ('break-formation', 'Break Formation', '60% 40%'), ('see-further', 'See Further', '70% 45%'), ('daybreak', 'Daybreak (for text)', 'center')])}</div>
<p class="small muted" style="margin-top:8px">All original renders made for AntiHero: no stock, no AI image generators, nothing to license. 4K desktop plus phone versions. Concrete and Bone Paper stay as utility grounds; the old dark set is archived in <span class="mono">_previous-dark-set</span>.</p></div></div>""", title='07 Imagery')

tex = ['01-concrete-stencil', '02-spun-steel-coin', '03-gold-foil-black-card', '04-liquid-chrome', '05-neon-brick', '06-letterpress-bone',
       '07-leather-deboss', '08-screen-print-tee', '09-chalkboard', '10-carbon-fiber-aluminum', '11-halftone-pop', '12-glitch-signal',
       '13-holo-sticker', '14-laser-etched-wood', '15-paper-cut']
page(f"""{hdr('07 Imagery')}<div style="display:flex;justify-content:space-between;align-items:end"><div><div class="eyebrow">Material studies &middot; 03_Logo-Textures</div><h2 style="margin-top:12px">THE LOGO IN <em>15 MATERIALS</em></h2></div>
<p class="small muted" style="max-width:40ch;text-align:right">For hero visuals, launch posts, merch mockups, and slide openers. Not for small sizes or UI.</p></div>
<div class="grid" style="grid-template-columns:repeat(5,1fr);gap:8px;margin-top:18px">{''.join(f'<div style="position:relative"><img src="assets/tex-{t}.jpg" style="width:100%;aspect-ratio:1;object-fit:cover"><div class="mono" style="position:absolute;left:6px;bottom:5px;font-size:9px;background:rgba(0,0,0,.6);padding:1px 4px">{t[3:].replace("-", " ")}</div></div>' for t in tex)}</div>""",
     title='07 Imagery')

# ---------------------------------------------------------------------------
section_opener('08', 'IN THE WILD', 'Facebook first, then everywhere else.', 'bg-rise-above.jpg', '68% 50%')

page(f"""{hdr('08 Facebook')}<div class="grid" style="grid-template-columns:1.35fr 1fr;gap:40px">
<div><div class="eyebrow">Facebook page &middot; 05_Social/Facebook</div><h2 style="margin:12px 0 16px">COVER + <em>PROFILE</em></h2>
<img src="assets/fb-cover-rise.jpg" style="width:100%">
<div class="grid" style="grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:8px"><img src="assets/fb-cover-launch.jpg" style="width:100%"><img src="assets/fb-cover-formation.jpg" style="width:100%"><img src="assets/fb-cover-manifesto.jpg" style="width:100%"></div>
<div class="cap">Four cover concepts: Rise Above (recommended), Launch, Break Formation, Manifesto</div></div>
<div><img src="assets/fb-profile-preview.jpg" style="width:230px;margin:0 auto"><div class="cap" style="text-align:center">Profile picture as Facebook crops it</div>
<h3 style="margin-top:14px">UPLOAD</h3><ol class="small" style="margin:6px 0 0 18px;display:grid;gap:5px">
<li>Profile: <span class="mono">antihero-fb-profile-carbon_2048px.png</span></li>
<li>Cover: <span class="mono">antihero-fb-page-cover-rise_1640x924.png</span>. Drag to centre if Facebook asks.</li>
<li>Group cover: the <span class="mono">_1640x856</span> file in <span class="mono">Group-Cover</span>.</li>
<li>Check the <span class="mono">_safe-zone-guides</span> folder to see what each device crops.</li></ol>
<p class="small muted" style="margin-top:10px">Every cover keeps its text inside a 1100 &times; 560 centre zone, so it survives desktop, mobile, and the profile-picture overlap.</p></div></div>""",
     title='08 Facebook')

page(f"""{hdr('08 Templates')}<div style="display:flex;justify-content:space-between;align-items:end"><div><div class="eyebrow">Feed + story templates &middot; 05_Social/Posts</div><h2 style="margin-top:12px">TEN POSTS <em>READY TO GO</em></h2></div>
<p class="small muted" style="max-width:46ch;text-align:right">1080 &times; 1350 for the feed (Facebook and Instagram), 1080 &times; 1920 for stories. Recipe: a bright scene, one black label stack, one red idea, the wordmark bar. Editable sources in <span class="mono">_build/templates</span>.</p></div>
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px 12px;margin-top:16px;align-items:start">
{''.join(f'<div><img src="assets/{p}.jpg" style="width:100%;aspect-ratio:4/5;object-fit:cover;object-position:top;background:#000"><div class="cap" style="font-size:9.5px;margin-top:4px">{t}</div></div>' for p, t in [('post-01', 'Welcome'), ('post-02', 'The creed'), ('post-03', 'AI tool of the week'), ('post-04', 'Live workshop'), ('post-05', 'SEO tip carousel'), ('post-07', 'Your runway'), ('post-08', 'Break formation'), ('post-09', 'Work with us (1 in 10)'), ('post-06', 'Now open (square)'), ('story-01', 'Story: join the group')])}</div>""",
     title='08 Templates')

page(f"""{hdr('08 Platforms')}<div class="eyebrow">Everywhere else</div><h2 style="margin:12px 0 16px">ONE LOOK, <em>EVERY SIZE</em></h2>
<div class="grid" style="grid-template-columns:1fr 1fr;gap:14px">
<div><img src="assets/yt-banner.jpg" style="width:100%;height:190px;object-fit:cover"><div class="cap">YouTube banner 2560 &times; 1440 + profile + watermark</div></div>
<div><img src="assets/yt-thumb.jpg" style="width:100%;height:190px;object-fit:cover"><div class="cap">YouTube thumbnail template 1280 &times; 720</div></div>
<div><img src="assets/li-banner.jpg" style="width:100%"><div class="cap">LinkedIn banner 1584 &times; 396 + company cover + logo</div>
<img src="assets/x-header.jpg" style="width:100%;margin-top:10px"><div class="cap">X header 1500 &times; 500 + profile</div></div>
<div><img src="assets/zoom-bg.jpg" style="width:100%"><div class="cap">Zoom / Teams / Meet background 1920 &times; 1080</div>
<img src="assets/email-sig.jpg" style="width:100%;margin-top:10px"><div class="cap">Email signature banner (600 &times; 150 at 2x)</div></div></div>""",
     title='08 Platforms')

card_front = f"""<div style="width:336px;height:192px;background:url(assets/bg-concrete.jpg) center/cover;display:grid;place-items:center;box-shadow:0 18px 40px rgba(0,0,0,.55)">{badge(104)}</div>"""
card_back = f"""<div style="width:336px;height:192px;background:{BONE};color:{VOID};padding:22px 24px;display:flex;flex-direction:column;box-shadow:0 18px 40px rgba(0,0,0,.55)">
<div style="font-family:'Bebas Neue';font-size:34px;line-height:.9">MATT HAYNES</div><div style="font-family:'Barlow Condensed';font-weight:700;font-size:10px;letter-spacing:.24em;margin-top:6px">FOUNDER &middot; AI &amp; BRAND STRATEGY</div>
<div class="mono" style="font-size:9px;line-height:1.7;margin-top:auto;opacity:.8">[email]<br>[phone]<br>[website]</div>
<div style="position:absolute"></div><img src="assets/wordmark-black-ignition_2048px.png" style="height:20px;align-self:flex-end;margin-top:-20px"></div>"""
page(f"""{hdr('08 Applications')}<div class="eyebrow">Applications</div><h2 style="margin:12px 0 18px">OFF THE <em>SCREEN</em></h2>
<div class="grid" style="grid-template-columns:1.1fr 1fr;gap:36px">
<div style="background:{GRAPHITE};padding:30px;display:flex;flex-direction:column;gap:22px;align-items:center;justify-content:center">{card_front}{card_back}
<div class="cap">Business card &middot; 3.5 &times; 2 in &middot; fill in the bracketed details</div></div>
<div class="grid" style="grid-template-columns:1fr 1fr;gap:10px">{''.join(f'<div><img src="assets/tex-{t}.jpg" style="width:100%;aspect-ratio:1;object-fit:cover"><div class="cap">{n}</div></div>' for t, n in [('08-screen-print-tee', 'Tee: knockout badge, distressed'), ('13-holo-sticker', 'Die-cut holo sticker'), ('02-spun-steel-coin', 'Challenge coin'), ('07-leather-deboss', 'Leather patch, hats + notebooks')])}</div></div>""",
     title='08 Applications')

# ---------------------------------------------------------------------------
section_opener('09', 'THE FAMILY', 'AntiHero teaches it. KR8TIV designs it. KR8TIV AI automates it.', 'bg-launch.jpg', '65% 40%')

fam = [('ANTIHERO', 'LEARN IT', 'The free school and community', 'AI tools, branding, SEO, and entrepreneurship, taught in the open: the Facebook group, lives, workshops, and 1:1 consulting.',
        [VOID, '#FFFFFF', RED], 'Bebas Neue &middot; black, white, one red', 'badge'),
       ('KR8TIV', 'DESIGN IT', 'kr8tiv.io &middot; the studio', 'A cyber-renaissance design atelier: brand identity, websites, motion, video, and AI solutions. The founder is on every project.',
        ['#050507', '#FF6AD5', '#8E00FF', '#FF2D4A', '#FFD166'], 'Instrument Serif &middot; dark ground, prism accents', 'kr'),
       ('KR8TIV AI', 'AUTOMATE IT', 'kr8tiv.ai &middot; the engine room', 'AI back-office systems wired into the tools a business already uses: receipts, quoting, dispatch, morning digests, watchdog agents. Products: JARVIS and KIN.',
        ['#050510', '#D4A853', '#FFFFFF'], 'Syne &middot; deep navy, one amber', 'krai')]


def fam_logo(kind):
    if kind == 'badge':
        return f'<div style="display:flex;align-items:center;gap:12px">{badge(56)}<span style="font-family:\'Bebas Neue\';font-size:44px;line-height:1">ANTIHERO</span></div>'
    s = 44 / KR_VB[3]
    kr = (f'<svg viewBox="{KR_VB[0]} {KR_VB[1]} {KR_VB[2]} {KR_VB[3]}" style="height:44px;width:{KR_VB[2] * s:.0f}px;display:block">'
          f'<path fill="#fff" fill-rule="evenodd" d="{KR_D}"/></svg>')
    if kind == 'kr':
        return f'<div style="height:56px;display:flex;align-items:center">{kr}</div>'
    return f'<div style="height:56px;display:flex;align-items:center;gap:8px">{kr}<span class="mono" style="font-weight:700;font-size:18px;margin-top:-18px">AI</span></div>'


page(f"""{hdr('09 The family')}<div class="eyebrow">Brand architecture</div><h2 style="margin:12px 0 18px">ONE FOUNDER, <em>THREE WAYS IN</em></h2>
<div class="grid" style="grid-template-columns:repeat(3,1fr);gap:14px">{''.join(f'''<div style="background:var(--carbon);padding:20px 20px 18px;display:flex;flex-direction:column;min-height:330px">
{fam_logo(kind)}<span class="lbl {'r' if i == 0 else ''}" style="font-size:20px;letter-spacing:.16em;margin-top:14px;align-self:flex-start;padding:.3em .5em .26em .62em">{role}</span>
<div class="cap" style="margin-top:10px;opacity:.9">{where}</div><p class="small muted" style="margin-top:8px">{what}</p>
<div style="margin-top:auto;display:flex;gap:0">{''.join(f'<span style="width:26px;height:18px;background:{c};outline:1px solid rgba(255,255,255,.15)"></span>' for c in chips)}</div>
<div class="mono" style="font-size:9.5px;margin-top:6px;opacity:.7">{look}</div></div>''' for i, (name, role, where, what, chips, look, kind) in enumerate(fam))}</div>
<div class="eyebrow" style="margin-top:22px">The give-first ladder</div>
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin-top:10px">{''.join(f'<div style="background:{bgc};color:{ink};padding:12px 12px 10px;font-family:\'Bebas Neue\';font-size:21px;line-height:1">{t}<div class="mono" style="font-size:9.5px;margin-top:6px;opacity:.8;line-height:1.35">{d}</div></div>' for t, d, bgc, ink in [('FREE POSTS', 'daily value, no ask', '#2B3035', '#fff'), ('THE GROUP', 'the product: community', '#2B3035', '#fff'), ('LIVE WORKSHOPS', 'teach it together', '#2B3035', '#fff'), ('1:1 CONSULTING', 'Matt, on your business', '#FFFFFF', VOID), ('DONE FOR YOU', 'KR8TIV + KR8TIV AI', RED, '#fff')])}</div>""",
     title='09 The family')

page(f"""{hdr('09 The family')}<div class="grid" style="grid-template-columns:1.05fr 1fr;gap:44px">
<div><div class="eyebrow">Co-branding rules</div><h2 style="margin:12px 0 16px">GIVE FIRST. <em>ASK RARELY.</em></h2>
<ol style="margin:0 0 0 18px;display:grid;gap:11px" class="small">
<li><b>The community is the product.</b> AntiHero leads everything members see. It gives away real value until people ask how to work with you.</li>
<li><b>Nine to one.</b> About nine posts of pure value for every post that points to KR8TIV or KR8TIV AI. The ask is an invitation or a case study, never a pitch in someone&rsquo;s DMs.</li>
<li><b>Teach with real work.</b> &ldquo;How we automated a crew&rsquo;s back office&rdquo; is a lesson first and a KR8TIV AI case study second.</li>
<li><b>One colour inside AntiHero.</b> On AntiHero layouts the sister logos appear single-colour (white or black), never in their own accents, so the one-red rule holds.</li>
<li><b>Each brand keeps its own look</b> on its own site. Optional: the studios can point back with the &ldquo;Part of the AntiHero family&rdquo; endorsement in their footers.</li>
<li><b>One founder voice.</b> Matt signs the posts. No corporate &ldquo;we&rdquo; in the group.</li></ol></div>
<div style="display:flex;flex-direction:column;gap:14px">
<div style="background:var(--carbon);padding:22px 18px"><img src="assets/family-lockup-on-dark.png" style="width:100%"><div class="cap">Family lockup &middot; 02_Logos/07_Family</div></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;align-items:start"><img src="assets/post-09.jpg" style="width:100%">
<div><div style="background:var(--carbon);padding:14px"><img src="assets/endorse-family-on-dark.png" style="width:100%"></div><div class="cap">Footer endorsement for kr8tiv.io and kr8tiv.ai</div>
<p class="small muted" style="margin-top:10px">The &ldquo;Work with us&rdquo; post is the one-in-ten ask: it names both studios and their sites, then gets out of the way.</p></div></div></div></div>""",
     title='09 The family')

tree = """AntiHero-Brand-Kit/
 00_START-HERE.html        open this first
 01_Brand-Bible/           this document (PDF + HTML)
 02_Logos/
   01_Badge/               primary logo, 11 color versions, SVG + PNG to 8192 px
   02_Mark/                logo without the disc
   03_Wordmark/            ANTI hero, caps, label box
   04_Lockups/             horizontal, stacked, tagline
   05_Icons/               favicon.ico, app + PWA icons
   06_Construction/        construction + clear-space drawings
   07_Family/              AntiHero + KR8TIV + KR8TIV AI lockups, endorsements
 03_Logo-Textures/         15 material studies + logo on every background
 04_Backgrounds/           5 original 3D skies + Daybreak, Concrete, Bone (4K + phone)
 05_Social/                Facebook, posts, YouTube, LinkedIn, X, Zoom, email, web
 06_Fonts/                 Bebas Neue, Barlow, Barlow Condensed, JetBrains Mono (OFL)
 07_Color/                 .ase, .css, .json, .gpl, palette card
 _build/                   the scripts that generated everything"""
page(f"""{hdr('Files')}<div class="grid" style="grid-template-columns:1.2fr 1fr;gap:50px">
<div><div class="eyebrow">File index</div><h2 style="margin:12px 0 18px">WHERE <em>EVERYTHING</em> LIVES</h2>
<pre class="mono" style="font-size:11.5px;line-height:1.62;background:var(--carbon);padding:18px 20px;white-space:pre">{tree}</pre></div>
<div><div class="eyebrow">Which file?</div><table style="margin-top:14px">
<tr><td>Facebook, Instagram avatar</td><td class="mono small">fb-profile-carbon_2048px</td></tr>
<tr><td>Website header</td><td class="mono small">lockup-horizontal-on-dark</td></tr>
<tr><td>Printer, sign shop, embroidery</td><td class="mono small">.svg from 02_Logos</td></tr>
<tr><td>Canva uploads</td><td class="mono small">_2048px.png (transparent)</td></tr>
<tr><td>T-shirt, vinyl, laser</td><td class="mono small">badge-knockout-*.svg</td></tr>
<tr><td>Website favicon</td><td class="mono small">05_Icons/favicon.ico</td></tr>
<tr><td>Slides and video</td><td class="mono small">04_Backgrounds + wordmark</td></tr>
<tr><td>About slide, KR8TIV footers</td><td class="mono small">07_Family lockups</td></tr></table>
<p class="small muted" style="margin-top:16px">SVG files are the masters: text is already converted to outlines, so they open anywhere without installing fonts.</p></div></div>""",
     title='Files')

# BACK COVER
page(f"""<div style="position:absolute;inset:0;background:url(assets/bg-break-formation.jpg) 60% 40%/cover"></div>
<div style="position:relative;height:100%;display:flex;flex-direction:column;align-items:flex-start;justify-content:flex-end;padding-bottom:30px">
<span class="lbl k" style="font-size:92px">NOBODY&rsquo;S COMING</span><span class="lbl k" style="font-size:92px">TO SAVE YOU.</span>
<span class="lbl r" style="font-size:58px;margin-top:14px">YOU NEVER NEEDED SAVING.</span>
<div style="display:flex;align-items:center;gap:14px;margin-top:26px">{badge(64)}<span class="lbl k" style="font-size:18px;letter-spacing:.2em;padding:.35em .6em .3em .8em">ANTIHERO &middot; BE YOUR OWN HERO</span></div></div>""",
     title='Back cover')


def build():
    out = []
    for i, (cls, title, body) in enumerate(PAGES, 1):
        out.append(f'<section class="page {cls}" aria-label="{title}">{body.replace("{PN}", f"{i:02d} / {len(PAGES):02d}")}</section>')
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AntiHero Brand Bible</title><style>{CSS}</style></head><body>{''.join(out)}</body></html>"""
    return html


if __name__ == '__main__':
    html = build()
    name = 'AntiHero-Brand-Bible-web.html' if WEB else 'AntiHero-Brand-Bible.html'
    p = os.path.join(BD, name)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(html)
    print('pages', len(PAGES), '->', p)
    if not WEB:
        from render import Renderer
        with Renderer() as r:
            r.pdf(p, os.path.join(BD, 'AntiHero-Brand-Bible.pdf'), width='11in', height='8.5in')
        print('pdf written')
