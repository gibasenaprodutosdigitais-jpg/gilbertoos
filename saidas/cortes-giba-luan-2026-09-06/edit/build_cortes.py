#!/usr/bin/env python3
"""Build 30s vertical cortes from the Giba e Luan podcast.
Usage: python build_cortes.py <clip_id 1..6> [--body-only]
Pipeline: extract+crop segments -> concat body -> (transcribe body audio elsewhere)
          -> karaoke caption PNG sequence -> overlay -> hook card -> concat -> final.
No ffmpeg text filters used (this build lacks libass/drawtext); all text via PIL.
"""
import json, os, subprocess, sys, math, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = "/Users/gilbertosena/Desktop/GilbertoOS/saidas/cortes-giba-luan-2026-09-06"
SRC = {"01": f"{BASE}/fonte/giba-luan-01.mp4",
       "02": f"{BASE}/fonte/giba-luan-02.mp4",
       "03": f"{BASE}/fonte/giba-luan-03.mp4"}
EDIT = f"{BASE}/edit"
WORK = f"{BASE}/edit/work"
OUT = f"{BASE}/cortes"
os.makedirs(WORK, exist_ok=True); os.makedirs(OUT, exist_ok=True)

FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_BOLD  = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

GOLD = (201, 162, 39)
INK  = (244, 241, 234)
PANEL = "0x0F1419"
VID_H = 1500          # video occupies top 1500px of 1080x1920
CAP_FPS = 15
HANDLE = "@gilbertosenaoficial"

def zone_h(c): return VID_H

# crop per episode: crop=W:H:X:Y from 1920x1080 then scale to 1080x1500
CROP = {"01": (700, 972, 730, 0),
        "03": (700, 972, 765, 0)}

CLIPS = {
 1: dict(ep="01", segs=[[173.20,205.15]],
         slug="golpe-ia",
         hook=("CAÍ NUM GOLPE", "feito por Inteligência Artificial")),
 2: dict(ep="01", segs=[[401.15,405.65],[422.50,442.45]],
         slug="7-piramides",
         hook=("CAÍ EM 7 PIRÂMIDES", "e nunca arrastei ninguém comigo")),
 3: dict(ep="01", segs=[[860.10,869.10],[869.75,879.25],[893.30,904.55]],
         slug="acharam-golpe",
         hook=("ACHARAM QUE ERA GOLPE", "hoje é um pedaço da Indonésia perto de SP")),
 4: dict(ep="03", segs=[[343.70,372.65]],
         slug="quero-20-mil",
         hook=("“QUERO 20 MIL”", "tá — e o que você me entrega?")),
 5: dict(ep="03", layout="fill",
         segs=[[241.50,254.90],[256.30,262.05],[267.40,272.40],[279.00,281.10],[282.60,285.60]],
         slug="engolia-o-u2",
         hook=("SE FOSSEM 4 IGUAIS A MIM", "eu engolia o U2")),
 6: dict(ep="03", layout="fill",
         segs=[[411.15,419.95],[401.65,409.70],[420.55,431.60]],
         slug="patrao-enriquece",
         hook=("TODO FUNCIONÁRIO PENSA ISSO", "“o patrão enriquece às minhas costas”")),
 # --- sacadas curtas (só falas do Gilberto, janelas onde a câmera fica nele) ---
 7: dict(ep="02", crop=(800,1080,860,0),
         segs=[[1064.30,1071.20],[1080.55,1087.15]],
         slug="sacada-40-certificacoes",
         hook=("40 CERTIFICAÇÕES", "e 7 vezes quebrado")),
 8: dict(ep="03",
         segs=[[521.90,530.85]],
         slug="sacada-certo-e-errado",
         hook=("NÃO EXISTE CERTO E ERRADO", "existe o caminho que você precisa trilhar")),
 9: dict(ep="03",
         segs=[[609.55,612.10],[614.10,617.80]],
         slug="sacada-parar-de-apanhar",
         hook=("CHEGA UMA HORA", "que tem que parar de apanhar")),
}

# single-token substitutions (match on stripped-lower text) -> replacement (keeps trailing punct)
SUB = {
 "youtube": "U2", "youtube.": "U2.",
 "jambê": "Jambeiro", "jambê.": "Jambeiro.",
 "comprado": "compromisso", "comprado.": "compromisso.",
 "contato": "contrato", "dela": "delas", "dela.": "delas.",
 "desembolar": "desenrolar", "desembolar.": "desenrolar.",
 "bebom": "BBom", "pl,": "PLR,",
}
# drop these tokens entirely (stray interjections from the other speaker)
DROP = {"exato", "exato."}
# splice: replace a consecutive run of tokens (matched by stripped-lower text seq) with new words,
# distributing the run's time span. per clip id.
SPLICE = {
 1: [(["r","$","1",".900",",00,"], ["mil","e","novecentos","reais"]),
     (["r","$","2",".000",",00","e","pouco"], ["dois","mil","e","pouco"]),
     (["r","$","1",".900",",00"],  ["mil","e","novecentos"])],
 4: [(["salário","assinado","a"], ["seu","salário","é"])],
 5: [(["engolir","o","youtube."], ["engolia","o","U2!"]),
     (["botei","o","estúdio"],    ["montei","o","estúdio"]),
     (["não","tinham","comprometido."], ["não","tinham","compromisso!"])],
 7: [(["fundo","do","ponto"], ["fundo","do","poço"]),
     (["em","a"], ["na"])],
}

def run(cmd):
    print("+", " ".join(str(c) for c in cmd)[:200])
    subprocess.run(cmd, check=True)

def ff(*a): run(["ffmpeg","-hide_banner","-loglevel","error","-y",*a])

def build_body(cid):
    c = CLIPS[cid]; ep = c["ep"]; src = SRC[ep]
    zh = zone_h(c)
    if c.get("layout") == "fill":
        # ep03 is a switched multicam (Gilberto CU / Luan CU / wide). A centred crop keeps
        # whoever is on their close-up framed; the brief wide 2-shot shows the middle.
        cw,ch,cx,cy = (778, 1080, 571, 0)
    else:
        cw,ch,cx,cy = c.get("crop") or CROP[ep]
    vf = (f"crop={cw}:{ch}:{cx}:{cy},scale=1080:{zh}:flags=lanczos,"
          f"pad=1080:1920:0:0:color={PANEL},setsar=1,fps=30,format=yuv420p")
    parts = []
    for i,(s,e) in enumerate(c["segs"]):
        dur = e - s
        p = f"{WORK}/c{cid}_seg{i}.mp4"
        af = f"afade=t=in:st=0:d=0.03,afade=t=out:st={max(dur-0.03,0):.3f}:d=0.03,aresample=48000"
        ff("-ss",f"{s:.3f}","-i",src,"-t",f"{dur:.3f}",
           "-vf",vf,"-af",af,
           "-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",
           "-c:a","aac","-b:a","192k","-ar","48000","-ac","2",
           "-video_track_timescale","30000", p)
        parts.append(p)
    lst = f"{WORK}/c{cid}_list.txt"
    open(lst,"w").write("".join(f"file '{p}'\n" for p in parts))
    body = f"{WORK}/c{cid}_body.mp4"
    ff("-f","concat","-safe","0","-i",lst,"-c","copy",body)
    # extract audio for transcription
    ff("-i",body,"-vn","-c:a","pcm_s16le","-ar","16000","-ac","1",f"{WORK}/c{cid}_body.wav")
    print("BODY:", body, "-> transcribe", f"{WORK}/c{cid}_body.wav")
    return body

def _key(s): return s.strip().lower()

def load_words(cid):
    j = json.load(open(f"{WORK}/c{cid}_body.json"))
    raw = [w for w in j["words"] if w.get("type","word")=="word" and w["text"].strip()]
    # 1) splice multi-token fixes
    for pat, rep in SPLICE.get(cid, []):
        i = 0
        while i <= len(raw)-len(pat):
            if [_key(raw[i+k]["text"]) for k in range(len(pat))] == pat:
                s = raw[i]["start"]; e = raw[i+len(pat)-1]["end"]
                step = (e-s)/len(rep)
                new = [dict(text=rep[k], start=s+k*step, end=s+(k+1)*step, type="word")
                       for k in range(len(rep))]
                raw = raw[:i] + new + raw[i+len(pat):]
                i += len(rep)
            else:
                i += 1
    # 2) per-token sub + drop
    out = []
    for w in raw:
        k = _key(w["text"])
        if k in DROP: continue
        t = w["text"].strip()
        if k in SUB: t = SUB[k]
        w = dict(w); w["t"] = t
        out.append(w)
    return out

def chunk_lines(ws, max_words=2, max_chars=13):
    lines, cur = [], []
    for w in ws:
        cand = cur + [w]
        if cur and (len(cand) > max_words or len(" ".join(x["t"] for x in cand)) > max_chars):
            lines.append(cur); cur = [w]
        else:
            cur = cand
    if cur: lines.append(cur)
    return lines

def measure(draw, txt, font):
    b = draw.textbbox((0,0), txt, font=font, stroke_width=0)
    return b[2]-b[0], b[3]-b[1]

def render_caption_seq(cid, body_dur):
    ws = load_words(cid)
    lines = chunk_lines(ws)
    capdir = f"{WORK}/c{cid}_caps"; os.makedirs(capdir, exist_ok=True)
    for f in os.listdir(capdir): os.remove(os.path.join(capdir,f))
    W, H = 1080, 1920 - zone_h(CLIPS[cid])   # caption panel size (below the video)
    MAXW = W - 120                       # usable text width (never clip)
    BASE = 58                            # base caption font size
    STROKE = 7
    hfont = ImageFont.truetype(FONT_BOLD, 28)
    _fcache = {}
    def fit_font(words):
        d0 = ImageDraw.Draw(Image.new("RGBA",(4,4)))
        for sz in range(BASE, 26, -3):
            f = _fcache.setdefault(sz, ImageFont.truetype(FONT_BLACK, sz))
            gap = d0.textlength(" ", font=f)
            tot = sum(measure(d0,w,f)[0] for w in words) + gap*(len(words)-1)
            if tot <= MAXW: return f
        return _fcache[29]
    n = math.ceil(body_dur * CAP_FPS)
    # active state per line: (line_idx, active_word_idx) chosen by time
    def state_at(t):
        for li,ln in enumerate(lines):
            if t < ln[0]["start"] - 0.15:
                return (li-1, len(lines[li-1])-1) if li>0 else None
            if t <= ln[-1]["end"] + 0.45:
                aw = 0
                for wi,w in enumerate(ln):
                    if t >= w["start"] - 0.05: aw = wi
                return (li, aw)
        return (len(lines)-1, len(lines[-1])-1)
    for fi in range(n):
        t = fi / CAP_FPS
        st = state_at(t)
        img = Image.new("RGBA",(W,H),(0,0,0,0))
        d = ImageDraw.Draw(img)
        d.rectangle([0,0,W,3], fill=GOLD)                       # seam rule
        d.text((W/2, H-42), HANDLE, font=hfont, fill=(140,140,150), anchor="mm")
        if st is not None:
            li, aw = st
            ln = lines[li]
            words = [w["t"].upper().rstrip(" .,;:") for w in ln]
            font = fit_font(words)
            gap = d.textlength(" ", font=font)
            sizes = [measure(d, wt, font) for wt in words]
            total = sum(s[0] for s in sizes) + gap*(len(words)-1)
            lh = max(s[1] for s in sizes)
            x = (W - total)/2
            y = (H - lh)/2 - 14
            for wi,wt in enumerate(words):
                col = GOLD if wi==aw else INK
                d.text((x,y), wt, font=font, fill=col,
                       stroke_width=STROKE, stroke_fill=(0,0,0))
                x += sizes[wi][0] + gap
        img.save(f"{capdir}/{fi:05d}.png")
    return capdir

def render_hook_card(cid, body_first_frame):
    c = CLIPS[cid]; title, sub = c["hook"]
    bg = Image.open(body_first_frame).convert("RGB").resize((1080,1920))
    bg = bg.filter(ImageFilter.GaussianBlur(14))
    dark = Image.new("RGB",(1080,1920),(8,11,15))
    bg = Image.blend(bg, dark, 0.72)
    d = ImageDraw.Draw(bg)
    # top wordmark
    wf = ImageFont.truetype(FONT_BOLD, 30)
    d.text((1080/2, 300), "G I L B E R T O   S E N A", font=wf, fill=GOLD, anchor="mm")
    d.line([(1080/2-60, 340),(1080/2+60,340)], fill=GOLD, width=3)
    # title (wrapped + auto-fit so no line is ever clipped)
    lines = textwrap.wrap(title, width=14)
    tsize = 118
    while tsize > 60:
        tf = ImageFont.truetype(FONT_BLACK, tsize)
        widest = max(d.textbbox((0,0), ln, font=tf, stroke_width=4)[2] for ln in lines)
        if widest <= 1000: break
        tsize -= 4
    lh = tsize + 22
    y = 860 - len(lines)*(lh/2)
    for ln in lines:
        d.text((1080/2, y), ln, font=tf, fill=INK, anchor="mm",
               stroke_width=4, stroke_fill=(0,0,0))
        y += lh
    # sub
    sf = ImageFont.truetype(FONT_BOLD, 46)
    for ln in textwrap.wrap(sub, width=34):
        d.text((1080/2, y+30), ln, font=sf, fill=GOLD, anchor="mm")
        y += 62
    p = f"{WORK}/c{cid}_card.png"; bg.save(p); return p

def build_final(cid):
    c = CLIPS[cid]
    body = f"{WORK}/c{cid}_body.mp4"
    body_dur = float(subprocess.check_output(
        ["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",body]).strip())
    # first frame for the hook card bg
    ff0 = f"{WORK}/c{cid}_ff.png"
    ff("-ss","0.2","-i",body,"-frames:v","1",ff0)
    capdir = render_caption_seq(cid, body_dur)
    card = render_hook_card(cid, ff0)
    # overlay captions on body
    cap = f"{WORK}/c{cid}_cap.mp4"
    ff("-i",body,"-framerate",str(CAP_FPS),"-i",f"{capdir}/%05d.png",
       "-filter_complex",
       f"[1:v]setpts=PTS-STARTPTS,fps=30[c];[0:v][c]overlay=x=0:y={zone_h(CLIPS[cid])}:eof_action=pass:format=auto[v]",
       "-map","[v]","-map","0:a",
       "-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",
       "-c:a","aac","-b:a","192k","-ar","48000","-ac","2",
       "-video_track_timescale","30000", cap)
    # hook card -> 1.6s silent clip, matched params
    cardmp4 = f"{WORK}/c{cid}_card.mp4"
    ff("-loop","1","-t","1.6","-i",card,
       "-f","lavfi","-t","1.6","-i","anullsrc=r=48000:cl=stereo",
       "-vf","scale=1080:1920,setsar=1,fps=30,format=yuv420p",
       "-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",
       "-c:a","aac","-b:a","192k","-ar","48000","-ac","2",
       "-video_track_timescale","30000", cardmp4)
    lst = f"{WORK}/c{cid}_final_list.txt"
    open(lst,"w").write(f"file '{cardmp4}'\nfile '{cap}'\n")
    final = f"{OUT}/corte-{cid}-{c['slug']}.mp4"
    ff("-f","concat","-safe","0","-i",lst,"-c","copy","-movflags","+faststart",final)
    print("FINAL:", final)

if __name__ == "__main__":
    cid = int(sys.argv[1])
    if "--body-only" in sys.argv:
        build_body(cid)
    elif "--final-only" in sys.argv:
        build_final(cid)
    else:
        build_body(cid); build_final(cid)
