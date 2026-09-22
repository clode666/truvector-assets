# -*- coding: utf-8 -*-
"""Génère 21 couvertures SVG (800x1200, ratio 2:3) aux couleurs TRUvector.
Chaque motif est déterministe (seed = numéro du livre) → visuel unique et reproductible.
"""
import math, random, html, os
from data import BOOKS

W, H = 800, 1200
OUT = "/home/claude/build/truvector-assets/ebooks/covers"
os.makedirs(OUT, exist_ok=True)

def esc(s): return html.escape(s, quote=True)

def hex_to_rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i+2],16) for i in (0,2,4))

def rgba(h, a):
    r,g,b = hex_to_rgb(h); return f"rgba({r},{g},{b},{a})"

# ---------- motifs procéduraux ----------
def m_grid(rng, acc):
    p = []
    for i in range(0, W+1, 40):
        o = round(rng.uniform(.04,.16),3)
        p.append(f'<line x1="{i}" y1="0" x2="{i}" y2="{H}" stroke="{rgba(acc,o)}" stroke-width="1"/>')
    for j in range(0, H+1, 40):
        o = round(rng.uniform(.04,.16),3)
        p.append(f'<line x1="0" y1="{j}" x2="{W}" y2="{j}" stroke="{rgba(acc,o)}" stroke-width="1"/>')
    for _ in range(9):
        x=rng.randrange(0,W,40); y=rng.randrange(0,H,40)
        p.append(f'<rect x="{x}" y="{y}" width="40" height="40" fill="{rgba(acc,round(rng.uniform(.08,.22),3))}"/>')
    return "".join(p)

def m_orbit(rng, acc):
    cx,cy = W*0.5, H*0.42; p=[]
    for k in range(5):
        r = 90 + k*70 + rng.uniform(-14,14)
        p.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r:.0f}" ry="{r*rng.uniform(.5,.8):.0f}" '
                 f'fill="none" stroke="{rgba(acc,.22)}" stroke-width="1.4" transform="rotate({rng.uniform(0,180):.0f} {cx:.0f} {cy:.0f})"/>')
        ang = rng.uniform(0,6.28)
        px = cx + math.cos(ang)*r; py = cy + math.sin(ang)*r*.65
        p.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rng.uniform(3,7):.0f}" fill="{acc}"/>')
    p.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="16" fill="{acc}"/>')
    p.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="30" fill="none" stroke="{rgba(acc,.5)}" stroke-width="1"/>')
    return "".join(p)

def m_rain(rng, acc):  # pluie de code cyberpunk
    p=[]; cols=list(range(20,W,34))
    for x in cols:
        y = rng.uniform(-300,200); n=rng.randint(6,16)
        for i in range(n):
            o = max(.05, .9 - i*0.08)
            yy = y + i*26
            if 0 < yy < H:
                p.append(f'<text x="{x}" y="{yy:.0f}" font-family="monospace" font-size="18" '
                         f'fill="{rgba(acc,round(o,2))}">{rng.choice("01")}</text>')
    return "".join(p)

def m_roots(rng, acc):  # racines / lianes qui montent
    p=[]
    def branch(x,y,ang,length,depth):
        if depth<=0 or length<6: return
        x2 = x + math.cos(ang)*length; y2 = y + math.sin(ang)*length
        w = max(1, depth*0.9)
        p.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
                 f'stroke="{rgba(acc,.3)}" stroke-width="{w:.1f}" stroke-linecap="round"/>')
        if rng.random()<.85: branch(x2,y2,ang-rng.uniform(.15,.6),length*.8,depth-1)
        if rng.random()<.85: branch(x2,y2,ang+rng.uniform(.15,.6),length*.8,depth-1)
    for bx in (W*0.25, W*0.5, W*0.75):
        branch(bx, H, -math.pi/2 + rng.uniform(-.3,.3), rng.uniform(70,110), 7)
    for _ in range(14):
        p.append(f'<circle cx="{rng.randrange(60,W-60)}" cy="{rng.randrange(120,H-160)}" r="{rng.uniform(2,5):.0f}" fill="{rgba(acc,.5)}"/>')
    return "".join(p)

def m_stars(rng, acc):
    p=[]
    for _ in range(160):
        x=rng.randrange(0,W); y=rng.randrange(0,H)
        r=rng.uniform(.6,2.6); o=round(rng.uniform(.25,1),2)
        p.append(f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="{rgba(acc,o)}"/>')
    # constellation
    pts=[(rng.randrange(120,W-120), rng.randrange(180,H-260)) for _ in range(6)]
    for i in range(len(pts)-1):
        p.append(f'<line x1="{pts[i][0]}" y1="{pts[i][1]}" x2="{pts[i+1][0]}" y2="{pts[i+1][1]}" stroke="{rgba(acc,.4)}" stroke-width="1"/>')
    for (x,y) in pts:
        p.append(f'<circle cx="{x}" cy="{y}" r="3.4" fill="{acc}"/>')
    return "".join(p)

def m_clock(rng, acc):
    cx,cy=W*0.5,H*0.42; p=[]
    for r in (150,110,70):
        p.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="none" stroke="{rgba(acc,.25)}" stroke-width="1.2"/>')
    for i in range(60):
        a=i/60*2*math.pi; r1=150; r2=150-(10 if i%5 else 20)
        p.append(f'<line x1="{cx+math.cos(a)*r1:.0f}" y1="{cy+math.sin(a)*r1:.0f}" '
                 f'x2="{cx+math.cos(a)*r2:.0f}" y2="{cy+math.sin(a)*r2:.0f}" stroke="{rgba(acc,.4)}" stroke-width="1"/>')
    for (ln,wd,a) in [(120,3,rng.uniform(0,6.28)),(80,4,rng.uniform(0,6.28))]:
        p.append(f'<line x1="{cx:.0f}" y1="{cy:.0f}" x2="{cx+math.cos(a)*ln:.0f}" y2="{cy+math.sin(a)*ln:.0f}" '
                 f'stroke="{acc}" stroke-width="{wd}" stroke-linecap="round"/>')
    p.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="6" fill="{acc}"/>')
    return "".join(p)

def m_wave(rng, acc):
    p=[]
    for k in range(7):
        base=200+k*120; amp=rng.uniform(20,60); ph=rng.uniform(0,6.28); step=8
        d=f'M 0 {base:.0f}'
        for x in range(0,W+step,step):
            y=base+math.sin(x/90+ph)*amp
            d+=f' L {x} {y:.0f}'
        p.append(f'<path d="{d}" fill="none" stroke="{rgba(acc,round(rng.uniform(.12,.3),2))}" stroke-width="1.4"/>')
    return "".join(p)

def m_lines(rng, acc):  # trames diagonales / faisceaux
    p=[]
    for _ in range(26):
        x1=rng.randrange(-100,W); y1=rng.randrange(0,H)
        ln=rng.uniform(200,700); a=rng.uniform(-.5,.5)
        x2=x1+math.cos(a)*ln; y2=y1+math.sin(a)*ln
        p.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
                 f'stroke="{rgba(acc,round(rng.uniform(.05,.2),2))}" stroke-width="1"/>')
    return "".join(p)

def m_bloom(rng, acc):  # fleur géométrique
    cx,cy=W*0.5,H*0.42; p=[]
    petals=rng.choice([8,10,12])
    for i in range(petals):
        a=i/petals*2*math.pi
        for r in (60,120,180):
            x=cx+math.cos(a)*r; y=cy+math.sin(a)*r
            p.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r*0.34:.0f}" fill="none" stroke="{rgba(acc,.18)}" stroke-width="1.2"/>')
    p.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="14" fill="{acc}"/>')
    for _ in range(20):
        a=rng.uniform(0,6.28); r=rng.uniform(0,210)
        p.append(f'<circle cx="{cx+math.cos(a)*r:.0f}" cy="{cy+math.sin(a)*r:.0f}" r="{rng.uniform(1.5,3.5):.0f}" fill="{rgba(acc,.6)}"/>')
    return "".join(p)

def m_maze(rng, acc):
    p=[]; g=48
    for x in range(0,W,g):
        for y in range(0,H,g):
            if rng.random()<.5:
                p.append(f'<line x1="{x}" y1="{y}" x2="{x+g}" y2="{y+g}" stroke="{rgba(acc,.2)}" stroke-width="1.4"/>')
            else:
                p.append(f'<line x1="{x+g}" y1="{y}" x2="{x}" y2="{y+g}" stroke="{rgba(acc,.2)}" stroke-width="1.4"/>')
    return "".join(p)

MOTIFS = dict(grid=m_grid, orbit=m_orbit, rain=m_rain, roots=m_roots, stars=m_stars,
              clock=m_clock, wave=m_wave, lines=m_lines, bloom=m_bloom, maze=m_maze)

TRISKELE = ('<g transform="translate({tx},{ty}) scale({s})">'
 '<g fill="none" stroke="{acc}" stroke-width="7" stroke-linecap="round">'
 '<path d="M100,100 C96,80 108,60 132,60 C156,60 168,82 156,103 C148,118 130,120 120,109 C114,102 116,91 125,89"/>'
 '<path transform="rotate(120 100 100)" d="M100,100 C96,80 108,60 132,60 C156,60 168,82 156,103 C148,118 130,120 120,109 C114,102 116,91 125,89"/>'
 '<path transform="rotate(240 100 100)" d="M100,100 C96,80 108,60 132,60 C156,60 168,82 156,103 C148,118 130,120 120,109 C114,102 116,91 125,89"/>'
 '</g><circle cx="100" cy="100" r="5" fill="{acc}"/></g>')

def wrap_title(title, maxlen=15):
    words=title.split(); lines=[]; cur=""
    for w in words:
        if len(cur)+len(w)+1<=maxlen: cur=(cur+" "+w).strip()
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines[:3]

def build(b):
    rng=random.Random(b["n"]*7919)
    acc=b["accent"]
    motif=MOTIFS[b["motif"]](rng, acc)
    # titre
    lines=wrap_title(b["title"])
    fs = 64 if max(len(l) for l in lines)<=12 else 54
    ty = 900
    title_svg=""
    for i,l in enumerate(lines):
        title_svg+=(f'<text x="60" y="{ty+i*(fs+8)}" font-family="\'Space Grotesk\',system-ui,sans-serif" '
                    f'font-weight="700" font-size="{fs}" fill="#e8f2ee" letter-spacing="-1">{esc(l)}</text>')
    tris=TRISKELE.format(tx=60, ty=120, s=0.62, acc=acc)
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Couverture : {esc(b["title"])}">
<defs>
 <radialGradient id="bg" cx="50%" cy="34%" r="80%">
  <stop offset="0%" stop-color="{rgba(acc,.16)}"/>
  <stop offset="45%" stop-color="#0b121a"/>
  <stop offset="100%" stop-color="#070b11"/>
 </radialGradient>
 <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#070b11" stop-opacity="0"/>
  <stop offset="62%" stop-color="#070b11" stop-opacity="0"/>
  <stop offset="100%" stop-color="#070b11" stop-opacity="0.96"/>
 </linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<g opacity="0.9">{motif}</g>
<rect width="{W}" height="{H}" fill="url(#fade)"/>
<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="{rgba(acc,.35)}" stroke-width="2"/>
{tris}
<text x="60" y="238" font-family="monospace" font-size="20" letter-spacing="4" fill="{acc}">{esc(b["genre"].upper())}</text>
{title_svg}
<line x1="60" y1="{ty+len(lines)*(fs+8)+6}" x2="240" y2="{ty+len(lines)*(fs+8)+6}" stroke="{acc}" stroke-width="3"/>
<text x="60" y="1120" font-family="monospace" font-size="22" letter-spacing="1" fill="#9db2ae">TRU<tspan fill="{acc}">vector</tspan>.dev</text>
<text x="60" y="1150" font-family="monospace" font-size="14" letter-spacing="2" fill="#6f8582">NOUVELLE · ÉDITION NUMÉRIQUE</text>
</svg>'''
    return svg

for b in BOOKS:
    svg=build(b)
    with open(f'{OUT}/{b["slug"]}.svg',"w",encoding="utf-8") as f:
        f.write(svg)
print("OK ->", len(BOOKS), "couvertures générées dans", OUT)
