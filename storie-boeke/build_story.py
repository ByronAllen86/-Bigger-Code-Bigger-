# -*- coding: utf-8 -*-
"""Bou albei storieboeke: python3 build_story.py"""
import math
import random
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
                                Table, TableStyle, Flowable, KeepTogether, NextPageTemplate)

from story_content import EN, AF

from reportlab.pdfgen import canvas as _cv


def _polygon(self, pts, fill=1, stroke=0):
    p = self.beginPath()
    p.moveTo(pts[0], pts[1])
    for k in range(2, len(pts), 2):
        p.lineTo(pts[k], pts[k + 1])
    p.close()
    self.drawPath(p, fill=fill, stroke=stroke)


_cv.Canvas.polygon = _polygon

FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("S", FD + "DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("S-B", FD + "DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("F", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("F-B", FD + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily("S", normal="S", bold="S-B", italic="S", boldItalic="S-B")
pdfmetrics.registerFontFamily("F", normal="F", bold="F-B", italic="F", boldItalic="F-B")

W, H = A4
M = 1.9 * cm
AW = W - 2 * M

PURPLE = colors.HexColor("#5B2A9E")
DPURPLE = colors.HexColor("#2E1065")
BLUE = colors.HexColor("#2D9CDB")
YELLOW = colors.HexColor("#FFC93C")
GOLD = colors.HexColor("#F5B800")
LYELLOW = colors.HexColor("#FFF6D6")
LPURPLE = colors.HexColor("#F0E8FB")
DARK = colors.HexColor("#1B1B3A")
GREY = colors.HexColor("#B0B0C0")
CREAM = colors.HexColor("#FFFDF6")

body = ParagraphStyle("body", fontName="S", fontSize=13.5, leading=22.5, textColor=DARK, spaceAfter=7)
ui = ParagraphStyle("ui", fontName="F", fontSize=11, leading=16, textColor=DARK)
h1 = ParagraphStyle("h1", fontName="F-B", fontSize=24, leading=30, textColor=PURPLE, spaceAfter=6)
quote = ParagraphStyle("quote", parent=body, fontName="F-B", fontSize=16, leading=24, alignment=TA_CENTER, textColor=DPURPLE)
STATE = {"label": ""}


def hexc(h):
    return colors.HexColor(h)


# ------------------------------------------------------------------ illustrasies
def sky(c, w, h, top="#7EC8F5", bottom="#E8F6FF", n=24):
    t, b = hexc(top), hexc(bottom)
    for i in range(n):
        f = i / (n - 1)
        c.setFillColorRGB(t.red * (1 - f) + b.red * f, t.green * (1 - f) + b.green * f, t.blue * (1 - f) + b.blue * f)
        c.rect(0, h - (i + 1) * h / n, w, h / n + 0.6, fill=1, stroke=0)


def cloud(c, x, y, s=1.0, col=colors.white):
    c.setFillColor(col)
    for dx, dy, r in [(0, 0, 14), (16, 7, 18), (36, 0, 15), (18, -4, 15)]:
        c.circle(x + dx * s, y + dy * s, r * s, fill=1, stroke=0)


def star(c, x, y, r, col=GOLD, rot=0):
    pts = []
    for i in range(10):
        ang = math.pi / 5 * i - math.pi / 2 + rot
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(ang), y + rr * math.sin(ang)))
    p = c.beginPath()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    c.setFillColor(col)
    c.setStrokeColor(colors.HexColor("#C98A00"))
    c.setLineWidth(1)
    c.drawPath(p, fill=1, stroke=1)


def face(c, x, y, r, sad=False, col=colors.white):
    c.setFillColor(DARK)
    c.circle(x - r * 0.35, y + r * 0.15, r * 0.1, fill=1, stroke=0)
    c.circle(x + r * 0.35, y + r * 0.15, r * 0.1, fill=1, stroke=0)
    c.setStrokeColor(DARK)
    c.setLineWidth(2)
    p = c.beginPath()
    if sad:
        p.arc(x - r * 0.3, y - r * 0.55, x + r * 0.3, y - r * 0.1, 20, 140)
    else:
        p.arc(x - r * 0.3, y - r * 0.5, x + r * 0.3, y - r * 0.05, 200, 140)
    c.drawPath(p, fill=0, stroke=1)


def scene(c, kind, w, h):
    c.saveState()
    p = c.beginPath()
    p.roundRect(0, 0, w, h, 14)
    c.clipPath(p, stroke=0, fill=0)
    rnd = random.Random(sum(map(ord, kind)) + 5)
    if kind == "party":
        sky(c, w, h, "#2E1065", "#7B4BC8")
    elif kind in ("cave",):
        sky(c, w, h, "#3A2A55", "#1B1B3A")
    elif kind in ("tower", "cloud", "gate"):
        sky(c, w, h, "#7C8DA6", "#CDD7E4")
    else:
        sky(c, w, h)
    if kind not in ("cave", "gate", "cloud"):
        cloud(c, w * 0.08, h * 0.78, 0.9)
        cloud(c, w * 0.75, h * 0.8, 1.1)
    if kind == "ticket":
        c.saveState()
        c.translate(w / 2, h / 2)
        c.rotate(-7)
        c.setFillColor(GOLD)
        c.setStrokeColor(colors.HexColor("#C98A00"))
        c.setLineWidth(3)
        c.roundRect(-150, -62, 300, 124, 14, fill=1, stroke=1)
        c.setFillColor(YELLOW)
        c.roundRect(-140, -52, 280, 104, 10, fill=1, stroke=0)
        star(c, -95, 0, 34)
        c.setFillColor(DPURPLE)
        c.setFont("F-B", 22)
        c.drawString(-50, 10, STATE.get("ticket", "GOLDEN TICKET"))
        c.setFont("F", 12)
        c.drawString(-50, -14, "★ ★ ★ ★ ★ ★ ★")
        c.restoreState()
        for _ in range(14):
            c.setFillColor(rnd.choice([YELLOW, colors.white]))
            star(c, rnd.uniform(10, w - 10), rnd.uniform(8, h - 8), rnd.uniform(3, 7), col=YELLOW)
    elif kind == "bus":
        bx, by = w * 0.28, h * 0.22
        c.setFillColor(colors.HexColor("#2D6CDF"))
        c.roundRect(bx, by, 250, 80, 18, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#1F4FA8"))
        c.rect(bx, by + 22, 250, 6, fill=1, stroke=0)
        for i in range(5):
            c.setFillColor(colors.HexColor("#CFEAFF"))
            c.roundRect(bx + 14 + i * 40, by + 40, 30, 28, 5, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#4CAF50"))
        c.circle(bx + 214, by + 56, 11, fill=1, stroke=0)
        c.setFillColor(YELLOW)
        c.polygon([bx + 224, by + 56, bx + 236, by + 52, bx + 224, by + 50], fill=1, stroke=0)
        for wx in (bx + 55, bx + 195):
            c.setFillColor(DARK)
            c.circle(wx, by, 15, fill=1, stroke=0)
            c.setFillColor(GREY)
            c.circle(wx, by, 6, fill=1, stroke=0)
        c.setFillColor(DARK)
        c.rect(bx + 120, by + 80, 6, 14, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#C0C8D8"))
        c.ellipse(bx + 60, by + 90, bx + 190, by + 100, fill=1, stroke=0)
        cloud(c, bx - 40, by - 14, 0.9)
        cloud(c, bx + 230, by - 22, 1.0)
    elif kind == "island":
        ix, iy = w * 0.5, h * 0.5
        c.setFillColor(colors.HexColor("#8D5B3A"))
        c.polygon([ix - 120, iy, ix + 120, iy, ix + 40, iy - 85, ix - 40, iy - 85], fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#5DBB63"))
        c.ellipse(ix - 125, iy - 14, ix + 125, iy + 16, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#4FA956"))
        c.ellipse(ix - 90, iy, ix + 20, iy + 55, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#8D5B3A"))
        c.rect(ix + 60, iy + 5, 6, 40, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#E4572E"))
        c.polygon([ix + 66, iy + 45, ix + 90, iy + 38, ix + 66, iy + 30], fill=1, stroke=0)
        c.setStrokeColor(colors.white)
        c.setLineWidth(3)
        for dx in (-100, 100, -60):
            c.line(ix + dx, iy - 4, ix + dx, iy + 52 if dx != -60 else iy + 30)
        star(c, ix, iy - 30, 12)
    elif kind in ("bridge", "chasm"):
        c.setFillColor(colors.HexColor("#8D5B3A"))
        c.rect(0, 0, w * 0.22, h * 0.5, fill=1, stroke=0)
        c.rect(w * 0.78, 0, w * 0.22, h * 0.5, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#5DBB63"))
        c.rect(0, h * 0.5 - 8, w * 0.22, 8, fill=1, stroke=0)
        c.rect(w * 0.78, h * 0.5 - 8, w * 0.22, 8, fill=1, stroke=0)
        if kind == "bridge":
            cloud(c, w * 0.35, h * 0.12, 1.4)
            cloud(c, w * 0.55, h * 0.08, 1.2)
            gap = [(w * 0.22 + i * (w * 0.56 / 9)) for i in range(9)]
            for i, x in enumerate(gap):
                if i in (3, 6):
                    continue
                c.setFillColor(colors.HexColor("#B07A44"))
                c.saveState()
                c.translate(x + 6, h * 0.5 - 4 + (4 if i % 2 else -2))
                c.rotate(3 if i % 2 else -3)
                c.rect(0, 0, w * 0.056, 7, fill=1, stroke=0)
                c.restoreState()
            c.setStrokeColor(colors.HexColor("#6B4423"))
            c.setLineWidth(2)
            c.line(w * 0.22, h * 0.5 + 24, w * 0.78, h * 0.5 + 14)
            c.setFillColor(colors.HexColor("#E4572E"))
            c.circle(w * 0.12, h * 0.5 + 20, 8, fill=1, stroke=0)
            c.rect(w * 0.12 - 6, h * 0.5 - 6, 12, 18, fill=1, stroke=0)
        else:
            c.setFillColor(colors.HexColor("#3B2A1F"))
            c.rect(w * 0.22, 0, w * 0.56, h * 0.5, fill=1, stroke=0)
            c.setFillColor(colors.HexColor("#B07A44"))
            for i in range(8):
                c.rect(w * 0.22 + i * (w * 0.56 / 8), h * 0.5 - 4, w * 0.56 / 8 - 3, 7, fill=1, stroke=0)
            hx, hy = w * 0.5, h * 0.17
            c.setFillColor(colors.HexColor("#C98A52"))
            c.circle(hx, hy, 24, fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.circle(hx - 8, hy + 6, 5, fill=1, stroke=0)
            c.circle(hx + 8, hy + 6, 5, fill=1, stroke=0)
            c.rect(hx - 6, hy - 14, 12, 8, fill=1, stroke=0)
            c.setFillColor(DARK)
            c.circle(hx - 8, hy + 6, 2, fill=1, stroke=0)
            c.circle(hx + 8, hy + 6, 2, fill=1, stroke=0)
    elif kind == "gate":
        c.setFillColor(colors.HexColor("#6B7280"))
        c.rect(w * 0.25, 0, w * 0.5, h * 0.9, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#4B5563"))
        c.rect(w * 0.2, 0, w * 0.06, h * 0.95, fill=1, stroke=0)
        c.rect(w * 0.74, 0, w * 0.06, h * 0.95, fill=1, stroke=0)
        fx, fy = w * 0.5, h * 0.52
        c.setFillColor(colors.HexColor("#9CA3AF"))
        c.circle(fx, fy, 62, fill=1, stroke=0)
        c.setStrokeColor(DARK)
        c.setLineWidth(3)
        for dx in (-24, 24):
            p = c.beginPath()
            p.arc(fx + dx - 11, fy + 10, fx + dx + 11, fy + 26, 180, 180)
            c.drawPath(p, fill=0, stroke=1)
        c.setFillColor(DARK)
        c.polygon([fx - 40, fy - 14, fx - 10, fy - 4, fx, fy - 12, fx + 10, fy - 4, fx + 40, fy - 14, fx + 28, fy - 28, fx, fy - 18, fx - 28, fy - 28], fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.setFont("F-B", 18)
        c.drawCentredString(w * 0.5, h * 0.06, "?  ?  ?")
    elif kind == "cave":
        c.setFillColor(colors.HexColor("#4A3B63"))
        c.ellipse(-20, -30, w + 20, h * 0.55, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#0E0B18"))
        c.ellipse(w * 0.22, -40, w * 0.78, h * 0.95, fill=1, stroke=0)
        bx, by = w * 0.5, h * 0.33
        c.setFillColor(colors.HexColor("#8E5BD0"))
        c.ellipse(bx - 90, by - 38, bx + 90, by + 50, fill=1, stroke=0)
        c.circle(bx - 40, by + 52, 14, fill=1, stroke=0)
        c.circle(bx + 40, by + 52, 14, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.circle(bx - 20, by + 18, 9, fill=1, stroke=0)
        c.circle(bx + 20, by + 18, 9, fill=1, stroke=0)
        c.setFillColor(DARK)
        c.circle(bx - 20, by + 16, 4, fill=1, stroke=0)
        c.circle(bx + 20, by + 16, 4, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#6E3FB5"))
        c.setFont("F-B", 16)
        c.drawString(bx + 70, by + 66, "Z z z")
        for _ in range(16):
            c.setFillColor(colors.HexColor("#6FD3FF"))
            c.circle(rnd.uniform(20, w - 20), rnd.uniform(8, h - 10), rnd.uniform(1.5, 3.5), fill=1, stroke=0)
    elif kind == "tower":
        tx = w * 0.4
        c.setFillColor(colors.HexColor("#5C6677"))
        c.rect(tx - 30, 0, 60, h * 0.88, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#3E4654"))
        c.polygon([tx - 40, h * 0.88, tx + 40, h * 0.88, tx, h * 1.02], fill=1, stroke=0)
        c.setFillColor(YELLOW)
        c.rect(tx - 8, h * 0.7, 16, 22, fill=1, stroke=0)
        cloud(c, tx - 90, h * 0.55, 1.5, colors.HexColor("#8E9AAD"))
        cloud(c, tx + 40, h * 0.35, 1.7, colors.HexColor("#8E9AAD"))
        c.setFillColor(YELLOW)
        c.polygon([w * 0.78, h * 0.9, w * 0.74, h * 0.62, w * 0.78, h * 0.64, w * 0.73, h * 0.38, w * 0.82, h * 0.7, w * 0.78, h * 0.68], fill=1, stroke=0)
        gx, gy = w * 0.64, h * 0.62
        c.setFillColor(colors.HexColor("#E4572E"))
        c.polygon([gx - 60, gy - 6, gx + 60, gy - 6, gx, gy + 18], fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#B8381B"))
        c.polygon([gx - 60, gy - 6, gx, gy - 14, gx + 60, gy - 6], fill=1, stroke=0)
        c.setFillColor(DARK)
        c.circle(gx - 8, gy + 2, 5, fill=1, stroke=0)
        c.circle(gx + 10, gy + 2, 5, fill=1, stroke=0)
    elif kind == "cloud":
        cx, cy = w * 0.4, h * 0.45
        cloud(c, cx - 70, cy - 10, 3.0, colors.HexColor("#8E9AAD"))
        face(c, cx + 5, cy + 5, 48, sad=True)
        star(c, w * 0.72, h * 0.45, 30)
        for _ in range(26):
            x = rnd.uniform(cx - 80, cx + 90)
            c.setFillColor(colors.HexColor("#6FA8DC"))
            c.circle(x, rnd.uniform(4, cy - 40), 2.4, fill=1, stroke=0)
    elif kind == "party":
        star(c, w * 0.5, h * 0.5, 54)
        for _ in range(90):
            c.setFillColor(rnd.choice([YELLOW, BLUE, colors.white, colors.HexColor("#FF6FB5"), colors.HexColor("#6FE3A5")]))
            c.circle(rnd.uniform(6, w - 6), rnd.uniform(6, h - 6), rnd.uniform(1.5, 4), fill=1, stroke=0)
        for i in range(10):
            c.setFillColor([YELLOW, BLUE, colors.HexColor("#FF6FB5"), colors.HexColor("#6FE3A5")][i % 4])
            c.polygon([w * i / 10, h, w * (i + 1) / 10, h, w * (i + 0.5) / 10, h - 22], fill=1, stroke=0)
    c.restoreState()


class Scene(Flowable):
    def __init__(self, kind, height=4.6 * cm):
        super().__init__()
        self.kind, self.h = kind, height

    def wrap(self, aw, ah):
        self.w = aw
        return aw, self.h

    def draw(self):
        scene(self.canv, self.kind, self.w, self.h)


class SetLabel(Flowable):
    def __init__(self, t):
        super().__init__()
        self.t = t

    def wrap(self, w, h):
        return 0, 0

    def draw(self):
        STATE["label"] = self.t


class Lines(Flowable):
    def __init__(self, n, gap=1.1 * cm):
        super().__init__()
        self.n, self.gap = n, gap

    def wrap(self, aw, ah):
        self.width = aw
        return aw, self.n * self.gap

    def draw(self):
        self.canv.setStrokeColor(GREY)
        self.canv.setLineWidth(0.7)
        for i in range(self.n):
            y = self.n * self.gap - (i + 1) * self.gap + 3
            self.canv.line(0, y, self.width, y)


class MapFlow(Flowable):
    def __init__(self, labels):
        super().__init__()
        self.labels = labels

    def wrap(self, aw, ah):
        self.w, self.h = aw, 15.5 * cm
        return self.w, self.h

    def draw(self):
        c, w, h = self.canv, self.w, self.h
        c.saveState()
        p = c.beginPath()
        p.roundRect(0, 0, w, h, 14)
        c.clipPath(p, stroke=0, fill=0)
        sky(c, w, h, "#BFE6FF", "#E9F8EC")
        c.setFillColor(colors.HexColor("#CDEBC8"))
        c.ellipse(-40, -60, w * 0.8, h * 0.35, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#B9DDF5"))
        c.ellipse(w * 0.55, h * 0.1, w * 1.1, h * 0.38, fill=1, stroke=0)
        pts = [(0.14, 0.09), (0.40, 0.2), (0.78, 0.30), (0.30, 0.48), (0.72, 0.66), (0.5, 0.90)]
        P = [(x * w, y * h) for x, y in pts]
        c.setStrokeColor(colors.HexColor("#B07A44"))
        c.setLineWidth(7)
        c.setDash(2, 9)
        c.setLineCap(1)
        path = c.beginPath()
        path.moveTo(*P[0])
        for a, b in zip(P, P[1:]):
            mx = (a[0] + b[0]) / 2
            path.curveTo(mx, a[1], mx, b[1], b[0], b[1])
        c.drawPath(path, fill=0, stroke=1)
        c.setDash()
        c.setLineCap(0)
        # decoratie
        cloud(c, w * 0.08, h * 0.82, 1.2)
        cloud(c, w * 0.78, h * 0.88, 1.0)
        # berg
        c.setFillColor(colors.HexColor("#8D7BA8"))
        c.polygon([w * 0.3, h * 0.72, w * 0.5, h * 1.0, w * 0.72, h * 0.72], fill=1, stroke=0)
        for i, ((x, y), lab) in enumerate(zip(P, self.labels), 1):
            col = PURPLE if i < 6 else colors.HexColor("#E4572E")
            c.setFillColor(col)
            c.setStrokeColor(colors.white)
            c.setLineWidth(3)
            c.circle(x, y, 15, fill=1, stroke=1)
            c.setFillColor(colors.white)
            c.setFont("F-B", 14)
            c.drawCentredString(x, y - 5, str(i))
            tw = pdfmetrics.stringWidth(lab, "F-B", 11) + 34
            lx = min(max(x - tw / 2, 6), w - tw - 6)
            ly = y - 38 if i != 6 else y + 20
            c.setFillColor(colors.white)
            c.roundRect(lx, ly, tw, 20, 8, fill=1, stroke=0)
            c.setFillColor(DARK)
            c.setFont("F-B", 11)
            c.drawString(lx + 8, ly + 6, lab)
            c.setStrokeColor(DARK)
            c.setLineWidth(1)
            c.rect(lx + tw - 20, ly + 5, 10, 10, fill=0, stroke=1)
        star(c, P[5][0] + 36, P[5][1] - 4, 11)
        c.restoreState()


# ------------------------------------------------------------------ bladsye
def draw_cover(c, doc, L):
    c.saveState()
    sky(c, W, H, "#2E1065", "#9ED8F7", n=48)
    random.seed(11)
    for _ in range(60):
        c.setFillColor(colors.white)
        c.circle(random.uniform(0, W), random.uniform(H * 0.55, H), random.uniform(0.8, 2.4), fill=1, stroke=0)
    c.restoreState()
    c.saveState()
    cloud(c, 40, H * 0.14, 2.8)
    cloud(c, W - 190, H * 0.1, 3.2)
    cloud(c, W / 2 - 60, H * 0.05, 3.4)
    # bus
    bx, by = W / 2 - 150, H * 0.2
    c.setFillColor(colors.HexColor("#2D6CDF"))
    c.roundRect(bx, by, 300, 96, 22, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#1F4FA8"))
    c.rect(bx, by + 26, 300, 7, fill=1, stroke=0)
    for i in range(6):
        c.setFillColor(colors.HexColor("#CFEAFF"))
        c.roundRect(bx + 16 + i * 40, by + 48, 32, 34, 6, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#4CAF50"))
    c.circle(bx + 262, by + 68, 13, fill=1, stroke=0)
    c.setFillColor(YELLOW)
    c.polygon([bx + 273, by + 68, bx + 288, by + 62, bx + 273, by + 60], fill=1, stroke=0)
    for wx in (bx + 62, bx + 240):
        c.setFillColor(DARK)
        c.circle(wx, by, 18, fill=1, stroke=0)
        c.setFillColor(GREY)
        c.circle(wx, by, 7, fill=1, stroke=0)
    c.setFillColor(DARK)
    c.rect(bx + 146, by + 96, 8, 16, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#C0C8D8"))
    c.ellipse(bx + 70, by + 108, bx + 230, by + 120, fill=1, stroke=0)
    star(c, W - 90, H * 0.52, 26)
    # titel
    c.setFillColor(YELLOW)
    c.setFont("F-B", 11)
    c.drawCentredString(W / 2, H - 2.6 * cm, L["cover_top"])
    words = L["title"].split()
    lines = []
    cur = ""
    for wd in words:
        if len(cur) + len(wd) > 17 and cur:
            lines.append(cur)
            cur = wd
        else:
            cur = (cur + " " + wd).strip()
    lines.append(cur)
    y = H - 4.8 * cm
    for i, ln in enumerate(lines):
        c.setFillColor(colors.white if i % 2 == 0 else YELLOW)
        c.setFont("F-B", 38)
        c.drawCentredString(W / 2, y, ln)
        y -= 1.6 * cm
    c.setFillColor(DPURPLE)
    c.roundRect(M, 1.2 * cm, AW, 2.6 * cm, 12, fill=1, stroke=0)
    c.setFillColor(YELLOW)
    c.setFont("F-B", 14)
    c.drawCentredString(W / 2, 3.0 * cm, L["cover_for"])
    c.setFillColor(colors.white)
    c.setFont("F", 12.5)
    c.drawCentredString(W / 2, 2.1 * cm, L["cover_names"])
    c.restoreState()


def page_end(c, doc):
    c.saveState()
    c.setFillColor(PURPLE)
    c.rect(0, H - 0.8 * cm, W, 0.8 * cm, fill=1, stroke=0)
    c.setFillColor(YELLOW)
    c.rect(0, H - 0.8 * cm - 3, W, 3, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("F-B", 9)
    c.drawString(M, H - 0.55 * cm, STATE["label"])
    c.setFillColor(colors.HexColor("#8888A0"))
    c.setFont("F", 9)
    c.drawCentredString(W / 2, 0.9 * cm, f"— {c.getPageNumber()} —")
    c.restoreState()


def page_bg(c, doc):
    c.saveState()
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.restoreState()


def bold_sounds(t):
    return re.sub(r"\b([A-ZÀ-Ý]{4,}(?:-[A-ZÀ-Ý]{3,})*[!?]*)", r'<font color="#E4572E"><b>\1</b></font>', t)


def banner(L, i, title):
    left = Paragraph(f'<font color="#FFC93C" size="9">{L["ui"]["chapter"]}</font><br/><font size="30" color="white"><b>{i}</b></font>',
                     ParagraphStyle("b1", fontName="F-B", alignment=TA_CENTER, leading=30, textColor=colors.white))
    right = Paragraph(f'<font size="21" color="white"><b>{title}</b></font>', ParagraphStyle("b2", fontName="F-B", leading=27))
    t = Table([[left, right]], colWidths=[2.8 * cm, AW - 2.8 * cm], rowHeights=[2.3 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PURPLE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("LEFTPADDING", (1, 0), (1, 0), 12), ("RIGHTPADDING", (1, 0), (1, 0), 10),
                           ("ROUNDEDCORNERS", [10, 10, 10, 10])]))
    return t


def box(content, bg=LYELLOW, border=YELLOW, pad=11):
    t = Table([[content]], colWidths=[AW])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg), ("BOX", (0, 0), (-1, -1), 1.6, border),
                           ("LEFTPADDING", (0, 0), (-1, -1), pad + 3), ("RIGHTPADDING", (0, 0), (-1, -1), pad + 3),
                           ("TOPPADDING", (0, 0), (-1, -1), pad), ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
                           ("ROUNDEDCORNERS", [8, 8, 8, 8])]))
    return t


def front(L):
    U = L["ui"]
    f = [NextPageTemplate("main"), Spacer(1, 1), PageBreak(), SetLabel(L["title"])]
    f.append(Spacer(1, 1.2 * cm))
    f.append(Paragraph(U["dedication_title"], ParagraphStyle("dd", fontName="F-B", fontSize=30, leading=38, textColor=PURPLE, alignment=TA_CENTER)))
    f.append(Spacer(1, 10))
    f.append(Paragraph(U["dedication"], ParagraphStyle("dp", parent=body, alignment=TA_CENTER, fontSize=15.5, leading=27)))
    f.append(Spacer(1, 1.2 * cm))
    f.append(Paragraph(U["squad_title"], h1))
    rows = []
    for name, talent, motto, col in L["squad"]:
        a = Paragraph(f'<font color="white" size="15"><b>{name}</b></font>', ParagraphStyle("n", fontName="F-B", leading=20))
        b = Paragraph(f'<font size="9" color="#777790">{U["talent"].upper()}</font><br/><b>{talent}</b>', ParagraphStyle("t", fontName="F", fontSize=12.5, leading=17, textColor=DARK))
        c = Paragraph(f'<font size="9" color="#777790">{U["motto"].upper()}</font><br/><i>“{motto}”</i>', ParagraphStyle("m", fontName="F", fontSize=12, leading=17, textColor=DARK))
        rows.append([a, b, c])
    t = Table(rows, colWidths=[3.4 * cm, 5.4 * cm, AW - 8.8 * cm], rowHeights=[1.55 * cm] * len(rows))
    st = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 10),
          ("LINEBELOW", (1, 0), (-1, -1), 0.6, colors.HexColor("#E3DFF0"))]
    for i, (_, _, _, col) in enumerate(L["squad"]):
        st.append(("BACKGROUND", (0, i), (0, i), hexc(col)))
    t.setStyle(TableStyle(st))
    f.append(t)
    f.append(PageBreak())
    f.append(Paragraph(U["map_title"], h1))
    f.append(Paragraph(U["map_sub"], ParagraphStyle("ms", fontName="F", fontSize=11.5, leading=17, textColor=DARK)))
    f.append(Spacer(1, 8))
    f.append(MapFlow(L["map_stops"]))
    f.append(PageBreak())
    return f


def chapter(L, i, ch):
    U = L["ui"]
    f = [SetLabel(f"{L['title']}  ·  {U['chapter']} {i}")]
    f.append(banner(L, i, ch["title"]))
    f.append(Spacer(1, 10))
    f.append(Scene(ch["scene"]))
    f.append(Spacer(1, 12))
    for p in ch["paras"]:
        if isinstance(p, tuple) and p[0] == "q":
            f.append(Spacer(1, 3))
            f.append(box(Paragraph(p[1], quote), bg=LYELLOW, border=GOLD))
            f.append(Spacer(1, 9))
        elif isinstance(p, tuple) and p[0] == "list":
            items = "".join(f"<br/>&nbsp;&nbsp;<b>{n}.</b> {t}" for n, t in enumerate(p[1], 1))
            f.append(Paragraph(items, ParagraphStyle("li", parent=body, leftIndent=18, spaceAfter=9)))
        else:
            f.append(Paragraph(bold_sounds(p), body))
    f.append(Spacer(1, 6))
    f.append(KeepTogether([box(Paragraph(f'<font name="F-B" color="#C98A00">★ {U["challenge"]}</font><br/>{ch["challenge"]}',
                                         ParagraphStyle("ch", fontName="S", fontSize=13.5, leading=22, textColor=DARK)), bg=LPURPLE, border=PURPLE)]))
    f.append(PageBreak())
    return f


def ending(L):
    U = L["ui"]
    f = [SetLabel(L["title"])]
    f.append(Spacer(1, 4 * cm))
    f.append(Scene("party", height=7 * cm))
    f.append(Spacer(1, 18))
    f.append(Paragraph(U["the_end"], ParagraphStyle("te", fontName="F-B", fontSize=46, leading=54, alignment=TA_CENTER, textColor=PURPLE)))
    f.append(Paragraph(U["the_end_sub"], ParagraphStyle("te2", fontName="F", fontSize=18, leading=24, alignment=TA_CENTER, textColor=colors.HexColor("#C98A00"))))
    f.append(PageBreak())
    # vasvra
    f.append(Paragraph(U["quiz_title"], h1))
    f.append(Paragraph(U["quiz_sub"], ParagraphStyle("qs", fontName="F", fontSize=11.5, leading=17, textColor=DARK)))
    f.append(Spacer(1, 6))
    for n, (q, a) in enumerate(L["quiz"], 1):
        f.append(KeepTogether([Paragraph(f"<b>{n}.</b> {q}", ParagraphStyle("qq", fontName="F", fontSize=12.5, leading=18, textColor=DARK)), Lines(1, 0.95 * cm), Spacer(1, 3)]))
    ans = " &nbsp;".join(f"<b>{n}.</b> {a}" for n, (q, a) in enumerate(L["quiz"], 1))
    f.append(Spacer(1, 6))
    f.append(box(Paragraph(f"<b>{U['answers']}</b> {ans}", ParagraphStyle("an", fontName="F", fontSize=9, leading=13, textColor=DARK)), bg=LPURPLE, border=PURPLE, pad=7))
    f.append(PageBreak())
    # volgende avontuur
    f.append(Paragraph(U["next_title"], h1))
    f.append(Paragraph(U["next_text"], ParagraphStyle("nt", fontName="F", fontSize=12.5, leading=19, textColor=DARK)))
    f.append(Spacer(1, 8))
    f.append(Paragraph(f"<b>{U['draw']}</b>", ParagraphStyle("dr", fontName="F-B", fontSize=12, textColor=BLUE)))
    dt = Table([[""]], colWidths=[AW], rowHeights=[8.5 * cm])
    dt.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1.6, BLUE), ("BACKGROUND", (0, 0), (-1, -1), colors.white), ("ROUNDEDCORNERS", [8, 8, 8, 8])]))
    f.append(Spacer(1, 3))
    f.append(dt)
    f.append(Spacer(1, 10))
    f.append(Paragraph(f"<b>{U['write']}</b>", ParagraphStyle("wr", fontName="F-B", fontSize=12, textColor=PURPLE)))
    f.append(Lines(8, 1.15 * cm))
    return f


def build(L):
    doc = BaseDocTemplate(L["file"], pagesize=A4, title=L["title"], author="Gemaak vir Daniel / Made for Daniel",
                          leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=M)
    main = Frame(M, 1.5 * cm, AW, H - 1.5 * cm - 1.9 * cm, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    cover = Frame(M, M, AW, H - 2 * M)
    doc.addPageTemplates([PageTemplate("cover", [cover], onPage=lambda c, d: draw_cover(c, d, L)),
                          PageTemplate("main", [main], onPage=page_bg, onPageEnd=page_end)])
    STATE["ticket"] = "GOUE KAARTJIE" if L["code"] == "AF" else "GOLDEN TICKET"
    flow = front(L)
    for i, ch in enumerate(L["chapters"], 1):
        flow += chapter(L, i, ch)
    flow += ending(L)
    doc.build(flow)
    print("klaar:", L["file"])


if __name__ == "__main__":
    build(EN)
    build(AF)
