#!/usr/bin/env python3
"""Renders 3D-look mockups of OCEO marks: extruded metal object, studio bg,
contact shadow, reflection + 'OCEO' wordmark. HTML/CSS -> PNG (Playwright)."""
import os, subprocess, re
HERE=os.path.dirname(os.path.abspath(__file__))

MARKS=[("12-oc","Monograma O·C"),("10-pilares","5 pilares"),("13-norte","Estrela-norte"),
       ("08-bi","Painel / BI"),("14-chave","Pedra-chave"),("09-orbita","Órbita")]

DEPTH=13   # camadas de extrusão

def inner(slug):
    s=open(f"{HERE}/logo-{slug}.svg").read()
    return re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1).strip()

layers_css="".join(
    f".obj .layer:nth-child({i+1}){{transform:translate({i*2.4:.1f}px,{i*2.4:.1f}px);"
    f"filter:brightness({0.42+0.028*i:.2f}) saturate(.7) contrast(1.15);}}" for i in range(DEPTH))

cards=""
for slug,name in MARKS:
    body=inner(slug)
    stack="".join(f'<div class="layer"><svg viewBox="0 0 200 200">{body}</svg></div>' for _ in range(DEPTH))
    cards+=f'''<div class="card">
      <div class="stage">
        <div class="obj">{stack}
          <div class="front"><svg viewBox="0 0 200 200">{body}</svg><div class="sheen"></div></div>
        </div>
        <div class="floorshadow"></div>
        <div class="reflection"><div class="obj r">{stack}<div class="front"><svg viewBox="0 0 200 200">{body}</svg></div></div></div>
      </div>
      <div class="wm">OCEO</div>
      <div class="lbl">{slug.split("-")[0]} · {name}</div>
    </div>'''

html=f'''<!doctype html><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@800;900&display=swap" rel="stylesheet">
<style>
*{{margin:0;box-sizing:border-box}}
body{{background:#0a0d12;font-family:Archivo,Arial,sans-serif;padding:52px}}
h1{{color:#8a8ea0;font-size:13px;letter-spacing:.26em;text-transform:uppercase;margin-bottom:34px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:30px}}
.card{{background:linear-gradient(180deg,#161b24,#0d1017);border:1px solid #232a37;border-radius:20px;
  padding:34px 20px 24px;text-align:center;overflow:hidden}}
.stage{{position:relative;height:220px;perspective:1100px;margin-bottom:14px}}
.obj{{position:absolute;left:50%;top:8px;width:150px;height:150px;margin-left:-75px;
  transform-style:preserve-3d;transform:rotateX(11deg) rotateY(-15deg);}}
.obj .layer,.obj .front{{position:absolute;inset:0}}
.obj .layer svg,.obj .front svg{{width:100%;height:100%;display:block}}
{layers_css}
.obj .front{{transform:translate({DEPTH*2.4:.1f}px,{DEPTH*2.4:.1f}px);
  filter:drop-shadow(14px 20px 22px rgba(0,0,0,.55));}}
.obj .front .sheen{{position:absolute;inset:0;border-radius:50%;
  background:linear-gradient(125deg,rgba(255,255,255,.42),rgba(255,255,255,.05) 38%,rgba(255,255,255,0) 60%);mix-blend-mode:screen;pointer-events:none}}
.floorshadow{{position:absolute;left:50%;bottom:14px;width:180px;height:34px;margin-left:-90px;
  background:radial-gradient(ellipse,rgba(0,0,0,.65),transparent 70%);filter:blur(6px)}}
.reflection{{position:absolute;left:0;right:0;top:170px;height:120px;opacity:.16;
  -webkit-mask-image:linear-gradient(#000,transparent 60%);mask-image:linear-gradient(#000,transparent 60%)}}
.reflection .obj.r{{transform:rotateX(11deg) rotateY(-15deg) scaleY(-1)}}
.wm{{color:#f1eee6;font-weight:900;font-size:30px;letter-spacing:.06em;margin-top:6px}}
.lbl{{color:#8a8ea0;font-size:12px;letter-spacing:.06em;margin-top:6px}}
</style>
<h1>OCEO · marca em 3D — estudo</h1>
<div class="grid">{cards}</div>'''
open(f"{HERE}/_3d-preview.html","w").write(html)
subprocess.run(["node","-e",f'''
const {{chromium}}=require('playwright');(async()=>{{
const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1240,height:1000}},deviceScaleFactor:2}});
await p.goto('file://{HERE}/_3d-preview.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
await p.screenshot({{path:'{HERE}/_3d-preview.png',fullPage:true}});await b.close();}})();
'''],check=True,env={**os.environ,"NODE_PATH":"/Users/gilbertosena/Desktop/GilbertoOS/scripts/node_modules"})
print("ok -> _3d-preview.png")
