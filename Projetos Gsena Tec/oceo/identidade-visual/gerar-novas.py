#!/usr/bin/env python3
"""Gera 7 novas opções de logo do OCEO (08-14) — SVG cor + mono — e um mosaico PNG.
Mesma linguagem visual do set 01-07: viewBox 200x200, traço navy + acento dourado."""
import math, os, subprocess

NAVY="#17335c"; GOLD="#dd9a34"
HERE=os.path.dirname(os.path.abspath(__file__))

def pol(cx,cy,r,deg):
    a=math.radians(deg); return (cx+r*math.cos(a), cy+r*math.sin(a))

def arc(cx,cy,r,a0,a1,large=None):
    x0,y0=pol(cx,cy,r,a0); x1,y1=pol(cx,cy,r,a1)
    if large is None: large=1 if abs(a1-a0)>180 else 0
    sweep=1 if a1>a0 else 0
    return f"M{x0:.1f},{y0:.1f} A{r},{r} 0 {large} {sweep} {x1:.1f},{y1:.1f}"

def svg(body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">\n'
            +body+'\n</svg>\n')

def make(acc):  # acc = cor do acento (dourado normal, navy no mono)
    L={}
    # 08 — BI: O com 3 barras crescentes
    L["08-bi"]=(f'<circle cx="100" cy="100" r="78" fill="none" stroke="{NAVY}" stroke-width="14"/>'
      f'<g fill="{acc}"><rect x="70" y="104" width="17" height="30" rx="3.5"/>'
      f'<rect x="91" y="86" width="17" height="48" rx="3.5"/>'
      f'<rect x="112" y="66" width="17" height="68" rx="3.5"/></g>')
    # 09 — órbita: O + ponto dourado orbitando + risco de trajetória
    ox,oy=pol(100,100,76,-58)
    L["09-orbita"]=(f'<circle cx="100" cy="100" r="76" fill="none" stroke="{NAVY}" stroke-width="12"/>'
      f'<path d="{arc(100,100,76,-120,-58,0)}" fill="none" stroke="{acc}" stroke-width="12" stroke-linecap="round" opacity="0.45"/>'
      f'<circle cx="{ox:.1f}" cy="{oy:.1f}" r="15" fill="{acc}"/>')
    # 10 — cinco arcos (os 5 pilares como um só sistema); um arco dourado, mais grosso
    segs=""
    for i in range(5):
        a0=-90+i*72+9; a1=a0+54
        gold=(i==0)
        segs+=(f'<path d="{arc(100,100,76,a0,a1,0)}" fill="none" '
               f'stroke="{acc if gold else NAVY}" stroke-width="{17 if gold else 14}" stroke-linecap="round"/>')
    L["10-pilares"]=segs
    # 11 — medidor: arco de ~250° (velocímetro) + ponteiro dourado + hub
    nx,ny=pol(100,100,52,-38)
    L["11-medidor"]=(f'<path d="{arc(100,100,74,125,415,1)}" fill="none" stroke="{NAVY}" stroke-width="13" stroke-linecap="round"/>'
      f'<line x1="100" y1="100" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{acc}" stroke-width="12" stroke-linecap="round"/>'
      f'<circle cx="100" cy="100" r="13" fill="{NAVY}"/>'
      f'<circle cx="100" cy="100" r="5" fill="{acc}"/>')
    # 12 — monograma OC: O externo + C interno dourado
    L["12-oc"]=(f'<circle cx="100" cy="100" r="78" fill="none" stroke="{NAVY}" stroke-width="14"/>'
      f'<path d="{arc(100,100,44,-52,232,1)}" fill="none" stroke="{acc}" stroke-width="13" stroke-linecap="round"/>')
    # 13 — estrela-norte: anel + estrela de 4 pontas dourada
    pts=[]
    for k in range(8):
        r = 48 if k%2==0 else 15
        x,y=pol(100,100,r,-90+k*45)
        pts.append(f"{x:.1f},{y:.1f}")
    L["13-norte"]=(f'<circle cx="100" cy="100" r="78" fill="none" stroke="{NAVY}" stroke-width="12"/>'
      f'<polygon points="{" ".join(pts)}" fill="{acc}"/>')
    # 14 — pedra-chave: anel com uma abertura no topo, cunha dourada encaixada (trava a estrutura)
    L["14-chave"]=(f'<path d="{arc(100,100,76,-70,250,1)}" fill="none" stroke="{NAVY}" stroke-width="13" stroke-linecap="round"/>'
      f'<path d="M74,36 L126,36 L118,6 L82,6 Z" fill="{acc}"/>')
    return L

col=make(GOLD); mono=make(NAVY)
for slug,body in col.items():
    open(f"{HERE}/logo-{slug}.svg","w").write(svg(body))
    open(f"{HERE}/logo-{slug}-mono.svg","w").write(svg(mono[slug]))

# mosaico HTML -> PNG
cards=""
NAMES={"08-bi":"BI / painel","09-orbita":"Órbita","10-pilares":"5 pilares",
       "11-medidor":"Medidor","12-oc":"Monograma O·C","13-norte":"Estrela-norte","14-chave":"Pedra-chave"}
for slug,body in col.items():
    cards+=f'''<div class="card"><div class="mk">{svg(body)}</div>
      <div class="wm"><span class="glyph">{svg(body)}</span><b>OCEO</b></div>
      <div class="lbl">{slug.split("-")[0]} · {NAMES[slug]}</div></div>'''
html=f'''<!doctype html><meta charset="utf-8"><style>
*{{margin:0;box-sizing:border-box}}
body{{background:#f4f2ec;font-family:Inter,Arial,sans-serif;padding:46px}}
h1{{font-size:15px;letter-spacing:.22em;color:#8a8374;text-transform:uppercase;margin-bottom:26px}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:22px}}
.card{{background:#fff;border:1px solid #e4ded0;border-radius:14px;padding:22px;text-align:center}}
.mk{{width:96px;height:96px;margin:0 auto 14px}} .mk svg{{width:100%;height:100%}}
.wm{{display:flex;align-items:center;justify-content:center;gap:9px;margin-bottom:12px}}
.wm .glyph{{width:26px;height:26px}} .wm .glyph svg{{width:100%;height:100%}}
.wm b{{font-family:'Archivo Black','Arial Black',sans-serif;font-size:24px;letter-spacing:.02em;color:#17335c}}
.lbl{{font-size:12px;color:#8a8374;letter-spacing:.04em}}
</style><h1>OCEO · novas opções de marca (08–14)</h1><div class="grid">{cards}</div>'''
open(f"{HERE}/_novas-preview.html","w").write(html)
subprocess.run(["node","-e",f'''
const {{chromium}}=require('playwright');(async()=>{{
const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1180,height:900}},deviceScaleFactor:2}});
await p.goto('file://{HERE}/_novas-preview.html');await p.waitForTimeout(400);
await p.screenshot({{path:'{HERE}/_novas-preview.png',fullPage:true}});await b.close();}})();
'''],check=True,env={**os.environ,"NODE_PATH":"/Users/gilbertosena/Desktop/GilbertoOS/scripts/node_modules"})
print("ok — 7 SVGs (cor+mono) + _novas-preview.png")
