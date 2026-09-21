#!/usr/bin/env python3
"""Génère les visuels du profil GitHub d'Axel (design du portfolio : Google Sans,
bleu #2563eb / vert #059669 / ciel #38bdf8, grille, halos, cartes vitrées).

    python scripts/build.py              # SVG (clair + sombre, EN + FR) + aperçus sociaux PNG
    python scripts/build.py --readme     # idem + regénère README.md et README.fr.md

Le texte est converti en tracés vectoriels : le rendu est identique partout,
même si Google Sans n'est pas installé chez le visiteur.
"""
import argparse
import io
import json
import re
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

import content as C

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
LOGOS = json.loads((ROOT / "logos.json").read_text(encoding="utf-8"))
LANGS = ("en", "fr")
FORCE_ACTIVITY = False


# ── Polices → tracés ────────────────────────────────────────────────────────
def _n(v):
    s = f"{v:.1f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class Face:
    def __init__(self, filename):
        self.key = filename[:22]
        tt = TTFont(ROOT / "fonts" / filename)
        self.gs, self.order = tt.getGlyphSet(), tt.getGlyphOrder()
        self.upem = tt["head"].unitsPerEm
        buf = io.BytesIO()
        tt.flavor = None
        tt.save(buf)
        self.hbfont = hb.Font(hb.Face(hb.Blob(buf.getvalue())))

    def layout(self, text, size, tracking=0.0):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, {"kern": True, "liga": True})
        s, x, parts = size / self.upem, 0.0, []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            pen = SVGPathPen(self.gs, ntos=_n)
            self.gs[self.order[info.codepoint]].draw(
                TransformPen(pen, (s, 0, 0, -s, x + pos.x_offset * s, -pos.y_offset * s)))
            if pen.getCommands():
                parts.append(pen.getCommands())
            x += pos.x_advance * s + tracking
        return " ".join(parts), max(x - tracking, 0.0)

    def glyphs(self, text, size, tracking=0.0):
        """[(clé, x, d)] : un tracé par glyphe, dessiné à l'origine, + largeur totale."""
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, {"kern": True, "liga": True})
        s, x, out = size / self.upem, 0.0, []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            pen = SVGPathPen(self.gs, ntos=_n)
            name = self.order[info.codepoint]
            self.gs[name].draw(TransformPen(pen, (s, 0, 0, -s, 0, -pos.y_offset * s)))
            if pen.getCommands():
                out.append(((self.key, name, round(size, 2), round(pos.y_offset * s, 1)), x + pos.x_offset * s, pen.getCommands()))
            x += pos.x_advance * s + tracking
        return out, max(x - tracking, 0.0)

    def width(self, text, size, tracking=0.0):
        return self.layout(text, size, tracking)[1]


SANS4 = Face("google-sans-latin-400-normal.woff2")
SANS5 = Face("google-sans-latin-500-normal.woff2")
SANS7 = Face("google-sans-latin-700-normal.woff2")
MONO5 = Face("google-sans-code-latin-500-normal.woff2")
MONO6 = Face("google-sans-code-latin-600-normal.woff2")


_REG = {}  # clé de glyphe -> (id, d) pour le document en cours de construction


def T(x, y, s, face, size, fill, anchor="start", tracking=0.0, opacity=None):
    """Texte vectorisé, ancré sur sa ligne de base. Les glyphes sont dédupliqués via <use>."""
    op = f' fill-opacity="{opacity}"' if opacity is not None else ""
    if fill.startswith("url("):  # dégradé : un seul tracé pour garder un dégradé continu
        d, w = face.layout(s, size, tracking)
        x -= {"start": 0, "middle": w / 2, "end": w}[anchor]
        return f'<path transform="translate({x:.2f} {y:.2f})" d="{d}" fill="{fill}"{op}/>'
    glyphs, w = face.glyphs(s, size, tracking)
    x -= {"start": 0, "middle": w / 2, "end": w}[anchor]
    uses = []
    for key, gx, d in glyphs:
        gid = _REG.setdefault(key, (f"g{len(_REG)}", d))[0]
        uses.append(f'<use href="#{gid}" x="{gx:.1f}"/>')
    return f'<g transform="translate({x:.2f} {y:.2f})" fill="{fill}"{op}>{"".join(uses)}</g>'


def wrap(text, face, size, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and face.width(trial, size) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + ([cur] if cur else [])


def fit(text, face, max_size, max_w):
    return min(max_size, max_size * max_w / face.width(text, max_size))


def L(v, lang):
    """Valeur simple ou dict {en, fr}."""
    return v[lang] if isinstance(v, dict) else v


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ── Thèmes (tokens du portfolio : index-*.css) ─────────────────────────────
THEMES = {
    "light": dict(bg="#F0F4FF", card="#FFFFFF", text="#0F172A", muted="#475569",
                  bord="#2563EB", bord_op=0.16, blue="#2563EB", blue_t="#2563EB",
                  green="#059669", green_t="#047857", sky="#38BDF8", sky_t="#0369A1",
                  violet="#8B5CF6", tint=0.09, glow_b=0.16, glow_v=0.12, grid_op=0.12),
    "dark": dict(bg="#070B14", card="#0D1526", text="#F0F4FF", muted="#7B8AAB",
                 bord="#FFFFFF", bord_op=0.10, blue="#2563EB", blue_t="#60A5FA",
                 green="#10B981", green_t="#34D399", sky="#38BDF8", sky_t="#7DD3FC",
                 violet="#8B5CF6", tint=0.14, glow_b=0.24, glow_v=0.16, grid_op=0.07),
}
TERM_BG, TERM_TXT, TERM_VAL, TERM_PROMPT = "#0B1220", "#E2E8F0", "#7DD3FC", "#34D399"


def lum(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def svg(w, h, body, title, defs="", desc=""):
    d = f"<desc>{esc(desc)}</desc>" if desc else ""
    defs += "".join(f'<path id="{gid}" d="{gd}"/>' for gid, gd in _REG.values())
    _REG.clear()
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>{d}<defs>{defs}</defs>{body}</svg>\n')


def glass(x, y, w, h, r, th, dashed=False, fill=None):
    dash = ' stroke-dasharray="6 5"' if dashed else ""
    return (f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="{r}" '
            f'fill="{fill or th["card"]}" stroke="{th["bord"]}" stroke-opacity="{th["bord_op"] * (2 if dashed else 1.4):.2f}"{dash}/>')


def tint(color, th, op=None):
    return f'fill="{color}" fill-opacity="{op if op is not None else th["tint"]}"'


def gradient(th, gid="g"):
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0" stop-color="{th["blue"] if th["bg"] == "#F0F4FF" else "#3B82F6"}"/>'
            f'<stop offset=".5" stop-color="{th["sky"]}"/><stop offset="1" stop-color="{th["green"]}"/></linearGradient>')


# ── Logos ───────────────────────────────────────────────────────────────────
def logo(key, x, y, size, th, bg=None):
    bg = bg or th["card"]
    L = LOGOS[key]
    hexc = L.get("hex")
    if L["kind"] == "si":
        col = hexc if contrast(hexc, bg) >= 2.4 else th["text"]
        inner = f'<g fill="{col}">{L["inner"]}</g>'
    else:
        inner = L["inner"]
        if hexc and "fill=" not in inner:
            inner = f'<g fill="{hexc if contrast(hexc, bg) >= 2.4 else th["text"]}">{inner}</g>'
        else:
            def fix(m):
                c = m.group(1)
                return m.group(0) if contrast(c if len(c) > 4 else "#" + "".join(ch * 2 for ch in c[1:]), bg) >= 2.0 \
                    else f'fill="{th["text"]}"'
            inner = re.sub(r'fill="(#[0-9a-fA-F]{3,6})"', fix, inner)
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{L["vb"]}">{inner}</svg>'


def stroke_icon(name, x, y, size, color, sw=1.8):
    paths = {
        "shield": '<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><path d="M9 12l2 2 4-4"/>',
        "cloud": '<path d="M7 18a4 4 0 0 1-.5-7.97A6 6 0 0 1 18 9a4.5 4.5 0 0 1-.5 9H7z"/>',
        "code": '<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M14 5l-4 14"/>',
        "lifebuoy": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.6"/>'
                    '<path d="M5.6 5.6l3.9 3.9M14.5 14.5l3.9 3.9M18.4 5.6l-3.9 3.9M9.5 14.5l-3.9 3.9"/>',
        "globe": '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>',
        "mail": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3.5 7.5l8.5 6 8.5-6"/>',
        "wifi": '<path d="M2 9a15 15 0 0 1 20 0M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0M12 19.5h.01"/>',
        "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
        "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
        "cap": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11.5V16c0 1.5 3 3 6 3s6-1.5 6-3v-4.5"/>',
        "award": '<circle cx="12" cy="9" r="6"/><path d="M8.5 14L7 22l5-3 5 3-1.5-8"/>',
        "building": '<path d="M4 21V5l8-2 8 2v16M3 21h18M9 9h.01M9 13h.01M15 9h.01M15 13h.01M10 21v-4h4v4"/>',
        "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
        "trophy": '<path d="M8 4h8v5a4 4 0 0 1-8 0zM8 6H4v1a4 4 0 0 0 4 4M16 6h4v1a4 4 0 0 1-4 4M12 13v4M8 21h8M10 17h4"/>',
        "layers": '<path d="M12 3l9 5-9 5-9-5zM3 13l9 5 9-5"/>',
    }
    return (f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{paths[name]}</svg>')


def monogram(x, y, s):
    k = s / 100
    a, tn = SANS7.width("A", 44 * k, -2 * k), SANS7.width("TN", 44 * k, -2 * k)
    x0 = x + 50 * k - (a + tn - 2 * k) / 2
    return (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{24 * k:.1f}" fill="#0F172A"/>'
            + T(x0, y + 62 * k, "A", SANS7, 44 * k, "#FFFFFF", tracking=-2 * k)
            + T(x0 + a - 2 * k, y + 62 * k, "TN", SANS7, 44 * k, "#3B82F6", tracking=-2 * k)
            + f'<path d="M{x + 35 * k:.1f} {y + 75 * k:.1f}H{x + 65 * k:.1f}" stroke="#3B82F6" stroke-width="{4 * k:.1f}" stroke-linecap="round"/>')


def backdrop(w, h, th, radius, grid=44, glow_scale=1.0):
    """Fond du portfolio : grille masquée en dégradé + halos bleu / violet."""
    defs = (f'<clipPath id="clip"><rect width="{w}" height="{h}" rx="{radius}"/></clipPath>'
            f'<pattern id="grid" width="{grid}" height="{grid}" patternUnits="userSpaceOnUse">'
            f'<path d="M{grid} 0H0V{grid}" fill="none" stroke="{th["bord"]}" stroke-opacity="{th["grid_op"]}"/></pattern>'
            '<radialGradient id="fade" cx=".5" cy="0" r=".85"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>'
            '<mask id="gm"><rect width="100%" height="100%" fill="url(#fade)"/></mask>'
            f'<radialGradient id="gb"><stop offset="0" stop-color="{th["blue"]}" stop-opacity="{th["glow_b"]}"/><stop offset="1" stop-color="{th["blue"]}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="gv"><stop offset="0" stop-color="{th["violet"]}" stop-opacity="{th["glow_v"]}"/><stop offset="1" stop-color="{th["violet"]}" stop-opacity="0"/></radialGradient>')
    body = (f'<g clip-path="url(#clip)"><rect width="{w}" height="{h}" fill="{th["bg"]}"/>'
            f'<rect width="{w}" height="{h}" fill="url(#grid)" mask="url(#gm)"/>'
            f'<circle cx="{w * .15}" cy="{h * .2}" r="{420 * glow_scale}" fill="url(#gb)"/>'
            f'<circle cx="{w * .88}" cy="{h * .85}" r="{380 * glow_scale}" fill="url(#gv)"/></g>'
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{radius}" fill="none" stroke="{th["bord"]}" stroke-opacity="{th["bord_op"] * 1.4:.2f}"/>')
    return defs, body


# ── Visuels ─────────────────────────────────────────────────────────────────
def banner(th, lang):
    W, H = 1000, 352
    defs, body = backdrop(W, H, th, 28)
    defs += gradient(th)
    B = C.BANNER
    out = [body, monogram(56, 48, 52)]
    # pastille de statut
    pill = B["pill"][lang]
    pw = MONO6.width(pill, 11.5, 1.6) + 46
    out.append(glass(120, 54, pw, 32, 16, th))
    out.append(f'<circle cx="138" cy="70" r="4" fill="{th["green"]}"/>')
    out.append(T(150, 74.2, pill, MONO6, 11.5, th["muted"], tracking=1.6))
    # nom
    size = fit("Axel Renaud", SANS7, 72, 500)
    out.append(T(54, 176, "Axel Renaud", SANS7, size, th["text"], tracking=-1.5))
    out.append(T(54, 176 + size * .97, "Tadjounteu", SANS7, size, "url(#g)", tracking=-1.5))
    out.append(T(56, 282, B["tagline"][lang], SANS5, 21, th["text"], opacity=.86))
    out.append(T(56, 310, B["line1"][lang], MONO5, 12, th["muted"]))
    out.append(T(56, 329, B["line2"][lang], MONO5, 12, th["muted"]))
    # terminal
    tx, ty, tw, tH = 618, 48, 326, 262
    out.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{tH}" rx="20" fill="{TERM_BG}" stroke="#FFFFFF" stroke-opacity=".10"/>')
    for i, c in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        out.append(f'<circle cx="{tx + 26 + i * 18}" cy="{ty + 24}" r="5" fill="{c}"/>')
    out.append(T(tx + tw - 22, ty + 28, "atn@douala ~", MONO5, 11, "#7B8AAB", anchor="end"))
    y = ty + 72
    for cmd, val in B["term"]:
        out.append(T(tx + 26, y, "$", MONO6, 14, TERM_PROMPT))
        out.append(T(tx + 44, y, cmd, MONO6, 14, TERM_TXT))
        out.append(T(tx + 44, y + 21, val[lang], MONO5, 13.5, TERM_VAL))
        y += 52
    lastw = MONO5.width(B["term"][-1][1][lang], 13.5)
    out.append(f'<rect x="{tx + 44 + lastw + 6:.1f}" y="{y - 52 + 21 - 11:.1f}" width="8" height="14" fill="{TERM_PROMPT}" fill-opacity=".9"/>')
    title = f'Axel Renaud Tadjounteu. {B["tagline"][lang]}. {B["pill"][lang].title()}'
    return svg(W, H, "".join(out), title, defs)


def header(th, num, title, caption):
    W, H = 1000, 64
    out = [glass(0, 0, W, H, 20, th),
           f'<rect x="16" y="16" width="46" height="32" rx="10" {tint(th["blue_t"], th, th["tint"] + .04)}/>',
           T(39, 37, f"{num:02d}", MONO6, 13.5, th["blue_t"], anchor="middle", tracking=1),
           T(80, 41.5, title, SANS7, 24, th["text"], tracking=-.3),
           T(W - 24, 37, caption, MONO5, 12.5, th["muted"], anchor="end")]
    return svg(W, H, "".join(out), title)


def toolbox(th, key, lang):
    cfg = C.TOOLBOX[key]
    tiles, per_row, tw, th_, gap = cfg["tools"], 8, 112, 104, 12
    rows = -(-len(tiles) // per_row)
    W = 1000
    H = 34 + rows * (th_ + gap) - gap + (44 if cfg.get("chips") else 0)
    out = [T(6, 14, cfg["label"][lang], MONO6, 11.5, th["muted"], tracking=2.2)]
    x0 = (W - (min(len(tiles), per_row) * tw + (min(len(tiles), per_row) - 1) * gap)) / 2 if False else 0
    for i, (lk, label) in enumerate(tiles):
        r, c = divmod(i, per_row)
        x, y = c * (tw + gap) + x0 + 10, 34 + r * (th_ + gap)
        out.append(glass(x, y, tw, th_, 20, th))
        out.append(logo(lk, x + tw / 2 - 20, y + 20, 40, th))
        out.append(T(x + tw / 2, y + 84, label, SANS5, fit(label, SANS5, 12.5, tw - 16), th["text"], anchor="middle"))
    if cfg.get("chips"):
        txt = cfg["chips"][lang]
        w = MONO5.width(txt, 11.5, .6) + 32
        y = 34 + rows * (th_ + gap) - gap + 14
        out.append(f'<rect x="10" y="{y}" width="{w:.1f}" height="30" rx="15" {tint(th["blue_t"], th)} stroke="{th["blue_t"]}" stroke-opacity=".25"/>')
        out.append(T(26, y + 19.5, txt, MONO5, 11.5, th["blue_t"], tracking=.6))
    return svg(W, H, "".join(out), cfg["label"][lang].title() + ": " + ", ".join(l for _, l in tiles))


def status_style(status, th):
    return {"done": (th["green"], th["green_t"]), "progress": (th["blue"], th["blue_t"]),
            "prep": (th["sky"], th["sky_t"]), "planned": (th["muted"], th["muted"]),
            "company": (th["blue"], th["blue_t"]), "live": (th["green"], th["green_t"]),
            "design": (th["sky"], th["sky_t"]), "pitched": (th["violet"], th["violet"] if th["bg"] != "#F0F4FF" else "#6D28D9"),
            "hack": (th["green"], th["green_t"])}[status]


def cert_card(th, c, lang):
    n = len(C.CERTS)
    W, H = (1000 - 20 * (n - 1)) / n, 206
    planned = c["status"] == "planned"
    out = [glass(0, 0, W, H, 22, th, dashed=planned), logo(c["logo"], 16, 16, 30, th),
           T(54, 36, c["vendor"], MONO6, 10.5, th["muted"], tracking=1)]
    titles = L(c["title"], lang)
    size = min(17, *(fit(l, SANS7, 17, W - 32) for l in titles))
    for j, line in enumerate(titles):
        out.append(T(16, 86 + j * (size + 6), line, SANS7, size, th["text"], tracking=-.2))
    out.append(T(16, 150, L(c["code"], lang), MONO5, 11, th["muted"], tracking=.8))
    col, txt_col = status_style(c["status"], th)
    label = C.STATUS_TEXT[c.get("done_key", c["status"])][lang]
    pw = MONO6.width(label, 10.5, 1.1) + 40
    fill = 'fill="none"' if planned else tint(col, th, .14 if th["bg"] != "#F0F4FF" else .12)
    dash = ' stroke-dasharray="4 4" stroke-opacity=".6"' if planned else ' stroke-opacity=".35"'
    out.append(f'<rect x="16" y="{H - 44}" width="{pw:.1f}" height="26" rx="13" {fill} stroke="{col}"{dash}/>')
    out.append(f'<circle cx="30" cy="{H - 31}" r="3.5" fill="{col}"/>')
    out.append(T(40, H - 27.3, label, MONO6, 10.5, txt_col, tracking=1.1))
    return svg(W, H, "".join(out), f'{" ".join(titles)} ({label.lower()})')


def project(th, p, lang):
    W, H = 490, 196
    out = [glass(0, 0, W, H, 24, th)]
    out.append(T(28, 46, p["title"], SANS7, 23, th["text"], tracking=-.3))
    col, txt_col = status_style(p["status"], th)
    label = C.PROJECT_STATUS[p["status"]][lang]
    cw = MONO6.width(label, 10.5, 1.1) + 34
    out.append(f'<rect x="{W - 28 - cw:.1f}" y="26" width="{cw:.1f}" height="26" rx="13" {tint(col, th, .14)} stroke="{col}" stroke-opacity=".35"/>')
    out.append(f'<circle cx="{W - 28 - cw + 14:.1f}" cy="39" r="3.5" fill="{col}"/>')
    out.append(T(W - 28 - cw + 24, 42.7, label, MONO6, 10.5, txt_col, tracking=1.1))
    for i, line in enumerate(wrap(p["desc"][lang], SANS4, 14.5, W - 56)[:4]):
        out.append(T(28, 82 + i * 21, line, SANS4, 14.5, th["muted"]))
    x = 28
    for tag in L(p["tags"], lang):
        w = MONO5.width(tag, 11, .3) + 22
        if x + w > W - 28:
            break
        out.append(f'<rect x="{x:.1f}" y="{H - 46}" width="{w:.1f}" height="26" rx="13" {tint(th["blue_t"], th, th["tint"] * .8)}/>')
        out.append(T(x + 11, H - 28.5, tag, MONO5, 11, th["blue_t"], tracking=.3))
        x += w + 8
    return svg(W, H, "".join(out), f'{p["title"]} ({label.lower()}): {p["desc"][lang]}')


def services(th, lang):
    W, H, gap = 1000, 124, 24
    cw = (W - gap * 3) / 4
    out = []
    for i, (icon, name) in enumerate(C.SERVICES):
        x = i * (cw + gap)
        out.append(glass(x, 0, cw, H, 22, th))
        out.append(f'<rect x="{x + 20}" y="20" width="46" height="46" rx="14" {tint(th["blue_t"], th, th["tint"] + .03)}/>')
        out.append(stroke_icon(icon, x + 31, 31, 24, th["blue_t"]))
        out.append(T(x + cw - 20, 40, f"{i + 1:02d}", MONO6, 12, th["muted"], anchor="end", tracking=1))
        out.append(T(x + 20, 100, name[lang], SANS7, fit(name[lang], SANS7, 19, cw - 40), th["text"], tracking=-.2))
    return svg(W, H, "".join(out), "Atnyx: " + ", ".join(n[lang] for _, n in C.SERVICES))


def principles(th, lang):
    W, H, gap = 1000, 176, 20
    cw = (W - gap * 3) / 4
    out = []
    for i, (icon, title, text) in enumerate(C.PRINCIPLES):
        x = i * (cw + gap)
        out.append(glass(x, 0, cw, H, 22, th))
        out.append(f'<rect x="{x + 20}" y="20" width="42" height="42" rx="13" {tint(th["blue_t"], th, th["tint"] + .03)}/>')
        out.append(stroke_icon(icon, x + 29, 29, 24, th["blue_t"]))
        out.append(T(x + 20, 92, title[lang], SANS7, fit(title[lang], SANS7, 17, cw - 40), th["text"], tracking=-.2))
        for j, line in enumerate(wrap(text[lang], SANS4, 13, cw - 40)[:4]):
            out.append(T(x + 20, 116 + j * 19, line, SANS4, 13, th["muted"]))
    return svg(W, H, "".join(out), "; ".join(f"{t[lang]}: {d[lang]}" for _, t, d in C.PRINCIPLES))


def achievements(th, lang):
    W, H, n = 1000, 178, len(C.ACHIEVEMENTS)
    step = W / n
    defs = gradient(th)
    out = []
    for i, (icon, title, sub) in enumerate(C.ACHIEVEMENTS):
        cx = step * (i + .5)
        out.append(f'<circle cx="{cx:.1f}" cy="52" r="42" fill="{th["card"]}" stroke="url(#g)" stroke-width="3"/>')
        out.append(f'<circle cx="{cx:.1f}" cy="52" r="34" {tint(th["blue_t"], th, th["tint"])}/>')
        out.append(stroke_icon(icon, cx - 15, 37, 30, th["blue_t"], 1.7))
        lines = title[lang]
        for j, line in enumerate(lines):
            out.append(T(cx, 122 + j * 17, line, SANS7, 14, th["text"], anchor="middle"))
        out.append(T(cx, 122 + len(lines) * 17 + 5, sub[lang], MONO5, 10, th["muted"], anchor="middle", tracking=.3))
    return svg(W, H, "".join(out), "Achievements: " + ", ".join(" ".join(t[lang]) for _, t, _ in C.ACHIEVEMENTS), defs)


def channel(th, ch, lang):
    W, H = 490, 132
    out = [glass(0, 0, W, H, 24, th),
           f'<rect x="24" y="24" width="52" height="52" rx="16" {tint(th["blue_t"], th, th["tint"] + .03)}/>',
           logo(ch["key"], 36, 36, 28, th),
           T(92, 46, ch["name"], SANS7, 22, th["text"], tracking=-.3)]
    for i, line in enumerate(wrap(ch["desc"][lang], SANS4, 14, W - 92 - 28)[:3]):
        out.append(T(92, 72 + i * 20, line, SANS4, 14, th["muted"]))
    cta = ch["cta"][lang]
    cw = MONO6.width(cta, 10.5, 1.1) + 40
    out.append(f'<rect x="{W - 24 - cw:.1f}" y="26" width="{cw:.1f}" height="26" rx="13" {tint(th["blue_t"], th, .14)} stroke="{th["blue_t"]}" stroke-opacity=".3"/>')
    out.append(T(W - 24 - cw + 14, 42.7, cta.upper(), MONO6, 10.5, th["blue_t"], tracking=1.1))
    ax = W - 24 - 14
    out.append(f'<path d="M{ax - 9} 39.5h9M{ax - 4} 35l4.5 4.5-4.5 4.5" fill="none" stroke="{th["blue_t"]}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>')
    return svg(W, H, "".join(out), f'{ch["name"]}: {ch["desc"][lang]}')


def fmt(n, lang):
    return f"{n:,}".replace(",", " " if lang == "fr" else ",")


def activity(th, lang, data=None):
    """Tableau de bord d'activité. data=None -> état « en attente de la première synchro »."""
    A = C.ACTIVITY_TEXT
    W = 1000
    out = []
    dash = "—"
    stats = [(A["contrib"][lang], data and fmt(data["total"], lang), th["blue_t"]),
             (A["commits"][lang], data and fmt(data["commits"], lang), th["sky_t"]),
             (A["prs"][lang], data and fmt(data["prs"], lang), th["green_t"]),
             (A["streak"][lang], data and fmt(data["streak"], lang), th["violet"] if th["bg"] != "#F0F4FF" else "#6D28D9")]
    tw = (W - 60) / 4
    for i, (label, val, col) in enumerate(stats):
        x = i * (tw + 20)
        out.append(glass(x, 0, tw, 92, 22, th))
        out.append(f'<circle cx="{x + 24}" cy="30" r="4.5" fill="{col}"/>')
        out.append(T(x + 36, 34, label, MONO6, 10.5, th["muted"], tracking=1))
        out.append(T(x + 22, 74, val or dash, SANS7, 34, th["text"], tracking=-.6))
    # graphique de contributions
    y0 = 112
    out.append(glass(0, y0, W, 226, 24, th))
    out.append(T(24, y0 + 34, A["heat"][lang], MONO6, 11, th["muted"], tracking=1.6))
    pitch, cell, gx, gy = 17, 14, 62, y0 + 72
    lv = [th["bord"], "#BFDBFE", "#60A5FA", "#2563EB", th["green"]] if th["bg"] == "#F0F4FF" else \
         ["#FFFFFF", "#1E3A8A", "#2563EB", "#38BDF8", "#34D399"]
    lv_op = [.07 if th["bg"] != "#F0F4FF" else .10, 1, 1, 1, 1]
    weeks = data["weeks"] if data else [[{"level": 0, "weekday": r} for r in range(7)] for _ in range(53)]
    days = A["days_fr"] if lang == "fr" else A["days"]
    for k, name in enumerate(days):
        out.append(T(24, gy + (k * 2 + 1) * pitch + 11, name, MONO5, 10, th["muted"]))
    last_month = None
    for wi, wk in enumerate(weeks):
        if data and wk and wk[0].get("date"):
            m = int(wk[0]["date"][5:7]) - 1
            if m != last_month and wi < len(weeks) - 2:
                out.append(T(gx + wi * pitch, y0 + 62, A["months"][lang][m], MONO5, 10, th["muted"]))
                last_month = m
        for d in wk:
            r = d.get("weekday", wk.index(d))
            out.append(f'<rect x="{gx + wi * pitch}" y="{gy + r * pitch}" width="{cell}" height="{cell}" rx="3.5" '
                       f'fill="{lv[d["level"]]}" fill-opacity="{lv_op[d["level"]]}"/>')
    ly = y0 + 226 - 30
    x_end = gx + 53 * pitch - 3
    more_w, less_w = MONO5.width(A["more"][lang], 10), MONO5.width(A["less"][lang], 10)
    cx0 = x_end - more_w - 8 - 5 * pitch + 3
    out.append(T(x_end, ly + 11, A["more"][lang], MONO5, 10, th["muted"], anchor="end"))
    out.append(T(cx0 - 8, ly + 11, A["less"][lang], MONO5, 10, th["muted"], anchor="end"))
    for k in range(5):
        out.append(f'<rect x="{cx0 + k * pitch:.1f}" y="{ly}" width="{cell}" height="{cell}" rx="3.5" fill="{lv[k]}" fill-opacity="{lv_op[k]}"/>')
    if not data:
        out.append(f'<rect x="{W / 2 - 330}" y="{y0 + 98}" width="660" height="44" rx="14" fill="{th["card"]}" stroke="{th["bord"]}" stroke-opacity="{th["bord_op"] * 1.6:.2f}"/>')
        out.append(T(W / 2, y0 + 125, A["waiting"][lang], SANS5, 13.5, th["text"], anchor="middle"))
    # langages + répartition
    y1, hh, cw = y0 + 226 + 20, 168, 490
    out.append(glass(0, y1, cw, hh, 24, th))
    out.append(T(24, y1 + 34, A["langs"][lang], MONO6, 11, th["muted"], tracking=1.6))
    langs = (data or {}).get("langs") or []
    out.append(f'<rect x="24" y="{y1 + 52}" width="{cw - 48}" height="10" rx="5" fill="{th["bord"]}" fill-opacity=".10"/>')
    if langs:
        clip = f'<clipPath id="lb"><rect x="24" y="{y1 + 52}" width="{cw - 48}" height="10" rx="5"/></clipPath>'
        bar, x = "", 24
        for name, color, pct in langs:
            w = (cw - 48) * pct / 100
            bar += f'<rect x="{x:.1f}" y="{y1 + 52}" width="{w:.1f}" height="10" fill="{color}"/>'
            x += w
        out.append(clip + f'<g clip-path="url(#lb)">{bar}</g>')
        for i, (name, color, pct) in enumerate(langs[:6]):
            cx_, cy_ = 24 + (i % 2) * 226, y1 + 92 + (i // 2) * 24
            out.append(f'<circle cx="{cx_ + 5}" cy="{cy_ - 4}" r="5" fill="{color}"/>')
            out.append(T(cx_ + 18, cy_, name, SANS5, 13.5, th["text"]))
            out.append(T(cx_ + 200, cy_, f"{pct:.1f}%", MONO5, 11.5, th["muted"], anchor="end"))
    else:
        out.append(T(24, y1 + 100, dash, SANS7, 22, th["muted"]))
    x2 = cw + 20
    out.append(glass(x2, y1, cw, hh, 24, th))
    out.append(T(x2 + 24, y1 + 34, A["mix"][lang], MONO6, 11, th["muted"], tracking=1.6))
    vals = [data["commits"], data["prs"], data["issues"], data["reviews"]] if data else [0, 0, 0, 0]
    tot = sum(vals) or 1
    cols = [th["blue"], th["sky"], th["violet"], th["green"]]
    for i, (name, v, col) in enumerate(zip(A["mix_rows"][lang], vals, cols)):
        yy = y1 + 66 + i * 26
        out.append(T(x2 + 24, yy + 4, name, SANS5, 13, th["text"]))
        out.append(f'<rect x="{x2 + 150}" y="{yy - 6}" width="{cw - 150 - 84}" height="10" rx="5" fill="{th["bord"]}" fill-opacity=".10"/>')
        if v:
            out.append(f'<rect x="{x2 + 150}" y="{yy - 6}" width="{max((cw - 234) * v / tot, 6):.1f}" height="10" rx="5" fill="{col}"/>')
        out.append(T(x2 + cw - 24, yy + 4, f"{v * 100 / tot:.0f}%" if data else dash, MONO5, 11.5, th["muted"], anchor="end"))
    H = y1 + hh
    upd = (data or {}).get("updated")
    if upd:
        out.append(T(W, H + 22, f'{A["updated"][lang]} {upd} · GitHub API', MONO5, 10.5, th["muted"], anchor="end"))
        H += 30
    return svg(W, H, "".join(out), "GitHub activity" if lang == "en" else "Activité GitHub")


def avatar():
    th = THEMES["dark"]
    W = 1024
    defs, body = backdrop(W, W, th, 0, grid=64, glow_scale=2.2)
    return svg(W, W, body + monogram(W / 2 - 240, W / 2 - 240, 480), "Avatar ATN", defs)


def button(th, kind, lang):
    label = {"portfolio": "Portfolio", "linkedin": "LinkedIn", "email": "E-mail" if lang == "fr" else "Email", "tiktok": "TikTok"}[kind]
    tw = SANS7.width(label, 15)
    W, H = int(tw + 84), 52
    primary = kind == "portfolio"
    defs = gradient(th) if primary else ""
    if primary:
        body = f'<rect width="{W}" height="{H}" rx="26" fill="url(#g)"/>' + stroke_icon("globe", 20, 14, 24, "#FFFFFF")
        col = "#FFFFFF"
    else:
        body = glass(0, 0, W, H, 26, th)
        col = th["text"]
        body += (stroke_icon("mail", 20, 14, 24, th["blue_t"]) if kind == "email"
                 else logo(kind, 20, 14, 24, th))
    body += T(56, 31.5, label, SANS7, 15, col, tracking=.1)
    return svg(W, H, body, label, defs)


def social(repo, lang="en"):
    th = THEMES["dark"]
    W, H = 1280, 640
    defs, body = backdrop(W, H, th, 0, grid=56, glow_scale=1.5)
    defs += gradient(th)
    out = [body, monogram(80, 72, 84)]
    size = fit(repo["name"], SANS7, 104, 1120)
    out.append(T(76, 330, repo["name"], SANS7, size, "url(#g)", tracking=-2))
    for i, line in enumerate(wrap(repo["sub"][lang], SANS4, 36, 1100)[:2]):
        out.append(T(80, 396 + i * 46, line, SANS4, 36, th["text"], opacity=.9))
    x = 80
    for tag in repo["tags"]:
        w = MONO5.width(tag, 19, .4) + 40
        out.append(f'<rect x="{x:.1f}" y="470" width="{w:.1f}" height="44" rx="22" {tint(th["blue_t"], th, .14)} stroke="{th["blue_t"]}" stroke-opacity=".3"/>')
        out.append(T(x + 20, 499, tag, MONO5, 19, th["blue_t"], tracking=.4))
        x += w + 14
    out.append(T(80, 590, C.BANNER["tagline"][lang], MONO5, 20, th["muted"]))
    out.append(T(W - 80, 590, "Axel Renaud Tadjounteu", SANS5, 22, th["text"], anchor="end", opacity=.85))
    return svg(W, H, "".join(out), f'{repo["name"]}: {repo["sub"][lang]}', defs)


# ── Écriture des fichiers ───────────────────────────────────────────────────
def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_assets():
    count = 0
    for tname, th in THEMES.items():
        base = REPO / "assets" / tname
        for lang in LANGS:
            write(base / f"banner.{lang}.svg", banner(th, lang)); count += 1
            for c in C.CERTS:
                write(base / f"cert-{c['id']}.{lang}.svg", cert_card(th, c, lang)); count += 1
            write(base / f"principles.{lang}.svg", principles(th, lang)); count += 1
            write(base / f"achievements.{lang}.svg", achievements(th, lang)); count += 1
            for ch in C.CHANNELS:
                write(base / f"channel-{ch['key']}.{lang}.svg", channel(th, ch, lang)); count += 1
            act = base / f"activity.{lang}.svg"
            if not act.exists() or FORCE_ACTIVITY:  # ne jamais écraser les vraies données
                write(act, activity(th, lang, None)); count += 1
            write(base / f"services.{lang}.svg", services(th, lang)); count += 1
            for i, (sid, title, cap) in enumerate(C.SECTIONS, 1):
                write(base / f"h-{sid}.{lang}.svg", header(th, i, title[lang], cap[lang])); count += 1
            for key in C.TOOLBOX:
                write(base / f"toolbox-{key}.{lang}.svg", toolbox(th, key, lang)); count += 1
            for p in C.PROJECTS:
                write(base / f"project-{p['key']}.{lang}.svg", project(th, p, lang)); count += 1
            for kind in ("portfolio", "linkedin", "email", "tiktok"):
                write(base / f"btn-{kind}.{lang}.svg", button(th, kind, lang)); count += 1
    print(f"{count} SVG écrits dans assets/light et assets/dark")


def build_social():
    try:
        import cairosvg
    except ImportError:
        print("cairosvg absent : aperçus sociaux ignorés (pip install cairosvg)")
        return
    for repo in C.REPOS:
        data = social(repo, "en")
        (REPO / "social").mkdir(exist_ok=True)
        cairosvg.svg2png(bytestring=data.encode(), write_to=str(REPO / "social" / f"{repo['name']}.png"), output_width=1280, output_height=640)
    (REPO / "brand").mkdir(exist_ok=True)
    cairosvg.svg2png(bytestring=avatar().encode(), write_to=str(REPO / "brand" / "avatar-atn.png"), output_width=1024, output_height=1024)
    print(f"{len(C.REPOS)} aperçus sociaux PNG (1280x640) dans social/ + brand/avatar-atn.png")


# ── README ──────────────────────────────────────────────────────────────────
def pic(name, alt, lang, width=None, link=None):
    fn = f"{name}.{lang}.svg"
    w = f' width="{width}"' if width else ""
    html = (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/{fn}">'
            f'<img src="assets/light/{fn}" alt="{esc(alt)}"{w}></picture>')
    return f'<a href="{link}">{html}</a>' if link else html


COPY = {
    "en": {
        "switch": '<p align="right"><a href="README.fr.md">Français</a></p>',
        "about": "I'm **Axel Renaud Tadjounteu**, a cybersecurity and cloud student and developer from Douala, Cameroon. I founded **Atnyx**, an IT services company, and I'm in my third year of a Networks & Telecommunications degree (security track) at the Université de Douala. I'm an AWS re/Start alumnus and hold the **AWS Cloud Practitioner** certification.\n\nI like following a system end to end, from the network to the cloud account to the login form, and finding where it can break. I build with my context in mind: unreliable connections, low-end devices, small budgets.",
        "now": ["Preparing the **AWS Solutions Architect Associate (SAA-C03)** exam",
                "Doing cloud and network labs from the command line (gcloud, Cisco Packet Tracer)",
                "Building **NKUL** and the **Atnyx Platform**, and designing **Branchline**",
                "Exploring AI agents with Google's Agent Development Kit",
                "Planning a 12-month path toward **CompTIA Security+**"],
        "atnyx_pre": "Atnyx is the IT services company I founded in Douala. It covers four areas:",
        "atnyx_post": "Around it, I'm building the **Atnyx Platform** (a multi-branch website) and **NKUL**, an audit product for African SMEs.",
        "labs": ["**Google Cloud Skills Boost**: challenge labs done entirely from the CLI (ADK agents, GKE, Cloud Run, HA VPN, VPC Flow Logs to BigQuery)",
                 "**Networking**: Cisco Packet Tracer labs on VLANs, ACLs, DMZ and firewall, IPsec VPN",
                 "**Security**: hands-on paths on Cisco NetAcad, Fortinet NSE, PortSwigger Academy and TryHackMe"],
        "content": "I make short videos on **TikTok** and write **LinkedIn** posts about cybersecurity, cloud and development, to explain what I learn in plain language.",
        "contact": "Open to collaborations, and to projects through **Atnyx**.",
        "alt": {"banner": "Axel Renaud Tadjounteu: cybersecurity, cloud and software development. Founder of Atnyx, Douala, Cameroon.",
                "certs": "Certifications: AWS re/Start completed, AWS Cloud Practitioner certified, AWS Solutions Architect Associate in progress, CompTIA Security+ planned.",
                "services": "Atnyx services: cybersecurity, cloud, web and mobile, IT support."},
    },
    "fr": {
        "switch": '<p align="right"><a href="README.md">English</a></p>',
        "about": "Je suis **Axel Renaud Tadjounteu**, étudiant et développeur en cybersécurité et cloud, basé à Douala, au Cameroun. J'ai fondé **Atnyx**, une entreprise de services IT, et je suis en troisième année de licence Réseaux & Télécommunications (spécialité sécurité) à l'Université de Douala. Je suis alumnus AWS re/Start et titulaire de la certification **AWS Cloud Practitioner**.\n\nJ'aime suivre un système de bout en bout, du réseau au compte cloud jusqu'au formulaire de connexion, et trouver où il peut casser. Je construis en pensant à mon contexte : connexions instables, appareils modestes, petits budgets.",
        "now": ["Je prépare l'examen **AWS Solutions Architect Associate (SAA-C03)**",
                "Je pratique des labs cloud et réseau en ligne de commande (gcloud, Cisco Packet Tracer)",
                "Je construis **NKUL** et la **Plateforme Atnyx**, et je conçois **Branchline**",
                "J'explore les agents IA avec l'Agent Development Kit de Google",
                "Je planifie un parcours de 12 mois vers **CompTIA Security+**"],
        "atnyx_pre": "Atnyx est l'entreprise de services IT que j'ai fondée à Douala. Elle couvre quatre domaines :",
        "atnyx_post": "Autour d'elle, je construis la **Plateforme Atnyx** (un site multi-branches) et **NKUL**, un produit d'audit pour les PME africaines.",
        "labs": ["**Google Cloud Skills Boost** : labs à défi réalisés entièrement en CLI (agents ADK, GKE, Cloud Run, VPN HA, VPC Flow Logs vers BigQuery)",
                 "**Réseau** : labs Cisco Packet Tracer sur les VLAN, ACL, DMZ et pare-feu, VPN IPsec",
                 "**Sécurité** : parcours pratiques sur Cisco NetAcad, Fortinet NSE, PortSwigger Academy et TryHackMe"],
        "content": "Je publie des vidéos courtes sur **TikTok** et des posts **LinkedIn** sur la cybersécurité, le cloud et le développement, pour expliquer simplement ce que j'apprends.",
        "contact": "Ouvert aux collaborations, et aux projets via **Atnyx**.",
        "alt": {"banner": "Axel Renaud Tadjounteu : cybersécurité, cloud et développement logiciel. Fondateur d'Atnyx, Douala, Cameroun.",
                "certs": "Certifications : AWS re/Start terminé, AWS Cloud Practitioner obtenue, AWS Solutions Architect Associate en cours, CompTIA Security+ prévue.",
                "services": "Services Atnyx : cybersécurité, cloud, web et mobile, support IT."},
    },
}


def toolbox_alt(key, lang):
    label = C.TOOLBOX[key]["label"][lang]
    nice = {"AI & PRODUCTIVITY": "AI & productivity", "IA & PRODUCTIVITÉ": "IA & productivité"}.get(label, label.capitalize())
    sep = " : " if lang == "fr" else ": "
    return nice + sep + ", ".join(l for _, l in C.TOOLBOX[key]["tools"])


def readme(lang):
    c, sec = COPY[lang], {s[0]: s[1][lang] for s in C.SECTIONS}
    H = lambda sid: f'<h3>{pic("h-" + sid, sec[sid], lang, "100%")}</h3>\n'
    bullets = lambda items: "\n".join(f"- {i}" for i in items)
    link = lambda html, url: f'<a href="{url}">{html}</a>' if url else html
    L_ = C.LINKS
    proj = "".join(link(pic(f"project-{p['key']}", f"{p['title']}: {p['desc'][lang]}", lang, "49%"), C.PROJECT_LINKS.get(p["key"])) + "\n"
                   for p in C.PROJECTS)
    strips = "\n\n".join(pic(f"toolbox-{k}", toolbox_alt(k, lang), lang, "100%") for k in ("cloud", "security", "dev", "data", "ai"))
    certs = "\n".join(link(pic(f"cert-{x['id']}", f'{" ".join(L(x["title"], lang))} ({C.STATUS_TEXT[x.get("done_key", x["status"])][lang].lower()})', lang, f"{(1000 - 20 * (len(C.CERTS) - 1)) / len(C.CERTS) / 10 - 0.3:.1f}%"),
                            C.CERT_PROOF.get(x["id"])) for x in C.CERTS)
    chans = "\n".join(link(pic(f"channel-{ch['key']}", f"{ch['name']}: {ch['desc'][lang]}", lang, "49%"), L_[ch["key"]]) for ch in C.CHANNELS)
    names = {"portfolio": "Portfolio", "linkedin": "LinkedIn", "email": "E-mail" if lang == "fr" else "Email", "tiktok": "TikTok"}
    btns = "\n".join(pic(f"btn-{k}", names[k], lang, link=L_[k]) for k in ("portfolio", "linkedin", "email", "tiktok"))
    prin_alt = "; ".join(f"{t[lang]}: {d[lang]}" for _, t, d in C.PRINCIPLES)
    ach_alt = ("Achievements: " if lang == "en" else "Réalisations : ") + ", ".join(" ".join(t[lang]) for _, t, _ in C.ACHIEVEMENTS)
    return f"""{c['switch']}

<p align="center">{pic('banner', c['alt']['banner'], lang, '100%')}</p>

{H('about')}
{c['about']}

{H('approach')}
{pic('principles', prin_alt, lang, '100%')}

{H('now')}
{bullets(c['now'])}

{H('atnyx')}
{c['atnyx_pre']}

{pic('services', c['alt']['services'], lang, '100%')}

{c['atnyx_post']}

{H('projects')}
<!-- Pour rendre une carte cliquable : ajoute son lien dans PROJECT_LINKS (scripts/content.py) puis relance build.py --readme -->
<p>
{proj}</p>

{H('toolbox')}
{strips}

{H('labs')}
{bullets(c['labs'])}
<!-- Quand les dépôts existent : ajoute [cloud-labs](https://github.com/{C.USERNAME}/cloud-labs) et [network-security-labs](https://github.com/{C.USERNAME}/network-security-labs) -->

{H('certs')}
<!-- Pour lier une carte à sa preuve (Credly...) : ajoute-la dans CERT_PROOF (scripts/content.py) -->
<p>
{certs}
</p>

{pic('toolbox-learning', toolbox_alt('learning', lang), lang, '100%')}

{H('achievements')}
{pic('achievements', ach_alt, lang, '100%')}

{H('activity')}
{pic('activity', 'GitHub activity' if lang == 'en' else 'Activité GitHub', lang, '100%')}

{H('content')}
{c['content']}

<p>
{chans}
</p>

{H('contact')}
{c['contact']}

<p>
{btns}
</p>
"""


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--readme", action="store_true", help="regénère aussi README.md et README.fr.md")
    ap.add_argument("--force-activity", action="store_true", help="remplace aussi les visuels d'activité par l'état « en attente »")
    args = ap.parse_args()
    FORCE_ACTIVITY = args.force_activity
    build_assets()
    build_social()
    if args.readme:
        write(REPO / "README.md", readme("en"))
        write(REPO / "README.fr.md", readme("fr"))
        print("README.md et README.fr.md régénérés")
