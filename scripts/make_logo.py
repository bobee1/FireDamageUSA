"""Builds SootMend logo SVGs. Wordmark: Inter Display ExtraBold (SIL OFL) converted to outlines.

Mark: a house outline (the property) holding an ember flame, with a small four-point
sparkle for "cleaned and mended". Colors: soot #211c1b, ember #c42b20, white.
Run: python3 scripts/make_logo.py src/static/img/brand
"""
import os
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

SOOT, EMBER, WHITE, EMBER_SOFT, SOOT_SOFT = "#211c1b", "#c42b20", "#ffffff", "#ff9b82", "#3a2f2c"
font = TTFont("/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf")
gs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
upm = font["head"].unitsPerEm


def text_paths(text, size, x0, baseline, tracking=-0.02):
    s = size / upm
    out, x = [], x0
    for ch in text:
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x, baseline)))
        out.append(pen.getCommands())
        x += hmtx[g][0] * s + tracking * size
    return out, x - tracking * size


# ---- the mark (viewBox 64x64)
HOUSE = "M32 4.5 4.5 27.2c-1.7 1.4-.7 4.1 1.5 4.1H10V56a3.5 3.5 0 0 0 3.5 3.5h37A3.5 3.5 0 0 0 54 56V31.3h4c2.2 0 3.2-2.7 1.5-4.1L32 4.5z"
FLAME = ("M32.6 23.5c1.2 5.2 6.9 8.2 7.6 14.4.8 6.6-3.6 12.6-8.6 12.6-5.3 0-9.1-4.4-8.7-9.8.3-3.9 2.6-6.4 4.3-8.2"
         " .3 2.3 1.2 4 2.9 4.6-.4-5.4.6-9.4 2.5-13.6z")
INNER = "M32 40.5c1.6 1.8 3 3.3 2.8 5.4-.2 1.9-1.4 3-3 3-1.8 0-3-1.3-2.9-3.1.1-1.7 1.4-3.2 3.1-5.3z"
SPARK = "M48.5 9.5c.5 3 1.5 4 4.5 4.5-3 .5-4 1.5-4.5 4.5-.5-3-1.5-4-4.5-4.5 3-.5 4-1.5 4.5-4.5z"


def mark(house, flame, inner, spark, small=False):
    sp = "" if small else f'<path d="{SPARK}" fill="{spark}"/>'
    inn = "" if small else f'<path d="{INNER}" fill="{inner}"/>'
    return f'<path d="{HOUSE}" fill="{house}"/><path d="{FLAME}" fill="{flame}"/>{inn}{sp}'


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')


OUT = sys.argv[1] if len(sys.argv) > 1 else "."
files = {}
files["sootmend-mark.svg"] = svg(64, 64, mark(SOOT, EMBER, "#ffd0c4", EMBER), "SootMend")
files["sootmend-mark-small.svg"] = svg(64, 64, mark(SOOT, EMBER, "#ffd0c4", EMBER, small=True), "SootMend")
files["sootmend-app-icon.svg"] = svg(64, 64,
    f'<rect width="64" height="64" rx="14" fill="{SOOT}"/><g transform="translate(8 7) scale(.75)">'
    f'{mark(WHITE, EMBER, "#ffd0c4", EMBER_SOFT)}</g>', "SootMend")
files["sootmend-app-icon-small.svg"] = svg(64, 64,
    f'<rect width="64" height="64" rx="14" fill="{SOOT}"/><g transform="translate(6.4 5.6) scale(.8)">'
    f'{mark(WHITE, EMBER, "#ffd0c4", EMBER_SOFT, small=True)}</g>', "SootMend")


def lockup(soot_c, mend_c, house, flame, inner, spark):
    size, base = 46, 48
    a, x = text_paths("Soot", size, 76, base)
    b, x2 = text_paths("Mend", size, x + 0.5, base)
    w = int(x2 + 4)
    body = (mark(house, flame, inner, spark) + f'<g fill="{soot_c}">' + "".join(f'<path d="{d}"/>' for d in a)
            + f'</g><g fill="{mend_c}">' + "".join(f'<path d="{d}"/>' for d in b) + "</g>")
    return svg(w, 64, body, "SootMend"), w


files["sootmend-logo.svg"], W = lockup(SOOT, EMBER, SOOT, EMBER, "#ffd0c4", EMBER)
files["sootmend-logo-reversed.svg"], _ = lockup(WHITE, EMBER_SOFT, WHITE, EMBER, "#ffd0c4", EMBER_SOFT)

# single-ink versions (one colour: set CSS color, or use as a stamp)
files["sootmend-mark-mono.svg"] = svg(64, 64,
    '<defs><mask id="m"><rect width="64" height="64" fill="#fff"/>'
    f'<path d="{FLAME}" fill="#000"/></mask></defs>'
    f'<path d="{HOUSE}" fill="currentColor" mask="url(#m)"/><path d="{SPARK}" fill="currentColor"/>', "SootMend")
mono, _ = lockup("currentColor", "currentColor", "currentColor", "#fff", "#fff", "currentColor")
start = mono.index('<path d="M32 4.5'); end = mono.index('<g fill=')
mono_mark = files["sootmend-mark-mono.svg"].split("<title>SootMend</title>")[1].replace("</svg>\n", "")
files["sootmend-logo-mono.svg"] = mono[:start] + mono_mark + mono[end:]


# stacked lockup: mark above the wordmark, for square spaces (social avatars, signage)
def stacked(soot_c, mend_c, house, flame, inner, spark):
    size, base = 40, 132
    a, x = text_paths("Soot", size, 0, base)
    b, x2 = text_paths("Mend", size, x + 0.5, base)
    w = int(x2 + 2)
    off = (w - 80) / 2
    body = (f'<g transform="translate({off:.1f} 0) scale(1.25)">{mark(house, flame, inner, spark)}</g>'
            + f'<g fill="{soot_c}">' + "".join(f'<path d="{d}"/>' for d in a)
            + f'</g><g fill="{mend_c}">' + "".join(f'<path d="{d}"/>' for d in b) + "</g>")
    return svg(w, 142, body, "SootMend")


files["sootmend-logo-stacked.svg"] = stacked(SOOT, EMBER, SOOT, EMBER, "#ffd0c4", EMBER)

for name, data in files.items():
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(data)
print("lockup width", W)
