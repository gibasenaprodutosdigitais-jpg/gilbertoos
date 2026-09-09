# -*- coding: utf-8 -*-
"""
Video de apresentacao dos 10 e-books de Gilberto Sena (16:9, locucao PT-BR).
Cada obra e um "pilar" da formacao do dono de empresa.

Fluxo:
  1. gera locucao por segmento (macOS `say` -> aiff -> wav 48k stereo)
  2. mede duracoes, monta a linha do tempo
  3. escreve video.html com a timeline embutida
  4. escreve mux.sh (bed musical + locucao + encode final)
Depois: `node render-frames.js` e `bash mux.sh`.
"""
import os, subprocess, json, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
AUD  = os.path.join(HERE, "audio")
os.makedirs(AUD, exist_ok=True)

VOICE = os.environ.get("VOICE", "Luciana")   # ex.: Rocko (masc.), Reed (masc.)
RATE  = int(os.environ.get("RATE", "190"))    # Rocko/Reed pedem ~260-270
FPS   = 30
W, H  = 1920, 1080
SUFFIX = "" if VOICE == "Luciana" else f" (voz {VOICE.lower()})"

# ------------------------------------------------------------------ conteudo
INTRO_NARR = "Dez e-books de Gilberto Sena. Um assunto só: parar de decidir no escuro."
CLOSE_NARR = "Dez pilares na formação de um dono de empresa. Comenta qual você quer primeiro."

BOOKS = [
    dict(n="01", pilar="EMPREENDER", cover="cover01.png",
         title="A Startup Unicórnio",
         tag="diálogo com “A Startup de $100”",
         forca="Não precisa de investidor nem galpão. Precisa de um problema real — e da inteligência artificial.",
         narr="Não precisa de investidor. Precisa de um problema real e da inteligência artificial."),
    dict(n="02", pilar="LIDERANÇA", cover="cover02.png",
         title="De Motoboy a Executivo",
         tag="diálogo com “O Monge e o Executivo”",
         forca="Liderança não é cargo, é serviço. Autoridade se conquista servindo.",
         narr="Liderança não é cargo, é serviço. Autoridade se conquista servindo."),
    dict(n="03", pilar="LEITURA DO NEGÓCIO", cover="cover03.png",
         title="Entenda Suas Finanças",
         tag="material original · o básico bem feito",
         forca="Quem quebra raramente quebra por falta de venda. Quebra por não saber ler o próprio balanço.",
         narr="Ninguém quebra por falta de venda. Quebra por não saber ler o próprio balanço."),
    dict(n="04", pilar="ESTRATÉGIA", cover="cover04.png",
         title="Estratégia da Gestão",
         tag="diálogo com “A Arte da Guerra”",
         forca="Vencer a batalha antes de lutar é planejar antes de agir. Sun Tzu na decisão de negócio.",
         narr="Vencer antes de lutar é planejar antes de agir. Sun Tzu na decisão de negócio."),
    dict(n="05", pilar="EMOÇÃO", cover="cover05.png",
         title="No Controle das Emoções",
         tag="diálogo com Goleman · “Inteligência Emocional”",
         forca="Decisão tomada com raiva sai cara. Sob medo, também. Inteligência emocional aplicada ao dinheiro.",
         narr="Decisão com raiva sai cara. Sob medo, também. A emoção a favor da escolha."),
    dict(n="06", pilar="MATEMÁTICA DO DINHEIRO", cover="cover06.png",
         title="O Segredo das Finanças",
         tag="material original · matemática financeira",
         forca="Juros não é opinião, é conta. Quem não sabe fazer essa conta paga por ela a vida inteira.",
         narr="Juros não é opinião, é conta. Quem não sabe fazer, paga a vida inteira."),
    dict(n="07", pilar="CARÁTER", cover="cover07.png",
         title="Os Pilares de um Homem Próspero",
         tag="diálogo com Provérbios",
         forca="Um texto de três mil anos ainda decide o seu próximo passo. Provérbios aplicado ao negócio e à vida.",
         narr="Um texto de três mil anos ainda decide o seu próximo passo."),
    dict(n="08", pilar="POSICIONAMENTO", cover="cover08.png",
         title="Posicione-se ou Morra",
         tag="releitura do clássico do Posicionamento",
         forca="Se o cliente não diz em uma frase o que você faz, você não existe pra ele.",
         narr="Se o cliente não diz numa frase o que você faz, você não existe pra ele."),
    dict(n="09", pilar="DÍVIDA", cover="cover09.png",
         title="Quite Suas Dívidas Já",
         tag="material original · guia de negociação",
         forca="Dívida não se resolve com vergonha. Se resolve com estratégia — e sabendo o que é irregular no contrato.",
         narr="Dívida não se resolve com vergonha. Se resolve com estratégia."),
    dict(n="10", pilar="MENTALIDADE", cover="cover10.png",
         title="Seja Rico ou Pobre",
         tag="diálogo com “Pai Rico, Pai Pobre”",
         forca="Alguém te ensinou que dinheiro é sujo. Troque o roteiro antes que ele decida a sua vida.",
         narr="Alguém te ensinou que dinheiro é sujo. Troque o roteiro antes que ele decida sua vida."),
]

# ------------------------------------------------------------------ TTS
def tts(name, text):
    aiff = os.path.join(AUD, name + ".aiff")
    wav  = os.path.join(AUD, name + ".wav")
    subprocess.run(["say", "-v", VOICE, "-r", str(RATE), "-o", aiff, text], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", aiff,
                    "-ar", "48000", "-ac", "2", wav], check=True)
    os.remove(aiff)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
              "format=duration", "-of", "csv=p=0", wav],
              capture_output=True, text=True).stdout.strip())
    return wav, d

segs = []   # (id, wavpath, narr_dur)
w, d = tts("intro", INTRO_NARR); segs.append(("intro", w, d))
for b in BOOKS:
    w, d = tts("s" + b["n"], b["narr"]); segs.append(("s" + b["n"], w, d))
w, d = tts("close", CLOSE_NARR); segs.append(("close", w, d))

# ------------------------------------------------------------------ timeline
LEAD = 0.45         # atraso da locucao dentro da cena
TAILS = {"intro": 1.1, "close": 1.6}
BOOK_TAIL = 1.15
BOOK_MIN = 4.8

scenes = []
t = 0.0
for sid, wav, nd in segs:
    if sid == "intro":
        dur = max(nd + LEAD + TAILS["intro"], 4.6)
        kind = "intro"
    elif sid == "close":
        dur = max(nd + LEAD + TAILS["close"], 5.0)
        kind = "close"
    else:
        dur = max(nd + LEAD + BOOK_TAIL, BOOK_MIN)
        kind = "book"
    scenes.append(dict(id="sc-" + sid, sid=sid, kind=kind,
                       start=round(t, 3), dur=round(dur, 3),
                       narr_at=round(t + LEAD, 3), narr_dur=round(nd, 3),
                       wav=os.path.relpath(wav, HERE)))
    t += dur

TOTAL = round(t, 3)
timeline = dict(fps=FPS, w=W, h=H, total=TOTAL, scenes=scenes)
json.dump(timeline, open(os.path.join(HERE, "timeline.json"), "w"),
          ensure_ascii=False, indent=1)
print("TOTAL %.2fs  (%d frames)" % (TOTAL, round(TOTAL * FPS)))
for s in scenes:
    print("  %-9s start %6.2f  dur %5.2f  narr %4.2f" %
          (s["sid"], s["start"], s["dur"], s["narr_dur"]))

# ------------------------------------------------------------------ video.html
def book_scene(b):
    return f"""
<div class="scene book" id="sc-s{b['n']}">
  <div class="stage">
    <img class="cover" src="assets/{b['cover']}" alt="">
    <div class="right">
      <div class="num">{b['n']}</div>
      <div class="pilar">PILAR&nbsp;&middot;&nbsp;{b['pilar']}</div>
      <div class="title">{b['title']}</div>
      <div class="rule"></div>
      <div class="tag">{b['tag']}</div>
      <div class="forca">{b['forca']}</div>
    </div>
  </div>
  <div class="brand"><img src="assets/leao.png" alt=""><span>GILBERTO&nbsp;SENA</span></div>
  <div class="counter">{b['n']}&nbsp;/&nbsp;10</div>
</div>"""

mini = "".join(f'<img class="mini" src="assets/{b["cover"]}" alt="">' for b in BOOKS)

HTML = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#0F1419}}
  #root{{position:relative;width:{W}px;height:{H}px;background:#0F1419;
        font-family:'Inter',system-ui,sans-serif}}
  .scene{{position:absolute;inset:0;opacity:0;will-change:opacity}}
  .grain{{position:absolute;inset:0;pointer-events:none;opacity:.035;
        background-image:radial-gradient(circle at 20% 30%, #fff 0, transparent 40%),
                         radial-gradient(circle at 80% 70%, #fff 0, transparent 40%)}}
  .vig{{position:absolute;inset:0;pointer-events:none;
        background:radial-gradient(ellipse at 50% 42%, transparent 55%, rgba(0,0,0,.45) 100%)}}

  /* marca comum */
  .brand{{position:absolute;left:72px;top:54px;display:flex;align-items:center;gap:16px}}
  .brand img{{height:48px;width:auto;display:block}}
  .brand span{{color:#F4F1EA;font-size:20px;font-weight:700;letter-spacing:.28em}}
  .counter{{position:absolute;right:84px;bottom:64px;color:#C9A227;
            font-size:20px;font-weight:700;letter-spacing:.22em}}

  /* cena de livro */
  .book .stage{{position:absolute;inset:0;perspective:1500px}}
  .book .cover{{position:absolute;left:210px;top:206px;height:668px;width:auto;
        border-radius:5px;transform-origin:center center;
        box-shadow:0 40px 90px rgba(0,0,0,.6),0 12px 28px rgba(0,0,0,.5);
        filter:drop-shadow(0 0 1px rgba(201,162,39,.25))}}
  .book .right{{position:absolute;left:1006px;top:214px;width:788px}}
  .book .num{{font-family:'Fraunces',serif;font-weight:300;font-size:150px;
        line-height:.9;color:#C9A227}}
  .book .pilar{{margin-top:10px;color:#C9A227;font-size:17px;font-weight:700;
        letter-spacing:.26em}}
  .book .title{{margin-top:22px;font-family:'Fraunces',serif;font-weight:600;
        font-size:58px;line-height:1.12;color:#F4F1EA;letter-spacing:-.01em}}
  .book .rule{{margin-top:24px;width:96px;height:3px;background:#C9A227;
        transform-origin:left center}}
  .book .tag{{margin-top:22px;font-size:19px;font-style:italic;color:#9a9384}}
  .book .forca{{margin-top:16px;font-size:26px;font-weight:500;line-height:1.5;
        color:#F4F1EA;max-width:760px}}

  /* intro */
  #sc-intro .wrap{{position:absolute;inset:0;display:flex;flex-direction:column;
        align-items:center;justify-content:center;text-align:center}}
  #sc-intro .leao{{height:220px;width:auto;margin-bottom:36px}}
  #sc-intro .kick{{color:#C9A227;font-size:20px;font-weight:700;letter-spacing:.34em;
        margin-bottom:24px}}
  #sc-intro .big{{font-family:'Fraunces',serif;font-weight:700;font-size:132px;
        color:#F4F1EA;line-height:1;letter-spacing:-.02em}}
  #sc-intro .rule{{width:120px;height:3px;background:#C9A227;margin:34px 0}}
  #sc-intro .sub{{font-size:30px;font-weight:500;color:#F4F1EA;max-width:1080px}}

  /* close */
  #sc-close .big10{{position:absolute;left:0;right:0;top:170px;text-align:center;
        font-family:'Fraunces',serif;font-weight:700;font-size:560px;color:#C9A227;
        opacity:.09;line-height:1}}
  #sc-close .row{{position:absolute;left:0;right:0;top:288px;display:flex;
        justify-content:center;gap:20px}}
  #sc-close .mini{{height:230px;width:auto;border-radius:4px;
        box-shadow:0 20px 44px rgba(0,0,0,.55)}}
  #sc-close .foot{{position:absolute;left:0;right:0;top:610px;text-align:center}}
  #sc-close .leao{{height:132px;width:auto;margin-bottom:22px}}
  #sc-close .handle{{color:#F4F1EA;font-size:40px;font-weight:700;letter-spacing:.02em}}
  #sc-close .cta{{margin-top:14px;color:#C9A227;font-size:24px;font-weight:600;
        letter-spacing:.06em}}
  #sc-close .wm{{margin-top:26px;color:#9a9384;font-size:18px;font-weight:700;
        letter-spacing:.3em}}
</style></head><body>
<div id="root">
  <div class="scene" id="sc-intro">
    <div class="wrap">
      <img class="leao" src="assets/leao.png" alt="">
      <div class="kick">A BIBLIOTECA DE GILBERTO SENA</div>
      <div class="big">10 e-books.</div>
      <div class="rule"></div>
      <div class="sub">Um assunto só: parar de decidir no escuro.</div>
    </div>
  </div>
  {"".join(book_scene(b) for b in BOOKS)}
  <div class="scene" id="sc-close">
    <div class="big10">10</div>
    <div class="row">{mini}</div>
    <div class="foot">
      <img class="leao" src="assets/leao.png" alt="">
      <div class="handle">@gilbertosenaoficial</div>
      <div class="cta">comenta qual você quer primeiro</div>
      <div class="wm">GILBERTO SENA</div>
    </div>
  </div>
  <div class="grain"></div><div class="vig"></div>
</div>
<script>
const TL = {json.dumps(timeline, ensure_ascii=False)};
const clamp01 = x => x < 0 ? 0 : x > 1 ? 1 : x;
const eOut = t => 1 - Math.pow(1 - t, 3);
const eIO  = t => t < .5 ? 4*t*t*t : 1 - Math.pow(-2*t+2,3)/2;

function reveal(node, local, delay, dur, dy){{
  const p = eOut(clamp01((local - delay) / dur));
  node.style.opacity = p;
  node.style.transform = 'translateY(' + ((1 - p) * dy).toFixed(2) + 'px)';
}}

function animBook(el, local){{
  const cov = el.querySelector('.cover');
  const cp = eOut(clamp01(local / .8));
  const drift = Math.sin(Math.max(0, local - .8) * .6) * 4;
  const ry = (-16 + cp * 9).toFixed(2);
  const tx = ((1 - cp) * -130).toFixed(2);
  cov.style.opacity = cp;
  cov.style.transform = 'translate(' + tx + 'px,' + drift.toFixed(2) +
                        'px) rotateY(' + ry + 'deg)';
  reveal(el.querySelector('.num'),   local, .12, .5, 26);
  reveal(el.querySelector('.pilar'), local, .28, .5, 22);
  reveal(el.querySelector('.title'), local, .40, .55, 30);
  const r = el.querySelector('.rule');
  r.style.transform = 'scaleX(' + eOut(clamp01((local - .62) / .5)).toFixed(3) + ')';
  reveal(el.querySelector('.tag'),   local, .82, .5, 16);
  reveal(el.querySelector('.forca'), local, .78, .6, 22);
  el.querySelector('.brand').style.opacity   = clamp01((local - .2) / .5);
  el.querySelector('.counter').style.opacity = clamp01((local - .2) / .5);
}}

function animIntro(el, local){{
  const l = el.querySelector('.leao');
  const p = eOut(clamp01(local / .7));
  l.style.opacity = p;
  l.style.transform = 'scale(' + (.82 + p * .18).toFixed(3) + ')';
  reveal(el.querySelector('.kick'), local, .25, .5, 18);
  reveal(el.querySelector('.big'),  local, .38, .6, 40);
  const r = el.querySelector('.rule');
  r.style.transform = 'scaleX(' + eOut(clamp01((local - .55) / .5)).toFixed(3) + ')';
  r.style.transformOrigin = 'center';
  reveal(el.querySelector('.sub'),  local, .68, .6, 28);
}}

function animClose(el, local){{
  const b = el.querySelector('.big10');
  const bp = eOut(clamp01(local / .9));
  b.style.opacity = (bp * .09).toFixed(3);
  b.style.transform = 'scale(' + (1.12 - bp * .12).toFixed(3) + ')';
  el.querySelectorAll('.mini').forEach((m, i) => {{
    const p = eOut(clamp01((local - i * .05) / .55));
    m.style.opacity = p;
    m.style.transform = 'translateY(' + ((1 - p) * 34).toFixed(2) + 'px)';
  }});
  reveal(el.querySelector('.leao'),   local, .75, .5, 20);
  reveal(el.querySelector('.handle'), local, .88, .5, 22);
  reveal(el.querySelector('.cta'),    local, 1.02, .5, 18);
  reveal(el.querySelector('.wm'),     local, 1.16, .5, 14);
}}

function seek(t){{
  let sc = TL.scenes[0], local = 0;
  for (const s of TL.scenes){{
    if (t >= s.start && t < s.start + s.dur){{ sc = s; local = t - s.start; break; }}
    if (t >= s.start) {{ sc = s; local = t - s.start; }}
  }}
  for (const s of TL.scenes){{
    const el = document.getElementById(s.id);
    if (el) el.style.opacity = '0';
  }}
  const el = document.getElementById(sc.id);
  const fin  = clamp01(local / .40);
  const fout = clamp01((sc.dur - local) / .35);
  el.style.opacity = Math.min(fin, fout);
  if (sc.kind === 'book') animBook(el, local);
  else if (sc.kind === 'intro') animIntro(el, local);
  else animClose(el, local);
}}
window.__seek = seek;
window.__ready = true;
seek(0);
</script></body></html>"""
open(os.path.join(HERE, "video.html"), "w").write(HTML)
print("video.html escrito")

# ------------------------------------------------------------------ mux.sh
delays = []
inputs = ["-i audio/bed.wav"]
fc = []
for i, s in enumerate(scenes):
    idx = i + 1
    inputs.append(f'-i "{s["wav"]}"')
    ms = int(s["narr_at"] * 1000)
    fc.append(f'[{idx}]adelay={ms}|{ms}[a{idx}]')
amix_ins = "".join(f"[a{i+1}]" for i in range(len(scenes)))
fc.append(f'[0]volume=0.9[bed]')
fc.append(f'[bed]{amix_ins}amix=inputs={len(scenes)+1}:normalize=0,'
          f'dynaudnorm=p=0.6:s=6,alimiter=limit=0.94[mix]')
filt = ";".join(fc)

MUX = f"""#!/bin/bash
set -e
cd "$(dirname "$0")"
FPS={FPS}
TOTAL={TOTAL}

# --- cama musical sutil (la2 + mi3, filtrada, baixa) ---
ffmpeg -y -loglevel error \\
  -f lavfi -i "sine=frequency=110:sample_rate=48000" \\
  -f lavfi -i "sine=frequency=164.81:sample_rate=48000" \\
  -f lavfi -i "sine=frequency=220:sample_rate=48000" \\
  -filter_complex "[0][1][2]amix=inputs=3,tremolo=f=0.13:d=0.4,lowpass=f=380,\\
highpass=f=60,volume=0.05,aecho=0.8:0.6:70:0.25,afade=t=in:d=1.5,afade=t=out:st=$(echo "$TOTAL-2"|bc):d=2" \\
  -t $TOTAL -ac 2 -ar 48000 audio/bed.wav

# --- mistura locucao + cama ---
ffmpeg -y -loglevel error {" ".join(inputs)} \\
  -filter_complex "{filt}" -map "[mix]" -t $TOTAL -ar 48000 -ac 2 audio/mix.wav

# --- encode final ---
ffmpeg -y -loglevel error -framerate $FPS -start_number 0 -i frames/f-%05d.png \\
  -i audio/mix.wav \\
  -c:v libx264 -pix_fmt yuv420p -crf 18 -preset slow \\
  -c:a aac -b:a 192k -movflags +faststart -shortest \\
  "Apresentacao 10 e-books - Gilberto Sena{SUFFIX}.mp4"

echo "OK -> Apresentacao 10 e-books - Gilberto Sena.mp4"
"""
open(os.path.join(HERE, "mux.sh"), "w").write(MUX)
os.chmod(os.path.join(HERE, "mux.sh"), 0o755)
print("mux.sh escrito")
