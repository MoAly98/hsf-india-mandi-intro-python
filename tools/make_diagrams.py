"""Draw the lecture diagrams as SVG files.

Run from the repository root:

    python tools/make_diagrams.py

Every diagram shares one palette and one set of shapes, so a change here
changes all three lessons.
"""

from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
L1 = L2 = L3 = IMG = ROOT / "img"

# palette
BG = "#FAF9F6"
EDGE = "#E4E2DC"
INK = "#1F2A44"
MUTED = "#6B7280"
LINE = "#B9C0CC"
BLUE = "#2F6FDE"
BLUE_L = "#E3ECFB"
ORANGE = "#D9691E"
ORANGE_L = "#FCE9D9"
GREY_L = "#F0F1F4"
WHITE = "#FFFFFF"

SANS = "Helvetica Neue, Helvetica, Arial, sans-serif"
MONO = "SFMono-Regular, Menlo, Consolas, DejaVu Sans Mono, monospace"

W = 960


class Svg:
    def __init__(self, h, w=W):
        self.w, self.h, self.e = w, h, []
        self.rect(1, 1, w - 2, h - 2, BG, EDGE, rx=14, sw=1.5)

    def rect(self, x, y, w, h, fill=WHITE, stroke=LINE, rx=8, sw=2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.e.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{s}{d}/>'
        )

    def text(self, x, y, s, size=22, fill=INK, anchor="middle", weight=400, mono=False, italic=False):
        fam = MONO if mono else SANS
        it = ' font-style="italic"' if italic else ""
        self.e.append(
            f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" dominant-baseline="central" font-weight="{weight}"{it}>'
            f"{escape(str(s))}</text>"
        )

    def line(self, x1, y1, x2, y2, color=LINE, sw=2.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.e.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round"{d}/>'
        )

    def arrow(self, x1, y1, x2, y2, color=MUTED, sw=2.5, dash=None):
        import math

        self.line(x1, y1, x2, y2, color, sw, dash)
        a = math.atan2(y2 - y1, x2 - x1)
        s = 11
        p = [
            (x2, y2),
            (x2 - s * math.cos(a - 0.45), y2 - s * math.sin(a - 0.45)),
            (x2 - s * math.cos(a + 0.45), y2 - s * math.sin(a + 0.45)),
        ]
        pts = " ".join(f"{px:.1f},{py:.1f}" for px, py in p)
        self.e.append(f'<polygon points="{pts}" fill="{color}"/>')

    def poly(self, pts, fill=WHITE, stroke=LINE, sw=2):
        p = " ".join(f"{x},{y}" for x, y in pts)
        self.e.append(f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>')

    def path(self, d, color=MUTED, sw=2.5, dash=None):
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        self.e.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"{ds}/>')

    def box(self, x, y, w, h, label, state="plain", size=22, mono=False, weight=500, sub=None):
        fill, stroke, ink, dash = STATES[state]
        self.rect(x, y, w, h, fill, stroke, dash=dash)
        if sub is None:
            self.text(x + w / 2, y + h / 2, label, size, ink, weight=weight, mono=mono)
        else:
            self.text(x + w / 2, y + h / 2 - 13, label, size, ink, weight=weight, mono=mono)
            self.text(x + w / 2, y + h / 2 + 15, sub, 17, MUTED if state != "off" else LINE)

    def cells(self, x, y, values, cw=96, ch=54, states=None, gap=6, size=21):
        """A row of value cells. Returns the x centre of each cell."""
        states = states or ["plain"] * len(values)
        xs = []
        for i, (v, st) in enumerate(zip(values, states)):
            cx = x + i * (cw + gap)
            self.box(cx, y, cw, ch, v, st, size=size, mono=True, weight=400)
            xs.append(cx + cw / 2)
        return xs

    def save(self, *paths):
        body = "\n".join(self.e)
        out = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
            f'width="{self.w}" height="{self.h}">\n{body}\n</svg>\n'
        )
        for p in paths:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(out)


# state -> (fill, stroke, ink, dash)
STATES = {
    "plain": (WHITE, LINE, INK, None),
    "blue": (BLUE_L, BLUE, INK, None),
    "hi": (ORANGE_L, ORANGE, INK, None),
    "off": (BG, LINE, LINE, "6 6"),
    "grey": (GREY_L, LINE, MUTED, None),
    "solid": (BLUE, BLUE, WHITE, None),
}


def row_width(n, cw=96, gap=6):
    return n * cw + (n - 1) * gap


# ---------------------------------------------------------------- shared

def course_map(active):
    s = Svg(230)
    items = [
        ("Python", "one event at a time"),
        ("NumPy", "one column at a time"),
        ("Classes", "data with methods"),
        ("Awkward", "columns of lists"),
        ("Analysis", "later lectures"),
    ]
    bw, bh, gap = 152, 80, 40
    x0 = (W - (5 * bw + 4 * gap)) / 2
    for i, (name, sub) in enumerate(items):
        x = x0 + i * (bw + gap)
        if i == 4:
            st = "off"
        elif active and i + 1 == active:
            st = "hi"
        elif active and i + 1 < active:
            st = "blue"
        else:
            st = "plain"
        s.box(x, 60, bw, bh, name, st, size=22, weight=600)
        s.text(x + bw / 2, 60 + bh + 26, sub, 17, MUTED)
        if i < 4:
            s.arrow(x + bw + 6, 60 + bh / 2, x + bw + gap - 6, 60 + bh / 2)
            s.text(x + bw / 2, 36, f"Lesson {i + 1}", 17, ORANGE if i + 1 == active else MUTED, weight=600)
    return s


def pipeline(active=(), later=()):
    s = Svg(230)
    items = [
        ("read", "file to arrays"),
        ("select", "keep what we want"),
        ("compute", "build a quantity"),
        ("histogram", "count and plot"),
    ]
    bw, bh, gap = 190, 84, 46
    x0 = (W - (4 * bw + 3 * gap)) / 2
    for i, (name, sub) in enumerate(items):
        x = x0 + i * (bw + gap)
        st = "hi" if name in active else ("off" if name in later else "plain")
        s.box(x, 56, bw, bh, name, st, size=25, weight=600, mono=False)
        s.text(x + bw / 2, 56 + bh + 28, sub, 18, LINE if name in later else MUTED)
        s.text(x + bw / 2, 32, str(i + 1), 18, ORANGE if name in active else MUTED, weight=600)
        if i < 3:
            s.arrow(x + bw + 8, 56 + bh / 2, x + bw + gap - 8, 56 + bh / 2)
    return s


# ---------------------------------------------------------------- lesson 1

def name_value():
    s = Svg(200)
    s.text(250, 60, "name", 18, MUTED)
    s.box(170, 82, 160, 62, "pt", "hi", size=26, mono=True)
    s.arrow(342, 113, 548, 113)
    s.text(445, 92, "refers to", 18, MUTED)
    s.text(640, 60, "value", 18, MUTED)
    s.box(560, 82, 160, 62, "63.0", "blue", size=26, mono=True)
    return s


def types():
    s = Svg(230)
    items = [("3", "int", "a count"), ("63.0", "float", "a measurement"), ('"muon"', "str", "a label"), ("True", "bool", "yes or no")]
    bw, gap = 190, 30
    x0 = (W - (4 * bw + 3 * gap)) / 2
    for i, (val, typ, what) in enumerate(items):
        x = x0 + i * (bw + gap)
        s.text(x + bw / 2, 40, typ, 22, ORANGE, weight=600, mono=True)
        s.box(x, 66, bw, 76, val, "blue", size=27, mono=True, weight=400)
        s.text(x + bw / 2, 174, what, 19, MUTED)
    return s


def list_index(slice_=None):
    s = Svg(240)
    vals = ["63.0", "38.1", "4.0"]
    cw = 140
    x0 = (W - row_width(3, cw)) / 2
    s.text(x0 - 24, 119, "pts", 24, INK, anchor="end", mono=True, weight=600)
    states = ["blue"] * 3
    if slice_:
        states = ["hi" if slice_[0] <= i < slice_[1] else "plain" for i in range(3)]
    xs = s.cells(x0, 88, vals, cw=cw, ch=62, states=states, size=25)
    for i, cx in enumerate(xs):
        s.text(cx, 58, str(i), 21, ORANGE, mono=True, weight=600)
        if not slice_:
            s.text(cx, 180, str(i - 3), 21, MUTED, mono=True)
    s.text(xs[-1] + 110, 58, "index", 18, MUTED, anchor="start")
    if not slice_:
        s.text(xs[-1] + 110, 180, "from the end", 18, MUTED, anchor="start")
    else:
        a, b = slice_
        xa = x0 + a * (cw + 6) - 2
        xb = x0 + b * (cw + 6) - 4
        s.path(f"M{xa},170 v14 H{xb} v-14", ORANGE, 3)
        s.text((xa + xb) / 2, 208, f"pts[{a}:{b}]  starts at {a}, stops before {b}", 20, INK, mono=True)
    return s


def dict_():
    s = Svg(250)
    rows = [('"pt"', "63.0"), ('"eta"', "-0.72"), ('"charge"', "1")]
    s.text(330, 36, "key", 18, MUTED)
    s.text(630, 36, "value", 18, MUTED)
    for i, (k, v) in enumerate(rows):
        y = 58 + i * 60
        s.box(230, y, 200, 50, k, "hi", size=23, mono=True, weight=400)
        s.arrow(442, y + 25, 518, y + 25)
        s.box(530, y, 200, 50, v, "blue", size=23, mono=True, weight=400)
    return s


def event_tree(path=False):
    s = Svg(330)
    hi = "hi" if path else "plain"
    s.box(40, 132, 150, 62, "event", "solid", size=24, mono=True, weight=600)
    keys = [('"run"', 60), ('"event"', 138), ('"muon"', 216)]
    for k, y in keys:
        st = hi if (k == '"muon"') else "plain"
        s.box(260, y, 150, 50, k, st, size=21, mono=True, weight=400)
        s.arrow(196, 163, 252, y + 25, ORANGE if (path and k == '"muon"') else MUTED)
    s.arrow(416, 85, 462, 85)
    s.box(470, 60, 110, 50, "1", "blue", size=21, mono=True, weight=400)
    s.arrow(416, 163, 462, 163)
    s.box(470, 138, 110, 50, "46501", "blue", size=21, mono=True, weight=400)
    # list of muons
    s.text(474, 236, "a list of dictionaries, one per muon", 17, MUTED, anchor="start")
    muons = [("63.0", "1"), ("38.1", "-1"), ("4.0", "1")]
    for i, (pt, q) in enumerate(muons):
        x = 470 + i * 156
        st = hi if (path and i == 0) else "plain"
        s.rect(x, 254, 146, 58, *STATES[st][:2])
        s.text(x + 73, 271, f"pt {pt}", 18, INK, mono=True, weight=600 if (path and i == 0) else 400)
        s.text(x + 73, 296, f"charge {q}", 18, MUTED, mono=True)
        s.text(x + 73, 222 if False else 326 - 4, "", 1)
    s.arrow(416, 241, 462, 270, ORANGE if path else MUTED)
    for i in range(3):
        s.text(470 + i * 156 + 12, 262, f"{i}", 15, ORANGE, anchor="start", mono=True, weight=600)
    return s


def for_loop():
    s = Svg(300)
    # diamond
    cx, cy = 250, 150
    s.poly([(cx, cy - 70), (cx + 150, cy), (cx, cy + 70), (cx - 150, cy)], ORANGE_L, ORANGE)
    s.text(cx, cy - 10, "another item", 20, INK, weight=600)
    s.text(cx, cy + 16, "in the list?", 20, INK, weight=600)
    s.arrow(cx + 156, cy, 498, cy)
    s.text(450, cy - 18, "yes", 18, MUTED)
    s.box(506, cy - 42, 250, 84, "run the indented block", "blue", size=20, sub="with the name set to that item")
    # back
    s.path(f"M631,{cy - 48} V46 H{cx} V{cy - 82}", MUTED)
    s.arrow(cx, cy - 86, cx, cy - 74)
    s.text(440, 30, "then take the next item", 18, MUTED)
    s.arrow(cx, cy + 74, cx, 262)
    s.text(cx + 22, 248, "no", 18, MUTED, anchor="start")
    s.text(cx, 280, "carry on after the loop", 20, INK)
    return s


def if_():
    s = Svg(260)
    cx, cy = 250, 120
    s.poly([(cx, cy - 66), (cx + 150, cy), (cx, cy + 66), (cx - 150, cy)], ORANGE_L, ORANGE)
    s.text(cx, cy - 10, "is the condition", 20, INK, weight=600)
    s.text(cx, cy + 16, "True?", 20, INK, weight=600, mono=True)
    s.arrow(cx + 156, cy, 498, cy)
    s.text(450, cy - 18, "yes", 18, MUTED)
    s.box(506, cy - 36, 250, 72, "run the indented block", "blue", size=20)
    s.path(f"M{cx},{cy + 72} V226 H820")
    s.text(cx + 22, 208, "no: skip it", 18, MUTED, anchor="start")
    s.path(f"M760,{cy} H820 V226")
    s.arrow(820, 226, 900, 226)
    s.text(870, 204, "carry on", 18, MUTED)
    return s


def filter_():
    s = Svg(250)
    s.text(150, 34, "all muons", 18, MUTED)
    for i, v in enumerate(["63.0", "38.1", "4.0"]):
        s.box(90, 56 + i * 58, 120, 48, v, "plain", size=21, mono=True, weight=400)
    s.arrow(224, 125, 356, 125)
    s.poly([(480, 60), (604, 125), (480, 190), (356, 125)], ORANGE_L, ORANGE)
    s.text(480, 125, "pt > 20 ?", 22, INK, mono=True, weight=600)
    s.arrow(612, 125, 720, 125)
    s.text(790, 34, "good", 18, MUTED)
    s.box(730, 56, 120, 48, "63.0", "blue", size=21, mono=True, weight=400)
    s.box(730, 114, 120, 48, "38.1", "blue", size=21, mono=True, weight=400)
    s.box(730, 172, 120, 48, "4.0", "off", size=21, mono=True, weight=400)
    s.text(664, 104, "keep", 17, MUTED)
    return s


def function():
    s = Svg(200)
    s.text(170, 52, "input", 18, MUTED)
    s.rect(80, 74, 180, 66, WHITE, LINE)
    s.text(170, 96, "pt 63.0", 19, INK, mono=True)
    s.text(170, 121, "charge 1", 19, MUTED, mono=True)
    s.arrow(272, 107, 368, 107)
    s.box(380, 68, 200, 78, "is_good", "hi", size=25, mono=True, weight=600)
    s.arrow(592, 107, 688, 107)
    s.text(790, 52, "output", 18, MUTED)
    s.box(700, 74, 180, 66, "True", "blue", size=23, mono=True, weight=400)
    s.text(480, 172, "a named block of code", 18, MUTED)
    return s


def loop_vs_column():
    s = Svg(290)
    vals = ["63.0", "38.1", "4.0", "54.3"]
    # left: loop
    s.text(240, 34, "loop: one value at a time", 20, INK, weight=600)
    xs = s.cells(46, 128, vals, cw=90, ch=52)
    for i, cx in enumerate(xs):
        s.arrow(cx, 86, cx, 122, ORANGE)
        s.text(cx, 70, f"step {i + 1}", 16, ORANGE, weight=600)
    s.text(240, 214, "Python works out the type", 18, MUTED)
    s.text(240, 240, "and the operation at every step", 18, MUTED)
    s.line(480, 30, 480, 262, EDGE, 2)
    # right: column
    s.text(720, 34, "array: the whole column at once", 20, INK, weight=600)
    x0 = 526
    s.rect(x0 - 8, 120, row_width(4, 90) + 16, 68, ORANGE_L, ORANGE, rx=12)
    s.cells(x0, 128, vals, cw=90, ch=52)
    s.arrow(720, 78, 720, 114, ORANGE)
    s.text(720, 62, "one step", 16, ORANGE, weight=600)
    s.text(720, 214, "the type is known once,", 18, MUTED)
    s.text(720, 240, "the loop runs in compiled code", 18, MUTED)
    return s


# ---------------------------------------------------------------- lesson 2

PT4 = ["63.0", "38.1", "4.0", "54.3"]
ETA4 = ["-0.72", "-0.88", "-0.32", "-1.06"]


def list_vs_array():
    s = Svg(300)
    s.text(240, 34, "list", 21, INK, weight=600)
    s.text(240, 60, "each slot points to a separate object", 17, MUTED)
    xs = s.cells(70, 86, ["", "", "", ""], cw=78, ch=44)
    places = [(60, 190), (170, 232), (286, 186), (380, 236)]
    for cx, (px, py), v in zip(xs, places, PT4):
        s.arrow(cx, 108, px + 40, py - 4, MUTED, 2)
        s.e.append(f'<circle cx="{cx}" cy="108" r="5" fill="{MUTED}"/>')
        s.box(px, py, 80, 40, v, "plain", size=18, mono=True, weight=400)
    s.line(480, 30, 480, 276, EDGE, 2)
    s.text(720, 34, "array", 21, INK, weight=600)
    s.text(720, 60, "one block, every value the same type", 17, MUTED)
    x0 = 526
    s.cells(x0, 120, PT4, cw=90, ch=56, states=["blue"] * 4, gap=0)
    s.text(720, 212, "dtype  float64", 20, ORANGE, mono=True, weight=600)
    s.text(720, 242, "shape  (4,)", 20, ORANGE, mono=True, weight=600)
    return s


def elementwise(two=False):
    s = Svg(290 if two else 230)
    x0 = 330
    lab = 300
    if not two:
        s.text(lab, 71, "pt", 22, INK, anchor="end", mono=True, weight=600)
        xs = s.cells(x0, 44, PT4)
        for cx in xs:
            s.arrow(cx, 104, cx, 142, ORANGE)
            s.text(cx + 12, 122, "× 2", 17, ORANGE, anchor="start", weight=600)
        s.text(lab, 175, "pt * 2", 22, INK, anchor="end", mono=True, weight=600)
        s.cells(x0, 148, ["126.0", "76.2", "8.0", "108.6"], states=["blue"] * 4)
    else:
        s.text(lab, 59, "pt", 22, INK, anchor="end", mono=True, weight=600)
        xs = s.cells(x0, 32, PT4)
        s.text(lab, 125, "np.sinh(eta)", 22, INK, anchor="end", mono=True, weight=600)
        s.cells(x0, 98, ["-0.78", "-1.00", "-0.33", "-1.27"])
        for cx in xs:
            s.text(cx, 92, "×", 18, ORANGE, weight=600)
            s.arrow(cx, 158, cx, 196, ORANGE)
        s.text(lab, 229, "pz", 22, INK, anchor="end", mono=True, weight=600)
        s.cells(x0, 202, ["-49.4", "-38.0", "-1.3", "-68.9"], states=["blue"] * 4)
    return s


def mask(other=False):
    s = Svg(300)
    x0, lab = 330, 300
    m = [True, True, False, True]
    s.text(lab, 59, "pt", 22, INK, anchor="end", mono=True, weight=600)
    xs = s.cells(x0, 32, PT4)
    s.text(lab, 125, "mask", 22, INK, anchor="end", mono=True, weight=600)
    s.cells(x0, 98, ["True" if b else "False" for b in m], states=["hi" if b else "grey" for b in m], size=19)
    top = ETA4 if other else PT4
    name = "eta" if other else "pt"
    y = 202
    if other:
        s.text(lab, 191, "eta", 22, INK, anchor="end", mono=True, weight=600)
        s.cells(x0, 164, ETA4)
        y = 236
        s.h = 320
    for cx, b in zip(xs, m):
        if not other:
            s.arrow(cx, 158, cx, 196, ORANGE if b else LINE)
    s.text(lab, y + 27, f"{name}[mask]", 22, INK, anchor="end", mono=True, weight=600)
    s.cells(x0, y, top, states=["blue" if b else "off" for b in m])
    if other:
        s.e[0] = f'<rect x="1" y="1" width="{W - 2}" height="318" rx="14" fill="{BG}" stroke="{EDGE}" stroke-width="1.5"/>'
    return s


def reduce_():
    s = Svg(200)
    x0 = 150
    s.text(x0 - 24, 99, "pt", 22, INK, anchor="end", mono=True, weight=600)
    s.cells(x0, 72, PT4)
    xe = x0 + row_width(4)
    s.arrow(xe + 16, 99, xe + 150, 99, ORANGE)
    s.text(xe + 82, 76, ".sum()", 20, ORANGE, mono=True, weight=600)
    s.box(xe + 162, 68, 130, 62, "159.4", "blue", size=23, mono=True, weight=400)
    s.text(xe + 227, 158, "one value", 18, MUTED)
    s.text(x0 + row_width(4) / 2, 158, "many values", 18, MUTED)
    return s


GRID = [["63.0", "38.1", "4.0"], ["54.3", "23.5", "52.9"]]


def array2d(hi_col=None, hi_cell=None):
    s = Svg(300)
    cw, ch, gap = 120, 56, 6
    x0, y0 = 370, 96
    for r, row in enumerate(GRID):
        st = []
        for c in range(3):
            if hi_cell == (r, c):
                st.append("hi")
            elif hi_col == c:
                st.append("hi")
            else:
                st.append("blue" if hi_col is None and hi_cell is None else "plain")
        s.cells(x0, y0 + r * (ch + gap), row, cw=cw, ch=ch, states=st)
        s.text(x0 - 22, y0 + r * (ch + gap) + ch / 2, f"event {r}", 19, MUTED, anchor="end")
    for c in range(3):
        s.text(x0 + c * (cw + gap) + cw / 2, y0 - 22, f"muon {c}", 19, MUTED)
    # axis arrows
    s.arrow(150, y0 + 2, 150, y0 + 2 * ch + gap - 2, ORANGE, 3)
    s.text(136, y0 + ch + 3, "axis 0", 20, ORANGE, anchor="end", mono=True, weight=600)
    yb = y0 + 2 * (ch + gap) + 22
    s.arrow(x0, yb, x0 + row_width(3, cw), yb, ORANGE, 3)
    s.text(x0 + row_width(3, cw) / 2, yb + 24, "axis 1", 20, ORANGE, mono=True, weight=600)
    s.text(x0 + row_width(3, cw) + 40, y0 + ch + 3, "shape (2, 3)", 20, INK, anchor="start", mono=True)
    return s


def axis():
    s = Svg(330)
    cw, ch, gap = 110, 52, 6
    x0, y0 = 250, 60
    for r, row in enumerate(GRID):
        s.cells(x0, y0 + r * (ch + gap), row, cw=cw, ch=ch)
        s.text(x0 - 22, y0 + r * (ch + gap) + ch / 2, f"event {r}", 19, MUTED, anchor="end")
    xe = x0 + row_width(3, cw)
    # axis=1 -> right
    sums1 = ["105.1", "130.7"]
    for r in range(2):
        y = y0 + r * (ch + gap)
        s.arrow(xe + 14, y + ch / 2, xe + 96, y + ch / 2, ORANGE)
        s.box(xe + 106, y, cw, ch, sums1[r], "blue", size=21, mono=True, weight=400)
    s.text(xe + 106 + cw / 2, y0 - 24, "sum(axis=1)", 19, ORANGE, mono=True, weight=600)
    s.text(xe + 106 + cw + 20, y0 + ch + 3, "one per event", 18, MUTED, anchor="start")
    # axis=0 -> down
    sums0 = ["117.3", "61.6", "56.9"]
    yb = y0 + 2 * (ch + gap)
    for c in range(3):
        x = x0 + c * (cw + gap)
        s.arrow(x + cw / 2, yb + 6, x + cw / 2, yb + 56, ORANGE)
        s.box(x, yb + 64, cw, ch, sums0[c], "blue", size=21, mono=True, weight=400)
    s.text(x0 - 22, yb + 64 + ch / 2, "sum(axis=0)", 19, ORANGE, anchor="end", mono=True, weight=600)
    s.text(xe + 20, yb + 64 + ch / 2, "one per column", 18, MUTED, anchor="start")
    return s


def broadcast():
    s = Svg(250)
    cw, ch, gap = 84, 46, 4
    y0 = 70

    def grid(x, rows, states):
        for r, row in enumerate(rows):
            s.cells(x, y0 + r * (ch + gap), row, cw=cw, ch=ch, states=states[r], gap=gap, size=18)

    grid(40, GRID, [["plain"] * 3] * 2)
    s.text(40 + row_width(3, cw, gap) / 2, 36, "pt2d   shape (2, 3)", 18, MUTED, mono=True)
    s.text(330, y0 + ch + 2, "×", 26, ORANGE, weight=600)
    sc = ["1.0", "1.0", "0.5"]
    grid(362, [sc, sc], [["hi"] * 3, ["off"] * 3])
    s.text(362 + row_width(3, cw, gap) / 2, 36, "scale   shape (3,)", 18, MUTED, mono=True)
    s.text(362 + row_width(3, cw, gap) / 2, y0 + 2 * (ch + gap) + 24, "repeated for every row", 17, MUTED)
    s.text(652, y0 + ch + 2, "=", 26, ORANGE, weight=600)
    grid(684, [["63.0", "38.1", "2.0"], ["54.3", "23.5", "26.4"]], [["blue"] * 3] * 2)
    s.text(684 + row_width(3, cw, gap) / 2, 36, "shape (2, 3)", 18, MUTED, mono=True)
    return s


def histogram():
    s = Svg(300)
    # number line with values
    x0, x1, yl = 90, 870, 86
    vals = [8, 14, 17, 22, 26, 29, 31, 33, 38, 44, 47, 55, 63, 78]
    s.text(x0, 34, "values", 18, MUTED, anchor="start")
    s.line(x0, yl, x1, yl, LINE, 2)
    for v in vals:
        x = x0 + (x1 - x0) * v / 100
        s.e.append(f'<circle cx="{x:.1f}" cy="{yl}" r="7" fill="{BLUE}"/>')
    edges = [0, 20, 40, 60, 80, 100]
    counts = [sum(1 for v in vals if a <= v < b) for a, b in zip(edges[:-1], edges[1:])]
    base = 262
    for e in edges:
        x = x0 + (x1 - x0) * e / 100
        s.line(x, yl - 16, x, base, LINE, 1.5, dash="5 5")
        s.text(x, base + 20, str(e), 17, MUTED, mono=True)
    for (a, b), c in zip(zip(edges[:-1], edges[1:]), counts):
        xa = x0 + (x1 - x0) * a / 100
        xb = x0 + (x1 - x0) * b / 100
        h = c * 22
        s.rect(xa + 4, base - h, xb - xa - 8, h, ORANGE_L, ORANGE, rx=4)
        s.text((xa + xb) / 2, base - h - 16, str(c), 20, ORANGE, weight=600, mono=True)
    s.text(x1 + 10, 150, "counts", 18, MUTED, anchor="end")
    return s


def tree():
    s = Svg(320)
    cols = ["nMuon", "nElectron", "MET_pt", "MET_phi"]
    rows = [["3", "0", "21.9", "-2.73"], ["0", "4", "17.0", "2.87"], ["0", "2", "19.1", "-2.17"], ["7", "1", "30.9", "-1.60"]]
    cw, ch, gap = 150, 42, 6
    x0, y0 = 250, 100
    s.text(x0 + row_width(4, cw) / 2, 28, "one branch = one column", 18, ORANGE, weight=600)
    for c, name in enumerate(cols):
        s.box(x0 + c * (cw + gap), y0 - 44, cw, 38, name, "hi", size=18, mono=True, weight=600)
    for r, row in enumerate(rows):
        s.cells(x0, y0 + r * (ch + gap), row, cw=cw, ch=ch, size=18)
        s.text(x0 - 22, y0 + r * (ch + gap) + ch / 2, f"event {r}", 18, MUTED, anchor="end")
    s.text(x0 - 22, y0 + 4 * (ch + gap) + 6, "...", 20, MUTED, anchor="end")
    s.text(100, 30, "tree  Events", 19, INK, mono=True, weight=600)
    s.text(100, 56, "one entry = one event", 16, MUTED)
    return s


JAG = [["63.0", "38.1", "4.0"], [], ["54.3", "23.5"], ["41.2"]]


def jag_rows(s, x0, y0, rows, states=None, cw=92, ch=44, gap=6, row_states=None, labels=True, size=19, lx=None):
    for r, row in enumerate(rows):
        y = y0 + r * (ch + gap)
        dead = row_states is not None and not row_states[r]
        if labels:
            s.text((lx if lx is not None else x0 - 18), y + ch / 2, f"event {r}", 18, LINE if dead else MUTED, anchor="end")
        if not row:
            s.text(x0 + 4, y + ch / 2, "[ ]", 19, LINE if dead else MUTED, anchor="start", mono=True)
            continue
        st = states[r] if states else ["plain"] * len(row)
        if dead:
            st = ["off"] * len(row)
        s.cells(x0, y, row, cw=cw, ch=ch, states=st, gap=gap, size=size)
        if dead:
            s.line(x0 - 6, y + ch / 2, x0 + row_width(len(row), cw, gap) + 6, y + ch / 2, LINE, 2)


def rect_vs_jagged():
    s = Svg(300)
    s.text(240, 34, "NumPy: every row has the same length", 19, INK, weight=600)
    rect = [["63.0", "38.1", "4.0"], ["54.3", "23.5", "52.9"], ["41.2", "17.8", "9.6"], ["33.0", "21.4", "5.1"]]
    for r, row in enumerate(rect):
        s.cells(96, 70 + r * 50, row, cw=92, ch=44, states=["blue"] * 3, size=19)
    s.line(480, 30, 480, 276, EDGE, 2)
    s.text(720, 34, "real events: rows of different length", 19, INK, weight=600)
    jag_rows(s, 620, 70, JAG, states=[["hi"] * len(r) for r in JAG])
    return s


def jagged():
    s = Svg(290)
    jag_rows(s, 330, 44, JAG, states=[["blue"] * len(r) for r in JAG], cw=110, ch=50)
    s.text(720, 69, "3 muons", 18, MUTED, anchor="start")
    s.text(720, 125, "0 muons", 18, MUTED, anchor="start")
    s.text(720, 181, "2 muons", 18, MUTED, anchor="start")
    s.text(720, 237, "1 muon", 18, MUTED, anchor="start")
    return s


def type_string():
    s = Svg(230)
    parts = [("4", "four events"), ("var", "a variable number in each"), ("float64", "of decimal numbers")]
    xs = [220, 440, 720]
    for (p, what), x in zip(parts, xs):
        s.box(x - 80, 50, 160, 64, p, "hi", size=26, mono=True, weight=600)
        s.arrow(x, 122, x, 158, MUTED)
        s.text(x, 182, what, 19, INK)
    s.text(330, 82, "*", 28, MUTED, mono=True)
    s.text(580, 82, "*", 28, MUTED, mono=True)
    return s


def mask_particles(x0=330, s=None, title=True, y0=70):
    own = s is None
    s = s or Svg(300)
    keep = [[True, True, False], [], [True, True], [True]]
    st = [["blue" if k else "off" for k in row] for row in keep]
    jag_rows(s, x0, y0, JAG, states=st)
    if title and own:
        s.text(480, 34, "pt[pt > 20]   a jagged mask, one True or False per muon", 19, INK, mono=False, weight=600)
        s.text(x0 + 330, 92, "muons are dropped,", 18, MUTED, anchor="start")
        s.text(x0 + 330, 118, "all four events remain", 18, MUTED, anchor="start")
    return s


def mask_events(x0=330, s=None, title=True, y0=70):
    own = s is None
    s = s or Svg(300)
    rs = [True, False, True, False]
    jag_rows(s, x0, y0, JAG, states=[["blue"] * len(r) for r in JAG], row_states=rs)
    if title and own:
        s.text(480, 34, "pt[ak.num(pt) >= 2]   a flat mask, one True or False per event", 19, INK, weight=600)
        s.text(x0 + 330, 92, "whole events are dropped,", 18, MUTED, anchor="start")
        s.text(x0 + 330, 118, "two events remain", 18, MUTED, anchor="start")
    return s


def two_masks():
    s = Svg(320)
    s.text(250, 32, "drop particles", 21, INK, weight=600)
    s.text(250, 58, "mask has one value per muon", 17, MUTED)
    mask_particles(130, s, title=False, y0=92)
    s.line(480, 24, 480, 296, EDGE, 2)
    s.text(730, 32, "drop events", 21, INK, weight=600)
    s.text(730, 58, "mask has one value per event", 17, MUTED)
    mask_events(610, s, title=False, y0=92)
    # shift rows down a little: rows were drawn at y=70, fine
    return s


def reduce_axis1(kind="sum"):
    s = Svg(290)
    x0 = 250
    jag_rows(s, x0, 50, JAG)
    if kind == "sum":
        res, st, name = ["105.1", "0.0", "77.8", "41.2"], ["blue"] * 4, "ak.sum(pt, axis=1)"
    elif kind == "max":
        res, st, name = ["63.0", "None", "54.3", "41.2"], ["blue", "hi", "blue", "blue"], "ak.max(pt, axis=1)"
    else:
        res, st, name = ["True", "False", "True", "False"], ["hi", "grey", "hi", "grey"], "ak.any(pt > 50, axis=1)"
    for r in range(4):
        y = 50 + r * 50
        s.arrow(x0 + 310, y + 22, 640, y + 22, ORANGE)
        s.box(652, y, 110, 44, res[r], st[r], size=19, mono=True, weight=400)
    s.text(707, 26, name, 18, ORANGE, mono=True, weight=600)
    s.text(780, 122, "one value", 18, MUTED, anchor="start")
    s.text(780, 148, "per event", 18, MUTED, anchor="start")
    return s


def record():
    s = Svg(300)
    pts = JAG
    qs = [["1", "-1", "1"], [], ["1", "-1"], ["-1"]]
    x0 = 210
    for r, (prow, qrow) in enumerate(zip(pts, qs)):
        y = 44 + r * 60
        s.text(x0 - 18, y + 26, f"event {r}", 18, MUTED, anchor="end")
        if not prow:
            s.text(x0 + 4, y + 26, "[ ]", 19, MUTED, anchor="start", mono=True)
        for i, (p, q) in enumerate(zip(prow, qrow)):
            x = x0 + i * 176
            s.rect(x, y, 166, 52, BLUE_L, BLUE)
            s.text(x + 14, y + 16, "pt", 15, MUTED, anchor="start", mono=True)
            s.text(x + 152, y + 16, p, 18, INK, anchor="end", mono=True)
            s.text(x + 14, y + 37, "charge", 15, MUTED, anchor="start", mono=True)
            s.text(x + 152, y + 37, q, 18, INK, anchor="end", mono=True)
    s.text(760, 70, "one record", 18, ORANGE, anchor="start", weight=600)
    s.text(760, 96, "= one muon", 18, ORANGE, anchor="start", weight=600)
    s.text(760, 150, "fields", 18, MUTED, anchor="start")
    s.text(760, 178, "pt, charge", 19, INK, anchor="start", mono=True)
    return s


def flatten():
    s = Svg(290)
    jag_rows(s, 150, 50, JAG, states=[["blue"] * len(r) for r in JAG], cw=84, size=18)
    s.arrow(450, 146, 560, 146, ORANGE)
    s.text(505, 122, "ak.flatten", 18, ORANGE, mono=True, weight=600)
    flat = ["63.0", "38.1", "4.0", "54.3", "23.5", "41.2"]
    for i, v in enumerate(flat):
        s.box(580 + (i % 3) * 110, 96 + (i // 3) * 54, 100, 46, v, "blue", size=18, mono=True, weight=400)
    s.text(740, 232, "one flat list, events forgotten", 18, MUTED)
    return s


def combinations():
    s = Svg(250)
    s.text(190, 40, "one event, three muons", 18, MUTED)
    names = ["a", "b", "c"]
    for i, n in enumerate(names):
        s.box(90 + i * 72, 100, 62, 56, n, "blue", size=24, mono=True, weight=600)
    s.arrow(320, 128, 440, 128, ORANGE)
    s.text(380, 104, "ak.combinations", 17, ORANGE, mono=True, weight=600)
    s.text(380, 152, "(…, 2)", 17, ORANGE, mono=True, weight=600)
    s.text(690, 40, "every pair, each counted once", 18, MUTED)
    pairs = [("a", "b"), ("a", "c"), ("b", "c")]
    for i, (p, q) in enumerate(pairs):
        x = 470 + i * 150
        s.rect(x, 96, 134, 64, ORANGE_L, ORANGE)
        s.box(x + 8, 106, 54, 44, p, "blue", size=22, mono=True, weight=600)
        s.box(x + 72, 106, 54, 44, q, "blue", size=22, mono=True, weight=600)
    s.text(690, 196, "3 muons give 3 pairs, 4 give 6, 2 give 1, fewer give none", 17, MUTED)
    return s


def two_muons():
    s = Svg(260)
    rows = [["63.0", "38.1"], ["54.3", "23.5"], ["47.9", "31.0"]]
    x0, cw = 310, 180
    for r, row in enumerate(rows):
        s.cells(x0, 84 + r * 52, row, cw=cw, ch=44, states=["hi", "blue"], size=19)
        s.text(x0 - 18, 106 + r * 52, f"event {r}", 18, MUTED, anchor="end")
    s.text(x0 + cw / 2, 40, "muons[:, 0]", 19, ORANGE, mono=True, weight=600)
    s.text(x0 + cw / 2, 64, "mu1", 18, MUTED, mono=True)
    s.text(x0 + cw + 6 + cw / 2, 40, "muons[:, 1]", 19, BLUE, mono=True, weight=600)
    s.text(x0 + cw + 6 + cw / 2, 64, "mu2", 18, MUTED, mono=True)
    return s


def higgs_flow():
    s = Svg(230)
    items = [
        ("select leptons", "pt and eta cuts"),
        ("keep 4-lepton events", "ak.num"),
        ("form groups of four", "ak.combinations"),
        ("add and take .mass", "vector"),
    ]
    bw, bh, gap = 196, 84, 40
    x0 = (W - (4 * bw + 3 * gap)) / 2
    for i, (name, sub) in enumerate(items):
        x = x0 + i * (bw + gap)
        s.box(x, 60, bw, bh, name, "hi" if i == 3 else "plain", size=18, weight=600)
        s.text(x + bw / 2, 60 + bh + 28, sub, 17, MUTED, mono=True)
        s.text(x + bw / 2, 36, str(i + 1), 18, MUTED, weight=600)
        if i < 3:
            s.arrow(x + bw + 6, 60 + bh / 2, x + bw + gap - 6, 60 + bh / 2)
    return s


# ---------------------------------------------------------------- introduction and exercises

def higgs_decay():
    s = Svg(330)
    s.text(150, 30, "decays at once, never seen", 17, MUTED)
    s.text(800, 30, "seen in the detector", 17, BLUE, weight=600)
    s.box(80, 132, 140, 66, "H", "hi", size=28, weight=700, sub="125 GeV")
    zs = [(380, 58, "Z", "about 91 GeV"), (380, 206, "Z", "below 91 GeV")]
    for x, y, n, sub in zs:
        s.box(x, y, 140, 66, n, "hi", size=26, weight=700, sub=sub)
        s.arrow(226, 165, x - 8, y + 33, ORANGE)
    leptons = [(58, "e+", 0), (58, "e-", 1), (206, "mu+", 2), (206, "mu-", 3)]
    names = {"e+": "e\u207a", "e-": "e\u207b", "mu+": "\u03bc\u207a", "mu-": "\u03bc\u207b"}
    for zy, lab, k in leptons:
        y = 48 + k * 64
        s.box(730, y, 140, 50, names[lab], "blue", size=24, weight=600)
        s.arrow(526, zy + 33, 722, y + 25, BLUE)
    s.text(450, 306, "add the four-momenta of the leptons to get back the Z and the Higgs", 18, INK)
    return s


def session_plan():
    s = Svg(220)
    items = [("1  Python", "plain"), ("2  NumPy", "plain"), ("3  Classes", "plain"), ("4  Awkward", "plain")]
    bw, bh, gap = 190, 84, 46
    x0 = (W - (4 * bw + 3 * gap)) / 2
    for i, (name, st) in enumerate(items):
        x = x0 + i * (bw + gap)
        s.rect(x, 50, bw, bh, *STATES[st][:2], dash=STATES[st][3])
        ink = LINE if st == "off" else INK
        s.text(x + bw / 2, 50 + 26, name, 22, ink, weight=600)
        s.rect(x + 12, 50 + 46, (bw - 32) / 2, 28, BLUE_L if st != "off" else BG, BLUE if st != "off" else LINE, rx=6, sw=1.5)
        s.text(x + 12 + (bw - 32) / 4, 50 + 60, "lecture", 15, ink)
        s.rect(x + 20 + (bw - 32) / 2, 50 + 46, (bw - 32) / 2, 28, ORANGE_L if st != "off" else BG, ORANGE if st != "off" else LINE, rx=6, sw=1.5)
        s.text(x + 20 + 3 * (bw - 32) / 4, 50 + 60, "project", 15, ink)
        if i < 3:
            s.arrow(x + bw + 8, 50 + bh / 2, x + bw + gap - 8, 50 + bh / 2)
    xb = x0 + 4 * bw + 3 * gap
    s.path(f"M{x0},{50 + bh + 14} v14 H{xb} v-14", ORANGE, 3)
    s.text((x0 + xb) / 2, 50 + bh + 52, "short lectures, then most of the time on projects that rebuild one Higgs analysis", 18, ORANGE, weight=600)
    return s


def jupyter_order():
    s = Svg(270)
    s.text(200, 30, "cells on the page", 18, MUTED)
    s.rect(60, 54, 290, 54, GREY_L, LINE)
    s.text(80, 81, "x = 1", 22, INK, anchor="start", mono=True)
    s.text(40, 81, "1", 18, ORANGE, anchor="end", mono=True, weight=600)
    s.rect(60, 128, 290, 54, GREY_L, LINE)
    s.text(80, 155, "x = x + 10", 22, INK, anchor="start", mono=True)
    s.text(40, 155, "2", 18, ORANGE, anchor="end", mono=True, weight=600)
    s.text(660, 30, "what Python remembers", 18, MUTED)
    vals = [("run cell 1", "x = 1"), ("run cell 2", "x = 11"), ("run cell 2 again", "x = 21")]
    for i, (lab, v) in enumerate(vals):
        y = 54 + i * 66
        s.text(540, y + 25, lab, 18, MUTED, anchor="end")
        s.box(560, y, 200, 50, v, "hi" if i == 2 else "blue", size=21, mono=True, weight=400)
    s.text(450, 250, "the order you run cells in matters, not their order on the page", 18, INK)
    return s


def event_higgs():
    s = Svg(350)
    s.box(40, 136, 150, 62, "event", "solid", size=24, mono=True, weight=600)
    keys = [('"run"', 30, "1"), ('"event"', 92, "46548")]
    for k, y, v in keys:
        s.box(250, y, 150, 46, k, "plain", size=20, mono=True, weight=400)
        s.arrow(196, 167, 242, y + 23)
        s.arrow(406, y + 23, 452, y + 23)
        s.box(460, y, 110, 46, v, "blue", size=20, mono=True, weight=400)
    groups = [('"electron"', 168, [("48.0", "+1"), ("42.4", "-1")]), ('"muon"', 250, [("22.3", "+1"), ("11.2", "-1")])]
    for k, y, recs in groups:
        s.box(250, y, 150, 46, k, "hi", size=20, mono=True, weight=400)
        s.arrow(196, 167, 242, y + 23)
        s.arrow(406, y + 23, 452, y + 23)
        for i, (pt, q) in enumerate(recs):
            x = 460 + i * 200
            s.rect(x, y - 6, 190, 58, BLUE_L, BLUE)
            s.text(x + 12, y + 10, "pt", 15, MUTED, anchor="start", mono=True)
            s.text(x + 178, y + 10, pt, 17, INK, anchor="end", mono=True)
            s.text(x + 12, y + 34, "charge", 15, MUTED, anchor="start", mono=True)
            s.text(x + 178, y + 34, q, 17, INK, anchor="end", mono=True)
    s.text(460, 328, "each lepton also has eta, phi and mass", 17, MUTED, anchor="start")
    return s


def lepton_columns():
    s = Svg(280)
    s.box(40, 106, 110, 62, "e1", "solid", size=24, mono=True, weight=600)
    rows = [('"pt"', ["5.47", "39.45", "48.01", "42.66"]), ('"eta"', ["1.68", "0.32", "1.95", "0.78"]), ('"charge"', ["-1", "-1", "1", "-1"])]
    for r, (k, vals) in enumerate(rows):
        y = 40 + r * 72
        s.box(210, y, 130, 50, k, "hi", size=20, mono=True, weight=400)
        s.arrow(156, 137, 202, y + 25)
        s.arrow(346, y + 25, 382, y + 25)
        s.cells(390, y, vals + ["..."], cw=88, ch=50, states=["blue"] * 4 + ["plain"], size=18)
    s.text(390 + 2.5 * 94, 262, "one entry per event, 30,868 events", 18, MUTED)
    return s


def two_ways():
    s = Svg(290)
    s.text(240, 34, "make each step faster", 20, INK, weight=600)
    s.text(240, 60, "arrays instead of loops, compiled loops", 17, MUTED)
    s.box(90, 100, 300, 56, "analyse one file", "plain", size=20)
    s.arrow(240, 162, 240, 196, ORANGE)
    s.box(165, 202, 150, 56, "analyse", "hi", size=20)
    s.line(480, 30, 480, 270, EDGE, 2)
    s.text(720, 34, "run several steps at once", 20, INK, weight=600)
    s.text(720, 60, "one file per core, then add the results", 17, MUTED)
    for i in range(3):
        s.box(540 + i * 124, 100 + i * 8, 112, 50, f"file {i}", "blue", size=18)
    s.arrow(720, 172, 720, 202, ORANGE)
    s.box(560, 208, 320, 50, "three cores at the same time", "hi", size=19)
    return s


def split_add(label="higgs_histogram", item="file", middle="one function per file", last="one histogram each", total="one histogram", note="the files are independent, so the middle step can run on several cores at once"):
    s = Svg(330)
    s.text(110, 30, item + "s", 18, MUTED)
    s.text(380, 30, middle, 18, MUTED)
    s.text(640, 30, last, 18, MUTED)
    ys = [52, 132, 212]
    for i, y in enumerate(ys):
        s.box(50, y, 120, 54, f"{item} {i}", "blue", size=19, mono=True, weight=400)
        s.arrow(178, y + 27, 268, y + 27)
        s.box(276, y, 210, 54, label, "plain", size=18, mono=True, weight=400)
        s.arrow(494, y + 27, 576, y + 27)
        s.rect(584, y + 4, 112, 46, WHITE, LINE)
        for k, hgt in enumerate([8, 18, 36, 14, 6]):
            s.rect(596 + k * 18, y + 44 - hgt, 14, hgt, ORANGE_L, ORANGE, rx=2, sw=1.5)
        s.arrow(704, y + 27, 772, 159)
    s.text(110, 284, "...", 24, MUTED)
    s.box(780, 118, 130, 82, "add", "hi", size=22, weight=600, sub=total)
    s.text(480, 312, note, 17, INK)
    return s


def class_objects():
    s = Svg(320)
    s.rect(40, 50, 300, 220, ORANGE_L, ORANGE, rx=12)
    s.text(190, 80, "class FourVector", 22, INK, mono=True, weight=700)
    s.text(60, 124, "data", 17, MUTED, anchor="start")
    s.text(60, 150, "E, px, py, pz", 19, INK, anchor="start", mono=True)
    s.text(60, 194, "methods", 17, MUTED, anchor="start")
    s.text(60, 220, "__add__, mass", 19, INK, anchor="start", mono=True)
    s.text(190, 300, "the recipe", 18, ORANGE, weight=600)
    objs = [("z_ee", "E 310.3  mass 90.3"), ("z_mumu", "E 87.0  mass 22.9"), ("higgs", "E 397.3  mass 125.2")]
    for i, (name, vals) in enumerate(objs):
        y = 50 + i * 78
        s.arrow(348, 160, 488, y + 30, MUTED)
        s.rect(496, y, 380, 60, BLUE_L, BLUE)
        s.text(516, y + 30, name, 20, INK, anchor="start", mono=True, weight=700)
        s.text(860, y + 30, vals, 17, MUTED, anchor="end", mono=True)
    s.text(686, 300, "objects made from it, each with its own data", 18, BLUE, weight=600)
    return s


def main():
    for i in (0, 1, 2, 3, 4):
        course_map(i).save(IMG / f"map-{i}.svg")
    two_ways().save(IMG / "two-ways.svg")
    split_add(label="process(events)", item="chunk", middle="the same method on every chunk", last="one output each", total="one output",
              note="you write the process method; a framework such as coffea runs the loop and adds the outputs").save(IMG / "process-chunks.svg")
    class_objects().save(IMG / "class-objects.svg")
    pipeline(("read", "select", "compute", "histogram")).save(IMG / "pipeline.svg")
    pipeline(("read",)).save(L2 / "pipeline-read.svg", L3 / "pipeline-read.svg")
    pipeline(("select",)).save(L2 / "pipeline-select.svg", L3 / "pipeline-select.svg")
    pipeline(("compute",)).save(L3 / "pipeline-compute.svg")
    pipeline(("histogram",)).save(L2 / "pipeline-histogram.svg", L3 / "pipeline-histogram.svg")
    pipeline(("read", "select", "histogram"), later=("compute",)).save(L2 / "pipeline-numpy.svg")

    name_value().save(L1 / "name-value.svg")
    types().save(L1 / "types.svg")
    list_index().save(L1 / "list.svg")
    list_index((0, 2)).save(L1 / "slice.svg")
    dict_().save(L1 / "dict.svg")
    event_tree().save(L1 / "event.svg")
    event_tree(path=True).save(L1 / "event-path.svg")
    for_loop().save(L1 / "for-loop.svg")
    if_().save(L1 / "if.svg")
    filter_().save(L1 / "filter.svg")
    function().save(L1 / "function.svg")
    loop_vs_column().save(L1 / "loop-vs-column.svg", L2 / "loop-vs-column.svg")

    list_vs_array().save(L2 / "list-vs-array.svg")
    elementwise().save(L2 / "elementwise.svg")
    elementwise(two=True).save(L2 / "elementwise-two.svg")
    mask().save(L2 / "mask.svg")
    mask(other=True).save(L2 / "mask-other.svg")
    reduce_().save(L2 / "reduce.svg")
    array2d().save(L2 / "array2d.svg")
    array2d(hi_col=0).save(L2 / "array2d-column.svg")
    axis().save(L2 / "axis.svg")
    broadcast().save(L2 / "broadcast.svg")
    histogram().save(L2 / "histogram.svg")
    tree().save(L2 / "tree.svg")
    rect_vs_jagged().save(L2 / "rect-vs-jagged.svg", L3 / "rect-vs-jagged.svg")

    jagged().save(L3 / "jagged.svg")
    type_string().save(L3 / "type.svg")
    two_masks().save(L3 / "two-masks.svg")
    mask_particles().save(L3 / "mask-particles.svg")
    mask_events().save(L3 / "mask-events.svg")
    reduce_axis1("sum").save(L3 / "reduce-sum.svg")
    reduce_axis1("max").save(L3 / "reduce-max.svg")
    reduce_axis1("any").save(L3 / "reduce-any.svg")
    record().save(L3 / "record.svg")
    flatten().save(L3 / "flatten.svg")
    combinations().save(L3 / "combinations.svg")
    two_muons().save(L3 / "two-muons.svg")
    higgs_flow().save(L3 / "higgs-flow.svg")

    higgs_decay().save(IMG / "higgs-decay.svg")
    session_plan().save(IMG / "session-plan.svg")
    jupyter_order().save(IMG / "jupyter-order.svg")
    event_higgs().save(IMG / "event-higgs.svg")
    lepton_columns().save(IMG / "lepton-columns.svg")


if __name__ == "__main__":
    main()
