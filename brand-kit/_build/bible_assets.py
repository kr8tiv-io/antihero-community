"""Collect + optimise the images the Brand Bible uses into 01_Brand-Bible/assets."""
import glob
import os

from PIL import Image

from brand import KIT

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(KIT, '01_Brand-Bible', 'assets')
os.makedirs(A, exist_ok=True)
for old in glob.glob(os.path.join(A, 'bg-*.jpg')) + glob.glob(os.path.join(A, 'fb-cover-*.jpg')):
    os.remove(old)          # regenerated below from the current (v2) set


def put(src, name, max_side=1400, fmt=None, crop=None):
    im = Image.open(src)
    if crop:
        im = im.crop(crop)
    has_alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    fmt = fmt or ('png' if has_alpha else 'jpg')
    out = os.path.join(A, f'{name}.{fmt}')
    if fmt == 'jpg':
        im.convert('RGB').save(out, quality=86, optimize=True, progressive=True)
    else:
        im.save(out, optimize=True)
    return out


L = os.path.join(KIT, '02_Logos')
S = os.path.join(KIT, '05_Social')
W = os.path.join(HERE, 'work')

# heritage + rebuild
put(os.path.join(W, 'source_youtube_channel.png'), 'heritage-channel', 1600, 'jpg', crop=(112, 74, 1450, 290))
put(os.path.join(W, 'source_logo.png'), 'heritage-logo-original', 400, 'png')
put(os.path.join(W, 'source_logo.png'), 'heritage-logo-original-zoom', 1400, 'png', crop=(170, 40, 300, 170))
# zoom crop of the rebuild at the same region (disc frame 1000u <-> source px: use the 4096 render)
reb = Image.open(os.path.join(L, '01_Badge', 'antihero-badge-carbon_4096px.png'))
k = 4096 / 1000.0
# source crop (170,40)-(300,170) in source px -> badge units: u = (x - 173.94)/150*500 + 500
def s2b(x, y):
    return ((x - 173.94) / 149.98 * 500 + 500) * k, ((y - 164.94) / 149.98 * 500 + 500) * k
x0, y0 = s2b(170, 40)
x1, y1 = s2b(300, 170)
reb.crop((int(x0), int(y0), int(x1), int(y1))).resize((1400, 1400), Image.LANCZOS).save(os.path.join(A, 'rebuild-zoom.png'), optimize=True)

for f in ['01_Badge/antihero-badge-carbon_1024px.png', '01_Badge/antihero-badge-black_1024px.png', '01_Badge/antihero-badge-white_1024px.png',
          '01_Badge/antihero-badge-ignition_1024px.png', '01_Badge/antihero-badge-bone_1024px.png', '01_Badge/antihero-badge-outline-white_1024px.png',
          '01_Badge/antihero-badge-knockout-white_1024px.png', '01_Badge/antihero-badge-knockout-carbon_1024px.png',
          '02_Mark/antihero-mark-white_1024px.png', '02_Mark/antihero-mark-black_1024px.png', '02_Mark/antihero-mark-duo-white-ignition_1024px.png',
          '03_Wordmark/antihero-wordmark-white-ignition_2048px.png', '03_Wordmark/antihero-wordmark-black-ignition_2048px.png',
          '03_Wordmark/antihero-wordmark-white_2048px.png', '03_Wordmark/antihero-wordmark-caps-white_2048px.png',
          '03_Wordmark/antihero-wordmark-label-white_2048px.png', '03_Wordmark/antihero-wordmark-label-ignition_2048px.png',
          '04_Lockups/antihero-lockup-horizontal-on-dark-ignition_2048px.png', '04_Lockups/antihero-lockup-horizontal-on-light-ignition_2048px.png',
          '04_Lockups/antihero-lockup-stacked-on-dark-ignition_1500px.png', '04_Lockups/antihero-tagline-white_1500px.png',
          '05_Icons/antihero-app-icon-rounded_512px.png', '05_Icons/favicon-32.png', '05_Icons/favicon-64.png',
          '06_Construction/antihero-construction_2400px.png', '06_Construction/antihero-clearspace_2400px.png']:
    name = os.path.splitext(os.path.basename(f))[0].replace('antihero-', '')
    put(os.path.join(L, f), name, 1200 if 'construction' in f or 'clearspace' in f else 900, 'png')

for f in sorted(glob.glob(os.path.join(KIT, '03_Logo-Textures', '*.jpg'))):
    put(f, 'tex-' + os.path.basename(f).split('texture-')[1].split('_')[0], 900, 'jpg')
for f in sorted(glob.glob(os.path.join(KIT, '04_Backgrounds', '*desktop*.jpg'))):
    put(f, 'bg-' + os.path.basename(f).split('bg-')[1].split('_')[0], 1300, 'jpg')

put(os.path.join(L, '07_Family', 'antihero-family-lockup-on-dark_3000px.png'), 'family-lockup-on-dark', 1400, 'png')
put(os.path.join(L, '07_Family', 'kr8tiv-endorsement-antihero-family-on-dark_1200px.png'), 'endorse-family-on-dark', 900, 'png')
for f, n in [('Facebook/Page-Cover/antihero-fb-page-cover-rise_1640x924.png', 'fb-cover-rise'),
             ('Facebook/Page-Cover/antihero-fb-page-cover-launch_1640x924.png', 'fb-cover-launch'),
             ('Facebook/Page-Cover/antihero-fb-page-cover-formation_1640x924.png', 'fb-cover-formation'),
             ('Facebook/Page-Cover/antihero-fb-page-cover-manifesto_1640x924.png', 'fb-cover-manifesto'),
             ('Facebook/Page-Cover/_safe-zone-guides/antihero-fb-page-cover-rise_1640x924__GUIDE.png', 'fb-cover-guide'),
             ('Facebook/Group-Cover/antihero-fb-group-cover-rise_1640x856.png', 'fb-group-cover'),
             ('Facebook/Profile-Picture/_preview-circle-crop.png', 'fb-profile-preview'),
             ('Posts/antihero-post-01-welcome_1080x1350.png', 'post-01'), ('Posts/antihero-post-02-quote_1080x1350.png', 'post-02'),
             ('Posts/antihero-post-03-ai-tool_1080x1350.png', 'post-03'), ('Posts/antihero-post-04-workshop_1080x1350.png', 'post-04'),
             ('Posts/antihero-post-05-seo-tip_1080x1350.png', 'post-05'), ('Posts/antihero-post-06-now-open_1080x1080.png', 'post-06'),
             ('Posts/antihero-post-07-runway_1080x1350.png', 'post-07'), ('Posts/antihero-post-08-break-formation_1080x1350.png', 'post-08'),
             ('Posts/antihero-post-09-work-with-us_1080x1350.png', 'post-09'),
             ('Posts/antihero-story-01-join_1080x1920.png', 'story-01'),
             ('YouTube/antihero-youtube-banner_2560x1440.png', 'yt-banner'), ('YouTube/antihero-youtube-thumbnail-template_1280x720.png', 'yt-thumb'),
             ('LinkedIn/antihero-linkedin-banner_1584x396.png', 'li-banner'), ('X-Twitter/antihero-x-header_1500x500.png', 'x-header'),
             ('Video-Call/antihero-zoom-background-concrete_1920x1080.png', 'zoom-bg'), ('Email/antihero-email-signature_1200x300.png', 'email-sig')]:
    put(os.path.join(S, f), n, 1100, 'jpg')
print('assets:', len(os.listdir(A)))
