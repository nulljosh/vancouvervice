#!/usr/bin/env python3
"""Draw the Vancouver Vice key art: a GTA cover grid of six flat Vancouver panels.
Writes docs/img/key-art.svg. Render it with tools/key_art.mjs."""
import random
from pathlib import Path

R = random.Random(7)
INK, CREAM, RED, BLUE, LAMP = '#121418', '#f5f3ee', '#c0392b', '#2b5fb3', '#f9c77c'
W, H = 1600, 900


def rect(x, y, w, h, f, extra=''):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{f}" {extra}/>'


def poly(pts, f, extra=''):
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{f}" {extra}/>'


def circ(cx, cy, r, f, extra=''):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{f}" {extra}/>'


def line(x1, y1, x2, y2, s, w, extra=''):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{s}" stroke-width="{w}" {extra}/>'


def bands(w, stops):
    # ponytail: stepped bands instead of gradients, it's the house rule and it reads as poster art
    out = []
    for (y, c), (y2, _) in zip(stops, stops[1:]):
        out.append(rect(0, y, w, y2 - y, c))
    return out


def rain(w, h, n, op):
    out = []
    for _ in range(n):
        x, y, l = R.uniform(-40, w), R.uniform(-20, h), R.uniform(18, 38)
        out.append(line(x, y, x + l * 0.3, y + l, '#ffffff', 1.4, f'opacity="{op}"'))
    return out


def skyline(x0, x1, base, hmin, hmax, fill, lit=0.0, skip=None, cap=0):
    out, x = [], x0
    while x < x1:
        w = R.uniform(26, 62)
        h = R.uniform(hmin, hmax)
        if skip and skip[0] < x + w and x < skip[1]:
            h = min(h, cap)
        out.append(rect(x, base - h, w, h + 2, fill))
        if lit:
            for wy in range(int(base - h + 10), int(base - 8), 12):
                for wx in range(int(x + 6), int(x + w - 8), 10):
                    if R.random() < lit:
                        out.append(rect(wx, wy, 4, 6, LAMP))
        x += w + R.uniform(-4, 6)
    return out


def car(x, y, body, roof, flip=False):
    # side view, wheels on y
    s = -1 if flip else 1
    out = [poly([(x, y - 8), (x, y - 26), (x + s * 18, y - 30), (x + s * 34, y - 46), (x + s * 74, y - 46),
                 (x + s * 92, y - 30), (x + s * 112, y - 26), (x + s * 112, y - 8)], body),
           poly([(x + s * 40, y - 42), (x + s * 72, y - 42), (x + s * 84, y - 30), (x + s * 30, y - 30)], roof),
           circ(x + s * 24, y - 6, 9, INK), circ(x + s * 90, y - 6, 9, INK),
           circ(x + s * 24, y - 6, 4, '#555a62'), circ(x + s * 90, y - 6, 4, '#555a62')]
    return out


def star(cx, cy, r, f, extra=''):
    import math
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return poly(pts, f, extra)


def panel(x, y, w, h, body):
    return (f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{"".join(body)}</svg>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{INK}" stroke-width="4"/>')


def joshua(fill, glasses=True):
    """Waist-up Joshua: curls, round glasses, polo, a bag of Mac minis. GTA covers live on the character."""
    b = []
    for a in range(190, 352, 18):
        import math
        r = math.radians(a)
        b.append(circ(870 + 44 * math.cos(r), 258 + 44 * math.sin(r), 19 + (a % 3) * 2, fill))
    b += [circ(870, 214, 22, fill), circ(846, 220, 18, fill), circ(894, 220, 18, fill),
          f'<ellipse cx="870" cy="268" rx="42" ry="50" fill="{fill}"/>',
          circ(828, 274, 10, fill), circ(912, 274, 10, fill), rect(850, 300, 40, 40, fill),
          poly([(744, 560), (752, 410), (770, 372), (820, 346), (850, 336), (890, 336), (922, 346), (978, 370), (1004, 404), (1010, 560)], fill)]
    if glasses:
        g = f'fill="none" stroke="{LAMP}" stroke-width="4"'
        b += [f'<circle cx="851" cy="266" r="15" {g}/>', f'<circle cx="889" cy="266" r="15" {g}/>',
              line(866, 264, 874, 264, LAMP, 4), line(836, 264, 828, 268, LAMP, 3), line(904, 264, 912, 268, LAMP, 3)]
        c = '#2a2e36'
        b += [poly([(836, 336), (870, 352), (862, 380)], c), poly([(904, 336), (870, 352), (878, 380)], c),
              line(870, 360, 870, 420, c, 3), line(944, 352, 812, 500, c, 12)]
    # the bag, Mac minis poking out the top
    b.append(rect(690, 486, 190, 80, fill if not glasses else '#1d2026', 'rx="14"'))
    if glasses:
        for i, (mx, my) in enumerate(((710, 466), (756, 458), (802, 470))):
            b += [rect(mx, my, 60, 18, '#c9ccd1', 'rx="5"'), rect(mx + 6, my + 3, 48, 3, '#eef0f2', 'rx="1.5"')]
    return b


def harbour_centre():
    """Hero: the downtown skyline at sunset from the water, Harbour Centre, the Lions, the SeaBus, rain."""
    w, h = 1000, 560
    b = bands(w, [(0, '#b8482c'), (90, '#d35d34'), (170, '#e8763f'), (245, '#f3944e'),
                  (310, '#f8b264'), (365, '#fbcd84'), (440, None)])
    b.append(circ(690, 300, 92, '#fde6ae'))
    for i, y in enumerate((318, 340, 360, 378)):
        b.append(rect(590, y, 200, 3 + i * 2, '#f8b264'))
    b.append(poly([(0, 330), (90, 300), (180, 318), (300, 270), (420, 300), (540, 262), (575, 236), (600, 258),
                   (625, 230), (660, 262), (780, 290), (880, 268), (1000, 300), (1000, 440), (0, 440)], '#c0603e'))
    b.append(poly([(0, 380), (140, 350), (260, 372), (380, 340), (520, 368), (700, 350), (840, 372), (1000, 344),
                   (1000, 440), (0, 440)], '#7a3b2c'))
    b.append(rect(0, 440, w, 120, '#1b2a40'))
    for i, y in enumerate(range(452, 552, 10)):
        ww = 170 - i * 14 + R.uniform(-10, 10)
        b.append(rect(690 - ww / 2 + R.uniform(-12, 12), y, ww, 3, '#f8b264', 'opacity=".75"'))
    b += skyline(110, 990, 442, 40, 120, '#5a2f28')
    b += skyline(-10, 1000, 442, 24, 150, INK, lit=0.1, skip=(330, 500), cap=90)
    # a few signature towers: Shangri-La, the Living Shangri-La step, the Vancouver House twist
    b += [rect(250, 196, 40, 246, INK), rect(258, 182, 24, 16, INK), rect(860, 236, 52, 206, INK),
          poly([(140, 442), (140, 250), (186, 226), (196, 442)], INK)]
    for x0, y0, x1 in ((254, 210, 286), (864, 250, 908)):
        for wy in range(y0, 430, 14):
            for wx in range(x0, x1 - 4, 9):
                if R.random() < 0.22:
                    b.append(rect(wx, wy, 4, 6, LAMP))
    b.append(rect(395, 212, 44, 230, INK))
    b.append(f'<ellipse cx="417" cy="210" rx="74" ry="21" fill="{INK}"/>')
    b.append(rect(347, 204, 140, 6, INK))
    for wx in range(356, 478, 13):
        b.append(rect(wx, 205, 7, 5, LAMP))
    b.append(rect(415, 130, 4, 64, INK))
    b.append(circ(417, 128, 4, RED))
    b.append(rect(0, 438, w, 6, INK))
    # SeaBus, mid crossing
    b.append(poly([(150, 512), (420, 512), (396, 530), (172, 530)], '#e3e6ea'))
    b.append(f'<rect x="168" y="474" width="236" height="40" rx="18" fill="#f3f4f6"/>')
    b.append(rect(238, 460, 90, 18, '#f3f4f6', 'rx="6"'))
    for wx in range(186, 380, 22):
        b.append(rect(wx, 482, 14, 12, '#253446', 'rx="3"'))
    b.append(rect(176, 500, 220, 6, BLUE))
    for i in range(4):
        b.append(line(60 + i * 18, 524 + i * 7, 150, 518 + i * 3, '#ffffff', 2, 'opacity=".55"'))
    b += rain(w, h, 170, 0.2)
    b += ['<g transform="translate(-6 -3)">'] + joshua('#fbcd84', glasses=False) + ['</g>']
    b += joshua(INK)
    return b


def burrard_chase():
    """Night chase across the Burrard Bridge, cop lights on the water."""
    w, h = 552, 272
    b = bands(w, [(0, '#0e1320'), (60, '#121a2a'), (120, '#18233a'), (200, None)])
    b += skyline(0, w, 176, 20, 90, '#1f2a3f', lit=0.22)
    b.append(rect(0, 196, w, 76, '#0b1018'))
    for px in (120, 410):
        b.append(rect(px, 94, 36, 120, '#2a2f38'))
        b.append(rect(px + 6, 80, 24, 16, '#2a2f38'))
        b.append(rect(px + 12, 66, 12, 16, '#2a2f38'))
        b.append(circ(px + 18, 62, 5, LAMP))
        b.append(circ(px + 18, 62, 16, LAMP, 'opacity=".2"'))
    for x in range(156, 410, 32):
        b.append(line(x, 118, x, 168, '#424a57', 5))
        b.append(line(x, 118, x + 32, 168, '#424a57', 4))
    b.append(line(156, 118, 410, 118, '#424a57', 7))
    b.append(rect(0, 166, w, 12, '#2a2f38'))
    # headlights from the cop onto the getaway car
    def big(x, parts):  # close-up camera: cars 1.45x, scaled from where the wheels meet the deck
        return [f'<g transform="translate({x} 168) scale(1.45) translate({-x} -168)">'] + parts + ['</g>']
    b.append(poly([(312, 140), (552, 104), (552, 176)], LAMP, 'opacity=".14"'))
    # drivers in the windows: Joshua's glasses catch the cop lights, the cop wears the cap
    josh_in = [circ(418, 134, 7, INK), circ(415, 128, 4, INK), circ(421, 128, 4, INK),
               f'<circle cx="420" cy="134" r="2.4" fill="none" stroke="{LAMP}" stroke-width="1.2"/>']
    cop_in = [circ(206, 134, 7, INK), rect(198, 125, 16, 4, INK), rect(200, 121, 12, 5, '#1d2b4a')]
    b += big(360, car(360, 168, RED, '#7d2119') + josh_in + [rect(358, 140, 5, 7, '#ff6b5b')])
    b += big(150, car(150, 168, '#f1f1ef', INK) + cop_in + [rect(152, 142, 108, 5, BLUE), rect(194, 116, 10, 6, RED), rect(204, 116, 10, 6, BLUE)])
    for cx, c in ((222, RED), (236, BLUE)):
        b.append(circ(cx, 92, 44, c, 'opacity=".16"'))
        b.append(circ(cx, 92, 9, c, 'opacity=".7"'))
    for x, c in ((214, RED), (244, BLUE)):
        for i in range(6):
            b.append(rect(x + R.uniform(-8, 8), 204 + i * 11, R.uniform(14, 34), 3, c, 'opacity=".45"'))
    return b


def gull_heist():
    """English Bay: a seagull steals your hot dog, Inukshuk on the beach."""
    w, h = 552, 272
    b = bands(w, [(0, '#8fc1e6'), (60, '#a6cfec'), (115, '#bfdcf0'), (150, None)])
    b.append(poly([(0, 150), (80, 136), (190, 144), (300, 128), (420, 142), (552, 132), (552, 152), (0, 152)], '#7d9fbd'))
    b.append(rect(0, 150, w, 54, '#2f6ea3'))
    for _ in range(26):
        x, y = R.uniform(0, w), R.uniform(156, 198)
        b.append(rect(x, y, R.uniform(8, 26), 2, '#ffffff', 'opacity=".55"'))
    b.append(rect(0, 202, w, 70, '#ecd3a0'))
    # Inukshuk
    s = '#6d6a66'
    b += [rect(420, 168, 14, 38, s), rect(450, 168, 14, 38, s), rect(414, 156, 56, 14, s),
          rect(396, 142, 92, 14, s), rect(426, 120, 32, 24, s), rect(430, 104, 24, 16, s)]
    # the victim, fist up
    b += [circ(96, 188, 12, INK), poly([(84, 184), (96, 172), (108, 184), (110, 200), (82, 200)], INK),
          poly([(78, 200), (114, 200), (118, 244), (74, 244)], INK), rect(80, 242, 12, 24, INK), rect(100, 242, 12, 24, INK),
          poly([(108, 204), (130, 176), (138, 182), (114, 212)], INK), circ(135, 176, 7, INK),
          poly([(80, 206), (64, 230), (70, 234), (86, 214)], INK), rect(60, 230, 14, 8, '#d9964b', 'rx="4"')]
    # the gull
    g = []
    g.append(poly([(176, 100), (120, 104), (66, 52), (40, 20), (96, 46)], '#b9bec6'))
    g.append(poly([(66, 52), (40, 20), (82, 40)], INK))
    g.append(poly([(150, 94), (212, 90), (250, 40), (276, 4), (214, 34)], '#d6d9de'))
    g.append(poly([(250, 40), (276, 4), (232, 26)], INK))
    g.append('<ellipse cx="180" cy="104" rx="62" ry="24" fill="#fbfbfa" transform="rotate(-8 180 104)"/>')
    g.append(poly([(120, 108), (90, 100), (96, 118)], '#e9eaec'))
    g.append(circ(238, 92, 20, '#fbfbfa'))
    g.append(circ(244, 86, 3.4, INK))
    g.append(poly([(254, 92), (290, 96), (256, 102)], '#f2c230'))
    g.append(circ(276, 98, 2.6, RED))
    # the hot dog
    g.append('<g transform="rotate(14 292 104)">'
             '<rect x="252" y="98" width="84" height="12" rx="6" fill="#b3442a"/>'
             '<rect x="258" y="102" width="72" height="18" rx="9" fill="#d9964b"/>'
             '<polyline points="262,99 270,95 278,100 286,95 294,100 302,95 310,100 318,95 326,99" '
             'fill="none" stroke="#f2c230" stroke-width="3"/></g>')
    b += g
    for i in range(4):
        b.append(line(10, 84 + i * 12, 70 - i * 6, 84 + i * 12, '#ffffff', 2.5, 'opacity=".8"'))
    return b


def steam_clock():
    """Gastown at night, rain on the cobbles, the steam clock venting."""
    w, h = 488, 292
    b = bands(w, [(0, '#121821'), (90, '#18202b'), (230, None)])
    x = -8
    for c in ('#4b2a22', '#5a3326', '#4f2c23', '#5d3528', '#4b2a22', '#563124', '#4f2c23'):
        bw, bh = R.uniform(62, 86), R.uniform(130, 190)
        b.append(rect(x, 230 - bh, bw, bh, c))
        b.append(rect(x, 230 - bh, bw, 8, '#2e1a15'))
        for wy in range(int(240 - bh), 210, 34):
            for wx in range(int(x + 10), int(x + bw - 18), 22):
                if R.random() < 0.6:
                    b.append(rect(wx, wy + 6, 12, 16, LAMP, 'opacity=".85"'))
                    b.append(circ(wx + 6, wy + 6, 6, LAMP, 'opacity=".85"'))
        x += bw
    b.append(rect(0, 228, w, 64, '#23262c'))
    for row, y in enumerate(range(236, 292, 10)):
        for cx in range(-10 + (row % 2) * 12, w, 24):
            b.append(f'<ellipse cx="{cx}" cy="{y}" rx="10" ry="3.5" fill="#30343b"/>')
    for lx in (70, 418):
        b += [rect(lx - 2, 150, 4, 80, INK), rect(lx - 7, 138, 14, 14, INK), circ(lx, 146, 5, LAMP),
              circ(lx, 146, 30, LAMP, 'opacity=".16"')]
        for i in range(5):
            b.append(rect(lx - 8 + R.uniform(-4, 4), 240 + i * 9, 16, 3, LAMP, 'opacity=".35"'))
    c = '#6b5a3e'
    b.append(rect(214, 36, 60, 196, '#18202b', 'opacity=".55"'))
    b += [rect(222, 196, 44, 34, c), rect(230, 130, 28, 68, c), rect(220, 86, 48, 46, c),
          poly([(216, 88), (244, 60), (272, 88)], c), rect(242, 40, 4, 22, c)]
    b += [circ(244, 109, 14, LAMP), line(244, 109, 244, 99, INK, 2), line(244, 109, 252, 112, INK, 2)]
    for i, (sx, sy, r) in enumerate(((252, 44, 10), (266, 34, 14), (286, 26, 18), (312, 22, 22), (342, 24, 18))):
        b.append(circ(sx, sy, r, '#ffffff', f'opacity="{0.42 - i * 0.06:.2f}"'))
    # a walker under a red umbrella, rim-lit by the gas lamp
    def walker(f, um):
        return [poly([(120, 206), (160, 206), (166, 270), (114, 270)], f), rect(122, 268, 10, 20, f), rect(146, 268, 10, 20, f),
                circ(140, 194, 13, f), line(140, 150, 140, 196, f, 3),
                f'<path d="M86 156 A54 40 0 0 1 194 156 Z" fill="{um}"/>']
    b += ['<g transform="translate(-4 -2)">'] + walker(LAMP, LAMP) + ['</g>'] + walker(INK, RED)
    for i in range(5):
        b.append(rect(118 + R.uniform(-6, 6), 290 - i * 0, 40, 2, RED, 'opacity=".4"'))
    b += rain(w, h, 110, 0.24)
    return b


def skytrain_surf():
    """SkyTrain at dusk, someone surfing the roof."""
    w, h = 496, 292
    b = bands(w, [(0, '#d35d34'), (70, '#e8763f'), (140, '#f3944e'), (200, '#f8b264'), (232, None)])
    b.append(circ(130, 128, 44, '#fde6ae'))
    b += skyline(-10, w, 232, 24, 70, '#5b3a33')
    b.append(rect(0, 230, w, 62, INK))
    for cx in (70, 240, 410):
        b.append(rect(cx - 9, 190, 18, 102, '#b9b3a8'))
    b.append(rect(0, 178, w, 14, '#cfcac0'))
    for i in range(6):
        b.append(line(0, 128 + i * 9, 60 + R.uniform(0, 40), 128 + i * 9, '#ffffff', 2, 'opacity=".7"'))
    for x0 in (60, 206, 352):
        b.append(f'<rect x="{x0}" y="132" width="142" height="44" rx="8" fill="#eeeeea"/>')
        for wx in range(x0 + 10, x0 + 130, 20):
            b.append(rect(wx, 140, 14, 14, '#253446', 'rx="2"'))
        b.append(rect(x0, 160, 142, 6, BLUE))
        b.append(rect(x0, 166, 142, 3, '#e0b23a'))
    b.append(poly([(494, 136), (506, 176), (494, 176)], '#eeeeea'))
    # the surfer, 1.6x so he reads at README size
    b += ['<g transform="translate(300 132) scale(1.6) translate(-300 -132)">']
    b += [circ(300, 82, 9, INK), poly([(294, 92), (306, 92), (310, 116), (290, 116)], INK),
          line(296, 96, 268, 88, INK, 5, 'stroke-linecap="round"'), line(304, 96, 334, 86, INK, 5, 'stroke-linecap="round"'),
          line(294, 114, 280, 132, INK, 6, 'stroke-linecap="round"'), line(306, 114, 320, 132, INK, 6, 'stroke-linecap="round"'),
          poly([(292, 80), (310, 78), (312, 72), (296, 72)], RED)]
    b.append('</g>')
    return b


def title():
    w, h = 552, 292
    font = 'font-family="Helvetica Neue, Helvetica, Arial, sans-serif" font-weight="900" font-stretch="condensed"'
    b = [rect(0, 0, w, h, INK),
         f'<text x="34" y="116" {font} font-size="96" letter-spacing="-1" fill="{CREAM}">VANCOUVER</text>',
         f'<text x="30" y="226" {font} font-size="128" letter-spacing="-2" fill="{RED}">VICE</text>']
    for i in range(5):
        lit = i < 3
        b.append(star(330 + i * 42, 186, 17, CREAM if lit else 'none',
                      '' if lit else f'stroke="{CREAM}" stroke-width="2.5"'))
    b.append(f'<text x="36" y="264" font-family="Helvetica Neue, Helvetica, Arial, sans-serif" font-size="19" '
             f'fill="#9a9ea6">Welcome to Vancouver. Don\'t get caught.</text>')
    return b


def main():
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
             rect(0, 0, W, H, CREAM),
             panel(16, 16, 1000, 560, harbour_centre()),
             panel(1032, 16, 552, 272, burrard_chase()),
             panel(1032, 304, 552, 272, gull_heist()),
             panel(16, 592, 488, 292, steam_clock()),
             panel(520, 592, 496, 292, skytrain_surf()),
             panel(1032, 592, 552, 292, title()),
             '</svg>']
    out = Path(__file__).resolve().parent.parent / 'docs/img/key-art.svg'
    out.write_text('\n'.join(parts))
    print(out)


if __name__ == '__main__':
    main()
