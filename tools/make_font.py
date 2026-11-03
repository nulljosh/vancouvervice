"""Seawall, the Vancouver Vice display face: condensed, square-cut, chamfered corners, the brand's 7 degree slant baked in.
Every glyph is a few strokes on a small grid, stroked with square caps and bevel joins, unioned, sheared, and written as
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
SLANT = math.tan(math.radians(7))
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

W4, W3 = 430, 330
GLYPHS = {
    "A": g(W4, [("L", B), ("L", T), ("R", T), ("R", B)], [("L", M), ("R", M)]),
    "B": g(W4, [("L", B), ("L", T), ("R-40", T), ("R-40", M), ("L", M)], [("L", M), ("R", M), ("R", B), ("L", B)]),
    "C": g(W4, [("R", T), ("L", T), ("L", B), ("R", B)]),
    "D": g(W4, [("L", B), ("L", T), ("R-80", T), ("R", T - 80), ("R", B + 80), ("R-80", B), ("L", B)]),
    "E": g(W4, [("R", T), ("L", T), ("L", B), ("R", B)], [("L", M), ("R-50", M)]),
    "F": g(W4, [("R", T), ("L", T), ("L", B)], [("L", M), ("R-50", M)]),
    "G": g(W4, [("R", T), ("L", T), ("L", B), ("R", B), ("R", M), ("C", M)]),
    "H": g(W4, [("L", B), ("L", T)], [("R", B), ("R", T)], [("L", M), ("R", M)]),
    "I": g(SW + 2, [("C", B), ("C", T)]),
    "J": g(W4, [("R", T), ("R", B), ("L", B), ("L", B + 150)]),
    "K": g(W4, [("L", B), ("L", T)], [("R", T), ("L+30", M), ("R", B)]),
    "L": g(W3 + 40, [("L", T), ("L", B), ("R", B)]),
    "M": g(570, [("L", B), ("L", T), ("C", M + 40), ("R", T), ("R", B)]),
    "N": g(W4 + 20, [("L", B), ("L", T), ("R", B), ("R", T)]),
    "O": g(W4, [("L", B), ("L", T), ("R", T), ("R", B), ("L", B)]),
    "P": g(W4, [("L", B), ("L", T), ("R", T), ("R", M), ("L", M)]),
    "Q": g(W4, [("L", B), ("L", T), ("R", T), ("R", B), ("L", B)], [("C+20", B + 140), ("R+30", B - 70)]),
    "R": g(W4, [("L", B), ("L", T), ("R", T), ("R", M), ("L", M)], [("C", M), ("R", B)]),
    "S": g(W4, [("R", T), ("L", T), ("L", M), ("R", M), ("R", B), ("L", B)]),
    "T": g(W4, [("L", T), ("R", T)], [("C", T), ("C", B)]),
    "U": g(W4, [("L", T), ("L", B), ("R", B), ("R", T)]),
    "V": g(W4 + 20, [("L", T), ("C", B), ("R", T)]),
    "W": g(620, [("L", T), ("L+70", B), ("C", M), ("R-70", B), ("R", T)]),
    "X": g(W4 + 20, [("L", T), ("R", B)], [("R", T), ("L", B)]),
    "Y": g(W4 + 20, [("L", T), ("C", M), ("R", T)], [("C", M), ("C", B)]),
    "Z": g(W4, [("L", T), ("R", T), ("L", B), ("R", B)]),
    "0": g(W4, [("L", B), ("L", T), ("R", T), ("R", B), ("L", B)], [("L+60", B + 90), ("R-60", T - 90)]),
    "1": g(W3, [("C-80", T - 70), ("C", T), ("C", B)]),
    "2": g(W4, [("L", T), ("R", T), ("R", M), ("L", M), ("L", B), ("R", B)]),
    "3": g(W4, [("L", T), ("R", T), ("R", B), ("L", B)], [("L+70", M), ("R", M)]),
    "4": g(W4, [("L", T), ("L", M), ("R", M)], [("R", T), ("R", B)]),
    "5": g(W4, [("R", T), ("L", T), ("L", M + 40), ("R-70", M + 40), ("R", M - 30), ("R", B), ("L", B)]),
    "6": g(W4, [("R", T), ("L", T), ("L", B), ("R", B), ("R", M), ("L", M)]),
    "7": g(W4, [("L", T), ("R", T), ("C-30", B)]),
    "8": g(W4, [("L", B), ("L", T), ("R", T), ("R", B), ("L", B)], [("L", M), ("R", M)]),
    "9": g(W4, [("R", M), ("L", M), ("L", T), ("R", T), ("R", B), ("L", B)]),
    ".": g(SW + 2, [("C", B), ("C", B + 1)]),
    ",": g(SW + 30, [("C", B + 10), ("C-40", B - 110)]),
    "'": g(SW + 2, [("C", T), ("C", T - 150)]),
    "\"": g(SW * 2 + 70, [("L", T), ("L", T - 150)], [("R", T), ("R", T - 150)]),
    "!": g(SW + 2, [("C", T), ("C", M - 60)], [("C", B), ("C", B + 1)]),
    "?": g(W4, [("L", T), ("R", T), ("R", M), ("C", M), ("C", M - 90)], [("C", B), ("C", B + 1)]),
    ":": g(SW + 2, [("C", B), ("C", B + 1)], [("C", M), ("C", M + 1)]),
    "-": g(W3, [("L", M), ("R", M)]),
    "/": g(W3 + 40, [("L", B - 20), ("R", T + 20)]),
    "$": g(W4, [("R", T), ("L", T), ("L", M), ("R", M), ("R", B), ("L", B)], [("C", T + 70), ("C", B - 70)]),
    "+": g(W4, [("L", M), ("R", M)], [("C", M - 150), ("C", M + 150)]),
}

OVERHANG = set(",/$Q")  # glyphs allowed below the baseline or above the caps

def outline(width, strokes, ch=""):
    shapes = [LineString(s).buffer(H, cap_style=3, join_style=3) for s in strokes]
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
