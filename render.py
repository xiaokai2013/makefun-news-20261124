"""Render the Nov 24, 2026 front page (1024x1024) from news.json.

A broadsheet column design: masthead, full-width lead with a drawn skyline
strip, a 2x2 middle grid, a two-story bottom band, and a source footer.
Pure Pillow, deterministic: no randomness, no time, no network.
Layout positions are computed from the text that is actually drawn, so
nothing can silently overlap.
"""

import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

W, H = 1024, 1024
MX = 46                      # side margin
PAPER = (246, 241, 231)      # warm newsprint
INK = (25, 25, 25)
RED = (158, 27, 27)
GRAY = (95, 95, 95)
SKY = (58, 62, 70)           # photo strip background
SMOKE = (150, 148, 140)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 80)
F_KICK = font("DejaVuSans-Bold.ttf", 18)
F_HEAD = font("DejaVuSerif-Bold.ttf", 54)
F_HEAD_MID = font("DejaVuSerif-Bold.ttf", 28)
F_HEAD_BOT = font("DejaVuSerif-Bold.ttf", 26)
F_DECK = font("DejaVuSans.ttf", 22)
F_DECK_MID = font("DejaVuSans.ttf", 18)
F_DATE = font("DejaVuSans-Bold.ttf", 17)
F_CAP = font("DejaVuSerif.ttf", 16)
F_FOOT = font("DejaVuSans.ttf", 15)


def wrap_text(text, fnt, width):
    """Greedy word wrap on measured pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_hline(d, y, x0=MX, x1=W - MX, width=2):
    d.line([(x0, y), (x1, y)], fill=INK, width=width)


def draw_kicker(d, text, x, y):
    d.text((x, y), text, font=F_KICK, fill=RED)


def draw_headline(d, text, fnt, x, y, width, leading):
    lines = wrap_text(text, fnt, width)
    for i, ln in enumerate(lines):
        d.text((x, y + i * leading), ln, font=fnt, fill=INK)
    return y + len(lines) * leading


def draw_deck(d, text, fnt, x, y, width, leading):
    lines = wrap_text(text, fnt, width)
    for i, ln in enumerate(lines):
        d.text((x, y + i * leading), ln, font=fnt, fill=GRAY)
    return y + len(lines) * leading


def draw_skyline(d, x0, y0, x1, y1):
    """A night skyline strip: dark band, building silhouettes, lit windows,
    smoke puffs. Fixed coordinates, fully deterministic."""
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    base = y1
    # buildings: (x offset, width, height, shade)
    towers = [
        (0, 70, 52, (30, 32, 38)),
        (74, 46, 78, (22, 24, 30)),
        (124, 84, 44, (30, 32, 38)),
        (212, 52, 66, (22, 24, 30)),
        (268, 96, 38, (30, 32, 38)),
        (368, 58, 72, (22, 24, 30)),
        (430, 78, 48, (30, 32, 38)),
        (512, 50, 80, (22, 24, 30)),
        (566, 90, 42, (30, 32, 38)),
        (660, 56, 68, (22, 24, 30)),
        (720, 88, 46, (30, 32, 38)),
        (812, 48, 74, (22, 24, 30)),
        (864, 68, 50, (30, 32, 38)),
    ]
    for ox, bw, bh, shade in towers:
        d.rectangle([x0 + ox, base - bh, x0 + ox + bw, base], fill=shade)
    # lit windows: fixed grid of tiny warm squares on some towers
    wins = [(82, 26), (96, 40), (136, 18), (150, 32), (224, 30), (282, 20),
            (296, 34), (380, 26), (396, 42), (446, 22), (524, 30), (540, 46),
            (578, 24), (676, 30), (732, 22), (748, 36), (826, 28), (878, 22)]
    for wx, wy in wins:
        d.rectangle([x0 + wx, base - wy, x0 + wx + 5, base - wy + 6],
                    fill=(232, 196, 120))
    # smoke puffs rising from one tower
    puffs = [(300, 22, 16), (322, 34, 12), (344, 46, 9), (288, 36, 10)]
    for px, py, pr in puffs:
        d.ellipse([x0 + px - pr, y0 + py - pr, x0 + px + pr, y0 + py + pr],
                  fill=SMOKE)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_masthead(d, data):
    title = data["masthead"]
    tw = F_TITLE.getlength(title)
    d.text(((W - tw) / 2, 22), title, font=F_TITLE, fill=INK)
    draw_hline(d, 114, width=3)
    d.text((MX, 120), data["dateline_left"], font=F_DATE, fill=INK)
    right = data["dateline_right"]
    d.text((W - MX - F_DATE.getlength(right), 120), right, font=F_DATE,
           fill=INK)
    draw_hline(d, 142, width=1)


def draw_lead(d, data):
    lead = data["lead"]
    y = 152
    draw_kicker(d, lead["kicker"], MX, y)
    y = 178
    y = draw_headline(d, lead["headline"], F_HEAD, MX, y, W - 2 * MX, 62)
    y = draw_deck(d, lead["deck"], F_DECK, MX, y + 8, W - 2 * MX, 28)
    return y


def draw_story(d, story, x, y, width, head_fnt, head_lead, deck_fnt,
               deck_lead):
    draw_kicker(d, story["kicker"], x, y)
    y2 = draw_headline(d, story["headline"], head_fnt, x, y + 24, width,
                       head_lead)
    draw_deck(d, story["deck"], deck_fnt, x, y2 + 4, width, deck_lead)


def build_page(data):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d, data)

    # Lead block, then the skyline strip and its caption.
    lead_end = draw_lead(d, data)
    strip_y0 = lead_end + 10
    strip_y1 = strip_y0 + 90
    draw_skyline(d, MX, strip_y0, W - MX, strip_y1)
    cap_y = strip_y1 + 6
    d.text((MX, cap_y), data["photo_caption"], font=F_CAP, fill=GRAY)

    # Middle 2x2 grid.
    col_w = (W - 2 * MX - 20) // 2
    x_left, x_right = MX, MX + col_w + 20
    row1 = cap_y + 30
    row2 = row1 + 148
    draw_story(d, data["stories"][0], x_left, row1, col_w, F_HEAD_MID, 32,
               F_DECK_MID, 22)
    draw_story(d, data["stories"][1], x_right, row1, col_w, F_HEAD_MID, 32,
               F_DECK_MID, 22)
    draw_hline(d, row1 + 144, width=1)
    d.line([(512, row1), (512, row2 + 136)], fill=INK, width=1)
    draw_story(d, data["stories"][2], x_left, row2, col_w, F_HEAD_MID, 32,
               F_DECK_MID, 22)
    draw_story(d, data["stories"][3], x_right, row2, col_w, F_HEAD_MID, 32,
               F_DECK_MID, 22)

    # Bottom band: two stories side by side.
    bot_rule = row2 + 148
    draw_hline(d, bot_rule, width=1)
    bot_y = bot_rule + 12
    draw_story(d, data["stories"][4], x_left, bot_y, col_w, F_HEAD_BOT, 30,
               F_DECK_MID, 22)
    draw_story(d, data["stories"][5], x_right, bot_y, col_w, F_HEAD_BOT, 30,
               F_DECK_MID, 22)
    d.line([(512, bot_y), (512, bot_y + 106)], fill=INK, width=1)

    # Footer.
    foot_rule = bot_y + 118
    draw_hline(d, foot_rule, width=2)
    d.text((MX, foot_rule + 8), data["footer"], font=F_FOOT, fill=GRAY)
    credit = data["credit"]
    d.text(((W - F_FOOT.getlength(credit)) / 2, foot_rule + 30), credit,
           font=F_FOOT, fill=GRAY)
    return img


def main():
    with open(os.path.join(HERE, "news.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    img = build_page(data)
    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG")
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
