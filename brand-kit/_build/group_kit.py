"""Facebook Group Kit: group cover, pinned posts, weekly series cards, templates, event cover, admin playbook PDF, paste-ready copy.

Output: 05_Social/Facebook/Group-Kit/.  Run:  python group_kit.py
"""
import os
import pathlib
import shutil

from PIL import Image

from brand import C, KIT, FONTS, font_face_css
from render import Renderer, file_url
import social as S
from social import BASE_CSS, DESC, badge_inline, guide_overlay, job, page_html, wordmark_svg
from social_v2 import bg, css_page, kr8tiv_svg, shell

GK = 'Facebook/Group-Kit'
OUT = os.path.join(S.OUT, *GK.split('/'))
WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'work', 'group-kit')
os.makedirs(WORK, exist_ok=True)

# =====================================================================================================
# COPY (single source for the graphics, the playbook PDF, and the paste-ready text file)
# =====================================================================================================
NAME = 'AntiHero | AI & Entrepreneurship'
NAME_ALTS = ['AntiHero: AI Tools for Small Business', 'AntiHero: Build It Yourself (AI, Branding, SEO)']
GROUP_URL = 'facebook.com/groups/antiheroai'     # live since 2026-09-23 (antiherogroup was taken)

ABOUT = """AntiHero is a free community for entrepreneurs who want to use AI to build the business of their dreams.

Every week we share AI tools, prompts, branding, and SEO you can put to work the same day, and once a week we go live and build something real together. You can walk in knowing nothing about AI and walk out with a ton you can actually use.

We're all about good vibes here: laughing, learning, and helping each other out, whatever level you're at. Nobody's coming to save you. You never needed saving.

THE WEEK
Mon: AI tool of the week
Tue: prompt swap
Wed: live workshop
Thu: get found (SEO)
Fri: wins and builds
Sat: build day

Run by Matt Haynes (kr8tiv.io, kr8tiv.ai) out of Edmonton. Almost everything here is free. Now and then I'll mention my private coaching for anyone who wants more hands-on help."""

# Matt's rules (2026-09-22), in his tone: fun and approachable, honest, not harsh. Good vibes, be nice to everybody,
# everyone's at a different level, ask before you advertise, politics stay outside, and removals come with a chat.
# The first sentence of each description is what the House Rules card shows, so keep it short.
RULES = [
    ('Good vibes only.', 'We\'re here to laugh, learn, and help each other out. Be nice to everybody, no matter who they are or what they do.'),
    ('Everyone\'s at a different level.', 'Some of us are just starting and some have been at it for years. No question is too basic, so meet people where they are.'),
    ('Ask before you advertise.', 'Just message me first so I can take a look. I\'m happy to let people promote their stuff.'),
    ('Politics stay outside.', 'This is a place for building, so let\'s leave politics at the door. And there\'s no room for hate toward anyone, ever.'),
    ('Help where you can.', 'Share what worked, what didn\'t, and what you\'d do differently. A good question counts too.'),
    ('Keep it real.', 'Real work, real numbers, real photos. If AI helped make something, just say which tool.'),
    ('If something goes sideways.', 'If a post crosses the line, I\'ll message you and we\'ll talk it out. I might take the post down or remove you for a bit, '
                                    'but it doesn\'t make you a bad person, and I\'m happy to let you back in.'),
]

QUESTIONS = [
    'What are you building right now, or what do you want to build?',
    'Which AI tools do you use today? ("None yet" is a great answer.)',
    'How did you find AntiHero?',
]
QUESTION_ALT = 'Once you have an email list: "Want the free weekly toolkit by email? Leave your best address (optional)."'

SERIES = [
    dict(slug='mon-ai-tool', day='MONDAY', short='MON', title=['AI TOOL', 'OF THE WEEK'], line='One tool. One job. One prompt to steal.',
         bg='see-further', phone=False, pos='74% center', topic='AI Tools',
         caption='AI tool of the week: [TOOL].\n\nThe job: [what it does for a small business, in one line].\nTry this: [one prompt, or three steps].\n\nPost what you got and what you changed. That\'s the whole lesson.'),
    dict(slug='tue-prompt-swap', day='TUESDAY', short='TUE', title=['PROMPT', 'SWAP'], line='Drop your best prompt. Take one home.',
         bg='daybreak', phone=True, pos='center 62%', topic='Prompts', light=True,
         caption='Prompt swap.\n\nDrop the one prompt you used most this week. Say what it\'s for and which tool you ran it in.\n\nTake one home. Try it. Report back Friday.'),
    dict(slug='wed-live', day='WEDNESDAY', short='WED', title=['LIVE', 'WORKSHOP'], line='60 minutes. Build something real with AI.',
         bg='launch', phone=True, pos='center 40%', topic='Live',
         caption='Live today at [TIME]: [TOPIC].\n\nWe build [the thing] from scratch in 60 minutes. Bring a laptop and one idea.\n\nThe replay stays in the group.'),
    dict(slug='thu-get-found', day='THURSDAY', short='THU', title=['GET', 'FOUND'], line='One SEO fix you can finish in five minutes.',
         bg='paper-bone', phone=True, pos='center', topic='SEO', light=True,
         caption='Get found: [the tip, in one line].\n\nThe five-minute fix:\n1. [step]\n2. [step]\n3. [step]\n\nDid it? Say so in the comments.'),
    dict(slug='fri-wins', day='FRIDAY', short='FRI', title=['WINS &amp;', 'BUILDS'], line='Post your win. However small. Show your work.',
         bg='rise-above', phone=True, pos='center 30%', topic='Wins',
         caption='Wins and builds.\n\nWhat did you ship, fix, finish, or figure out this week? Post it here. Small wins count, and they compound.\n\nToday is also the day to show your work and link your stuff. One link each, and say what it is.'),
    # text on top here: the formation sits mid-frame in this render, so the card breaks the series layout on purpose
    dict(slug='sat-build-day', day='SATURDAY', short='SAT', title=['BUILD', 'DAY'], line='Side-project hours. What are you building this weekend?',
         bg='break-formation', phone=False, pos='70% center', topic='Build Day', align='top',
         caption='Build day.\n\nWhat are you building this weekend? A logo, a page, a first post, or a prompt that saves you an hour?\n\nDrop it here before you start, and come back to say how far you got.'),
]

# The first ten posts, in order. img = path relative to 05_Social.
LAUNCH = [
    dict(when='Day 1', title='Start here (feature it)', img=f'{GK}/02_Pinned/antihero-group-start-here_1080x1350.png',
         caption='Start here.\n\nAntiHero is where we learn AI tools, branding, and SEO by using them on real businesses, including yours. We\'re all about good vibes: laughing, learning, and helping each other out.\n\n1. Say hi in the comments: your name, where you\'re from, and what you\'re building.\n2. Learn the week. Monday is tools, Tuesday is prompts, Wednesday we go live, Thursday is SEO, Friday is wins, and Saturday we build.\n3. Post one win this week. However small.\n\nGive the house rules a quick read. They\'re short and friendly.\n\nNobody\'s coming to save you. You never needed saving.'),
    dict(when='Day 1', title='Welcome thread', img=f'{GK}/02_Pinned/antihero-group-welcome_1080x1350.png',
         caption='Welcome in.\n\nDrop three things in the comments:\n1. Your name and where you are.\n2. What you\'re building, or want to build.\n3. One job you want AI to take off your plate.\n\nYour answers decide what we build in the first live workshops.'),
    dict(when='Day 2', title='Mon: AI tool of the week', img='Posts/antihero-post-03-ai-tool_1080x1350.png',
         caption='AI tool of the week: Claude.\n\nThe job: your always-on marketing department. Paste this in and fill the brackets:\n\n"Act as a local SEO strategist. Write 5 Google Business Profile posts for my [business] in [city]. Each under 250 words, one clear call to action, no hype."\n\nPost what it gave you and what you changed. That\'s the whole lesson.'),
    dict(when='Day 3', title='Tue: prompt swap', img=f'{GK}/03_Weekly-Series/antihero-series-tue-prompt-swap_1080x1350.png',
         caption='Prompt swap.\n\nDrop the one prompt you use more than any other. Say what it\'s for and which tool you run it in.\n\nTake one home. Try it this week. Report back Friday.'),
    dict(when='Day 4', title='Wed: first live workshop', img=f'{GK}/05_Event/antihero-group-event-live-workshop_1920x1005.png',
         caption='Live this Wednesday: build your brand with AI in 60 minutes.\n\nWe take one member\'s business from idea to name, logo direction, and a one-page site plan, live, with free tools. Want it to be yours? Say so in the comments.\n\nBring a laptop and one business idea. RSVP to the event so you get the reminder. The replay stays in the group.'),
    dict(when='Day 5', title='Thu: get found', img='Posts/antihero-post-05-seo-tip_1080x1350.png',
         caption='Get found: your Google Business Profile is your new homepage.\n\nMost local customers decide before they ever reach your website. The five-minute fix:\n1. Add 10 real photos: your work, your space, and your face.\n2. Check your categories. The primary one matters most.\n3. Post one update a week. Offers, projects, and tips all count.\n4. Answer every review, good or bad, within two days.\n\nDone one of these? Say which.'),
    dict(when='Day 6', title='Fri: wins and builds', img=f'{GK}/03_Weekly-Series/antihero-series-fri-wins_1080x1350.png',
         caption='Wins and builds.\n\nWhat did you ship, fix, finish, or figure out this week? Post it here. Screenshots welcome. Small wins count, and they compound.\n\nToday is also the day to show your work and link your stuff. One link each, and say what it is.'),
    dict(when='Day 7', title='Sat: build day', img=f'{GK}/03_Weekly-Series/antihero-series-sat-build-day_1080x1350.png',
         caption='Build day.\n\nWhat are you building this weekend? A logo, a page, a first post, or a prompt that saves you an hour?\n\nDrop it here before you start, and come back to say how far you got.'),
    dict(when='Day 9', title='Poll: what\'s stopping you', img=f'{GK}/04_Templates/antihero-group-poll_1080x1080.png',
         caption='Quick poll. Honest answers only.\n\nWhat\'s the one thing stopping you from starting?\nA. Time\nB. Money\nC. Not sure where to start\nD. Worried about looking silly\n\nVote, then tell us why in a comment. The top answer becomes next Wednesday\'s workshop.\n\n(Use Facebook\'s poll option with these four answers, and add the graphic.)'),
    dict(when='Day 10', title='Runway', img='Posts/antihero-post-07-runway_1080x1350.png',
         caption='Hate your job? Good. That\'s your runway.\n\nEvery skill in this group is a way out: AI tools, branding, and getting found online. You don\'t have to quit on Monday. Start on a Saturday. Leave when the numbers say you can.\n\nWho\'s building their way out right now? Say so. We\'ll help.'),
]

LADDER = [
    ('GIVE', 'The AntiHero group', 'Weekly lives, prompts, templates, and replays. Free, always. Nobody needs to buy anything to get the full value.'),
    ('TEACH', '1:1 coaching', 'Four in-person sessions a month, with homework, from $250 a month. Runs as an AntiHero or a kr8tiv.io program.'),
    ('BUILD', 'KR8TIV studio', 'kr8tiv.io: brand, web, motion, and video, done for you.'),
    ('AUTOMATE', 'KR8TIV AI', 'kr8tiv.ai: AI systems that run the back office.'),
]
ASK_RULES = [
    'No asks in the first eight weeks. The group earns the right first.',
    'After that, at most one post in ten asks for anything, and it\'s an invitation ("Want it done for you?"), never a countdown.',
    'Answer the question in the thread first. Offer help in DMs only when someone asks for it.',
    'Teach with case studies, not pitches: member wins (with permission) and KR8TIV builds, shown as lessons.',
    'The KR8TIV names live in the About section and the occasional family post. That is enough.',
]
SETUP = [
    ('Create it as the Page', 'Create the group as the AntiHero Page, or link it to the Page afterwards, so admins can post as the brand.'),
    ('Name', NAME),
    ('Privacy', 'Private, and visible in search. The Page is the public megaphone. The group is the room.'),
    ('Cover', '01_Cover/antihero-group-cover-write-your-story_1640x856.png. The _safe-zone-guides file shows the mobile crop.'),
    ('About', 'Paste the description from the next page. Location: Edmonton, Alberta.'),
    ('Rules', 'Add the five house rules. Turn on "ask people to agree to the rules" in membership questions.'),
    ('Membership questions', 'Add the three questions. Approve anyone who answers like a person.'),
    ('Topics', 'AI Tools, Prompts, Live, SEO, Wins, and Build Day. Tag every series post so members can browse.'),
    ('Feature', 'Feature the Start Here post and the House Rules post, in that order.'),
    ('Events', 'Make the Wednesday live a recurring event with the event cover. Go live from inside the event.'),
]
SCORE = [('New members', 'per week'), ('Active members', 'Group insights, per week'), ('Live attendance', 'peak viewers plus replays'), ('Wins posted', 'on Friday')]


# =====================================================================================================
# GRAPHICS
# =====================================================================================================
def label_block(lines, size, cls='blk'):
    return ''.join(f'<span class="lbl {cls} t" style="font-size:{size}px">{ln}</span>' for ln in lines)


def cover():
    W, H = 1640, 856
    blk = (1100, 560, f"""<style>.gc{{width:1100px;height:560px;display:flex;align-items:center;gap:46px}}
.gc .st{{display:flex;flex-direction:column;align-items:flex-start}}
.gc .l1{{font-size:150px;letter-spacing:.012em;padding:18px 24px 18px 27px}}
.gc .row{{display:flex;align-items:center;gap:16px;margin-top:26px}}
.gc .l3{{font-size:30px;letter-spacing:.16em;padding:11px 16px 11px 21px}}
.gc .l4{{font-size:30px;letter-spacing:.16em;padding:11px 16px 11px 21px}}</style>
<div class="gc">{badge_inline(250)}<div class="st"><span class="lbl blk l1">WRITE YOUR</span><span class="lbl blk l1">OWN STORY.</span>
<div class="row"><span class="lbl red l3">THE ANTIHERO GROUP</span><span class="lbl blk l4">AI &middot; BRANDING &middot; SEO</span></div></div></div>""")
    safe = ((W - 1100) / 2, (H - 540) / 2, 1100, 540)
    pos = '30% 50%'
    job(f'{GK}/01_Cover/antihero-group-cover-write-your-story_1640x856.png', W, H, page_html(W, H, bg('first-light'), blk, safe, bg_pos=pos),
        page_html(W, H, bg('first-light'), blk, safe, bg_pos=pos,
                  overlay=guide_overlay(W, H, [(0, (H - 662) // 2, W, 662, 'desktop crop band', '#1e88ff'),
                                               ((W - 1100) // 2, (H - 540) // 2, 1100, 540, 'KEEP TEXT HERE', '#e0261e')])))


def event():
    W, H = 1920, 1005
    blk = (1100, 560, """<style>.ev{width:1100px;height:560px;display:flex;flex-direction:column;justify-content:center;align-items:flex-start;padding-left:6px}
.ev .k{font-size:40px;letter-spacing:.16em;padding:13px 19px 13px 25px}
.ev .l1{font-size:190px;letter-spacing:.012em;padding:22px 28px 22px 31px}
.ev .l3{font-size:40px;letter-spacing:.08em;padding:13px 19px 13px 23px;margin-top:26px}</style>
<div class="ev"><span class="lbl red k" style="margin-bottom:26px">THE ANTIHERO GROUP</span><span class="lbl blk l1">LIVE</span><span class="lbl blk l1">WORKSHOP.</span>
<span class="lbl blk l3">60 MINUTES &middot; BUILD SOMETHING REAL WITH AI</span></div>""")
    job(f'{GK}/05_Event/antihero-group-event-live-workshop_1920x1005.png', W, H,
        page_html(W, H, bg('launch'), blk, ((W - 1300) / 2 - 120, (H - 640) / 2, 1300, 640), bg_pos='center 50%'))


PANEL_CSS = """<style>
.k{font-size:42px;letter-spacing:.15em;padding:12px 18px 12px 24px}
.t{padding:22px 28px 22px 30px;letter-spacing:.01em}
.p{font-size:34px;line-height:1.36;font-weight:600;padding:22px 28px;max-width:880px}
.list{padding:26px 30px 10px;width:100%}
.list .it{display:grid;grid-template-columns:86px 1fr;gap:6px;padding:0 0 20px}
.list .n{font-family:'Bebas Neue';font-size:58px;line-height:.9;color:var(--red)}
.list .h{font-family:'Bebas Neue';font-size:46px;line-height:.95;letter-spacing:.02em}
.list .d{font-size:26px;line-height:1.36;color:#dfe1e3;margin-top:6px}
</style>"""


def pinned():
    W, H = 1080, 1350
    # start here
    items = [('01', 'SAY HI', 'Name, town, and what you&rsquo;re building. Drop it in the comments.'),
             ('02', 'LEARN THE WEEK', 'Every day has a job. Monday tools, Wednesday live, Friday wins.'),
             ('03', 'POST ONE WIN', 'This week. However small. That&rsquo;s how it starts.')]
    li = ''.join(f'<div class="it"><div class="n">{n}</div><div><div class="h">{h}</div><div class="d">{d}</div></div></div>' for n, h, d in items)
    inner = f"""{PANEL_CSS}<div style="display:flex;flex-direction:column;align-items:flex-start;height:100%">
<span class="lbl red k">NEW HERE?</span><span style="margin-top:28px"></span>{label_block(['START', 'HERE.'], 250)}
<div class="list panel" style="margin-top:auto">{li}</div></div>"""
    job(f'{GK}/02_Pinned/antihero-group-start-here_1080x1350.png', W, H, shell(W, H, bg('rise-above', True), inner, 'center 30%'))

    # welcome
    inner = f"""{PANEL_CSS}<div style="display:flex;flex-direction:column;align-items:flex-start;height:100%">
<span class="lbl red k">THE ANTIHERO GROUP</span><span style="margin-top:28px"></span>{label_block(['WELCOME', 'IN.'], 250)}
<p class="p panel" style="margin-top:auto">You&rsquo;re the hero of your own story. We just bring the tools. Say hi in the comments: who you are, where you are, and what you&rsquo;re building.</p></div>"""
    job(f'{GK}/02_Pinned/antihero-group-welcome_1080x1350.png', W, H, shell(W, H, bg('first-light', True), inner, 'center 30%'))

    # house rules
    li = ''.join(f'<div class="it"><div class="n">0{i + 1}</div><div><div class="h">{h.upper()}</div><div class="d">{d}</div></div></div>'
                 for i, (h, d) in enumerate([(r[0], r[1].split('. ')[0] + '.') for r in RULES]))
    inner = f"""{PANEL_CSS}<style>.list{{padding:28px 30px 10px}}.list .it{{padding-bottom:16px;grid-template-columns:84px 1fr}}
.list .n{{font-size:54px}}.list .h{{font-size:44px}}.list .d{{font-size:24px;line-height:1.34}}</style>
<div style="display:flex;flex-direction:column;align-items:flex-start;height:100%">
{label_block(['HOUSE RULES.'], 130)}
<div class="list panel" style="margin-top:26px">{li}</div></div>"""
    job(f'{GK}/02_Pinned/antihero-group-house-rules_1080x1350.png', W, H, shell(W, H, bg('daybreak', True), inner, 'center 62%', foot='light'))


MAGNIFIER = ('<svg viewBox="0 0 40 40" style="width:46px;height:46px;flex:none"><circle cx="17" cy="17" r="11" fill="none" stroke="#0A0A0B" stroke-width="4"/>'
             '<path d="M25.5 25.5 36 36" stroke="#0A0A0B" stroke-width="4.4" stroke-linecap="round"/></svg>')
ART = {
    # a prompt window: technology as the friendly tool, monochrome so the red tag stays the one red
    'tue-prompt-swap': """<style>.term{width:820px;background:rgba(10,10,11,.9);box-shadow:0 30px 60px rgba(10,10,11,.25)}
.term .tb{display:flex;align-items:center;gap:12px;padding:18px 24px;border-bottom:1px solid rgba(255,255,255,.12)}
.term .tb i{width:14px;height:14px;border-radius:50%;background:#8A9096;opacity:.8}
.term .tb span{margin-left:14px;font:500 22px 'JetBrains Mono';color:#8A9096}
.term .body{padding:28px 30px 32px;font:400 30px/1.6 'JetBrains Mono';color:#ECE8E1}
.term .body b{color:#8A9096;font-weight:400}.term .dim{color:#5d6268}
.term .cur{display:inline-block;width:17px;height:34px;background:#ECE8E1;vertical-align:-6px;margin-left:8px}</style>
<div class="term"><div class="tb"><i></i><i></i><i></i><span>prompt-swap.txt</span></div>
<div class="body"><div><b>&gt;</b> the prompt that saved me</div><div><b>&gt;</b> five hours this week:</div>
<div class="dim">&gt; ____________________</div><div><b>&gt;</b> paste yours below<span class="cur"></span></div></div></div>""",
    # "near me" search with you as the top result: what getting found looks like
    'thu-get-found': f"""<style>.srch{{width:820px;display:flex;align-items:center;gap:22px;background:#fff;border-radius:60px;padding:26px 36px;
box-shadow:0 18px 44px rgba(10,10,11,.14);font:500 38px 'Barlow';color:#0A0A0B}}
.srch u{{text-decoration:none;border-bottom:3px solid #0A0A0B;display:inline-block;width:150px;margin:0 10px;transform:translateY(-6px)}}
.res{{width:820px;margin-top:22px;display:flex;align-items:center;gap:26px;background:#fff;padding:26px 32px;box-shadow:0 18px 44px rgba(10,10,11,.14)}}
.res .pin{{width:74px;height:74px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:#0A0A0B;display:grid;place-items:center;flex:none}}
.res .pin span{{transform:rotate(45deg);font:400 40px 'Bebas Neue';color:#fff}}
.res .nm{{font:400 62px/1 'Bebas Neue';color:#0A0A0B}}.res .mt{{font:600 26px 'Barlow';color:#2B3035;margin-top:8px;letter-spacing:.01em}}</style>
<div class="srch">{MAGNIFIER}<span>best<u></u>near me</span></div>
<div class="res"><div class="pin"><span>1</span></div><div><div class="nm">YOU.</div><div class="mt">&#9733;&#9733;&#9733;&#9733;&#9733; 5.0 &middot; Open now &middot; 2 min away</div></div></div>""",
}


def series_cards():
    W, H = 1080, 1350
    for s in SERIES:
        head = f"""<span class="lbl red k">EVERY {s['day']}</span><span style="margin-top:26px"></span>{label_block(s['title'], 188)}"""
        if s.get('align') == 'top':
            inner = f"""{PANEL_CSS}<div style="display:flex;flex-direction:column;align-items:flex-start;height:100%">{head}
<p class="p panel" style="margin-top:auto">{s['line']}</p></div>"""
        else:
            art = f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:40px">{ART[s["slug"]]}</div>' if s['slug'] in ART else ''
            inner = f"""{PANEL_CSS}<div style="display:flex;flex-direction:column;align-items:flex-start;justify-content:flex-end;height:100%">{art}{head}
<p class="p panel" style="margin-top:30px">{s['line']}</p></div>"""
        u = bg(s['bg'], s['phone'])
        job(f"{GK}/03_Weekly-Series/antihero-series-{s['slug']}_1080x1350.png", W, H,
            shell(W, H, u, inner, s['pos'], foot='light' if s.get('light') else 'bar'))


def templates():
    # member spotlight (reusable title card; the story goes in the post text)
    W, H = 1080, 1350
    inner = f"""{PANEL_CSS}<div style="display:flex;flex-direction:column;align-items:flex-start;justify-content:flex-end;height:100%">
<span class="lbl red k">REAL PEOPLE. REAL BUILDS.</span><span style="margin-top:26px"></span>{label_block(['MEMBER', 'SPOTLIGHT.'], 188)}
<p class="p panel" style="margin-top:30px">Their story is in the post. Say congrats, then steal the idea.</p></div>"""
    job(f'{GK}/04_Templates/antihero-group-member-spotlight_1080x1350.png', W, H, shell(W, H, bg('first-light', True), inner, 'center 40%'))

    # poll
    S2 = 1080
    opts = [('A', 'TIME'), ('B', 'MONEY'), ('C', 'NOT SURE WHERE TO START'), ('D', 'WORRIED ABOUT LOOKING SILLY')]
    ol = ''.join(f'<div style="display:flex;align-items:center;gap:18px;padding:13px 0;border-top:1px solid rgba(255,255,255,.16)">'
                 f'<span class="lbl red" style="font-size:40px;padding:10px 14px 10px 16px">{a}</span>'
                 f'<span style="font-family:\'Bebas Neue\';font-size:44px;letter-spacing:.03em">{t}</span></div>' for a, t in opts)
    inner = f"""{PANEL_CSS}<div style="display:flex;flex-direction:column;align-items:flex-start;height:100%">
<span class="lbl red k">QUICK POLL</span><span style="margin-top:24px"></span>{label_block(['WHAT&rsquo;S STOPPING YOU', 'FROM STARTING?'], 104)}
<div class="panel" style="margin-top:auto;padding:14px 30px 14px;width:100%">{ol}</div></div>"""
    job(f'{GK}/04_Templates/antihero-group-poll_1080x1080.png', S2, S2, shell(S2, S2, bg('daybreak', True), inner, 'center 62%', foot='light'))


# =====================================================================================================
# PLAYBOOK PDF  (11 x 8.5 landscape, same system as the Brand Bible)
# =====================================================================================================
BIBLE_ASSETS = pathlib.Path(KIT, '01_Brand-Bible', 'assets').as_uri()
THUMBS = os.path.join(WORK, 'thumbs')


def thumb(rel):
    """JPEG preview of a rendered kit file for the PDF (keeps the PDF small)."""
    src = os.path.join(S.OUT, *rel.split('/'))
    os.makedirs(THUMBS, exist_ok=True)
    dst = os.path.join(THUMBS, os.path.basename(rel).rsplit('.', 1)[0] + '.jpg')
    im = Image.open(src).convert('RGB')
    im.thumbnail((640, 640))
    im.save(dst, quality=86)
    return file_url(dst)


GUIDE_CSS = font_face_css(pathlib.Path(FONTS).as_uri()) + """
:root{--void:%VOID%;--carbon:%CARBON%;--ash:%ASH%;--bone:%BONE%;--red:%RED%}
@page{size:11in 8.5in;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Barlow',system-ui,sans-serif;color:#fff;-webkit-font-smoothing:antialiased;font-size:13px;line-height:1.5}
.page{width:1056px;height:816px;position:relative;overflow:hidden;background:var(--void);padding:74px 72px 56px;break-after:page}
.page.light{background:var(--bone);color:var(--void)}
.hdr{position:absolute;top:30px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center;
     font-family:'Barlow Condensed';font-weight:700;font-size:11px;letter-spacing:.26em;opacity:.62}
.hdr .pn{font-family:'JetBrains Mono';font-weight:400;letter-spacing:.06em}
.lbl{font-family:'Bebas Neue';font-weight:400;line-height:1;text-box:trim-both cap alphabetic;display:inline-block;
     background:#fff;color:var(--void);white-space:nowrap;padding:.14em .2em .14em .22em}
.lbl.r{background:var(--red);color:#fff}.lbl.k{background:var(--void);color:#fff}
.eyebrow{font-family:'Barlow Condensed';font-weight:700;font-size:12px;letter-spacing:.28em;color:var(--red);text-transform:uppercase}
h1,h2,h3{font-family:'Bebas Neue';font-weight:400;line-height:.92;letter-spacing:.005em}
h1{font-size:84px}h2{font-size:54px}h3{font-size:24px;letter-spacing:.02em}
h1 em,h2 em,h3 em{font-style:normal;color:var(--red)}
p{max-width:64ch}
.muted{opacity:.74}
.mono{font-family:'JetBrains Mono',monospace}
.small{font-size:11.6px;line-height:1.5}
.num{font-family:'JetBrains Mono';font-size:12px;color:var(--red);letter-spacing:.08em}
.paste{font-family:'JetBrains Mono';font-size:10.6px;line-height:1.55;white-space:pre-wrap;background:#fff;color:#1d2124;border-left:3px solid var(--red);padding:14px 16px}
.page:not(.light) .paste{background:#16181b;color:#e8e8e8}
.cap{font-family:'Barlow Condensed';font-weight:700;font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;opacity:.7}
.row{border-bottom:1px solid rgba(255,255,255,.12)}.light .row{border-color:rgba(0,0,0,.12)}
img.shot{display:block;width:100%;box-shadow:0 8px 24px rgba(0,0,0,.25)}
"""
for k, v in dict(VOID=C['void'], CARBON=C['carbon'], ASH=C['ash'], BONE=C['bone'], RED=C['ignition']).items():
    GUIDE_CSS = GUIDE_CSS.replace(f'%{k}%', v)

GPAGES = []


def gpage(body, cls=''):
    GPAGES.append((cls, body))


def ghdr(title):
    return f'<div class="hdr"><span>ANTIHERO / FACEBOOK GROUP KIT</span><span>{title}</span><span class="pn">{{PN}}</span></div>'


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def guide():
    # 1 cover
    gpage(f"""<div style="position:absolute;inset:0;background:url({BIBLE_ASSETS}/bg-first-light.jpg) 30% 50%/cover"></div>
<div style="position:relative;height:100%;display:flex;flex-direction:column;align-items:flex-start;justify-content:center">
<div style="margin-bottom:28px">{badge_inline(150)}</div>
<span class="lbl k" style="font-size:112px">THE GROUP KIT</span>
<span class="lbl k" style="font-size:32px;letter-spacing:.06em">FACEBOOK GROUP PLAYBOOK &middot; SETUP, RHYTHM, AND THE FIRST TEN POSTS</span>
<span class="lbl r" style="font-size:22px;letter-spacing:.18em;padding:.3em .5em .3em .66em;margin-top:24px">BE YOUR OWN HERO</span>
<div class="mono" style="position:absolute;bottom:26px;left:0;font-size:11px;letter-spacing:.14em;color:var(--void);background:rgba(236,232,225,.86);padding:6px 10px">VERSION 1.0 &middot; SEPTEMBER 2026 &middot; FOR ADMINS</div></div>""")

    # 2 setup
    rows = ''.join(f'<div class="row" style="display:grid;grid-template-columns:34px 170px 1fr;gap:10px;padding:8px 0;align-items:baseline">'
                   f'<span class="num">{i + 1:02d}</span><span style="font-family:\'Bebas Neue\';font-size:22px;line-height:1">{t}</span>'
                   f'<span class="small muted">{esc(d)}</span></div>' for i, (t, d) in enumerate(SETUP))
    gpage(f"""{ghdr('Setup')}<div style="display:grid;grid-template-columns:1.25fr 1fr;gap:44px;height:100%">
<div><div class="eyebrow">Thirty minutes, once</div><h1 style="margin-top:10px">SET IT UP <em>RIGHT</em></h1><div style="margin-top:18px">{rows}</div></div>
<div style="display:flex;flex-direction:column;justify-content:center;gap:12px"><img class="shot" src="{thumb(f'{GK}/01_Cover/antihero-group-cover-write-your-story_1640x856.png')}">
<div class="cap">Group cover &middot; 1640 x 856 &middot; write your own story</div>
<p class="small muted" style="margin-top:8px">Four more group covers (Rise, Launch, Formation, Manifesto) live in 05_Social/Facebook/Group-Cover. Rotate them for launches and seasons.</p></div></div>""")

    # 3 name + about
    gpage(f"""{ghdr('Name and About')}<div style="display:grid;grid-template-columns:1fr 1.15fr;gap:44px;height:100%">
<div><div class="eyebrow">What people see first</div><h1 style="margin-top:10px">NAME IT. <em>SAY WHY.</em></h1>
<div class="cap" style="margin-top:26px">Group name</div><div style="font-family:'Bebas Neue';font-size:36px;line-height:1.05;margin-top:6px">{esc(NAME)}</div>
<div class="cap" style="margin-top:16px">Alternates</div>{''.join(f'<div class="small" style="margin-top:4px">{esc(a)}</div>' for a in NAME_ALTS)}
<p class="small muted" style="margin-top:18px">Keep AntiHero first so the brand is searchable, and put the topic after it so strangers know what they&rsquo;re joining. The group is live at <span class="mono">{GROUP_URL}</span>.</p>
<div class="cap" style="margin-top:18px">Privacy</div><p class="small" style="margin-top:4px">Private and visible. Anyone can find the group and read the About; only members see the posts. People share real numbers and real doubts in a room, not on a stage.</p></div>
<div><div class="cap">About this group &middot; paste as is</div><div class="paste" style="margin-top:8px">{esc(ABOUT)}</div></div></div>""", 'light')

    # 4 rules + questions
    # seven rules: one wide column for the rules, the graphic and the questions share the other
    rl = ''.join(f'<div class="row" style="display:grid;grid-template-columns:30px 1fr;gap:10px;padding:6px 0"><span class="num">{i + 1:02d}</span>'
                 f'<div><div style="font-family:\'Bebas Neue\';font-size:20px;line-height:1">{esc(t.upper())}</div><div class="muted" style="margin-top:2px;font-size:11px;line-height:1.42">{esc(d)}</div></div></div>'
                 for i, (t, d) in enumerate(RULES))
    ql = ''.join(f'<div style="display:grid;grid-template-columns:34px 1fr;gap:10px;margin-top:8px"><span class="num">Q{i + 1}</span><span class="small">{esc(q)}</span></div>'
                 for i, q in enumerate(QUESTIONS))
    gpage(f"""{ghdr('Rules and questions')}<div style="display:grid;grid-template-columns:1.45fr 1fr;gap:40px;height:100%">
<div><div class="eyebrow">Short on purpose</div><h2 style="margin-top:8px">HOUSE <em>RULES</em></h2><p class="small muted" style="margin-top:6px">Add each one in the group&rsquo;s Rules section: bold line as the title, the rest as the description.</p>
<div style="margin-top:6px">{rl}</div></div>
<div><div style="display:grid;grid-template-columns:140px 1fr;gap:16px;align-items:end"><img class="shot" src="{thumb(f'{GK}/02_Pinned/antihero-group-house-rules_1080x1350.png')}"><div class="cap">House rules graphic, for the featured post</div></div>
<div class="eyebrow" style="margin-top:22px">At the door</div><h2 style="margin-top:8px">THREE <em>QUESTIONS</em></h2>
<p class="small muted" style="margin-top:8px">They filter out bots and tell you what to teach. Read the answers weekly.</p>{ql}
<div class="small" style="margin-top:14px;padding:10px 12px;border-left:3px solid var(--red);background:rgba(255,255,255,.05)">{esc(QUESTION_ALT)}</div>
<p class="small muted" style="margin-top:14px">Turn on &ldquo;ask people to agree to the rules&rdquo; so the rules become a checkbox at the door.</p></div></div>""")

    # 5 weekly rhythm
    cards = ''.join(f"""<div><img class="shot" src="{thumb(f"{GK}/03_Weekly-Series/antihero-series-{s['slug']}_1080x1350.png")}">
<div style="display:flex;align-items:baseline;gap:8px;margin-top:10px"><span class="num">{s['short']}</span><span style="font-family:'Bebas Neue';font-size:20px;line-height:1">{' '.join(s['title'])}</span></div>
<div class="small muted" style="margin-top:3px;font-size:10.8px">{s['line']}</div><div class="cap" style="margin-top:4px;font-size:9.5px">TOPIC &middot; {s['topic']}</div></div>""" for s in SERIES)
    gpage(f"""{ghdr('The weekly rhythm')}<div class="eyebrow">Every day has a job</div><h1 style="margin-top:10px">THE <em>WEEK</em></h1>
<p class="muted" style="margin-top:10px;max-width:90ch">Six series, one per day, same card every week. Members learn the rhythm, and you never stare at a blank post. The card stays the same; the caption changes. Sunday is off. Go outside.</p>
<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:16px;margin-top:22px">{cards}</div>""")

    # 6-7 launch posts
    def post_cell(i, p):
        return f"""<div style="display:grid;grid-template-columns:104px 1fr;gap:16px;align-items:start">
<img class="shot" src="{thumb(p['img'])}"><div><div style="display:flex;gap:10px;align-items:baseline"><span class="num">{i:02d} &middot; {p['when'].upper()}</span></div>
<div style="font-family:'Bebas Neue';font-size:22px;line-height:1;margin-top:3px">{esc(p['title'].upper())}</div>
<div class="small" style="white-space:pre-line;margin-top:5px;font-size:10.4px;line-height:1.42;opacity:.86">{esc(p['caption'])}</div></div></div>"""
    for a, b, note in [(0, 4, 'Captions are ready to paste. Zero asks. Every post gives something away.'), (4, 8, 'Continued.'), (8, 10, 'Continued.')]:
        gpage(f"""{ghdr(f'The first ten posts, {a + 1} to {b}')}<div style="display:flex;align-items:baseline;gap:22px"><h2>THE FIRST <em>TEN POSTS</em></h2>
<span class="small muted">{note}</span></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:26px 40px;margin-top:22px">{''.join(post_cell(a + i + 1, p) for i, p in enumerate(LAUNCH[a:b]))}</div>{AFTER if b == 10 else ''}""", 'light')

    # 9 give first
    lad = ''.join(f"""<div style="display:grid;grid-template-columns:120px 1fr;gap:14px;padding:12px 0;align-items:baseline" class="row">
<span class="lbl {'r' if i == 0 else ''}" style="font-size:24px;letter-spacing:.1em;justify-self:start">{a}</span>
<div><div style="font-family:'Bebas Neue';font-size:22px;line-height:1">{b.upper()}</div><div class="small muted" style="margin-top:3px">{esc(c)}</div></div></div>""" for i, (a, b, c) in enumerate(LADDER))
    rules = ''.join(f'<div style="display:grid;grid-template-columns:30px 1fr;gap:8px;margin-top:9px"><span class="num">{i + 1:02d}</span><span class="small">{esc(r)}</span></div>' for i, r in enumerate(ASK_RULES))
    score = ''.join(f'<div style="border-top:1px solid rgba(255,255,255,.18);padding-top:8px"><div style="font-family:\'Bebas Neue\';font-size:20px;line-height:1">{a.upper()}</div><div class="cap" style="margin-top:3px;font-size:9.5px">{b}</div></div>' for a, b in SCORE)
    gpage(f"""{ghdr('Give first, ask rarely')}<div style="display:grid;grid-template-columns:1.1fr 1fr;gap:48px;height:100%">
<div><div class="eyebrow">The Gary Vee rule, our way</div><h1 style="margin-top:10px">GIVE FIRST. <em>ASK RARELY.</em></h1>
<p class="muted" style="margin-top:12px">The group is the product, not the funnel. When the group is worth joining on its own, the people who want more find the next rung without a push.</p>
<div style="margin-top:14px">{lad}</div></div>
<div><div class="cap">Five rules for asking</div>{rules}
<div class="cap" style="margin-top:26px">Keep score, weekly</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:12px 18px;margin-top:10px">{score}</div>
<div style="display:flex;gap:14px;align-items:center;margin-top:26px">{kr8tiv_svg(24)}<span class="cap" style="opacity:.6">THE FAMILY &middot; LEARN IT, DESIGN IT, AUTOMATE IT</span></div></div></div>""")

    # 10 asset index
    day = {s['slug']: i for i, s in enumerate(SERIES)}      # weekly cards in day order, not alphabetical
    files = sorted((p for p in pathlib.Path(OUT).rglob('*.png') if '_safe-zone-guides' not in p.parts),
                   key=lambda p: (p.parent.name, day.get(p.stem.replace('antihero-series-', '').split('_')[0], 99), p.name))
    tiles = ''.join(f"""<div><div style="height:118px;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.05)">
<img src="{thumb(str(p.relative_to(S.OUT)).replace(os.sep, '/'))}" style="max-height:118px;max-width:100%;display:block"></div>
<div class="mono" style="font-size:8.6px;margin-top:5px;word-break:break-all;opacity:.8">{p.parent.name}/<br>{p.name}</div></div>""" for p in files)
    gpage(f"""{ghdr('What&rsquo;s in the folder')}<div style="display:flex;align-items:baseline;gap:22px"><h2>EVERY <em>FILE</em></h2>
<span class="small muted">05_Social/Facebook/Group-Kit. The editable HTML sources sit in _build/templates.</span></div>
<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:16px 14px;margin-top:20px">{tiles}</div>""", 'light')

    # 11 back
    gpage(f"""<div style="position:absolute;inset:0;background:url({BIBLE_ASSETS}/bg-rise-above.jpg) 62% 50%/cover"></div>
<div style="position:relative;height:100%;display:flex;flex-direction:column;align-items:flex-start;justify-content:center">
<span class="lbl k" style="font-size:82px">NOBODY&rsquo;S COMING TO SAVE YOU.</span>
<span class="lbl r" style="font-size:82px">YOU NEVER NEEDED SAVING.</span>
<div style="margin-top:34px">{wordmark_svg(C['void'], C['ignition'], 64)}</div></div>""")
    return _write_guide()


AFTER = """<div style="margin-top:26px;padding:16px 20px;background:var(--void);color:#fff;display:grid;grid-template-columns:170px 1fr;gap:20px;align-items:center">
<div style="font-family:'Bebas Neue';font-size:30px;line-height:1">AFTER <span style="color:var(--red)">POST TEN</span></div>
<div class="small" style="opacity:.86">Run the weekly series. Mix in the kit&rsquo;s other posts: Break Formation (post 08), the creed (post 02), and the member spotlight whenever someone ships. The first &ldquo;Want it done for you?&rdquo; post (post 09) waits until week nine.</div></div>"""


def _write_guide():
    n = len(GPAGES)
    body = ''.join(f'<section class="page {c}">{b.replace("{PN}", f"{i:02d} / {n:02d}")}</section>' for i, (c, b) in enumerate(GPAGES, 1))
    html = f'<!doctype html><html><head><meta charset="utf-8"><title>AntiHero Facebook Group Kit</title><style>{GUIDE_CSS}</style></head><body>{body}</body></html>'
    hp = os.path.join(WORK, 'group-guide.html')
    open(hp, 'w', encoding='utf-8').write(html)
    return hp


FIT_JS = """() => [...document.querySelectorAll('.page')].map((pg, i) => {
  const r = pg.getBoundingClientRect(); let bottom = 0, right = 0;
  for (const el of pg.querySelectorAll('*')) {
    const cs = getComputedStyle(el);
    if (cs.position === 'absolute' && el.children.length === 0 && !el.textContent.trim()) continue;   // full-bleed image layers
    const b = el.getBoundingClientRect();
    if (!b.height) continue;
    bottom = Math.max(bottom, b.bottom - r.top); right = Math.max(right, b.right - r.left);
  }
  return {page: i + 1, bottom: Math.round(bottom), right: Math.round(right), h: Math.round(r.height), w: Math.round(r.width)};
})"""


def check_fit(r, html_path, margin=18):
    """Fails when any page's content runs into the bottom or right edge (clipped text is invisible in a PDF)."""
    pg = r.browser.new_page(viewport={'width': 1056, 'height': 816})
    pg.goto(file_url(html_path))
    pg.wait_for_timeout(500)
    rows = pg.evaluate(FIT_JS)
    pg.close()
    bad = [x for x in rows if x['bottom'] > x['h'] - margin or x['right'] > x['w'] - margin]
    print('guide fit (bottom/816):', ' '.join(f"p{x['page']}={x['bottom']}" for x in rows))
    if bad:
        raise SystemExit(f'guide content hits the page edge: {bad}')


def copy_txt():
    L = ['ANTIHERO FACEBOOK GROUP KIT - PASTE-READY COPY', '=' * 60, '', 'GROUP NAME', NAME, 'Alternates: ' + ' / '.join(NAME_ALTS), '',
         'GROUP ADDRESS', GROUP_URL, '',
         'PRIVACY', 'Private, visible in search.', '', 'ABOUT THIS GROUP', ABOUT, '', 'HOUSE RULES (title / description)']
    L += [f'{i + 1}. {t}\n   {d}' for i, (t, d) in enumerate(RULES)]
    L += ['', 'MEMBERSHIP QUESTIONS'] + [f'{i + 1}. {q}' for i, q in enumerate(QUESTIONS)] + ['Optional: ' + QUESTION_ALT, 'Turn on: ask people to agree to the rules.', '']
    L += ['THE WEEKLY SERIES (card + caption template)']
    for s in SERIES:
        L += ['', f"{s['short']} - {' '.join(t.replace('&amp;', '&') for t in s['title'])}  [topic: {s['topic']}]",
              f"Card: Group-Kit/03_Weekly-Series/antihero-series-{s['slug']}_1080x1350.png", s['caption']]
    L += ['', 'SUN - off. Go outside.', '', '=' * 60, 'THE FIRST TEN POSTS']
    for i, p in enumerate(LAUNCH, 1):
        L += ['', f"{i:02d}. {p['when']} - {p['title']}", f"Image: 05_Social/{p['img']}", '-' * 40, p['caption']]
    L += ['', '=' * 60, 'GIVE FIRST, ASK RARELY'] + [f'{a}: {b} - {c}' for a, b, c in LADDER] + [''] + [f'- {r}' for r in ASK_RULES]
    open(os.path.join(OUT, 'antihero-group-copy.txt'), 'w', encoding='utf-8').write('\n'.join(L).replace('&rsquo;', "'") + '\n')


if __name__ == '__main__':
    cover()
    event()
    pinned()
    series_cards()
    templates()
    with Renderer() as r:
        for hp, png, W, H in S.JOBS:
            r.png(hp, png, W, H, wait_ms=80)
        print('rendered', len(S.JOBS))
        gp = guide()
        check_fit(r, gp)
        r.pdf(gp, os.path.join(OUT, 'AntiHero-Facebook-Group-Kit.pdf'), width='11in', height='8.5in')
    copy_txt()
    print('guide pages', len(GPAGES))
