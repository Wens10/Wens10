"""Génère les SVG animés du profil (versions sombre et claire).

Palette alignée sur https://wenceslas-bouity.ovh (assets/css/style.css).
Usage : python scripts/gen_assets.py
"""
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

BLUE, CYAN, PURPLE = "#2564CF", "#00B7C3", "#8764B8"

THEMES = {
    "dark": dict(bg="#0A0E1A", soft="#10151F", card="#151B28", txt="#F3F6FB",
                 muted="#99A3B5", faint="#6B7688", border="#232B3D", grid=0.13, glow=0.55),
    "light": dict(bg="#F6F7FB", soft="#EEF1F7", card="#FFFFFF", txt="#1B1F2A",
                  muted="#5B6272", faint="#8A93A3", border="#E2E6EF", grid=0.10, glow=0.30),
}

SANS = "'Segoe UI Variable Display','Segoe UI',Inter,system-ui,-apple-system,sans-serif"
MONO = "'DM Mono','Fira Code','JetBrains Mono',Consolas,monospace"


def wave_gradient(gid, animate=True):
    anim = ('<animateTransform attributeName="gradientTransform" type="translate" '
            'values="-1 0;1 0" dur="8s" repeatCount="indefinite"/>') if animate else ""
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0" spreadMethod="reflect">'
            f'<stop offset="0" stop-color="{BLUE}"/><stop offset="0.5" stop-color="{CYAN}"/>'
            f'<stop offset="1" stop-color="{PURPLE}"/>{anim}</linearGradient>')


def brackets(x0, y0, x1, y1, size, color, width=2):
    s = size
    d = (f"M{x0} {y0+s}V{y0}H{x0+s} M{x1-s} {y0}H{x1}V{y0+s} "
         f"M{x1} {y1-s}V{y1}H{x1-s} M{x0+s} {y1}H{x0}V{y1-s}")
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="square"/>'


def chip(x, y, label, t, color):
    w = int(len(label) * 7.9) + 34
    return (w, f'<g transform="translate({x} {y})">'
               f'<rect width="{w}" height="30" rx="6" fill="{t["card"]}" fill-opacity="0.75" stroke="{color}" stroke-opacity="0.55"/>'
               f'<circle cx="14" cy="15" r="3" fill="{color}"/>'
               f'<text x="24" y="20" font-family="{MONO}" font-size="13" fill="{t["txt"]}" letter-spacing="0.5">{label}</text></g>')


def neural_net(t, rng):
    layers_x = [880, 965, 1050, 1130]
    counts = [4, 6, 6, 3]
    nodes = []
    for x, n in zip(layers_x, counts):
        top, bottom = 105, 300
        step = (bottom - top) / (n - 1)
        nodes.append([(x, round(top + i * step)) for i in range(n)])
    edges = [(a, b) for l in range(len(nodes) - 1) for a in nodes[l] for b in nodes[l + 1]]
    parts = [f'<g stroke="{t["muted"]}" stroke-opacity="0.18" stroke-width="1">']
    parts += [f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>' for a, b in edges]
    parts.append("</g>")
    colors = [CYAN, BLUE, PURPLE]
    for i, (a, b) in enumerate(rng.sample(edges, 16)):
        c = colors[i % 3]
        dur = round(rng.uniform(1.6, 3.2), 2)
        begin = round(rng.uniform(0, 3), 2)
        parts.append(f'<circle r="2.6" fill="{c}" filter="url(#glow)">'
                     f'<animateMotion path="M{a[0]} {a[1]}L{b[0]} {b[1]}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="0;1;1;0" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></circle>')
    for li, layer in enumerate(nodes):
        for (x, y) in layer:
            c = colors[(li + y) % 3]
            d = round(rng.uniform(1.8, 3.6), 2)
            parts.append(f'<circle cx="{x}" cy="{y}" r="5.5" fill="{t["card"]}" stroke="{c}" stroke-width="1.8">'
                         f'<animate attributeName="r" values="5;6.5;5" dur="{d}s" repeatCount="indefinite"/></circle>'
                         f'<circle cx="{x}" cy="{y}" r="2" fill="{c}"/>')
    labels = ["LLM", "AGENT", "TOOLS"]
    for (x, y), lab in zip(nodes[-1], labels):
        parts.append(f'<text x="{x + 12}" y="{y + 4}" font-family="{MONO}" font-size="10" fill="{t["muted"]}" letter-spacing="1">{lab}</text>')
    parts.append(f'<text x="880" y="335" font-family="{MONO}" font-size="10" fill="{t["faint"]}" letter-spacing="2">NEURAL.CORE // INFERENCE ACTIVE</text>')
    return "".join(parts)


def hero(name, t):
    rng = random.Random(10)
    W, H = 1200, 380
    chips_svg, x = [], 70
    for label, c in [("ECE PARIS · BACHELOR 3 IA", CYAN), ("ALTERNANCE 2026–2027", BLUE), ("PARIS · FRANCE", PURPLE)]:
        w, s = chip(x, 318, label, t, c)
        chips_svg.append(s)
        x += w + 12
    name_font = f'font-family="{SANS}" font-size="78" font-weight="800" letter-spacing="6"'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Wenceslas Bouity — Développeur IA générative">
<defs>
{wave_gradient("wave")}
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{BLUE}" stroke-opacity="{t["grid"]}"/></pattern>
<radialGradient id="gB"><stop offset="0" stop-color="{BLUE}" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<radialGradient id="gC"><stop offset="0" stop-color="{CYAN}" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<radialGradient id="gP"><stop offset="0" stop-color="{PURPLE}" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></radialGradient>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="0.5" stop-color="{CYAN}" stop-opacity="0.16"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
<linearGradient id="fadeGrid" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0.35"/><stop offset="0.6" stop-color="#fff" stop-opacity="1"/></linearGradient>
<mask id="gridMask"><rect width="{W}" height="{H}" fill="url(#fadeGrid)"/></mask>
<clipPath id="frame"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="22"/></clipPath>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="{t["bg"]}"/>
<rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gridMask)"/>
<ellipse cx="180" cy="60" rx="320" ry="200" fill="url(#gB)"><animate attributeName="cx" values="180;320;180" dur="14s" repeatCount="indefinite"/></ellipse>
<ellipse cx="1000" cy="330" rx="360" ry="220" fill="url(#gP)"><animate attributeName="cx" values="1000;860;1000" dur="16s" repeatCount="indefinite"/></ellipse>
<ellipse cx="640" cy="200" rx="260" ry="160" fill="url(#gC)" opacity="0.6"><animate attributeName="opacity" values="0.35;0.7;0.35" dur="7s" repeatCount="indefinite"/></ellipse>
{neural_net(t, rng)}
<rect x="0" y="-140" width="{W}" height="140" fill="url(#scan)"><animate attributeName="y" values="-140;{H}" dur="5.5s" repeatCount="indefinite"/></rect>
</g>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="22" fill="none" stroke="url(#wave)" stroke-width="1.5" stroke-opacity="0.9"/>
{brackets(18, 18, W-18, H-18, 26, CYAN)}
<text x="70" y="66" font-family="{MONO}" font-size="13" fill="{t["muted"]}" letter-spacing="2.5">SYS://GITHUB.COM/WENS10  ·  NODE PARIS-FR  ·  BUILD 2026.09</text>
<g transform="translate({W-250} 57)">
<circle cx="0" cy="4" r="5" fill="{CYAN}"><animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/></circle>
<circle cx="0" cy="4" r="5" fill="none" stroke="{CYAN}"><animate attributeName="r" values="5;14" dur="1.6s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.8;0" dur="1.6s" repeatCount="indefinite"/></circle>
<text x="16" y="9" font-family="{MONO}" font-size="13" fill="{CYAN}" letter-spacing="2">ONLINE · OPEN TO WORK</text>
</g>
<text x="66" y="160" {name_font} fill="{t["txt"]}">WENCESLAS</text>
<g {name_font}>
<text x="68" y="244" fill="{CYAN}" opacity="0"><animate attributeName="opacity" values="0;0;0.8;0;0.6;0;0" keyTimes="0;0.86;0.88;0.9;0.92;0.94;1" dur="5s" repeatCount="indefinite"/><animate attributeName="x" values="68;72;63;68" dur="0.25s" repeatCount="indefinite"/>BOUITY</text>
<text x="64" y="244" fill="{PURPLE}" opacity="0"><animate attributeName="opacity" values="0;0;0.8;0;0.6;0;0" keyTimes="0;0.86;0.88;0.9;0.92;0.94;1" dur="5s" repeatCount="indefinite"/>BOUITY</text>
<text x="66" y="244" fill="url(#wave)">BOUITY</text>
</g>
<text x="70" y="290" font-family="{MONO}" font-size="19" fill="{t["txt"]}" letter-spacing="1"><tspan fill="{CYAN}">&gt; </tspan>GENERATIVE_AI_DEVELOPER <tspan fill="{t["muted"]}">::</tspan> LLM · AGENTS IA · FULL STACK<tspan fill="{CYAN}"> ▋<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/></tspan></text>
{"".join(chips_svg)}
</svg>'''


def header(num, title, code, t):
    W, H = 1200, 96
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title}">
<defs>{wave_gradient("wave")}
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<g transform="translate(14 30)">
<path d="M0 -10L10 0L0 10L-10 0Z" fill="none" stroke="{CYAN}" stroke-width="1.6"><animateTransform attributeName="transform" type="rotate" values="0;90;90;180" keyTimes="0;0.2;0.5;1" dur="4s" repeatCount="indefinite"/></path>
<circle r="3" fill="{CYAN}"><animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/></circle>
</g>
<text x="38" y="35" font-family="{MONO}" font-size="14" letter-spacing="3"><tspan fill="{CYAN}">[{num}]</tspan><tspan fill="{t["muted"]}">  // {code}</tspan></text>
<text x="36" y="74" font-family="{SANS}" font-size="32" font-weight="800" letter-spacing="3" fill="{t["txt"]}">{title}</text>
<rect x="0" y="91" width="{W}" height="2" fill="url(#wave)" fill-opacity="0.85"/>
<g fill="{t["faint"]}">{"".join(f'<rect x="{x}" y="84" width="2" height="5"/>' for x in range(W - 300, W, 12))}</g>
<circle cy="92" r="4" fill="{CYAN}" filter="url(#glow)"><animate attributeName="cx" values="0;{W}" dur="6s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.95;1" dur="6s" repeatCount="indefinite"/></circle>
</svg>'''


def footer(t):
    W, H = 1200, 170
    pts = " ".join(f"L{x} {85 + 26 * math.sin(x / 38) * math.sin(x / 290)}" for x in range(0, W + 1, 6))
    wave_path = "M" + pts[1:]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Fin de transmission — wenceslas-bouity.ovh">
<defs>{wave_gradient("wave")}
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{BLUE}" stroke-opacity="{t["grid"]}"/></pattern>
<clipPath id="frame"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="22"/></clipPath></defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="{t["bg"]}"/>
<rect width="{W}" height="{H}" fill="url(#grid)"/>
<path d="{wave_path}" fill="none" stroke="url(#wave)" stroke-width="2" stroke-opacity="0.5" stroke-dasharray="14 8"><animate attributeName="stroke-dashoffset" values="0;-220" dur="3s" repeatCount="indefinite"/></path>
</g>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="22" fill="none" stroke="url(#wave)" stroke-width="1.5"/>
{brackets(16, 16, W-16, H-16, 20, CYAN)}
<rect x="{W/2-230}" y="52" width="460" height="68" rx="12" fill="{t["bg"]}" fill-opacity="0.9" stroke="{t["border"]}"/>
<text x="{W/2}" y="78" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t["muted"]}" letter-spacing="4">END OF TRANSMISSION<tspan fill="{CYAN}"> ▋<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/></tspan></text>
<text x="{W/2}" y="106" text-anchor="middle" font-family="{SANS}" font-size="22" font-weight="800" letter-spacing="2" fill="url(#wave)">wenceslas-bouity.ovh</text>
</svg>'''


SECTIONS = [
    ("01", "À PROPOS", "SYSTEM.PROFILE"),
    ("02", "EXPÉRIENCES", "LOG.EXPERIENCE"),
    ("03", "PROJETS", "PROJECTS.DEPLOYED"),
    ("04", "STACK", "MODULES.LOADED"),
    ("05", "TÉLÉMÉTRIE", "GITHUB.METRICS"),
    ("06", "CONTRIBUTIONS", "SNAKE.EXE"),
]

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for mode, t in THEMES.items():
        (OUT / f"hero-{mode}.svg").write_text(hero("Wenceslas Bouity", t), encoding="utf-8")
        (OUT / f"footer-{mode}.svg").write_text(footer(t), encoding="utf-8")
        for num, title, code in SECTIONS:
            (OUT / f"section-{num}-{mode}.svg").write_text(header(num, title, code, t), encoding="utf-8")
    print("ok:", sorted(p.name for p in OUT.iterdir()))
