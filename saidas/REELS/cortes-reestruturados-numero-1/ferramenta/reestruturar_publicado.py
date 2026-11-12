"""Cortes reestruturados nº 1, para os vídeos que já foram ao ar com legenda e título gravados na imagem
(lotes editados por terceiros, AME, antigos, 7 pecados...). Não temos a gravação original deles, então:

- a legenda e o título antigos ficam (estão na imagem), e NÃO entra legenda nova por cima;
- muda todo o resto: velocidade 1,22x, cor pelo assunto (clima), capa no meio cobrindo o rosto com a headline nova,
  efeitos pelo sentido da fala (com a transcrição local), zoom mais leve pra não cortar o título antigo,
  arquivo novo por dentro (sem metadado nenhum do original) e texto novo.

Uso: python3 reestruturar_publicado.py <copys-publicados.json> [fonte ...]
"""
import datetime, importlib.util, json, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("r", AQUI + "/reestruturar.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
C = R.C
R.ZOOM_FATOR = 0.5

SCR = R.SCR
PUB = SCR + "/publicados"
TRANS = SCR + "/transcricoes"


def tokens(nome):
    d = json.load(open(f"{TRANS}/{nome}.json", encoding="utf-8"))
    out = []
    for w in d["words"]:
        if w.get("type", "word") != "word":
            continue
        n = C.norm(w["text"])
        if n:
            out.append({"text": w["text"], "n": n, "cap": w["text"].upper(),
                        "start": w["start"] / R.VEL, "end": w["end"] / R.VEL})
    return out


def monta(cp):
    nome = cp["fonte"]
    src = f"{PUB}/{nome}.mp4"
    wd = f"{R.WORK}/pub-{nome}"; os.makedirs(wd, exist_ok=True); os.makedirs(R.OUT, exist_ok=True)
    dur = float(C.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]).stdout)
    total = dur / R.VEL
    toks = tokens(nome)
    bls = C.blocos(toks) if toks else []
    ev = R.eventos(toks, bls, total)
    efx = R.filtro_efeitos(ev, [], total)
    cp["efeitos"] = [f"{a:.1f}s {f}" for a, f in ev]
    capa = f"{wd}/capa.png"; R.png_capa(cp["capa"], capa, topo=0, base=int(R.H * 0.80), opac=255)  # cobre também o título antigo do topo
    climas = {
        "neutro": "eq=contrast=1.10:saturation=1.05:gamma=0.97,colorbalance=rs=0.03:bs=-0.04:rh=0.02:bh=-0.02,vignette=angle=PI/5",
        "tenso": "eq=contrast=1.15:saturation=0.90:gamma=0.94,colorbalance=rs=-0.02:bs=0.05:rm=0.02:bh=0.02,vignette=angle=PI/4",
        "dinheiro": "eq=contrast=1.10:saturation=1.08:gamma=0.97,colorbalance=rs=0.03:bs=-0.05:rh=0.05:gh=0.03:bh=-0.07,vignette=angle=PI/5",
        "inspirador": "eq=contrast=1.06:saturation=1.08:brightness=0.02,colorbalance=rs=0.03:bs=-0.03:rh=0.04:gh=0.02:bh=-0.04,vignette=angle=PI/6",
    }
    tem_audio = "audio" in C.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", src]).stdout
    v = (f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,"
         f"{climas[cp.get('clima', 'neutro')]},setpts=PTS/{R.VEL},fps=30,{efx}[v1];"
         f"[1:v]format=rgba,fade=t=out:st={R.CAPA_DUR-0.25}:d=0.25:alpha=1[cp];"
         f"[v1][cp]overlay=0:0:format=auto:eof_action=pass,format=yuv420p[vv]")
    if tem_audio:
        v += f";[0:a]atempo={R.VEL},highpass=f=60,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[a]"
    quando = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=random.randint(5, 600))
    out = f"{R.OUT}/{cp['arquivo']}"
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", src, "-loop", "1", "-t", f"{R.CAPA_DUR}", "-i", capa,
           "-filter_complex", v, "-map", "[vv]"] + (["-map", "[a]"] if tem_audio else []) + [
           "-map_metadata", "-1", "-map_chapters", "-1",
           "-metadata", f"creation_time={quando.strftime('%Y-%m-%dT%H:%M:%S.000000Z')}",
           "-metadata", f"title={cp['titulo']}",
           "-metadata:s:v:0", "handler_name=VideoHandler", "-metadata:s:a:0", "handler_name=SoundHandler",
           "-fflags", "+bitexact", "-flags:v", "+bitexact", "-flags:a", "+bitexact",
           "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-g", "60", "-bf", "2", "-maxrate", "5M", "-bufsize", "10M",
           "-profile:v", "high", "-level", "4.1", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-movflags", "+faststart", "-t", f"{total:.3f}", out]
    C.run(cmd)
    os.makedirs(R.BASE + "/capas", exist_ok=True)
    C.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.6", "-i", out, "-frames:v", "1", "-q:v", "2",
           R.BASE + "/capas/" + cp["arquivo"].replace(".mp4", ".jpg")])
    print(f"{nome} -> {cp['arquivo']}: {total:.1f}s (era {dur:.1f}s), {len(ev)} efeito(s)", flush=True)
    return round(total, 1)


if __name__ == "__main__":
    arq = sys.argv[1]
    copys = json.load(open(arq, encoding="utf-8"))
    so = set(sys.argv[2:])
    for i, cp in enumerate(copys):
        if so and cp["fonte"] not in so:
            continue
        R.PAL.clear(); R.PAL.update(R.PALETAS[(i + 2) % len(R.PALETAS)])  # continua o rodízio depois dos 26 do carro
        cp["paleta"] = R.PAL["nome"]
        cp["segundos"] = monta(cp)
        json.dump(copys, open(arq, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
