"""Monta os cortes das gravacoes do carro: corte por ancora de palavra, cor HLG->709,
legenda queimada com PIL (faixa qtrle com alfa), bip de 1 kHz em palavrao, -14 LUFS."""
import json, os, re, subprocess, sys, unicodedata
from PIL import Image, ImageDraw, ImageFont

REPO = "/Users/gilbertosena/Desktop/GilbertoOS"
SRC = REPO + "/entrada-videos/longos"
WORK = "/private/tmp/claude-501/-Users-gilbertosena-Desktop-GilbertoOS/29d965c1-1431-4b69-89da-47df60783c24/scratchpad/cortes/work"
OUT = REPO + "/saidas/REELS/reels-gravacoes-do-carro-2026-10-30/videos"
SDR = "/private/tmp/claude-501/-Users-gilbertosena-Desktop-GilbertoOS/29d965c1-1431-4b69-89da-47df60783c24/scratchpad/cortes/sdr"
FONT = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
W, H = 1080, 1920

PALAVRAO = ("foda", "fode", "fuck", "caralh", "merd")
PALAVRAO_EXATO = ("porra", "porras")
# correcoes da legenda (sequencia normalizada -> texto)
CORRECOES = [
    (["split", "pain"], "SPLIT PAYMENT"),
    (["martim", "davila"], "MARTINHO DA VILA"),
    (["era", "colo"], "ERA COLLOR"),
    (["pronump"], "PRONAMPE"),
    (["alfanilhas"], "ALPHANILHAS"),
    (["alfanilha"], "ALPHANILHA"),
    (["reenginharia"], "REENGENHARIA"),
    (["embrolho"], "EMBRÓGLIO"),
    (["embrolio"], "EMBRÓGLIO"),
    (["know", "how"], "KNOW-HOW"),
    (["saudar"], "SALDAR"),
    (["de", "folha"], "DE FÔLEGO"),
    (["de", "oito"], "DE OUTRO"),
    (["mil", "meses"], "MIL AO MÊS"),
    (["sob", "tributacao"], "SOBRE TRIBUTAÇÃO"),
    (["chegar", "de", "balela"], "CHEGA DE BALELA"),
    (["contaveis"], "CONTÁBEIS"),
]

def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9%]", "", t)

_cache = {}
def words(vid):
    if vid not in _cache:
        d = json.load(open(f"{SRC}/edit/transcripts/{vid}.json", encoding="utf-8"))
        ws = [w for w in d["words"] if w.get("type") == "word"]
        # junta "foda" + "-se" e "know" + "-how" num token so
        out = []
        for w in ws:
            if out and w["text"].startswith("-"):
                out[-1] = dict(out[-1], text=out[-1]["text"] + w["text"], end=w["end"])
            else:
                out.append(dict(w))
        for w in out:
            w["n"] = norm(w["text"])
        _cache[vid] = [w for w in out if w["n"]]
    return _cache[vid]

def acha(ws, frase, a, b, ultimo=False):
    alvo = [norm(x) for x in frase.split() if norm(x)]
    hits = []
    for i in range(len(ws)):
        if ws[i]["start"] < a - 10 or ws[i]["start"] > b + 10:
            continue
        if [w["n"] for w in ws[i:i + len(alvo)]] == alvo:
            hits.append(i)
    if not hits:
        sys.exit(f"ancora nao achada: '{frase}' em {a}-{b}")
    i = hits[-1] if ultimo else hits[0]
    return i, i + len(alvo) - 1

def segmentos(vid, segs):
    ws = words(vid)
    res = []
    for (a, b, ini, fim) in segs:
        i, _ = acha(ws, ini, a, b)
        _, j = acha(ws, fim, a, b, ultimo=True)
        prev_end = ws[i - 1]["end"] if i > 0 else 0
        nxt = ws[j + 1]["start"] if j + 1 < len(ws) else ws[j]["end"] + 1
        t0 = max(ws[i]["start"] - 0.12, (prev_end + ws[i]["start"]) / 2)
        t1 = min(ws[j]["end"] + 0.25, (ws[j]["end"] + nxt) / 2 + 0.05)
        res.append((t0, t1, ws[i:j + 1]))
    return res

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffmpeg falhou:\n" + r.stderr[-2000:])
    return r

def corrige(tokens):
    """tokens: lista de dicts com n, text, start, end (tempo de saida). Devolve com 'cap'."""
    out, i = [], 0
    while i < len(tokens):
        for seq, rep in CORRECOES:
            if [t["n"] for t in tokens[i:i + len(seq)]] == seq:
                t = dict(tokens[i], end=tokens[i + len(seq) - 1]["end"], cap=rep)
                out.append(t); i += len(seq); break
        else:
            t = dict(tokens[i])
            if t["n"].startswith(PALAVRAO) or t["n"] in PALAVRAO_EXATO:
                t["cap"] = t["text"].strip(" ,.!?")[0].upper() + "***"
                t["bip"] = True
            else:
                t["cap"] = t["text"].upper()
            out.append(t); i += 1
    return out

def blocos(tokens):
    bl, cur = [], []
    for t in tokens:
        txt = " ".join(x["cap"] for x in cur + [t])
        gap = cur and t["start"] - cur[-1]["end"] > 0.45
        if cur and (len(cur) >= 3 or len(txt) > 20 or gap):
            bl.append(cur); cur = []
        cur.append(t)
        fim_frase = re.search(r"[.!?]$", t["text"].strip())
        virgula = re.search(r",$", t["text"].strip()) and len(cur) >= 2
        if fim_frase or virgula:
            bl.append(cur); cur = []
    if cur:
        bl.append(cur)
    return bl

def png_legenda(texto, path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    size = 96
    while True:
        f = ImageFont.truetype(FONT, size)
        x0, y0, x1, y1 = d.textbbox((0, 0), texto, font=f, stroke_width=7)
        if x1 - x0 <= 940 or size <= 60:
            break
        size -= 4
    x = (W - (x1 - x0)) // 2 - x0
    y = int(H * 0.70) - (y1 - y0) // 2 - y0
    d.text((x + 4, y + 6), texto, font=f, fill=(0, 0, 0, 140), stroke_width=7, stroke_fill=(0, 0, 0, 140))
    d.text((x, y), texto, font=f, fill="white", stroke_width=7, stroke_fill="black")
    img.save(path)

def monta(c):
    cid, vid = c["id"], c["vid"]
    wd = f"{WORK}/{cid}"; os.makedirs(wd, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    segs = segmentos(vid, c["segs"])
    src = f"{SRC}/{vid}.mov"
    sdr = f"{SDR}/{vid}.mov"  # convertido pelo avconvert do Mac (HDR do iPhone -> SDR com a cor certa)
    cor = "scale=1080:1920:flags=lanczos,eq=contrast=1.08:saturation=1.15:gamma=0.97,unsharp=5:5:0.4"
    lista, tokens, t_out = [], [], 0.0
    for k, (t0, t1, ws) in enumerate(segs):
        zoom = ",crop=iw/1.08:ih/1.08,scale=1080:1920" if k % 2 else ""
        dur = t1 - t0
        f = f"{wd}/seg{k:02d}.mov"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-i", sdr, "-ss", f"{t0:.3f}", "-i", src, "-t", f"{dur:.3f}",
             "-map", "0:v:0", "-map", "1:a:0",
             "-vf", cor + zoom + ",format=yuv420p,fps=30", "-af", f"aresample=48000,afade=t=in:d=0.02,afade=t=out:st={dur-0.04:.3f}:d=0.04",
             "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-c:a", "pcm_s16le", "-ac", "2", f])
        lista.append(f)
        for w in ws:
            tokens.append(dict(w, start=w["start"] - t0 + t_out, end=w["end"] - t0 + t_out))
        t_out += dur
    with open(f"{wd}/lista.txt", "w") as fh:
        fh.writelines(f"file '{x}'\n" for x in lista)
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{wd}/lista.txt", "-c", "copy", f"{wd}/corpo.mov"])
    total = t_out
    toks = corrige(tokens)
    bips = [(t["start"], t["end"]) for t in toks if t.get("bip")]
    # legenda: sequencia de PNG com duracao
    vazio = f"{wd}/vazio.png"; Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(vazio)
    linhas, cursor = [], 0.0
    bls = blocos(toks)
    for n, b in enumerate(bls):
        ini = b[0]["start"]; fim = b[-1]["end"] + 0.15
        if n + 1 < len(bls):
            prox = bls[n + 1][0]["start"]
            fim = prox if prox - fim < 0.35 else fim
        fim = min(fim, total)
        if ini > cursor:
            linhas.append((vazio, ini - cursor))
        p = f"{wd}/cap{n:03d}.png"; png_legenda(" ".join(t["cap"] for t in b), p)
        linhas.append((p, fim - max(ini, cursor))); cursor = fim
    if total > cursor:
        linhas.append((vazio, total - cursor))
    with open(f"{wd}/caps.txt", "w") as fh:
        for p, d in linhas:
            fh.write(f"file '{p}'\nduration {max(d, 0.034):.3f}\n")
        fh.write(f"file '{linhas[-1][0]}'\n")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{wd}/caps.txt", "-vf", "fps=30,format=argb",
         "-c:v", "qtrle", "-t", f"{total:.3f}", f"{wd}/caps.mov"])
    # audio: bip + loudnorm em dois passos
    if bips:
        en = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in bips)
        af = (f"[0:a]highpass=f=80,volume=0:enable='{en}'[v];"
              f"sine=f=1000:sample_rate=48000:d={total:.3f},volume=0.3,volume=0:enable='not({en})',aformat=channel_layouts=stereo[s];"
              f"[v][s]amix=inputs=2:normalize=0")
    else:
        af = "[0:a]highpass=f=80"
    r = run(["ffmpeg", "-v", "info", "-y", "-i", f"{wd}/corpo.mov", "-filter_complex", af + ",loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
    m = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    fc = af.replace("[0:a]", "[0:a]") + f",{ln}[a];[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[vv]"
    out = f"{OUT}/{cid}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{wd}/corpo.mov", "-i", f"{wd}/caps.mov", "-filter_complex", fc,
         "-map", "[vv]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-maxrate", "4M", "-bufsize", "8M",
         "-profile:v", "high", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-t", f"{total:.3f}", out])
    texto = " ".join(t["cap"] for t in toks)
    json.dump({"id": cid, "seg": round(total, 1), "bips": bips, "legenda_na_tela": texto},
              open(f"{wd}/info.json", "w"), ensure_ascii=False, indent=1)
    print(f"{cid}: {total:.1f}s, {len(segs)} trecho(s), {len(bips)} bip(s)")
    return texto

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    so = set(sys.argv[2:])
    for c in spec:
        if not so or c["id"] in so:
            monta(c)
