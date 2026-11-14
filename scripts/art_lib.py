"""MasakJe kitchen art: flat, warm SVG drawings for every ingredient and cooking method.

Each drawing is the inside of an <svg viewBox="0 0 120 120">. A few shared shapes (drumstick, fish,
leafy bunch, bottle, spice jar, noodle nest...) are recoloured per ingredient, so all 86 keep one look.
Animations are CSS classes prefixed "a-" (see ART_CSS); each drawing moves one thing, and nothing moves
when the phone asks for reduced motion. Used by build_prototype.py, which ships the strings in DATA.art.
"""

C = dict(chili="#c8420c", chili2="#9a330a", orange="#f26a1b", cream="#fff1e8", wok="#3b3530", wok2="#2a2522", rim="#4a423c",
         steel="#b9b4ae", steel2="#8f8a85", wood="#8a5a3b", wood2="#6e4630", leaf="#4f8a3c", leaf2="#7cb342", red="#d7301f",
         turmeric="#e9a21f", gold="#f6c453", shallot="#b0496b", shallot2="#d27896", garlic="#f3ead8", garlic2="#ddcfb4",
         brown="#6b4a33", steam="#cfc8c1", bamboo="#d9a35b", bamboo2="#b9803e", fish="#7f9bb0", fish2="#c9d6df",
         prawn="#f08a5d", prawn2="#e06c3f", egg="#fbf1dc", milk="#fbf7ef", ink="#1c1917", line="#e2d3b8")

SHADOW = '<ellipse cx="60" cy="106" rx="38" ry="5" fill="#1c1917" opacity=".08"/>'


def steam(xs, y=46):
    return "".join(f'<path class="a-st" style="animation-delay:{i * 0.8}s" d="M{x} {y} q-5 -6 0 -12 q5 -6 0 -12" fill="none" stroke="{C["steam"]}" stroke-width="3.5" stroke-linecap="round"/>' for i, x in enumerate(xs))


def bubbles(pts, cls="a-bb"):
    return "".join(f'<circle class="{cls}" style="animation-delay:{d}s" cx="{x}" cy="{y}" r="{r}" fill="#fff8e3"/>' for x, y, r, d in pts)


# ---------------------------------------------------------------- shared shapes
def wok(paste=True, paste_col=None):
    p = f'''<rect x="4" y="57" width="18" height="7" rx="3.5" fill="{C['wood']}"/>
      <path d="M98 58 q12 -2 12 6 q0 6 -10 4" fill="none" stroke="{C['wok']}" stroke-width="4" stroke-linecap="round"/>
      <path d="M18 62 Q60 108 102 62 Z" fill="{C['wok']}"/><ellipse cx="60" cy="62" rx="42" ry="9" fill="{C['rim']}"/>
      <ellipse cx="60" cy="63" rx="37" ry="6.5" fill="{C['wok2']}"/>'''
    if paste:
        p += f'''<ellipse cx="60" cy="63" rx="22" ry="4.6" fill="{paste_col or C['chili']}"/>
      <circle cx="52" cy="62.5" r="1.6" fill="{C['chili2']}"/><circle cx="66" cy="63.5" r="1.4" fill="{C['chili2']}"/>
      <ellipse class="a-sh" cx="47" cy="64" rx="5" ry="1.4" fill="{C['gold']}"/><ellipse class="a-sh" style="animation-delay:.7s" cx="72" cy="62" rx="4" ry="1.2" fill="{C['gold']}"/>'''
    return p


def drumstick(cx=60, cy=60, s=1, rot=-25, meat="#c97a2b", hi="#e8a35a", fat=False):
    body = "M-24 0 C-24 -19 4 -19 14 -6 L14 6 C4 19 -24 19 -24 0 Z" if fat else "M-22 0 C-22 -16 4 -16 14 -5 L14 5 C4 16 -22 16 -22 0 Z"
    return f'''<g transform="translate({cx} {cy}) rotate({rot}) scale({s})">
      <g stroke="{C['line']}" stroke-width="1.5"><rect x="10" y="-3.5" width="20" height="7" rx="3.5" fill="#fff"/>
      <circle cx="31" cy="-4" r="4.5" fill="#fff"/><circle cx="31" cy="4" r="4.5" fill="#fff"/></g><rect x="9" y="-2.6" width="18" height="5.2" fill="#fff"/>
      <path d="{body}" fill="{meat}"/>
      <path d="M-15 -6 C-8 -11 2 -10 7 -5" fill="none" stroke="{hi}" stroke-width="3" stroke-linecap="round"/></g>'''


def fish(cx=60, cy=60, s=1, col=None, belly=None, stripe=None, marks=True):
    col = col or C['fish']
    belly = belly or C['fish2']
    st = f'<path d="M-30 -1 C-14 -5 10 -5 24 -1" stroke="{stripe}" stroke-width="4" fill="none" stroke-linecap="round"/>' if stripe else ""
    mk = '<path d="M-8 -9 l6 3 M2 -9 l6 3 M12 -7 l5 3" stroke="#5f7a8e" stroke-width="1.6" stroke-linecap="round" opacity=".8"/>' if marks else ""
    return f'''<g transform="translate({cx} {cy}) scale({s})">
      <path d="M-34 0 C-22 -16 14 -16 26 0 C14 16 -22 16 -34 0 Z" fill="{col}"/>
      <path d="M-34 0 C-22 -6 10 -8 26 0 C10 10 -22 10 -34 0 Z" fill="{belly}" opacity=".75"/>{st}
      <path d="M24 0 L40 -11 L37 0 L40 11 Z" fill="{col}"/><path d="M-6 -12 q6 -5 12 0" fill="{col}"/>
      <circle cx="-25" cy="-3" r="2.6" fill="#fff"/><circle cx="-25" cy="-3" r="1.3" fill="{C['ink']}"/>
      <path d="M-18 -4 v8" stroke="#5f7a8e" stroke-width="1.5" stroke-linecap="round"/>{mk}</g>'''


def leaf(x, y, rot, s=1, col=None, vein="#3f7030"):
    col = col or C['leaf']
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><path d="M0 0 C6 -8 18 -8 26 0 C18 8 6 8 0 0 Z" fill="{col}"/><path d="M2 0 H22" stroke="{vein}" stroke-width="1.2"/></g>'


def roundleaf(x, y, rot, s=1, col="#2f6b34", vein="#24552a"):
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><path d="M0 0 C2 -12 22 -14 26 0 C22 14 2 12 0 0 Z" fill="{col}"/><path d="M2 0 H22" stroke="{vein}" stroke-width="1.2"/></g>'


def chili(x=60, y=60, s=1, rot=0, col=None, hi="#ef6a52", stem=None, wrinkle=False):
    col = col or C['red']
    stem = stem or C['leaf']
    w = '<path d="M-18 -4 q4 3 8 0 M-2 -5 q4 3 8 0 M12 -2 q3 3 7 1" stroke="#5e1009" stroke-width="1.4" fill="none" opacity=".7"/>' if wrinkle else ""
    return f'''<g transform="translate({x} {y}) rotate({rot}) scale({s})">
      <path d="M-30 -6 C-10 -14 20 -10 32 8 C34 12 30 13 27 10 C16 -2 -8 -2 -28 2 C-33 3 -34 -4 -30 -6 Z" fill="{col}"/>
      <path d="M-24 -6 C-8 -11 10 -9 20 -2" fill="none" stroke="{hi}" stroke-width="2.4" stroke-linecap="round"/>{w}
      <path d="M-30 -2 C-36 -4 -38 -10 -36 -14" fill="none" stroke="{stem}" stroke-width="4" stroke-linecap="round"/>
      <path d="M-33 -6 l-5 -1 l2 5 Z" fill="{stem}"/></g>'''


def bulb(x=60, y=62, s=1, col=None, line=None, root=C['garlic2'], top=C['garlic2'], cloves=False, outline=None):
    col = col or C['shallot']
    line = line or C['shallot2']
    ol = f' stroke="{outline}" stroke-width="1.5"' if outline else ""
    inner = (f'<path d="M0 -14 C-4 -2 -4 10 -1 18 M0 -14 C5 -2 6 8 4 18 M0 -14 C-12 -6 -13 8 -8 16 M0 -14 C11 -6 13 8 8 16" fill="none" stroke="{line}" stroke-width="1.4"/>' if cloves
             else f'<path d="M0 -15 C8 -10 9 8 4 17 M0 -15 C-8 -10 -9 8 -4 17" fill="none" stroke="{line}" stroke-width="1.6"/>')
    return f'''<g transform="translate({x} {y}) scale({s})">
      <path d="M0 -26 C3 -18 2 -16 1 -14" stroke="{top}" stroke-width="3" stroke-linecap="round" fill="none"/>
      <path d="M0 -16 C16 -14 20 8 10 16 C6 19 -6 19 -10 16 C-20 8 -16 -14 0 -16 Z" fill="{col}"{ol}/>{inner}
      <path d="M-5 18 l-2 5 M0 18 v6 M5 18 l2 5" stroke="{root}" stroke-width="1.6" stroke-linecap="round"/></g>'''


def bottle(body="#2b211c", label=C['cream'], band=C['chili'], cap=C['chili'], liquid=None, short=False):
    top = 30 if not short else 44
    liq = f'<path d="M44 {top + 26} H76 V94 Q76 98 72 98 H48 Q44 98 44 94 Z" fill="{liquid}" opacity=".85"/>' if liquid else ""
    return f'''<rect x="52" y="{top - 14}" width="16" height="14" rx="3" fill="{cap}"/>
      <path d="M54 {top} H66 L70 {top + 14} C76 {top + 18} 78 {top + 24} 78 {top + 32} V94 Q78 100 72 100 H48 Q42 100 42 94 V{top + 32} C42 {top + 24} 44 {top + 18} 50 {top + 14} Z" fill="{body}"/>{liq}
      <rect x="42" y="66" width="36" height="20" fill="{label}"/><path d="M48 76 H72" stroke="{band}" stroke-width="4" stroke-linecap="round"/>
      <path class="a-gl" d="M47 {top + 22} v8" stroke="#fff" stroke-width="2.5" stroke-linecap="round" opacity=".4"/>'''


def jar(fill, grains=None, label="#ffffff", lid=C['chili']):
    g = grains or fill
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="1.3" fill="{g}"/>' for x, y in ((50, 40), (60, 37), (70, 41), (55, 44), (66, 45)))
    return f'''<rect x="36" y="40" width="48" height="58" rx="10" fill="#ffffff" stroke="#e6d8c8" stroke-width="2"/>
      <rect x="39" y="52" width="42" height="43" rx="8" fill="{fill}"/>
      <path d="M44 34 C50 26 70 26 76 34 L76 44 L44 44 Z" fill="{fill}"/>{dots}
      <rect x="34" y="28" width="52" height="10" rx="4" fill="{lid}"/>
      <rect x="44" y="66" width="32" height="16" rx="3" fill="{label}" opacity=".9"/><path d="M50 74 H70" stroke="{lid}" stroke-width="3" stroke-linecap="round"/>'''


def heap(fill, dots, dot_col, plate=True):
    d = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{dot_col}"/>' for x, y, r in dots)
    p = f'<ellipse cx="60" cy="88" rx="44" ry="10" fill="#ffffff" stroke="#e6d8c8" stroke-width="2"/>' if plate else ""
    return f'''{p}<path d="M26 86 C30 60 46 46 60 46 C74 46 90 60 94 86 Z" fill="{fill}"/>{d}'''


def bag(col, label, word_col):
    return f'''<path d="M34 30 H86 L90 98 Q90 102 86 102 H34 Q30 102 30 98 Z" fill="{col}"/>
      <path d="M34 30 L40 22 H80 L86 30 Z" fill="#ffffff" opacity=".6"/><path d="M34 30 H86" stroke="#d9cdbd" stroke-width="2"/>
      <rect x="40" y="52" width="40" height="30" rx="6" fill="{label}"/><path d="M48 62 H72 M50 70 H70" stroke="{word_col}" stroke-width="3" stroke-linecap="round"/>'''


def nest(col, w=4, flat=False, edge="#d9c9a8"):
    """A bowl with noodles heaped above the rim (outlined so pale noodles still read)."""
    sw = 7 if flat else w
    paths = [f"M{26 + i * 4} 66 C{34 + i * 3} {40 - i} {58 + i * 2} {38 + i * 2} {64 + i * 3} {50 + i} S{90 - i * 2} {58 - i} {94 - i * 3} 66" for i in range(6)]
    under = "".join(f'<path d="{d}" fill="none" stroke="{edge}" stroke-width="{sw + 2}" stroke-linecap="round"/>' for d in paths)
    over = "".join(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>' for d in paths)
    bowl = '<path d="M14 66 H106 C106 88 88 102 60 102 C32 102 14 88 14 66 Z" fill="#ffffff" stroke="#e6d8c8" stroke-width="2"/><path d="M22 80 Q60 92 98 80" fill="none" stroke="#5b8fc7" stroke-width="2.5"/>'
    return under + over + bowl


def bunch(leaves, stems, tie=True):
    t = f'<rect x="52" y="78" width="16" height="8" rx="3" fill="{C["chili"]}"/>' if tie else ""
    return stems + leaves + t


# ---------------------------------------------------------------- ingredients
def I():
    a = {}
    a["chicken"] = drumstick(52, 62, 1.55, -25)
    a["chicken_thigh"] = drumstick(52, 62, 1.5, -15, meat="#d18a3f", fat=True)
    a["chicken_breast"] = f'''<path d="M22 70 C20 46 52 34 74 40 C96 46 100 70 86 82 C70 96 30 96 22 70 Z" fill="#f2b8a2"/>
      <path d="M34 64 C46 52 66 48 82 56" stroke="#f8d3c4" stroke-width="5" fill="none" stroke-linecap="round"/>'''
    a["chicken_wing"] = f'''<path d="M20 76 C20 60 36 50 52 56 L66 62 C76 50 94 46 100 56 C104 66 92 74 80 74 L60 84 C44 92 20 90 20 76 Z" fill="#d18a3f"/>
      <path d="M30 70 C38 62 48 62 56 66 M72 60 C80 56 90 56 94 60" stroke="#e8a35a" stroke-width="3" fill="none" stroke-linecap="round"/>'''
    a["beef"] = f'''<path d="M20 64 C18 44 50 36 74 40 C98 44 104 66 92 80 C78 96 26 94 20 64 Z" fill="#b5372a"/>
      <path d="M30 60 C44 52 60 56 72 50 M36 74 C52 70 66 76 84 68" stroke="#f4d8cc" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M20 64 C26 88 82 94 92 80" stroke="#f4d8cc" stroke-width="4" fill="none"/>'''
    a["mutton"] = f'''<path d="M24 66 C22 46 50 40 70 46 C88 52 88 74 74 84 C58 94 28 88 24 66 Z" fill="#a8463a"/>
      <path d="M32 62 C44 54 58 58 68 54" stroke="#f1d0c4" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M74 60 L100 48" stroke="#fff" stroke-width="7" stroke-linecap="round"/><circle cx="102" cy="45" r="5" fill="#fff" stroke="{C['line']}" stroke-width="1.5"/>
      <circle cx="54" cy="70" r="5" fill="#fff" stroke="{C['line']}" stroke-width="1.5"/>'''
    a["fish_kembung"] = fish(58, 60, 1.1)
    a["fish_selar"] = fish(58, 60, 1.1, col="#8ea2ad", stripe="#e9c46a")
    a["fish_siakap"] = fish(58, 60, 1.15, col="#8c969c", belly="#dfe4e6", marks=False)
    a["fish_tilapia"] = fish(58, 60, 1.1, col="#6f7b80", belly="#e3c7c0", marks=False)
    a["fish_tenggiri"] = f'''<ellipse cx="60" cy="66" rx="38" ry="30" fill="#7c8a92"/><ellipse cx="60" cy="66" rx="34" ry="26" fill="#f1e2d6"/>
      <path d="M60 42 V90 M40 58 Q60 66 80 58 M40 76 Q60 68 80 76" stroke="#e2cbb9" stroke-width="2.5" fill="none"/><circle cx="60" cy="66" r="4" fill="#d9c0ac"/>'''
    a["prawn"] = f'''<g transform="translate(60 62)">
      <path d="M-26 -14 C-2 -30 30 -14 24 10 C20 22 4 26 -6 20" fill="none" stroke="{C['prawn']}" stroke-width="16" stroke-linecap="round"/>
      <path d="M-16 -22 l4 10 M-4 -26 l2 11 M8 -24 l-1 11 M18 -16 l-4 9 M22 -4 l-8 4" stroke="{C['prawn2']}" stroke-width="2" stroke-linecap="round"/>
      <path d="M-6 20 L-22 26 L-18 18 L-24 12 Z" fill="{C['prawn2']}"/>
      <circle cx="-24" cy="-18" r="2.2" fill="{C['ink']}"/><path d="M-30 -16 C-44 -24 -50 -10 -54 -4 M-30 -14 C-40 -12 -46 2 -50 8" stroke="{C['prawn2']}" stroke-width="1.4" fill="none"/></g>'''
    a["squid"] = f'''<path d="M60 18 C76 34 78 54 74 68 H46 C42 54 44 34 60 18 Z" fill="#f3d2c7"/>
      <path d="M46 40 L34 30 L48 30 Z M74 40 L86 30 L72 30 Z" fill="#eebcad"/>
      <circle cx="54" cy="62" r="2.2" fill="{C['ink']}"/><circle cx="66" cy="62" r="2.2" fill="{C['ink']}"/>
      {''.join(f'<path d="M{48 + i * 5} 68 C{46 + i * 5} 80 {52 + i * 5} 88 {48 + i * 5} 98" stroke="#eebcad" stroke-width="4" fill="none" stroke-linecap="round"/>' for i in range(5))}'''
    a["cockle"] = "".join(f'''<g transform="translate({x} {y}) scale({s})"><path d="M-18 6 C-18 -14 18 -14 18 6 Z" fill="#c7a27c"/>
      <path d="M-12 4 L-8 -8 M-4 4 L-2 -10 M4 4 L2 -10 M12 4 L8 -8" stroke="#9c7652" stroke-width="2"/><rect x="-6" y="5" width="12" height="4" rx="2" fill="#9c7652"/></g>''' for x, y, s in ((44, 70, 1.2), (76, 72, 1.1), (60, 52, 1.0)))
    a["ikan_bilis"] = "".join(f'<g transform="translate({x} {y}) rotate({r})"><path d="M-14 0 C-8 -4 6 -4 10 0 C6 4 -8 4 -14 0 Z" fill="#c9ccc8"/><path d="M10 0 l6 -4 v8 Z" fill="#c9ccc8"/><circle cx="-10" cy="-0.5" r="1" fill="{C["ink"]}"/></g>' for x, y, r in ((44, 56, -20), (70, 52, 15), (56, 70, 5), (80, 72, -10), (40, 80, 20), (64, 86, -5)))
    a["dried_shrimp"] = heap("#f2b69c", [(x, y, 4) for x, y in ((46, 70), (58, 62), (70, 68), (52, 80), (66, 80), (78, 78), (40, 82))], "#e0835c")
    a["salted_fish"] = fish(58, 62, 1.1, col="#c49a6c", belly="#e8d3b3", marks=False) + "".join(f'<circle cx="{x}" cy="{y}" r="1.4" fill="#fff"/>' for x, y in ((44, 56), (56, 60), (68, 54), (50, 66), (74, 64)))
    a["dried_chili"] = chili(60, 56, 1.0, -18, col="#8e1b10", hi="#b23a2a", stem="#6b5a3a", wrinkle=True) + chili(62, 76, .85, 8, col="#a0281a", hi="#c24c3a", stem="#6b5a3a", wrinkle=True)
    a["santan"] = f'''<path d="M22 60 H98 C98 84 82 98 60 98 C38 98 22 84 22 60 Z" fill="{C['brown']}"/>
      <ellipse cx="60" cy="60" rx="38" ry="9" fill="#fff"/><ellipse cx="60" cy="61" rx="31" ry="6" fill="{C['milk']}"/>
      <path d="M32 72 q6 4 12 2 M70 80 q6 2 10 -2" stroke="#4e3524" stroke-width="2" fill="none" stroke-linecap="round"/>
      <path class="a-drip" d="M60 22 C60 22 52 32 52 37 C52 41 56 44 60 44 C64 44 68 41 68 37 C68 32 60 22 60 22 Z" fill="#fff" stroke="#e9e1d4" stroke-width="1.5"/>'''
    a["tamarind"] = f'''<path d="M18 70 C22 54 40 48 52 54 C62 44 82 46 92 58 C102 70 92 88 74 86 C60 94 30 92 18 70 Z" fill="#5c3a21"/>
      {''.join(f'<ellipse cx="{x}" cy="{y}" rx="3.4" ry="2.4" fill="#3b2414"/>' for x, y in ((40, 66), (56, 72), (72, 64), (80, 76), (48, 80)))}
      <path d="M30 40 C46 30 72 30 92 38" stroke="#8a6440" stroke-width="9" stroke-linecap="round" fill="none"/>'''
    a["peanuts"] = "".join(f'<g transform="translate({x} {y}) rotate({r})"><path d="M-12 0 C-12 -8 -2 -8 0 -3 C2 -8 12 -8 12 0 C12 8 2 8 0 3 C-2 8 -12 8 -12 0 Z" fill="#d6aa72" stroke="#b98a52" stroke-width="1.5"/></g>' for x, y, r in ((44, 60, -20), (70, 56, 25), (58, 76, 5), (80, 78, -15), (38, 82, 30)))
    a["dhal"] = (f'<path d="M14 62 H106 C106 86 88 100 60 100 C32 100 14 86 14 62 Z" fill="#ffffff" stroke="#e6d8c8" stroke-width="2"/><ellipse cx="60" cy="62" rx="46" ry="9" fill="#f0a24a"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="2" fill="#e08a2c"/>' for x, y in ((34, 61), (46, 64), (58, 60), (70, 64), (82, 61), (52, 57), (66, 57))) + '<path d="M22 76 Q60 88 98 76" fill="none" stroke="#5b8fc7" stroke-width="2.5"/>')
    a["rice"] = f'''<path d="M14 64 H106 C106 88 88 102 60 102 C32 102 14 88 14 64 Z" fill="#ffffff" stroke="#e6d8c8" stroke-width="2"/>
      <path d="M22 64 C26 42 44 34 60 34 C76 34 94 42 98 64 Z" fill="#fbf7ef" stroke="#ece4d6" stroke-width="2"/>
      {''.join(f'<ellipse cx="{x}" cy="{y}" rx="3" ry="1.4" fill="#e9e0cf" transform="rotate({r} {x} {y})"/>' for x, y, r in ((44, 52, 20), (58, 44, -10), (72, 50, 30), (52, 58, -30), (66, 58, 10), (82, 58, -20), (38, 60, 40)))}
      <path d="M22 80 Q60 92 98 80" fill="none" stroke="#5b8fc7" stroke-width="2.5"/>{steam([48, 72], 34)}'''
    a["egg"] = f'''<path d="M60 26 C80 26 90 56 88 72 C86 90 74 98 60 98 C46 98 34 90 32 72 C30 56 40 26 60 26 Z" fill="{C['egg']}" stroke="#dcc49a" stroke-width="2.5"/>
      <ellipse cx="50" cy="48" rx="5" ry="9" fill="#fff" opacity=".8" transform="rotate(20 50 48)"/>'''
    a["tofu"] = f'''<path d="M26 52 L60 38 L94 52 L60 66 Z" fill="#fbf3dc"/><path d="M26 52 V84 L60 98 V66 Z" fill="#efe1bd"/><path d="M94 52 V84 L60 98 V66 Z" fill="#e4d2a8"/>
      <path d="M40 50 l2 1 M60 46 l2 1 M74 52 l2 1" stroke="#e0cfa6" stroke-width="2" stroke-linecap="round"/>'''
    a["tempe"] = f'''<rect x="20" y="44" width="80" height="44" rx="8" fill="#e8d6a8"/>
      {''.join(f'<ellipse cx="{x}" cy="{y}" rx="4" ry="3" fill="#d4bb82"/>' for x in (32, 46, 60, 74, 88) for y in (56, 72))}
      <path d="M20 52 Q60 44 100 52" stroke="#f3e7c6" stroke-width="3" fill="none"/>'''
    # leafy greens
    stems = lambda col, pts: "".join(f'<path d="M60 100 C{a} {b} {c} {d} {e} {f}" stroke="{col}" stroke-width="4" stroke-linecap="round" fill="none"/>' for a, b, c, d, e, f in pts)
    fan = ((58, 80, 52, 60, 44, 40), (62, 78, 70, 58, 78, 38), (60, 80, 60, 60, 60, 36))
    a["kangkung"] = bunch(leaf(40, 44, -110, 1.1) + leaf(60, 38, -90, 1.15, C['leaf2']) + leaf(80, 42, -70, 1.1) + leaf(50, 64, -150, .9, C['leaf2']) + leaf(70, 62, -30, .9), stems(C['leaf2'], fan), tie=False)
    a["bayam"] = bunch(roundleaf(40, 44, -110, 1.1) + roundleaf(60, 36, -90, 1.15, "#3c7d3f") + roundleaf(80, 42, -70, 1.1), stems("#c2567a", fan))
    a["sawi"] = bunch(leaf(38, 46, -110, 1.2, "#5f9c45") + leaf(60, 38, -90, 1.25, C['leaf2']) + leaf(82, 46, -70, 1.2, "#5f9c45") + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#f2c84b"/>' for x, y in ((58, 22), (64, 26), (54, 28))), stems("#a7c96b", fan))
    a["kailan"] = bunch(roundleaf(38, 46, -110, 1.25, "#3d6e5b", "#2c5244") + roundleaf(60, 36, -90, 1.3, "#467a64", "#2c5244") + roundleaf(82, 46, -70, 1.25, "#3d6e5b", "#2c5244"), stems("#8fb39a", fan))
    a["pak_choy"] = f'''<path d="M48 100 C40 80 40 60 46 44 M72 100 C80 80 80 60 74 44 M60 100 V40" stroke="#eef3e2" stroke-width="12" stroke-linecap="round" fill="none"/>
      {roundleaf(46, 40, -105, 1.1, '#4f8a3c')}{roundleaf(74, 40, -75, 1.1, '#4f8a3c')}{roundleaf(60, 34, -90, 1.2, '#5f9c45')}'''
    a["spring_onion"] = "".join(f'<path d="M{x} 100 V{t}" stroke="#7cb342" stroke-width="7" stroke-linecap="round"/><path d="M{x} 100 V80" stroke="#f3f0e3" stroke-width="7" stroke-linecap="round"/>' for x, t in ((48, 26), (60, 20), (72, 30))) + f'<rect x="44" y="84" width="32" height="7" rx="3" fill="{C["chili"]}"/>'
    a["curry_leaves"] = '<path d="M30 96 C46 74 62 52 92 26" stroke="#4e6b2e" stroke-width="3" fill="none" stroke-linecap="round"/>' + "".join(leaf(x, y, r, .7, "#2f6b34") for x, y, r in ((40, 82, -150), (44, 80, -30), (52, 70, -150), (56, 66, -30), (64, 56, -150), (68, 52, -30), (76, 42, -150), (80, 38, -30)))
    a["lemongrass"] = f'''<g transform="rotate(-30 60 60)"><rect x="54" y="14" width="12" height="80" rx="6" fill="#d9e3a1"/><rect x="54" y="70" width="12" height="24" rx="6" fill="#efe6c2"/>
      <path d="M57 16 v54 M63 16 v54" stroke="#b9c97a" stroke-width="1.4"/><path d="M56 94 l-2 6 M60 94 v7 M64 94 l2 6" stroke="#c9b98a" stroke-width="1.6" stroke-linecap="round"/></g>'''
    a["cabbage"] = f'''<circle cx="60" cy="64" r="36" fill="#b8d98a"/><path d="M60 30 C40 44 40 84 60 100 M60 30 C80 44 80 84 60 100 M30 56 C46 60 74 60 90 56" stroke="#93bd63" stroke-width="2.4" fill="none"/>
      <path d="M26 70 C24 46 44 30 60 30 C44 40 36 56 36 72 Z" fill="#a3cc72"/>'''
    a["chinese_cabbage"] = f'''<path d="M60 18 C82 26 86 70 76 100 H44 C34 70 38 26 60 18 Z" fill="#dfeec0"/><path d="M60 18 C48 34 44 70 50 100 M60 18 C72 34 76 70 70 100" stroke="#bcd889" stroke-width="2.4" fill="none"/>
      <path d="M60 18 C78 22 88 40 84 56 C74 44 64 40 60 18 Z" fill="#9cc45f"/><path d="M60 18 C42 22 32 40 36 56 C46 44 56 40 60 18 Z" fill="#a9cd6c"/>'''
    a["taugeh"] = "".join(f'<path d="M{x} 96 C{x - 4} 76 {x + 6} 56 {x} 36" stroke="#f6f1e1" stroke-width="5" stroke-linecap="round" fill="none"/><ellipse cx="{x}" cy="34" rx="5" ry="4" fill="#f1d36b"/>' for x in (40, 52, 64, 76)) + '<path d="M36 96 H84" stroke="#e8dcc0" stroke-width="3" stroke-linecap="round"/>'
    a["long_bean"] = '<path d="M20 40 C60 20 100 40 80 60 C60 80 30 70 40 90 C46 100 80 100 96 92" stroke="#5f9c45" stroke-width="8" fill="none" stroke-linecap="round"/><path d="M20 40 C60 20 100 40 80 60" stroke="#8fbf62" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
    a["french_bean"] = "".join(f'<g transform="rotate({r} 60 60)"><path d="M24 {y} C44 {y - 6} 76 {y - 6} 96 {y}" stroke="#5f9c45" stroke-width="9" fill="none" stroke-linecap="round"/>' + "".join(f'<circle cx="{cx}" cy="{y - 4}" r="2.2" fill="#8fbf62"/>' for cx in (44, 58, 72)) + '</g>' for y, r in ((50, -12), (66, -4), (82, 6)))
    a["okra"] = f'''<g transform="rotate(-30 60 60)"><path d="M60 18 C72 30 74 80 60 102 C46 80 48 30 60 18 Z" fill="#6aa84f"/><path d="M60 22 V98 M54 30 C52 60 54 84 58 96 M66 30 C68 60 66 84 62 96" stroke="#4f8a3c" stroke-width="1.6" fill="none"/>
      <rect x="54" y="12" width="12" height="10" rx="3" fill="#4f7a34"/></g>'''
    a["brinjal"] = f'''<g transform="rotate(-25 60 60)"><path d="M60 30 C80 34 82 70 74 92 C68 104 52 104 46 92 C38 70 40 34 60 30 Z" fill="#6a3b7a"/>
      <path d="M50 44 C48 60 48 78 52 90" stroke="#9a6aaa" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M44 34 C50 24 70 24 76 34 L66 38 L60 32 L54 38 Z" fill="#4f7a34"/><path d="M60 26 V14" stroke="#4f7a34" stroke-width="4" stroke-linecap="round"/></g>'''
    a["carrot"] = f'''<g transform="rotate(30 60 60)"><path d="M48 36 H72 C72 60 66 86 60 104 C54 86 48 60 48 36 Z" fill="#f08a2c"/><path d="M52 52 h6 M62 64 h5 M54 76 h5" stroke="#d76f16" stroke-width="2" stroke-linecap="round"/>
      <path d="M54 36 C50 24 44 18 40 14 M60 36 V12 M66 36 C70 24 76 18 80 14" stroke="{C['leaf2']}" stroke-width="4" stroke-linecap="round" fill="none"/></g>'''
    a["potato"] = f'''<path d="M22 66 C20 44 46 36 66 40 C92 44 102 62 94 78 C84 96 28 94 22 66 Z" fill="#d9b27c"/>
      {''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="#b8915c"/>' for x, y in ((40, 58), (62, 52), (78, 66), (52, 76), (70, 82)))}<path d="M34 54 C44 46 58 44 70 46" stroke="#e8c999" stroke-width="3" fill="none" stroke-linecap="round"/>'''
    a["tomato"] = f'''<circle cx="60" cy="66" r="34" fill="#e2412c"/><path d="M60 34 L54 26 L60 30 L66 24 L66 32 L76 30 L68 38 L60 36 L52 40 L46 32 L56 34 Z" fill="#4f8a3c"/>
      <ellipse cx="46" cy="54" rx="6" ry="9" fill="#fff" opacity=".35" transform="rotate(30 46 54)"/>'''
    a["cucumber"] = f'''<g transform="rotate(-30 60 60)"><rect x="46" y="16" width="28" height="88" rx="14" fill="#4f8a3c"/><path d="M56 22 V98" stroke="#7cb342" stroke-width="3" stroke-linecap="round"/>
      {''.join(f'<circle cx="{x}" cy="{y}" r="1.4" fill="#c5e3a0"/>' for x, y in ((52, 34), (66, 46), (52, 60), (66, 74), (54, 88)))}</g>'''
    a["broccoli"] = f'''<path d="M52 100 L56 70 H64 L68 100 Z" fill="#8fbf62"/>
      {''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r, c in ((42, 58, 15, '#3f7a34'), (60, 48, 17, '#4f8a3c'), (78, 58, 15, '#3f7a34'), (52, 66, 12, '#5f9c45'), (70, 66, 12, '#5f9c45')))}'''
    a["cauliflower"] = f'''{leaf(28, 82, -30, 1.1)}{leaf(92, 82, -150, 1.1)}
      {''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r, c in ((44, 60, 15, '#f4ecd6'), (60, 50, 17, '#faf4e2'), (76, 60, 15, '#f4ecd6'), (52, 70, 12, '#efe5c9'), (68, 70, 12, '#efe5c9')))}'''
    a["capsicum"] = f'''<path d="M60 36 C82 34 96 52 92 74 C88 96 72 100 60 94 C48 100 32 96 28 74 C24 52 38 34 60 36 Z" fill="#d7301f"/>
      <path d="M60 40 C56 56 56 80 60 94" stroke="#a8220f" stroke-width="2.5" fill="none"/><path d="M60 36 C60 26 66 20 72 18" stroke="#4f8a3c" stroke-width="5" stroke-linecap="round" fill="none"/>
      <ellipse cx="42" cy="58" rx="5" ry="10" fill="#fff" opacity=".3" transform="rotate(20 42 58)"/>'''
    a["lime"] = f'''<circle cx="44" cy="66" r="22" fill="#7cb342"/><circle cx="44" cy="66" r="22" fill="none" stroke="#5f9c45" stroke-width="2"/>
      <circle cx="80" cy="64" r="20" fill="#7cb342"/><circle cx="80" cy="64" r="16" fill="#f3b23a"/>
      {''.join(f'<path d="M80 64 L{80 + 15 * x} {64 + 15 * y}" stroke="#f8d27a" stroke-width="1.6"/>' for x, y in ((1, 0), (0.5, 0.87), (-0.5, 0.87), (-1, 0), (-0.5, -0.87), (0.5, -0.87)))}'''
    # onions, roots, chillies
    a["shallot"] = bulb(60, 64, 1.5)
    a["onion"] = bulb(60, 64, 1.65, col="#d99b4a", line="#b97a2e", top="#c9a26a", root="#c9a26a")
    a["garlic"] = bulb(60, 64, 1.5, col=C['garlic'], line=C['garlic2'], cloves=True, outline="#cdbb98")
    a["ginger"] = f'''<path d="M22 70 C20 58 34 54 42 60 C44 46 58 42 64 52 C70 40 88 42 90 56 C100 58 102 74 90 80 C80 92 30 90 22 70 Z" fill="#d6b07a"/>
      <path d="M34 72 h10 M58 70 h10 M80 68 h6" stroke="#b78f57" stroke-width="2" stroke-linecap="round"/>'''
    a["galangal"] = f'''<path d="M22 70 C20 58 34 54 42 60 C44 46 58 42 64 52 C70 40 88 42 90 56 C100 58 102 74 90 80 C80 92 30 90 22 70 Z" fill="#e6c3a3"/>
      <path d="M34 64 v14 M52 58 v20 M70 56 v22 M86 62 v12" stroke="#d48a7a" stroke-width="2.4" stroke-linecap="round"/>'''
    a["chili_red"] = chili(62, 62, 1.2, -18)
    a["chili_green"] = chili(62, 62, 1.2, -18, col="#4f8a3c", hi="#7cb342", stem="#3f6e2e")
    a["chili_padi"] = chili(56, 52, .7, -30) + chili(66, 70, .7, 10, col="#4f8a3c", hi="#7cb342", stem="#3f6e2e") + chili(54, 84, .65, -5)
    # noodles
    a["yellow_mee"] = nest("#f2c14e", 4)
    a["kuetiau"] = nest("#f7f2e4", flat=True)
    a["bihun"] = nest("#fbf8ef", 2)
    # pantry
    a["oil"] = bottle(body="#f6e7b8", label="#ffffff", band=C['gold'], cap="#f2b33d", liquid=C['gold'])
    a["kicap_manis"] = bottle()
    a["soy_light"] = bottle(band="#4f8a3c", cap="#4f8a3c")
    a["soy_dark"] = bottle(body="#16110e", band="#1c1917", cap="#1c1917")
    a["oyster_sauce"] = bottle(body="#5a3a26", band="#3f6fa8", cap="#3f6fa8")
    a["chili_sauce"] = bottle(body="#c8301c", label="#ffffff", band="#4f8a3c", cap="#ffffff")
    a["tomato_sauce"] = bottle(body="#b8261a", label="#ffffff", band=C['red'], cap="#4f8a3c")
    a["fish_sauce"] = bottle(body="#d39a3e", label="#ffffff", band="#3f6fa8", cap="#3f6fa8")
    a["sesame_oil"] = bottle(body="#b5772e", label="#ffffff", band=C['chili'], cap=C['chili'], short=True)
    a["tomyam_paste"] = jar("#d9541e", "#f2b33d", lid="#4f8a3c")
    a["belacan"] = f'''<path d="M26 58 L60 46 L94 58 L94 82 L60 96 L26 82 Z" fill="{C['brown']}"/><path d="M26 58 L60 70 L94 58 L60 46 Z" fill="#87613f"/><path d="M60 70 V96" stroke="#4e3524" stroke-width="1.5"/>
      {''.join(f'<circle cx="{x}" cy="{y}" r="1.2" fill="#a07a52"/>' for x, y in ((40, 74), (48, 82), (72, 80), (80, 72), (52, 60), (66, 56)))}'''
    a["salt"] = jar("#eeeae2", "#cfc8bb", lid="#3f6fa8")
    a["sugar"] = heap("#fbf8f1", [(46, 72, 0), (60, 60, 0)], "#fff") + '<rect x="70" y="68" width="14" height="14" rx="2" fill="#fff" stroke="#e6d8c8" stroke-width="2"/><rect x="82" y="78" width="12" height="12" rx="2" fill="#fff" stroke="#e6d8c8" stroke-width="2"/>'
    a["cornflour"] = bag("#f6f1e6", "#f2c14e", "#b9803e")
    a["flour"] = bag("#f6f1e6", "#5b8fc7", "#ffffff")
    # spices
    a["chili_powder"] = jar("#c8301c", "#e2412c")
    a["turmeric_powder"] = jar("#e9a21f", "#f2c14e", lid="#4f8a3c")
    a["curry_meat"] = jar("#a4561f", "#c9752f")
    a["curry_fish"] = jar("#d98a2b", "#eaa94a", lid="#3f6fa8")
    a["kurma_powder"] = jar("#d6b07a", "#e8c999", lid="#4f8a3c")
    a["soup_spice"] = jar("#8a6440", "#a88058", lid="#3f6fa8")
    a["white_pepper"] = jar("#efe6cf", "#d8cba9", lid="#1c1917")
    a["black_pepper"] = '<ellipse cx="60" cy="88" rx="44" ry="10" fill="#ffffff" stroke="#e6d8c8" stroke-width="2"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="4.2" fill="#2a2522"/><circle cx="{x - 1.2}" cy="{y - 1.2}" r="1.2" fill="#5a524b"/>' for x, y in ((44, 80), (54, 72), (64, 66), (74, 74), (50, 84), (62, 82), (72, 84), (84, 82), (40, 86), (58, 88), (66, 76)))
    a["cinnamon"] = "".join(f'<g transform="rotate({r} 60 60)"><rect x="18" y="{y}" width="84" height="14" rx="7" fill="#9a5a2e"/><path d="M22 {y + 4} H98" stroke="#c07c45" stroke-width="2.5" stroke-linecap="round"/><circle cx="18" cy="{y + 7}" r="7" fill="#7a4220"/><path d="M14 {y + 7} a4 4 0 1 0 8 0" stroke="#c07c45" stroke-width="1.6" fill="none"/></g>' for y, r in ((44, -14), (62, -6)))
    a["star_anise"] = '<g transform="translate(60 62)">' + "".join(f'<g transform="rotate({i * 45})"><path d="M0 0 C6 -6 6 -26 0 -32 C-6 -26 -6 -6 0 0 Z" fill="#7a4220"/><ellipse cx="0" cy="-16" rx="2.4" ry="4" fill="#c58a4a"/></g>' for i in range(8)) + '<circle r="5" fill="#5a2e14"/></g>'
    a["fennel"] = '<ellipse cx="60" cy="88" rx="44" ry="10" fill="#ffffff" stroke="#e6d8c8" stroke-width="2"/>' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="4.5" ry="2" fill="#b7a46a" transform="rotate({r} {x} {y})"/>' for x, y, r in ((44, 74, 20), (54, 68, -30), (64, 62, 10), (74, 70, -40), (52, 80, 50), (62, 76, -10), (72, 82, 30), (84, 78, -20), (40, 84, 0), (58, 86, 60), (66, 70, 80)))
    for k, v in list(a.items()):
        a[k] = SHADOW + v
    return a


# ---------------------------------------------------------------- cooking methods
def M():
    m = {}
    m["tumis"] = SHADOW + wok() + f'''<g class="a-flip" style="transform-origin:90px 20px"><path d="M90 20 L70 54" stroke="{C['wood']}" stroke-width="5" stroke-linecap="round"/><path d="M60 56 L74 50 L78 60 L64 66 Z" fill="{C['steel']}"/></g>{steam([42, 58, 74], 50)}'''
    m["goreng"] = SHADOW + f'''<path d="M18 60 Q60 108 102 60 Z" fill="{C['wok']}"/><ellipse cx="60" cy="60" rx="42" ry="9" fill="{C['rim']}"/>
      <ellipse cx="60" cy="61" rx="37" ry="6.5" fill="{C['gold']}"/><ellipse class="a-sh" cx="60" cy="61" rx="30" ry="4.5" fill="#f9d77a"/>
      <rect x="4" y="55" width="18" height="7" rx="3.5" fill="{C['wood']}"/><g class="a-bob">{drumstick(60, 56, .8, -15)}</g>
      {bubbles([(40, 62, 2.2, 0), (50, 63, 1.6, .5), (72, 62, 2.4, .3), (82, 61, 1.8, .9), (62, 63, 1.5, 1.2)])}'''
    m["rebus"] = SHADOW + f'''<rect x="18" y="60" width="12" height="6" rx="3" fill="{C['wok']}"/><rect x="90" y="60" width="12" height="6" rx="3" fill="{C['wok']}"/>
      <rect x="26" y="52" width="68" height="46" rx="8" fill="{C['chili']}"/><rect x="26" y="64" width="68" height="5" fill="{C['chili2']}" opacity=".35"/>
      <g class="a-lid"><ellipse cx="60" cy="52" rx="38" ry="6" fill="{C['steel']}"/><rect x="54" y="42" width="12" height="7" rx="3" fill="{C['wok']}"/></g>
      {steam([30, 90], 48)}{bubbles([(36, 50, 1.8, 0), (84, 50, 2, .6)], "a-bb2")}'''
    m["kukus"] = SHADOW + f'''<rect x="24" y="76" width="72" height="22" rx="5" fill="{C['bamboo']}"/><rect x="24" y="54" width="72" height="22" rx="5" fill="{C['bamboo']}"/>
      <path d="M24 64 H96 M24 86 H96" stroke="{C['bamboo2']}" stroke-width="2.4"/>
      <path d="M34 54 v22 M50 54 v22 M66 54 v22 M82 54 v22 M34 76 v22 M50 76 v22 M66 76 v22 M82 76 v22" stroke="{C['bamboo2']}" stroke-width="1.2" opacity=".6"/>
      <path d="M22 56 Q60 22 98 56 Z" fill="#e6b873"/><path d="M40 46 Q60 34 80 46" fill="none" stroke="{C['bamboo2']}" stroke-width="2"/><circle cx="60" cy="34" r="4" fill="{C['bamboo2']}"/>
      {steam([28, 46, 76, 94], 40)}'''
    flame = lambda x, d: f'''<g class="a-fl" style="transform-origin:{x}px 102px;animation-delay:{d}s"><path d="M{x} 102 C{x - 10} 92 {x - 4} 84 {x} 76 C{x + 4} 84 {x + 10} 92 {x} 102 Z" fill="{C['orange']}"/><path d="M{x} 100 C{x - 4} 94 {x - 2} 90 {x} 86 C{x + 2} 90 {x + 4} 94 {x} 100 Z" fill="{C['gold']}"/></g>'''
    m["bakar"] = SHADOW + flame(40, 0) + flame(60, .4) + flame(80, .8) + f'''<path d="M14 70 H106" stroke="{C['wok']}" stroke-width="4" stroke-linecap="round"/>
      <path d="M24 70 v6 M44 70 v6 M64 70 v6 M84 70 v6 M100 70 v6" stroke="{C['wok']}" stroke-width="3"/>
      <g class="a-bob">{fish(58, 56, .95)}<path d="M38 52 l6 8 M50 50 l6 9 M62 50 l6 9" stroke="#3a3a3a" stroke-width="2" stroke-linecap="round" opacity=".55"/></g>'''
    m["kacau"] = SHADOW + f'''<rect x="16" y="62" width="12" height="6" rx="3" fill="{C['wok']}"/><rect x="92" y="62" width="12" height="6" rx="3" fill="{C['wok']}"/>
      <path d="M24 58 H96 V88 Q96 100 84 100 H36 Q24 100 24 88 Z" fill="{C['steel2']}"/>
      <ellipse cx="60" cy="58" rx="36" ry="7" fill="{C['steel']}"/><ellipse cx="60" cy="59" rx="32" ry="5.2" fill="{C['turmeric']}"/>
      <ellipse class="a-sh" cx="50" cy="59" rx="6" ry="1.4" fill="#f7cf6a"/>
      <g class="a-circ"><path d="M66 58 L84 16" stroke="{C['wood']}" stroke-width="5" stroke-linecap="round"/><ellipse cx="65" cy="59" rx="6" ry="3" fill="{C['wood2']}"/></g>{steam([40, 56], 50)}'''
    m["tumbuk"] = SHADOW + f'''<g class="a-pound"><rect x="52" y="18" width="16" height="44" rx="8" fill="{C['steel']}"/><rect x="55" y="22" width="4" height="30" rx="2" fill="#d6d2cc"/></g>
      <path d="M22 60 H98 C98 86 82 100 60 100 C38 100 22 86 22 60 Z" fill="{C['steel2']}"/>
      <ellipse cx="60" cy="60" rx="38" ry="8" fill="#a9a39d"/><ellipse cx="60" cy="61" rx="31" ry="5.5" fill="#6f6a65"/>
      <circle cx="48" cy="61" r="3" fill="{C['red']}"/><circle cx="58" cy="62" r="2.6" fill="{C['shallot']}"/><circle cx="70" cy="60.5" r="3" fill="{C['red']}"/><circle cx="64" cy="62.5" r="2" fill="{C['garlic']}"/>
      <g class="a-spark"><circle cx="40" cy="52" r="1.8" fill="{C['red']}"/><circle cx="80" cy="50" r="1.6" fill="{C['shallot']}"/></g>'''
    m["gaul"] = SHADOW + f'''<g class="a-hop">{leaf(32, 52, -20, .9)}</g><g class="a-hop" style="animation-delay:.25s">{chili(70, 48, .4, 20)}</g>
      <g class="a-hop" style="animation-delay:.5s">{leaf(58, 46, 15, .8, C['leaf2'])}</g><g class="a-hop" style="animation-delay:.75s"><circle cx="46" cy="50" r="3" fill="{C['red']}"/></g>
      <path d="M16 58 H104 C104 84 86 100 60 100 C34 100 16 84 16 58 Z" fill="#ffffff" stroke="#e6d8c8" stroke-width="2"/>
      <ellipse cx="60" cy="58" rx="44" ry="7" fill="#f4ede4"/><ellipse cx="60" cy="59" rx="38" ry="4.5" fill="{C['leaf']}" opacity=".85"/>
      <path d="M24 70 Q60 82 96 70" fill="none" stroke="#5b8fc7" stroke-width="3"/><path d="M30 78 Q60 88 90 78" fill="none" stroke="#5b8fc7" stroke-width="1.5" opacity=".7"/>'''
    m["prep"] = SHADOW + f'''<rect x="14" y="68" width="92" height="28" rx="8" fill="{C['bamboo']}"/><circle cx="96" cy="82" r="4" fill="{C['bamboo2']}"/>
      <g class="a-chop" style="transform-origin:30px 64px"><path d="M30 64 L78 52 L84 62 L34 70 Z" fill="{C['steel']}"/><path d="M78 52 L100 46" stroke="{C['wok']}" stroke-width="7" stroke-linecap="round"/></g>
      {''.join(f'<circle cx="{x}" cy="78" r="3.4" fill="{C["red"]}"/><circle cx="{x}" cy="78" r="1.4" fill="#ffd2c4"/>' for x in (38, 48, 58))}'''
    m["serve"] = SHADOW + f'''<ellipse cx="60" cy="78" rx="48" ry="18" fill="#ffffff" stroke="#e6d8c8" stroke-width="2"/><ellipse cx="60" cy="76" rx="36" ry="11" fill="#f3ead8"/>
      <path d="M36 74 C44 62 76 62 84 74 C76 82 44 82 36 74 Z" fill="{C['chili']}"/>{leaf(66, 66, -30, .5)}<circle cx="50" cy="70" r="2" fill="{C['red']}"/>{steam([46, 60, 74], 58)}'''
    return m


ART_CSS = """
.art{display:block}.art svg{display:block;width:100%;height:auto;overflow:visible}
.art *{transform-box:view-box}
@keyframes a-rise{0%{transform:translateY(6px);opacity:0}25%{opacity:.85}100%{transform:translateY(-16px);opacity:0}}
.a-st{animation:a-rise 2.6s ease-in infinite}
@keyframes a-bub{0%{transform:translateY(0);opacity:0}20%{opacity:1}100%{transform:translateY(-18px);opacity:0}}
.a-bb{animation:a-bub 1.6s ease-out infinite}.a-bb2{animation:a-bub 2.4s ease-out infinite}
@keyframes a-shim{0%,100%{opacity:.25}50%{opacity:.95}}.a-sh{animation:a-shim 1.8s ease-in-out infinite}
@keyframes a-flip{0%,100%{transform:rotate(-8deg)}50%{transform:rotate(10deg)}}.a-flip{animation:a-flip 1.6s ease-in-out infinite}
@keyframes a-bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}.a-bob{animation:a-bob 3.2s ease-in-out infinite}
@keyframes a-lid{0%,70%,100%{transform:translateY(0) rotate(0)}76%{transform:translateY(-4px) rotate(-3deg)}82%{transform:translateY(0) rotate(0)}88%{transform:translateY(-3px) rotate(2deg)}}
.a-lid{transform-origin:60px 52px;animation:a-lid 2.8s ease-in-out infinite}
@keyframes a-fl{0%,100%{transform:scaleY(1)}50%{transform:scaleY(.82)}}.a-fl{animation:a-fl .9s ease-in-out infinite}
@keyframes a-circ{0%{transform:translate(0,0) rotate(0)}25%{transform:translate(-6px,1px) rotate(-6deg)}50%{transform:translate(-10px,0) rotate(-2deg)}75%{transform:translate(-4px,-1px) rotate(4deg)}100%{transform:translate(0,0) rotate(0)}}
.a-circ{animation:a-circ 2.4s ease-in-out infinite}
@keyframes a-pound{0%,100%{transform:translateY(-10px)}45%{transform:translateY(-10px)}60%{transform:translateY(8px)}70%{transform:translateY(6px)}}
.a-pound{animation:a-pound 1.4s cubic-bezier(.5,0,.6,1) infinite}
@keyframes a-spark{0%,55%{opacity:0;transform:translateY(0)}62%{opacity:1}100%{opacity:0;transform:translateY(-8px)}}.a-spark{animation:a-spark 1.4s ease-out infinite}
@keyframes a-hop{0%,100%{transform:translateY(0)}40%{transform:translateY(-12px)}60%{transform:translateY(-10px)}}.a-hop{animation:a-hop 1.8s ease-in-out infinite}
@keyframes a-chop{0%,100%{transform:rotate(0)}30%{transform:rotate(-14deg)}45%{transform:rotate(1deg)}}.a-chop{animation:a-chop 1.3s ease-in-out infinite}
@keyframes a-gl{0%,80%,100%{opacity:0}88%{opacity:.6}}.a-gl{animation:a-gl 4s ease-in-out infinite}
@keyframes a-drip{0%{transform:translateY(-6px);opacity:0}30%{opacity:1}70%{transform:translateY(8px);opacity:1}100%{transform:translateY(14px);opacity:0}}.a-drip{animation:a-drip 2.6s ease-in infinite}
@keyframes a-idle{0%,100%{transform:translateY(0) rotate(0)}50%{transform:translateY(-3px) rotate(-1.5deg)}}.a-idle{transform-origin:60px 100px;animation:a-idle 4s ease-in-out infinite}
@media (prefers-reduced-motion: reduce){.art *{animation:none!important}}
"""


def build(ingredient_keys):
    ing = I()
    missing = [k for k in ingredient_keys if k not in ing]
    if missing:
        raise SystemExit(f"art_lib: no drawing for {missing}")
    return {"ing": ing, "method": M()}
