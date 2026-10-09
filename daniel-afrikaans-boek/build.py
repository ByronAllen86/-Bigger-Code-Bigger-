# -*- coding: utf-8 -*-
"""Bou die PDF: python3 build.py"""
import random
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
                                Table, TableStyle, Flowable, KeepTogether, NextPageTemplate)

from content import CHAPTERS, WORDSEARCH, TESTS

FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("F", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("F-B", FD + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily("F", normal="F", bold="F-B", italic="F", boldItalic="F-B")

W, H = A4
M = 1.8 * cm
AW = W - 2 * M

PURPLE = colors.HexColor("#5B2A9E")
DPURPLE = colors.HexColor("#2E1065")
BLUE = colors.HexColor("#2D9CDB")
LBLUE = colors.HexColor("#E3F2FD")
YELLOW = colors.HexColor("#FFC93C")
LYELLOW = colors.HexColor("#FFF6D6")
LPURPLE = colors.HexColor("#F0E8FB")
GREEN = colors.HexColor("#2EAD6B")
LGREEN = colors.HexColor("#E3F6EC")
GREY = colors.HexColor("#B0B0C0")
DARK = colors.HexColor("#1B1B3A")

body = ParagraphStyle("body", fontName="F", fontSize=13, leading=20, textColor=DARK)
story_st = ParagraphStyle("story", parent=body, fontSize=15, leading=25, spaceAfter=8)
small = ParagraphStyle("small", parent=body, fontSize=10.5, leading=15)
tiny = ParagraphStyle("tiny", parent=body, fontSize=9, leading=12, textColor=colors.HexColor("#555566"))
h1 = ParagraphStyle("h1", parent=body, fontName="F-B", fontSize=24, leading=30, textColor=PURPLE, spaceAfter=4)
h2 = ParagraphStyle("h2", parent=body, fontName="F-B", fontSize=16, leading=22, textColor=PURPLE, spaceBefore=6, spaceAfter=6)
q_st = ParagraphStyle("q", parent=body, fontName="F-B", fontSize=13, leading=19)
ex_st = ParagraphStyle("ex", parent=body, fontSize=13.5, leading=27)
center = ParagraphStyle("center", parent=body, alignment=TA_CENTER)
ans_st = ParagraphStyle("ans", parent=body, fontSize=10, leading=14)
ans_h = ParagraphStyle("ansh", parent=body, fontName="F-B", fontSize=11.5, leading=16, textColor=PURPLE, spaceBefore=6)

STATE = {"label": "", "right": ""}


class SetState(Flowable):
    def __init__(self, label, right=""):
        super().__init__()
        self.label, self.right = label, right

    def wrap(self, w, h):
        return 0, 0

    def draw(self):
        STATE["label"], STATE["right"] = self.label, self.right


class Lines(Flowable):
    def __init__(self, n, gap=1.2 * cm, width=None):
        super().__init__()
        self.n, self.gap, self.w = n, gap, width

    def wrap(self, aw, ah):
        self.width = self.w or aw
        return self.width, self.n * self.gap

    def draw(self):
        c = self.canv
        c.setStrokeColor(GREY)
        c.setLineWidth(0.7)
        for i in range(self.n):
            y = self.n * self.gap - (i + 1) * self.gap + 3
            c.line(0, y, self.width, y)


def box(content, bg=LYELLOW, border=YELLOW, pad=10):
    t = Table([[content]], colWidths=[AW])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg), ("BOX", (0, 0), (-1, -1), 1.5, border),
        ("LEFTPADDING", (0, 0), (-1, -1), pad + 2), ("RIGHTPADDING", (0, 0), (-1, -1), pad + 2),
        ("TOPPADDING", (0, 0), (-1, -1), pad), ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ("ROUNDEDCORNERS", [8, 8, 8, 8])]))
    return t


def banner(num, title, sub, color=PURPLE):
    left = Paragraph(f'<font color="#FFC93C" size="11">VLAK</font><br/><font size="30" color="white"><b>{num}</b></font>',
                     ParagraphStyle("b1", parent=center, textColor=colors.white, leading=30))
    right = Paragraph(f'<font size="20" color="white"><b>{title}</b></font><br/><font size="11" color="#FFE9A8">{sub}</font>',
                      ParagraphStyle("b2", parent=body, leading=24))
    t = Table([[left, right]], colWidths=[2.6 * cm, AW - 2.6 * cm], rowHeights=[2.2 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), color), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("LEFTPADDING", (1, 0), (1, 0), 12), ("ROUNDEDCORNERS", [10, 10, 10, 10])]))
    return t


def section_title(icon, text):
    return Paragraph(f'<font color="#FFC93C">{icon}</font> {text}', h2)


# ------------------------------------------------------------------ bladsy-versiering
def draw_cover(c, doc):
    c.saveState()
    c.setFillColor(DPURPLE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(PURPLE)
    c.rect(0, H * 0.28, W, H * 0.44, fill=1, stroke=0)
    c.setFillColor(YELLOW)
    c.rect(0, H * 0.28 - 8, W, 8, fill=1, stroke=0)
    c.rect(0, H * 0.72, W, 8, fill=1, stroke=0)
    random.seed(7)
    for _ in range(60):
        c.setFillColor(random.choice([YELLOW, BLUE, colors.white]))
        c.circle(random.uniform(0, W), random.uniform(H * 0.74, H), random.uniform(1, 3), fill=1, stroke=0)
    c.setFillColor(YELLOW)
    c.setFont("F-B", 16)
    c.drawCentredString(W / 2, H * 0.66, "GRAAD 3  ·  AFRIKAANS WERKBOEK")
    c.setFillColor(colors.white)
    c.setFont("F-B", 50)
    c.drawCentredString(W / 2, H * 0.58, "DANIEL SE")
    c.setFillColor(YELLOW)
    c.setFont("F-B", 50)
    c.drawCentredString(W / 2, H * 0.51, "AFRIKAANS")
    c.setFillColor(colors.white)
    c.drawCentredString(W / 2, H * 0.44, "AVONTUUR")
    c.setFont("F", 15)
    c.drawCentredString(W / 2, H * 0.36, "12 Vlakke  ·  Stories  ·  Speletjies  ·  Skryf soos 'n kampioen!")
    c.setFillColor(YELLOW)
    c.setFont("F-B", 22)
    c.drawCentredString(W / 2, H * 0.20, "Spesiaal gemaak vir Daniel")
    c.setFillColor(colors.white)
    c.setFont("F", 13)
    c.drawCentredString(W / 2, H * 0.165, "Land. Loot. Bou. Skryf. WEN!")
    c.setFont("F", 8.5)
    c.setFillColor(colors.HexColor("#B9A6E0"))
    c.drawCentredString(W / 2, 1.3 * cm, "Fan-gemaakte leerboek geïnspireer deur Fortnite. Nie amptelik nie en nie geaffilieer met Epic Games nie.")
    c.restoreState()


def page_end(c, doc):
    c.saveState()
    c.setFillColor(PURPLE)
    c.rect(0, H - 0.9 * cm, W, 0.9 * cm, fill=1, stroke=0)
    c.setFillColor(YELLOW)
    c.rect(0, H - 0.9 * cm - 3, W, 3, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("F-B", 9)
    c.drawString(M, H - 0.6 * cm, STATE["label"])
    c.drawRightString(W - M, H - 0.6 * cm, STATE["right"])
    c.setFillColor(colors.HexColor("#777790"))
    c.setFont("F", 8.5)
    c.drawString(M, 0.9 * cm, "Daniel se Afrikaans Avontuur")
    c.drawRightString(W - M, 0.9 * cm, f"Bladsy {c.getPageNumber()}")
    c.restoreState()


# ------------------------------------------------------------------ voorwerk
def front_matter():
    f = []
    f += [NextPageTemplate("main"), Spacer(1, 1), PageBreak()]
    f.append(SetState("Welkom"))
    f.append(Paragraph("Hallo Daniel!", h1))
    f.append(Paragraph(
        "Jy is 'n baie goeie speler. Nou is dit tyd om 'n <b>Afrikaans-kampioen</b> te word! "
        "In hierdie boek speel jy saam met Lisa, Pieter en Sipho. Saam beleef julle 12 vlakke vol stories, "
        "speletjies en slim taalkuns.", body))
    f.append(Spacer(1, 10))
    f.append(section_title("★", "So werk elke vlak"))
    steps = [("1. LAND", "Lees die storie hardop. Lees dit dan nog 'n keer."),
             ("2. LOOT", "Beantwoord die vrae oor die storie. Kyk mooi terug na die storie."),
             ("3. BOU", "Leer 'n nuwe taalreël en oefen dit."),
             ("4. SPEL", "Oefen jou spelwoorde. Bedek, skryf, kyk!"),
             ("5. WEN", "Skryf jou eie stukkie. Dis hier waar jy regtig beter word.")]
    rows = [[Paragraph(f"<b>{a}</b>", ParagraphStyle("s", parent=body, textColor=PURPLE)), Paragraph(b, body)] for a, b in steps]
    t = Table(rows, colWidths=[3.2 * cm, AW - 3.2 * cm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -2), 0.5, GREY),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    f.append(t)
    f.append(Spacer(1, 12))
    f.append(box(Paragraph(
        "<b>Daniel se Kampioen-reëls</b><br/>"
        "★ Doen net 1 vlak op 'n slag (ongeveer 20 – 30 minute).<br/>"
        "★ Lees altyd die vraag twee keer voor jy antwoord.<br/>"
        "★ Skryf in volsinne met 'n hoofletter en 'n leesteken.<br/>"
        "★ Maak jy 'n fout? Nie 'n probleem nie! Foute help jou leer.<br/>"
        "★ Kleur 'n ster in op die Vorderingsblad as jy klaar is.", body)))
    f.append(Spacer(1, 12))
    f.append(Paragraph("Jou span", h2))
    cast = [("Daniel", "Jy! Die leier wat altyd na almal luister."), ("Lisa", "Vinnig, slim en lees die kaart."),
            ("Pieter", "Sterk en 'n meester bouer."), ("Sipho", "Die nuwe speler wat baie vrae vra.")]
    rows = [[Paragraph(f"<b>{a}</b>", ParagraphStyle("c", parent=body, textColor=PURPLE)), Paragraph(b, body)] for a, b in cast]
    t = Table(rows, colWidths=[3.2 * cm, AW - 3.2 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), LBLUE), ("TOPPADDING", (0, 0), (-1, -1), 5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("LEFTPADDING", (0, 0), (-1, -1), 10),
                           ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.white), ("ROUNDEDCORNERS", [8, 8, 8, 8])]))
    f.append(t)
    f.append(PageBreak())

    # ouers
    f.append(Paragraph("Nota vir ouers", h1))
    f.append(Paragraph(
        "Hierdie werkboek is geskryf vir 'n Graad 3-leerder. Elke vlak volg dieselfde patroon sodat Daniel weet wat om te verwag, "
        "en elkeen oefen leesbegrip, woordeskat, taalstruktuur, spelling en skryf.", body))
    f.append(Spacer(1, 6))
    tips = [
        "<b>Roetine:</b> Een vlak per dag of per skooldag, 20 – 30 minute. Kort en gereeld werk beter as lang sessies.",
        "<b>Lees saam:</b> Laat Daniel die storie eers hardop lees. Help met moeilike woorde en bespreek die “Nuwe woorde”-blokkie.",
        "<b>Skryf-tyd:</b> Die skryfopdragte is die belangrikste deel. Moenie te veel regmaak nie. Prys eers die inhoud en pas dan gentlik 1 – 2 foute aan.",
        "<b>Nasienbord:</b> Die antwoorde is agter in die boek. By oop vrae is enige goeie, volledige antwoord reg.",
        "<b>Spelling:</b> Gebruik die “Bedek, skryf, kyk”-metode. Dikteer die woorde in die Toets Jouself-bladsye as 'n klein toets.",
        "<b>Motivering:</b> Die sterre op die Vorderingsblad en die Sertifikaat aan die einde gee Daniel iets om voor te werk.",
    ]
    for tp in tips:
        f.append(Paragraph("• " + tp, ParagraphStyle("tip", parent=body, fontSize=12, leading=18, leftIndent=12, firstLineIndent=-10, spaceAfter=7)))
    f.append(Spacer(1, 6))
    f.append(box(Paragraph(
        "<b>Skryf-nasienriglyn (4 sterre):</b><br/>"
        "★ Die sinne maak sin en pas by die opdrag.<br/>"
        "★ Elke sin begin met 'n hoofletter en eindig met 'n leesteken.<br/>"
        "★ Die nuwe taalreël van die vlak is gebruik.<br/>"
        "★ Spelling is nagegaan (veral die vlak se spelwoorde).", small), bg=LGREEN, border=GREEN))
    f.append(Spacer(1, 8))
    f.append(Paragraph(
        "Die taalinhoud is op Graad 3-vlak, maar kan makliker of moeiliker gemaak word deur meer of minder hulp te gee. "
        "Hierdie boek vervang nie die skool se werk nie. Dis ekstra oefening om selfvertroue en vaardigheid te bou.", tiny))
    f.append(PageBreak())

    # vorderingsblad
    f.append(Paragraph("Vorderingsblad", h1))
    f.append(Paragraph("Kleur 'n ster in vir elke deel wat jy klaar het. Wanneer al 3 sterre ingekleur is, kry jy 'n <b>OORWINNING</b>!", body))
    f.append(Spacer(1, 8))
    hdr = [Paragraph(f"<b>{x}</b>", ParagraphStyle("th", parent=small, textColor=colors.white)) for x in
           ["Vlak", "Onderwerp", "Lees", "Taal", "Skryf", "Datum", "WEN!"]]
    rows = [hdr]
    for i, ch in enumerate(CHAPTERS, 1):
        rows.append([Paragraph(f"<b>{i}</b>", small), Paragraph(f"{ch['title']}<br/><font size=8 color='#666677'>{ch['key']}</font>", small),
                     "☆", "☆", "☆", "", "☐"])
    t = Table(rows, colWidths=[1.4 * cm, 5.9 * cm, 1.8 * cm, 1.8 * cm, 1.8 * cm, 2.6 * cm, 2.1 * cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PURPLE), ("FONTNAME", (0, 0), (-1, -1), "F"), ("FONTSIZE", (2, 1), (4, -1), 17),
        ("FONTSIZE", (6, 1), (6, -1), 18), ("TEXTCOLOR", (2, 1), (4, -1), colors.HexColor("#E0A800")),
        ("ALIGN", (2, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.6, GREY), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LPURPLE]),
        ("TOPPADDING", (0, 1), (-1, -1), 4), ("BOTTOMPADDING", (0, 1), (-1, -1), 4)]))
    f.append(t)
    f.append(PageBreak())
    return f


# ------------------------------------------------------------------ hoofstuk
def answer_line(open_q):
    return Lines(2 if open_q else 1)


def render_exercise(label, ex):
    f = [Paragraph(f"<b>{label}</b> {ex['title']}", ParagraphStyle("et", parent=body, fontName="F-B", fontSize=13, leading=19, textColor=PURPLE, spaceBefore=4, spaceAfter=3))]
    if ex.get("bank"):
        f.append(box(Paragraph("  ·  ".join(f"<b>{w}</b>" for w in ex["bank"]), ParagraphStyle("bk", parent=center, fontSize=13)), bg=LBLUE, border=BLUE, pad=6))
        f.append(Spacer(1, 4))
    mode = ex["mode"]
    for n, (txt, _a) in enumerate(ex["items"], 1):
        if mode == "word":
            f.append(Paragraph(f"{n}. &nbsp;{txt} &nbsp;<font color='#8888AA'>→ ____________________</font>", ex_st))
        elif mode == "blank":
            f.append(Paragraph(f"{n}. &nbsp;{txt}", ex_st))
        elif mode == "line":
            f.append(KeepTogether([Paragraph(f"{n}. &nbsp;{txt}", ex_st), Lines(1, gap=0.95 * cm), Spacer(1, 2)]))
        else:
            f.append(Paragraph(txt, ex_st))
    return f


def chapter(i, ch):
    f = []
    lab = f"VLAK {i}  ·  {ch['title']}"
    # --- 1: storie
    f.append(SetState(lab, "1  Land: Lees"))
    f.append(banner(i, ch["title"], f"Taalsleutel: {ch['key']}"))
    f.append(Spacer(1, 12))
    f.append(section_title("▶", "1. LAND: Lees die storie (hardop!)"))
    parts = [Paragraph(p, story_st) for p in ch["story"]]
    f.append(box(parts, bg=colors.white, border=PURPLE, pad=12))
    f.append(Spacer(1, 12))
    rows = [[Paragraph(f"<b>{w}</b>", ParagraphStyle("v", parent=body, textColor=PURPLE, fontSize=12.5)),
             Paragraph(m, ParagraphStyle("vm", parent=body, fontSize=12))] for w, m in ch["vocab"]]
    vt = Table(rows, colWidths=[3.6 * cm, AW - 3.6 * cm - 24])
    vt.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    f.append(box([Paragraph("<b>Nuwe woorde</b>", ParagraphStyle("nw", parent=body, textColor=colors.HexColor("#8A6500"))), Spacer(1, 3), vt]))
    f.append(Spacer(1, 10))
    f.append(Paragraph("Lees die storie nog 'n keer. Onderstreep een woord wat jy nie goed ken nie.", small))
    f.append(Spacer(1, 8))
    dt = Table([[""]], colWidths=[AW], rowHeights=[3.8 * cm if len(ch["story"]) < 4 else 1.6 * cm])
    dt.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1.5, BLUE), ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                            ("ROUNDEDCORNERS", [8, 8, 8, 8])]))
    f.append(Paragraph("<b>Teken die spannendste deel van die storie:</b>", ParagraphStyle("dr", parent=body, textColor=BLUE, fontSize=12)))
    f.append(Spacer(1, 3))
    f.append(dt)
    f.append(PageBreak())

    # --- 2: vrae
    f.append(SetState(lab, "2  Loot: Vrae"))
    f.append(section_title("◆", "2. LOOT: Wat onthou jy?"))
    f.append(Paragraph("Skryf jou antwoord in 'n volsin op die lyn.", small))
    f.append(Spacer(1, 4))
    for n, (q, a, op) in enumerate(ch["questions"], 1):
        f.append(KeepTogether([Paragraph(f"{n}. {q}", q_st), answer_line(op), Spacer(1, 9)]))
    f.append(Spacer(1, 4))
    f.append(Paragraph("<b>Waar of vals?</b> Sit 'n regmerkie (✓) by die regte antwoord.", ParagraphStyle("tf", parent=body, textColor=PURPLE)))
    rows = [[Paragraph(f"{n}. {s}", body), "☐ Waar", "☐ Vals"] for n, (s, _v) in enumerate(ch["tf"], 1)]
    t = Table(rows, colWidths=[AW - 6 * cm, 3 * cm, 3 * cm])
    t.setStyle(TableStyle([("FONTNAME", (1, 0), (-1, -1), "F"), ("FONTSIZE", (1, 0), (-1, -1), 13),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LINEBELOW", (0, 0), (-1, -1), 0.5, GREY),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    f.append(t)
    f.append(PageBreak())

    # --- 3: taalkuns
    f.append(SetState(lab, "3  Bou: Taalkuns"))
    f.append(section_title("■", f"3. BOU: Taalkuns · {ch['key']}"))
    f.append(box(Paragraph("<b>Onthou!</b><br/>" + ch["explain"], body), bg=LYELLOW, border=YELLOW))
    f.append(Spacer(1, 8))
    f += render_exercise("A.", ch["exA"])
    f.append(Spacer(1, 8))
    f += render_exercise("B.", ch["exB"])
    f.append(PageBreak())

    # --- 4: spelling
    f.append(SetState(lab, "4  Spel: Spelwoorde"))
    f.append(section_title("✎", "4. SPEL: Spelwoorde van hierdie vlak"))
    f.append(box(Paragraph("<b>Bedek, skryf, kyk!</b> 1) Lees die woord. 2) Bedek dit met jou hand. 3) Skryf dit twee keer. 4) Kyk of jy reg is.", small),
                 bg=LBLUE, border=BLUE, pad=7))
    f.append(Spacer(1, 8))
    rows = [[Paragraph(f"<b>{w}</b>", ParagraphStyle("sw", parent=body, fontSize=15, textColor=PURPLE)), "", "", ""] for w in ch["spell"]]
    t = Table(rows, colWidths=[4.2 * cm, 4.5 * cm, 4.5 * cm, 1.8 * cm], rowHeights=[1.5 * cm] * len(rows))
    t.setStyle(TableStyle([("LINEBELOW", (1, 0), (2, -1), 0.8, GREY), ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                           ("LEFTPADDING", (1, 0), (2, -1), 6)]))
    f.append(t)
    f.append(Spacer(1, 10))
    f.append(Paragraph("<b>Maak 'n sin met twee van die spelwoorde:</b>", ParagraphStyle("ms", parent=body, textColor=PURPLE)))
    f.append(Lines(3, gap=1.2 * cm))
    f.append(Spacer(1, 10))
    f.append(Paragraph("<b>Wie is die Spelkoning?</b> Vra iemand om al 8 woorde vir jou voor te lees. Hoeveel het jy reg? ____ / 8", body))
    f.append(PageBreak())

    # --- 5: skryf
    f.append(SetState(lab, "5  Wen: Skryf"))
    f.append(section_title("★", "5. WEN: Skryf-tyd!"))
    f.append(box(Paragraph("<b>Opdrag:</b> " + ch["writing"], ParagraphStyle("wr", parent=body, fontSize=13.5, leading=21)), bg=LPURPLE, border=PURPLE))
    f.append(Spacer(1, 6))
    if ch.get("long_writing"):
        f.append(Paragraph("<b>Titel:</b> ______________________________________________", body))
        f.append(Spacer(1, 4))
        f.append(Lines(17, gap=1.2 * cm))
    else:
        f.append(Lines(15, gap=1.2 * cm))
    f.append(Spacer(1, 8))
    f.append(box(Paragraph(
        "<b>Kyk jou werk na:</b> &nbsp; ☐ Hoofletter aan die begin &nbsp; ☐ Leesteken aan die einde &nbsp; "
        "☐ Spelling gekyk &nbsp; ☐ Dit maak sin", small), bg=LGREEN, border=GREEN, pad=7))
    f.append(PageBreak())
    return f


# ------------------------------------------------------------------ woordsoek
def make_grid(words, size=12, seed=1):
    rnd = random.Random(seed)
    dirs = [(0, 1), (1, 0), (1, 1)]
    for attempt in range(500):
        grid = [[""] * size for _ in range(size)]
        placed = {}
        ok = True
        for w in sorted(words, key=len, reverse=True):
            done = False
            for _ in range(300):
                dr, dc = rnd.choice(dirs)
                r = rnd.randrange(size - (len(w) - 1) * dr)
                c = rnd.randrange(size - (len(w) - 1) * dc)
                cells = [(r + k * dr, c + k * dc) for k in range(len(w))]
                if all(grid[a][b] in ("", w[k]) for k, (a, b) in enumerate(cells)):
                    for k, (a, b) in enumerate(cells):
                        grid[a][b] = w[k]
                    placed[w] = (r + 1, c + 1, {(0, 1): "→", (1, 0): "↓", (1, 1): "↘"}[(dr, dc)])
                    done = True
                    break
            if not done:
                ok = False
                break
        if ok:
            for a in range(size):
                for b in range(size):
                    if not grid[a][b]:
                        grid[a][b] = rnd.choice("ABDEGHIKLMNOPRSTUVW")
            return grid, placed
    raise RuntimeError("woordsoek misluk")


WS_KEYS = {}


def wordsearch_page(idx, after, title, words):
    grid, placed = make_grid(words, seed=idx + 3)
    WS_KEYS[title] = placed
    f = [SetState(title, "Speletjie"), Paragraph(title, h1),
         Paragraph("Vind al 10 woorde. Hulle loop <b>van links na regs →</b>, <b>van bo na onder ↓</b> of <b>skuins ↘</b>. "
                   "Trek 'n sirkel om elkeen en kruis dit dan af op die lys.", body), Spacer(1, 10)]
    cs = 1.18 * cm
    t = Table(grid, colWidths=[cs] * 12, rowHeights=[cs] * 12)
    t.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, -1), "F-B"), ("FONTSIZE", (0, 0), (-1, -1), 15),
                           ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("BOX", (0, 0), (-1, -1), 2, PURPLE), ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#DDD6EE")),
                           ("TEXTCOLOR", (0, 0), (-1, -1), DARK), ("BACKGROUND", (0, 0), (-1, -1), colors.white)]))
    f.append(t)
    f.append(Spacer(1, 12))
    ws = sorted(words)
    rows = [[f"☐ {a}", f"☐ {b}"] for a, b in zip(ws[:5], ws[5:])]
    wt = Table(rows, colWidths=[AW / 2] * 2)
    wt.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, -1), "F-B"), ("FONTSIZE", (0, 0), (-1, -1), 13),
                            ("TEXTCOLOR", (0, 0), (-1, -1), PURPLE), ("TOPPADDING", (0, 0), (-1, -1), 4),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    f.append(box(wt, bg=LYELLOW, border=YELLOW, pad=6))
    f.append(Spacer(1, 6))
    f.append(Paragraph(f"Bonus: Skryf 'n sin met elkeen van 2 woorde in jou skryfboek!", small))
    f.append(PageBreak())
    return f


def test_page(after, title, qs, dikt):
    f = [SetState(title, "Toets"), Paragraph(title, h1),
         Paragraph("Kyk hoe baie jy onthou het. Doen dit sonder om terug te blaai. Daarna kan jy jou antwoorde nasien.", body), Spacer(1, 8)]
    for n, (q, opts, a) in enumerate(qs, 1):
        blk = [Paragraph(f"{n}. {q}", q_st)]
        if opts:
            blk.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;" + "&nbsp;&nbsp;&nbsp;&nbsp;".join(f"☐ {o}" for o in opts), ParagraphStyle("o", parent=body, fontSize=12.5, leading=22)))
        else:
            blk.append(Lines(2, gap=0.95 * cm))
        blk.append(Spacer(1, 5))
        f.append(KeepTogether(blk))
    f.append(Spacer(1, 4))
    f.append(KeepTogether([
        Paragraph("<b>Dikteetyd!</b> Iemand lees die woorde een vir een vir jou voor. Skryf hulle neer.", ParagraphStyle("d", parent=body, textColor=PURPLE)),
        Table([[f"{k}.", ""] for k in range(1, 6)], colWidths=[1 * cm, AW - 1 * cm], rowHeights=[0.95 * cm] * 5,
              style=TableStyle([("LINEBELOW", (1, 0), (1, -1), 0.8, GREY), ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                                ("FONTNAME", (0, 0), (-1, -1), "F"), ("FONTSIZE", (0, 0), (-1, -1), 12)])),
        Spacer(1, 6),
        Paragraph("Jou telling: ____ / 6 vrae &nbsp;&nbsp;&nbsp; ____ / 5 woorde", body)]))
    f.append(PageBreak())
    return f


def certificate():
    f = [SetState("Sertifikaat", ""), Spacer(1, 1.5 * cm)]
    inner = [Paragraph('<font color="#FFC93C" size="15"><b>★ ★ ★ ★ ★</b></font>', center), Spacer(1, 10),
             Paragraph('<font size="30" color="#2E1065"><b>SERTIFIKAAT</b></font>', ParagraphStyle("c1", parent=center, leading=38)), Spacer(1, 4),
             Paragraph('<font size="14" color="#5B2A9E">van Afrikaans-Kampioen</font>', ParagraphStyle("c2", parent=center, leading=20)), Spacer(1, 26),
             Paragraph("Hiermee word bevestig dat", center), Spacer(1, 14),
             Paragraph('<font size="40" color="#5B2A9E"><b>DANIEL</b></font>', ParagraphStyle("c3", parent=center, leading=48)), Spacer(1, 18),
             Paragraph("al 12 vlakke van <b>Daniel se Afrikaans Avontuur</b> voltooi het,<br/>"
                       "baie nuwe woorde geleer het en 'n beter leser en skrywer geword het.", ParagraphStyle("cc", parent=center, fontSize=14, leading=24)),
             Spacer(1, 22), Paragraph('<font size="22" color="#E0A800"><b>OORWINNING!</b></font>', ParagraphStyle("c4", parent=center, leading=28)), Spacer(1, 40),
             Table([["Datum: ______________", "Handtekening: ______________"]], colWidths=[AW / 2 - 20] * 2,
                   style=TableStyle([("FONTNAME", (0, 0), (-1, -1), "F"), ("FONTSIZE", (0, 0), (-1, -1), 11), ("ALIGN", (0, 0), (-1, -1), "CENTER")])),
             Spacer(1, 12)]
    t = Table([[inner]], colWidths=[AW])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 5, PURPLE), ("BACKGROUND", (0, 0), (-1, -1), LYELLOW),
                           ("TOPPADDING", (0, 0), (-1, -1), 30), ("BOTTOMPADDING", (0, 0), (-1, -1), 30),
                           ("LEFTPADDING", (0, 0), (-1, -1), 20), ("RIGHTPADDING", (0, 0), (-1, -1), 20)]))
    f.append(t)
    f.append(PageBreak())
    return f


# ------------------------------------------------------------------ antwoorde
def answers():
    f = [SetState("Antwoorde (vir ouers)", ""), Paragraph("Antwoorde", h1),
         Paragraph("Oop vrae en skryfopdragte: enige goeie, volledige antwoord is reg. Moenie Daniel hierdie bladsye laat sien voor hy klaar is nie!", body), Spacer(1, 6)]
    for i, ch in enumerate(CHAPTERS, 1):
        blk = [Paragraph(f"Vlak {i} · {ch['title']}", ans_h)]
        qa = " &nbsp;|&nbsp; ".join(f"<b>{n}.</b> {a}" for n, (q, a, o) in enumerate(ch["questions"], 1))
        blk.append(Paragraph("<b>Vrae:</b> " + qa, ans_st))
        tf = ", ".join(f"{n}. {'Waar' if v else 'Vals'}" for n, (s, v) in enumerate(ch["tf"], 1))
        blk.append(Paragraph("<b>Waar/Vals:</b> " + tf, ans_st))
        for lab, ex in (("A", ch["exA"]), ("B", ch["exB"])):
            if ex["mode"] == "none":
                ans = ex["items"][-1][1]
                blk.append(Paragraph(f"<b>{lab}:</b> {ans}", ans_st))
            else:
                ans = " &nbsp;|&nbsp; ".join(f"<b>{n}.</b> {a}" for n, (t, a) in enumerate(ex["items"], 1))
                blk.append(Paragraph(f"<b>{lab}:</b> {ans}", ans_st))
        f.append(KeepTogether(blk))
    f.append(Paragraph("Toetse", ans_h))
    for after, title, qs, dikt in TESTS:
        txt = " &nbsp;|&nbsp; ".join(f"<b>{n}.</b> {a}" for n, (q, o, a) in enumerate(qs, 1))
        f.append(KeepTogether([Paragraph(f"<b>{title}</b>", ans_st), Paragraph(txt, ans_st),
                               Paragraph("Dikteewoorde: " + ", ".join(dikt), ans_st), Spacer(1, 4)]))
    f.append(Paragraph("Woordsoeke (rystaat: <b>(ry, kolom, rigting)</b>, getel van links bo)", ans_h))
    for title, placed in WS_KEYS.items():
        txt = "; ".join(f"{w} ({r},{c},{d})" for w, (r, c, d) in sorted(placed.items()))
        f.append(Paragraph(f"<b>{title}:</b> {txt}", ans_st))
        f.append(Spacer(1, 3))
    return f


# ------------------------------------------------------------------ bou
def build(path):
    doc = BaseDocTemplate(path, pagesize=A4, title="Daniel se Afrikaans Avontuur",
                          author="Gemaak vir Daniel", leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=M)
    main = Frame(M, 1.5 * cm, AW, H - 1.5 * cm - 1.9 * cm, id="main", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    cover = Frame(M, M, AW, H - 2 * M, id="cover")
    doc.addPageTemplates([PageTemplate("cover", [cover], onPage=draw_cover),
                          PageTemplate("main", [main], onPageEnd=page_end)])
    flow = front_matter()
    ws_by_after = {a: (t, w) for a, t, w in WORDSEARCH}
    test_by_after = {a: (t, q, d) for a, t, q, d in TESTS}
    for i, ch in enumerate(CHAPTERS, 1):
        flow += chapter(i, ch)
        if i in ws_by_after:
            t, w = ws_by_after[i]
            flow += wordsearch_page(i, i, t, w)
        if i in test_by_after:
            t, q, d = test_by_after[i]
            flow += test_page(i, t, q, d)
    flow += certificate()
    flow += answers()
    doc.build(flow)


if __name__ == "__main__":
    build("Daniel_se_Afrikaans_Avontuur.pdf")
    print("klaar")
