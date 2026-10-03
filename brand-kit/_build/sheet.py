"""Contact sheets: lay PNGs into a grid (checker behind transparent ones) with labels."""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
LABEL_FONT = os.path.join(HERE, 'fonts', 'barlowcondensed__BarlowCondensed-SemiBold.ttf')


def checker(w, h, s=16, a=(58, 62, 66), b=(46, 50, 54)):
    im = Image.new('RGB', (w, h), a)
    d = ImageDraw.Draw(im)
    for y in range(0, h, s):
        for x in range(0, w, s):
            if (x // s + y // s) % 2:
                d.rectangle([x, y, x + s - 1, y + s - 1], fill=b)
    return im


def contact_sheet(files, out, cols=4, cell=(420, 300), pad=18, bg=(20, 22, 24), label=True, light_cells=()):
    rows = (len(files) + cols - 1) // cols
    lab_h = 30 if label else 0
    W = cols * cell[0] + (cols + 1) * pad
    H = rows * (cell[1] + lab_h) + (rows + 1) * pad
    sheet = Image.new('RGB', (W, H), bg)
    font = ImageFont.truetype(LABEL_FONT, 20)
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(files):
        r, c = divmod(i, cols)
        x = pad + c * (cell[0] + pad)
        y = pad + r * (cell[1] + lab_h + pad)
        tile = checker(*cell) if not any(k in os.path.basename(f) for k in light_cells) else checker(*cell, a=(214, 214, 210), b=(196, 196, 192))
        im = Image.open(f).convert('RGBA')
        im.thumbnail((cell[0] - 24, cell[1] - 24), Image.LANCZOS)
        tile.paste(im, ((cell[0] - im.width) // 2, (cell[1] - im.height) // 2), im)
        sheet.paste(tile, (x, y))
        if label:
            name = os.path.splitext(os.path.basename(f))[0]
            d.text((x, y + cell[1] + 4), name[:58], font=font, fill=(200, 204, 208))
    sheet.save(out)
    return out


if __name__ == '__main__':
    import glob
    root = sys.argv[1]
    pattern = sys.argv[2]
    out = sys.argv[3]
    cols = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    light = sys.argv[5].split(',') if len(sys.argv) > 5 else ()
    files = sorted(glob.glob(os.path.join(root, pattern), recursive=True))
    contact_sheet(files, out, cols=cols, light_cells=light)
    print(len(files), 'files ->', out)
