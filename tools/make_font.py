"""Seawall, the Vancouver Vice display face, inspired by Apple's San Francisco: an upright heavy grotesque with flat
terminals and superellipse bowls.
Every glyph is a few strokes (lines and superellipse arcs), stroked with square caps and sharp mitre joins, unioned, sheared, and written as
a TrueType font. Caps only (lowercase maps to the capitals). Replaces Anton in the menus, wordmark and icon.
Run: uvx --with shapely --with fonttools python tools/make_font.py  ->  brand/Seawall.ttf"""
import math, os, re
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from shapely.geometry import LineString, Polygon, MultiPolygon, box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

SW = 124                      # stroke width
H = SW / 2
B, M, T = H, 362, 700 - H     # baseline, middle, cap height (stroke centres)
SLANT = 0.0  # upright, like San Francisco (Joshua 2026-11-02)
SIDE = 46                     # side bearing each side

def g(width, *strokes):
    L, R = H, width - H
    C = width / 2
    return width, [[(eval_pt(p, L, C, R)) for p in s] for s in strokes]

def eval_pt(p, L, C, R):
    x, y = p
    if isinstance(x, str):  # "L", "R-40", "C+20": a grid column plus an offset
        m = re.match(r"([LCR])([+-]\d+)?$", x)
        x = {"L": L, "C": C, "R": R}[m.group(1)] + float(m.group(2) or 0)
    return (x, y)

W4, W3, WO = 470, 340, 520
N = 2.4  # superellipse exponent: San Francisco-style bowls, rounder than a square, squarer than a circle

def arc(cx, cy, rx, ry, a0, a1, steps=40):
    pts = []
    for i in range(steps + 1):
        t = math.radians(a0 + (a1 - a0) * i / steps); c, s_ = math.cos(t), math.sin(t)
        pts.append((cx + rx * math.copysign(abs(c) ** (2 / N), c), cy + ry * math.copysign(abs(s_) ** (2 / N), s_)))
    return pts

def cg(width, *strokes):  # curved glyphs: strokes as absolute points
    return width, [list(s) for s in strokes]

def _glyphs():
    G = {}
    def box(w): return H, w - H, w / 2
    for ch, w in (("O", WO), ("0", W4)):
        L, R, C = box(w); G[ch] = cg(w, arc(C, (T + B) / 2, (R - L) / 2, (T - B) / 2, 0, 361, 80))
    L, R, C = box(WO); E = (C, (T + B) / 2, (R - L) / 2, (T - B) / 2)
    G["C"] = cg(WO, arc(*E, 40, 320, 60))
    G["G"] = cg(WO, arc(*E, 40, 360, 64) + [(C + 30, (T + B) / 2)])
    G["Q"] = cg(WO, arc(*E, 0, 361, 80), [(C + 50, B + 150), (R + 30, B - 80)])
    L, R, C = box(W4)
    bx = L + (R - L) * 0.35
    G["D"] = cg(W4, [(L, B), (L, T), (bx, T)] + arc(bx, M, R - bx, (T - B) / 2, 90, -90) + [(L, B)])
    ub, lb = L + (R - L) * 0.45, L + (R - L) * 0.4
    G["B"] = cg(W4, [(L, B), (L, T), (ub, T)] + arc(ub, (T + M) / 2, R - 40 - ub, (T - M) / 2, 90, -90) + [(L, M)],
                [(L, M), (lb, M)] + arc(lb, (M + B) / 2, R - lb, (M - B) / 2, 90, -90) + [(L, B)])
    pb = [(L, B), (L, T), (ub, T)] + arc(ub, (T + M - 30) / 2, R - ub, (T - M + 30) / 2, 90, -90) + [(L, M - 30)]
    G["P"] = cg(W4, pb)
    G["R"] = cg(W4, pb, [(C - 10, M - 30), (R, B)])
    G["S"] = cg(W4, arc(C, (T + M) / 2, (R - L) / 2, (T - M) / 2, 25, 270) + arc(C, (M + B) / 2, (R - L) / 2, (M - B) / 2, 90, -155))
    G["J"] = cg(W4, [(R, T)] + arc(C, B + 170, (R - L) / 2, 170, 0, -180))
    G["U"] = cg(W4, [(L, T)] + arc(C, B + 190, (R - L) / 2, 190, 180, 360) + [(R, T)])
    G["2"] = cg(W4, arc(C, (T + M) / 2 + 20, (R - L) / 2, (T - M) / 2 - 10, 160, -20) + [(L, B), (R, B)])
    G["3"] = cg(W4, arc(C, (T + M) / 2, (R - L) / 2 - 10, (T - M) / 2, 150, -90), arc(C, (M + B) / 2, (R - L) / 2, (M - B) / 2, 90, -150))
    G["5"] = cg(W4, [(R, T), (L + 10, T), (L, M + 30)] + arc(C, (M + 30 + B) / 2, (R - L) / 2, (M + 30 - B) / 2, 130, -150))
    six = [arc(C, (M + B) / 2 + 10, (R - L) / 2, (M - B) / 2 + 10, 0, 361, 60), [(L, (M + B) / 2 + 10), (L, T - 170)] + arc(C, T - 170, (R - L) / 2, 170, 180, 35)]
    G["6"] = cg(W4, *six)
    G["9"] = cg(W4, *[[(W4 - x, 700 - y) for x, y in s] for s in six])
    G["8"] = cg(W4, arc(C, (T + M) / 2, (R - L) / 2 - 15, (T - M) / 2, 0, 361, 60), arc(C, (M + B) / 2, (R - L) / 2, (M - B) / 2, 0, 361, 60))
    return G

GLYPHS = {
    'A': g(W4 + 30, [("L", B), ("C", T), ("R", B)], [("L+135", 250), ("R-135", 250)]),
    'E': g(W4, [("R", T), ("L", T), ("L", B), ("R", B)], [("L", M), ("R-50", M)]),
    'F': g(W4, [("R", T), ("L", T), ("L", B)], [("L", M), ("R-50", M)]),
    'H': g(W4, [("L", B), ("L", T)], [("R", B), ("R", T)], [("L", M), ("R", M)]),
    'I': g(SW + 2, [("C", B), ("C", T)]),
    'K': g(W4, [("L", B), ("L", T)], [("R", T), ("L+30", M), ("R", B)]),
    'L': g(W3 + 40, [("L", T), ("L", B), ("R", B)]),
    'M': g(600, [("L", B), ("L", T), ("C", B + 130), ("R", T), ("R", B)]),
    'N': g(W4 + 20, [("L", B), ("L", T), ("R", B), ("R", T)]),
    'T': g(W4, [("L", T), ("R", T)], [("C", T), ("C", B)]),
    'V': g(W4 + 20, [("L", T), ("C", B), ("R", T)]),
    'W': g(620, [("L", T), ("L+70", B), ("C", M), ("R-70", B), ("R", T)]),
    'X': g(W4 + 20, [("L", T), ("R", B)], [("R", T), ("L", B)]),
    'Y': g(W4 + 20, [("L", T), ("C", M), ("R", T)], [("C", M), ("C", B)]),
    'Z': g(W4, [("L", T), ("R", T), ("L", B), ("R", B)]),
    '1': g(W3, [("C-80", T - 70), ("C", T), ("C", B)]),
    '4': g(W4, [("L", T), ("L", M), ("R", M)], [("R", T), ("R", B)]),
    '7': g(W4, [("L", T), ("R", T), ("C-30", B)]),
    '9': g(W4, [("R", M), ("L", M), ("L", T), ("R", T), ("R", B), ("L", B)]),
    '.': g(SW + 2, [("C", B), ("C", B + 1)]),
    ',': g(SW + 30, [("C", B + 10), ("C-40", B - 110)]),
    "'": g(SW + 2, [("C", T), ("C", T - 150)]),
    '"': g(SW * 2 + 70, [("L", T), ("L", T - 150)], [("R", T), ("R", T - 150)]),
    '!': g(SW + 2, [("C", T), ("C", M - 60)], [("C", B), ("C", B + 1)]),
    '?': g(W4, [("L", T), ("R", T), ("R", M), ("C", M), ("C", M - 90)], [("C", B), ("C", B + 1)]),
    ':': g(SW + 2, [("C", B), ("C", B + 1)], [("C", M), ("C", M + 1)]),
    '-': g(W3, [("L", M), ("R", M)]),
    '/': g(W3 + 40, [("L", B - 20), ("R", T + 20)]),
    '$': g(W4, [("R", T), ("L", T), ("L", M), ("R", M), ("R", B), ("L", B)], [("C", T + 70), ("C", B - 70)]),
    '+': g(W4, [("L", M), ("R", M)], [("C", M - 150), ("C", M + 150)]),
}
GLYPHS.update(_glyphs())

OVERHANG = set(",/$Q")  # glyphs allowed below the baseline or above the caps

def outline(width, strokes, ch=""):
    shapes = [LineString(s).buffer(H, cap_style=3, join_style=2, mitre_limit=3.0) for s in strokes]
    u = unary_union(shapes)
    if ch not in OVERHANG:  # square caps on diagonals poke past the baseline and cap height: trim them flat
        u = u.intersection(box(-500, 0, width + 500, 700))
    polys = list(u.geoms) if isinstance(u, MultiPolygon) else [u]
    pen = TTGlyphPen(None)
    for p in polys:
        p = orient(p, sign=-1.0)  # TrueType: outer contours clockwise
        for ring in [p.exterior] + list(p.interiors):
            pts = [(round(x + y * SLANT + SIDE), round(y)) for x, y in ring.coords[:-1]]
            pen.moveTo(pts[0])
            for q in pts[1:]: pen.lineTo(q)
            pen.closePath()
    return pen.glyph(), width + 2 * SIDE

names = {c: ("uni%04X" % ord(c)) for c in GLYPHS}
order = [".notdef", "space"] + [names[c] for c in GLYPHS]
glyf, metrics = {".notdef": TTGlyphPen(None).glyph(), "space": TTGlyphPen(None).glyph()}, {".notdef": (500, 0), "space": (230, 0)}
for c, (w, s) in GLYPHS.items():
    gl, adv = outline(w, s, c); glyf[names[c]] = gl; metrics[names[c]] = (adv, 0)
cmap = {32: "space"}
for c in GLYPHS:
    cmap[ord(c)] = names[c]
    if c.isalpha(): cmap[ord(c.lower())] = names[c]
fb = FontBuilder(1000, isTTF=True)
fb.setupGlyphOrder(order); fb.setupCharacterMap(cmap); fb.setupGlyf(glyf)
for n in order:  # fill left side bearings from the outlines
    gl = fb.font["glyf"][n]; gl.recalcBounds(fb.font["glyf"]) if hasattr(gl, "recalcBounds") else None
    metrics[n] = (metrics[n][0], getattr(gl, "xMin", 0) or 0)
fb.setupHorizontalMetrics(metrics); fb.setupHorizontalHeader(ascent=820, descent=-180)
fb.setupNameTable({"familyName": "Seawall", "styleName": "Regular", "uniqueFontIdentifier": "Seawall-Regular-1.0",
                   "fullName": "Seawall", "psName": "Seawall-Regular", "version": "Version 1.000",
                   "copyright": "Copyright 2026 Joshua Trommel. Made for Vancouver Vice."})
fb.setupOS2(sTypoAscender=820, sTypoDescender=-180, usWinAscent=880, usWinDescent=200, achVendID="JTVV")
fb.setupPost()
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "brand", "Seawall.ttf")
fb.save(out); print("wrote", out, len(GLYPHS), "glyphs")
