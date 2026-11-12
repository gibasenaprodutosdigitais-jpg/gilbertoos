"""Cortes reestruturados nº 1: refaz um corte que já foi ao ar com cara de vídeo novo.

Parte da gravação original (a mesma receita de corte por palavra de cortes.py) e muda tudo o que se vê, se ouve
e o que vai dentro do arquivo:
- velocidade 1,08x (voz no mesmo tom, sem efeito de esquilo);
- cor nova: mais quente, mais contraste e uma vinheta leve; enquadramento mais fechado (zoom de base 1,06);
- legenda nova: Futura, maiúsculas e minúsculas, numa faixa escura, com a palavra falada em dourado;
- título fixo no topo (a chamada nova do vídeo);
- arquivo novo por dentro: sem nenhum metadado do original, data de criação nova, outro perfil de codificação,
  áudio em 44,1 kHz.

Uso: python3 reestruturar.py <copys.json> [id ...]
"""
import datetime, importlib.util, json, os, random, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

REPO = "/Users/gilbertosena/Desktop/GilbertoOS"
AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(AQUI)
OUT = BASE + "/videos"
SCR = "/private/tmp/claude-501/-Users-gilbertosena-Desktop-GilbertoOS/581a240b-ffc7-4c1e-9cfb-a8ff5ca771ad/scratchpad"
WORK = SCR + "/reestruturar"
SDR = SCR + "/sdr"

# a receita dos cortes do carro (âncoras de palavra, correções da legenda, bip)
spec_c = importlib.util.spec_from_file_location(
    "cortes", REPO + "/saidas/REELS/reels-gravacoes-do-carro-2026-10-30/ferramenta/cortes.py")
C = importlib.util.module_from_spec(spec_c); spec_c.loader.exec_module(C)
SPEC = {c["id"]: c for c in json.load(open(
    REPO + "/saidas/REELS/reels-gravacoes-do-carro-2026-10-30/ferramenta/spec.json", encoding="utf-8"))}

W, H = 1080, 1920
VEL = 1.08
FUTURA = "/System/Library/Fonts/Supplemental/Futura.ttc"
F_LEG = ImageFont.truetype(FUTURA, 66, index=2)      # Futura Bold
F_TIT = ImageFont.truetype(FUTURA, 70, index=4)      # Futura Condensed ExtraBold
CREME = (250, 244, 232, 255)
OURO = (232, 180, 74, 255)
FAIXA = (16, 18, 22, 178)


def legenda_txt(t):
    """Texto da palavra na tela: a correção do dicionário, ou a palavra como foi dita (sem caixa alta forçada)."""
    cap = t["cap"]
    if t.get("bip"):
        return cap
    bruto = t["text"].strip()
    if cap == bruto.upper():
        return bruto
    txt = cap.lower()
    for errado, certo in (("martinho da vila", "Martinho da Vila"), ("collor", "Collor"), ("pronampe", "Pronampe"),
                          ("alphanilha", "Alphanilha")):
        txt = txt.replace(errado, certo)
    return txt


def quebra(palavras, fonte, larg, d):
    linhas, cur = [], []
    for p in palavras:
        teste = " ".join(x for x, _ in cur + [p])
        if cur and d.textlength(teste, font=fonte) > larg:
            linhas.append(cur); cur = []
        cur.append(p)
    if cur:
        linhas.append(cur)
    return linhas


def png_bloco(palavras, ativa, path):
    """palavras: lista de textos; ativa: índice da palavra falada (ou -1)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    itens = [(p, i) for i, p in enumerate(palavras)]
    linhas = quebra(itens, F_LEG, 860, d)
    alt_l = 84
    bloco_h = alt_l * len(linhas) + 44
    larg = max(d.textlength(" ".join(p for p, _ in l), font=F_LEG) for l in linhas) + 72
    y0 = int(H * 0.60) - bloco_h // 2
    x0 = (W - larg) // 2
    d.rounded_rectangle([x0, y0, x0 + larg, y0 + bloco_h], radius=26, fill=FAIXA)
    y = y0 + 22
    esp = d.textlength(" ", font=F_LEG)
    for l in linhas:
        lw = d.textlength(" ".join(p for p, _ in l), font=F_LEG)
        x = (W - lw) / 2
        for p, i in l:
            d.text((x, y), p, font=F_LEG, fill=OURO if i == ativa else CREME)
            x += d.textlength(p, font=F_LEG) + esp
        y += alt_l
    img.save(path)


def png_titulo(texto, path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    linhas = quebra([(p, 0) for p in texto.split()], F_TIT, 900, d)
    y = 210
    for l in linhas:
        t = " ".join(p for p, _ in l)
        lw = d.textlength(t, font=F_TIT)
        x = (W - lw) / 2
        d.text((x + 3, y + 4), t, font=F_TIT, fill=(0, 0, 0, 150))
        d.text((x, y), t, font=F_TIT, fill=CREME)
        y += 82
    d.rectangle([W / 2 - 60, y + 26, W / 2 + 60, y + 32], fill=OURO)
    img.save(path)


def monta(cid, copy):
    c = SPEC[cid]
    vid = c["vid"]
    wd = f"{WORK}/{cid}"; os.makedirs(wd, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    segs = C.segmentos(vid, c["segs"])
    src, sdr = f"{C.SRC}/{vid}.mov", f"{SDR}/{vid}.mov"
    cor = ("scale=1145:2036:flags=lanczos,crop=1080:1920:(iw-1080)/2:(ih-1920)/2-30,"
           "eq=contrast=1.13:saturation=1.06:gamma=0.95:brightness=0.01,"
           "colorbalance=rs=0.04:gs=0.01:bs=-0.05:rh=0.02:bh=-0.03,vignette=angle=PI/5,unsharp=5:5:0.35")
    lista, tokens, t_out = [], [], 0.0
    for k, (t0, t1, ws) in enumerate(segs):
        zoom = ",crop=iw/1.07:ih/1.07,scale=1080:1920" if k % 2 == 0 and len(segs) > 1 else ""
        dur = t1 - t0
        f = f"{wd}/seg{k:02d}.mov"
        C.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-i", sdr, "-ss", f"{t0:.3f}", "-i", src, "-t", f"{dur:.3f}",
               "-map", "0:v:0", "-map", "1:a:0", "-vf", cor + zoom + ",format=yuv420p,fps=30",
               "-af", f"aresample=48000,afade=t=in:d=0.02,afade=t=out:st={dur-0.04:.3f}:d=0.04",
               "-c:v", "libx264", "-crf", "15", "-preset", "veryfast", "-c:a", "pcm_s16le", "-ac", "2", f])
        lista.append(f)
        for w in ws:
            tokens.append(dict(w, start=w["start"] - t0 + t_out, end=w["end"] - t0 + t_out))
        t_out += dur
    with open(f"{wd}/lista.txt", "w") as fh:
        fh.writelines(f"file '{x}'\n" for x in lista)
    C.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{wd}/lista.txt", "-c", "copy", f"{wd}/corpo.mov"])
    total = t_out / VEL
    toks = C.corrige(tokens)
    for t in toks:  # tempos já na velocidade nova
        t["start"] /= VEL; t["end"] /= VEL
    bips = [(t["start"], t["end"]) for t in toks if t.get("bip")]

    # legenda palavra a palavra: um quadro por palavra falada dentro de cada bloco
    vazio = f"{wd}/vazio.png"; Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(vazio)
    linhas, cursor, n = [], 0.0, 0
    bls = C.blocos(toks)
    for bi, b in enumerate(bls):
        fim_b = b[-1]["end"] + 0.12
        if bi + 1 < len(bls):
            prox = bls[bi + 1][0]["start"]
            fim_b = prox if prox - fim_b < 0.3 else fim_b
        fim_b = min(fim_b, total)
        textos = [legenda_txt(t) for t in b]
        if b[0]["start"] > cursor:
            linhas.append((vazio, b[0]["start"] - cursor)); cursor = b[0]["start"]
        for wi, t in enumerate(b):
            fim_w = b[wi + 1]["start"] if wi + 1 < len(b) else fim_b
            p = f"{wd}/cap{n:04d}.png"; n += 1
            png_bloco(textos, wi, p)
            linhas.append((p, max(fim_w - cursor, 0.034))); cursor = max(fim_w, cursor + 0.034)
    if total > cursor:
        linhas.append((vazio, total - cursor))
    with open(f"{wd}/caps.txt", "w") as fh:
        for p, dd in linhas:
            fh.write(f"file '{p}'\nduration {dd:.3f}\n")
        fh.write(f"file '{linhas[-1][0]}'\n")
    C.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{wd}/caps.txt", "-vf", "fps=30,format=argb",
           "-c:v", "qtrle", "-t", f"{total:.3f}", f"{wd}/caps.mov"])
    tit = f"{wd}/titulo.png"; png_titulo(copy["titulo_na_tela"], tit)

    # áudio: velocidade nova sem mudar o tom, bip, -14 LUFS em dois passos
    vel = f"atempo={VEL}"
    if bips:
        en = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in bips)
        af = (f"[0:a]{vel},highpass=f=80,volume=0:enable='{en}'[v];"
              f"sine=f=1000:sample_rate=48000:d={total:.3f},volume=0.3,volume=0:enable='not({en})',aformat=channel_layouts=stereo[s];"
              f"[v][s]amix=inputs=2:normalize=0")
    else:
        af = f"[0:a]{vel},highpass=f=80"
    r = C.run(["ffmpeg", "-v", "info", "-y", "-i", f"{wd}/corpo.mov", "-filter_complex",
               af + ",loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
    m = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    fc = (af + f",{ln},aresample=44100[a];"
          f"[0:v]setpts=PTS/{VEL},fps=30[v0];[v0][1:v]overlay=0:0:format=auto[v1];"
          f"[v1][2:v]overlay=0:0:format=auto,format=yuv420p[vv]")

    # arquivo novo por dentro: nada do original, data de criação nova
    quando = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=random.randint(5, 600))
    out = f"{OUT}/{copy['arquivo']}"
    C.run(["ffmpeg", "-v", "error", "-y", "-i", f"{wd}/corpo.mov", "-i", f"{wd}/caps.mov", "-loop", "1", "-i", tit,
           "-filter_complex", fc, "-map", "[vv]", "-map", "[a]", "-map_metadata", "-1", "-map_chapters", "-1",
           "-metadata", f"creation_time={quando.strftime('%Y-%m-%dT%H:%M:%S.000000Z')}",
           "-metadata", f"title={copy['titulo_na_tela']}",
           "-metadata:s:v:0", "handler_name=VideoHandler", "-metadata:s:a:0", "handler_name=SoundHandler",
           "-fflags", "+bitexact", "-flags:v", "+bitexact", "-flags:a", "+bitexact",
           "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-g", "60", "-bf", "2", "-maxrate", "5M", "-bufsize", "10M",
           "-profile:v", "high", "-level", "4.1", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-movflags", "+faststart", "-t", f"{total:.3f}", out])
    print(f"{cid} -> {copy['arquivo']}: {total:.1f}s (era {t_out:.1f}s), {len(segs)} trecho(s), {len(bips)} bip(s)")
    return round(total, 1)


if __name__ == "__main__":
    copys = json.load(open(sys.argv[1], encoding="utf-8"))
    so = set(sys.argv[2:])
    for cp in copys:
        if not so or cp["id"] in so:
            cp["segundos"] = monta(cp["id"], cp)
    json.dump(copys, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
