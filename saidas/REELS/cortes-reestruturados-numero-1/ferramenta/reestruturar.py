"""Cortes reestruturados nº 1: refaz um corte que já foi ao ar com cara de vídeo novo.

Parte da gravação original (a mesma receita de corte por palavra de cortes.py) e muda tudo o que se vê, se ouve
e o que vai dentro do arquivo:
- velocidade 1,22x (voz no mesmo tom, sem efeito de esquilo);
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
VEL = 1.22  # era 1,08, depois 1,15; ele pediu mais rápido duas vezes em 12/nov
ZOOM_FATOR = 1.0  # nos vídeos que já têm legenda e título na imagem, o zoom é mais leve (0,5)
FUTURA = "/System/Library/Fonts/Supplemental/Futura.ttc"
F_LEG = ImageFont.truetype(FUTURA, 66, index=2)      # Futura Bold
F_TIT = ImageFont.truetype(FUTURA, 70, index=4)      # Futura Condensed ExtraBold
CREME = (250, 244, 232, 255)
OURO = (232, 180, 74, 255)
FAIXA = (16, 18, 22, 178)

# cada corte com uma combinação própria de fundo e letra (pedido dele em 12/nov); vai em rodízio pela ordem do copys.json
PALETAS = [
    {"nome": "grafite e dourado", "fundo": (13, 14, 17), "texto": (250, 244, 232), "destaque": (232, 180, 74), "medo": (229, 72, 77)},
    {"nome": "marinho e amarelo", "fundo": (10, 26, 54), "texto": (255, 255, 255), "destaque": (255, 204, 0), "medo": (255, 92, 92)},
    {"nome": "vinho e champanhe", "fundo": (70, 12, 24), "texto": (252, 238, 222), "destaque": (255, 205, 140), "medo": (255, 110, 110)},
    {"nome": "verde-escuro e limão", "fundo": (8, 46, 36), "texto": (255, 255, 255), "destaque": (170, 230, 60), "medo": (255, 96, 96)},
    {"nome": "creme e preto", "fundo": (246, 240, 228), "texto": (22, 22, 24), "destaque": (196, 32, 44), "medo": (196, 32, 44)},
    {"nome": "roxo e laranja", "fundo": (36, 18, 64), "texto": (255, 255, 255), "destaque": (255, 146, 30), "medo": (255, 92, 92)},
    {"nome": "amarelo e preto", "fundo": (255, 204, 0), "texto": (18, 18, 18), "destaque": (168, 16, 28), "medo": (120, 0, 12)},
    {"nome": "petróleo e coral", "fundo": (6, 52, 64), "texto": (240, 250, 250), "destaque": (255, 128, 100), "medo": (255, 80, 80)},
]
PAL = dict(PALETAS[0])


def rgba(c, a=255):
    return tuple(c[:3]) + (a,)


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


def png_bloco(palavras, ativa, path, cor_ativa=None, pop=None):
    """palavras: lista de textos; ativa: índice da palavra falada (ou -1)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    itens = [(p, i) for i, p in enumerate(palavras)]
    linhas = quebra(itens, F_LEG, 860, d)
    alt_l = 84
    bloco_h = alt_l * len(linhas) + 44
    larg = max(d.textlength(" ".join(p for p, _ in l), font=F_LEG) for l in linhas) + 72
    y0 = int(H * 0.775) - bloco_h // 2
    x0 = (W - larg) // 2
    claro = sum(PAL['fundo']) > 500
    d.rounded_rectangle([x0, y0, x0 + larg, y0 + bloco_h], radius=26, fill=rgba(PAL['fundo'], 235 if claro else 205))
    if pop:  # número falado, grande, logo acima da legenda
        fp = ImageFont.truetype(FUTURA, 120, index=4)
        pw = d.textlength(pop, font=fp)
        while pw > 940:
            fp = ImageFont.truetype(FUTURA, fp.size - 8, index=4); pw = d.textlength(pop, font=fp)
        py = y0 - fp.size - 70
        d.rounded_rectangle([(W - pw) / 2 - 34, py - 14, (W + pw) / 2 + 34, py + fp.size + 24], radius=30,
                            fill=rgba(PAL['destaque']))
        d.text(((W - pw) / 2, py), pop, font=fp, fill=rgba(PAL['fundo']))
    y = y0 + 22
    esp = d.textlength(" ", font=F_LEG)
    for l in linhas:
        lw = d.textlength(" ".join(p for p, _ in l), font=F_LEG)
        x = (W - lw) / 2
        for p, i in l:
            d.text((x, y), p, font=F_LEG, fill=rgba(cor_ativa or PAL['destaque']) if i == ativa else rgba(PAL['texto']))
            x += d.textlength(p, font=F_LEG) + esp
        y += alt_l
    img.save(path)


CAPA_H = int(H * 0.60)
CAPA_DUR = 1.4  # segundos com a capa na tela; depois ela some e fica o título pequeno


def png_capa(texto, path, topo=None, base=None, opac=240):
    """Faixa de 60% da tela no meio, cobrindo o rosto, com a headline grande. *palavra* sai em dourado."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # faixa de 60% da tela no MEIO do vídeo, em cima do rosto (pedido dele), com as bordas esfumadas
    borda = 150
    topo = (H - CAPA_H) // 2 if topo is None else topo
    base = (H + CAPA_H) // 2 if base is None else base
    for y in range(topo - borda, base + borda):
        dist = max(topo - y, y - base, 0)
        a = int(opac * (1 - dist / borda))
        d.line([(0, y), (W, y)], fill=rgba(PAL['fundo'], a))
    marca, partes = False, []
    for parte in texto.split("|"):  # '|' força quebra de linha
        pal2 = []
        for p in parte.split():  # marcação pode abranger várias palavras: *pedir ajuda*
            if p.startswith("*"):
                marca = True
            pal2.append((p.strip("*"), marca))
            if p.endswith("*"):
                marca = False
        partes.append(pal2)
    escolha = None
    for maximo in (3, 4):  # a maior letra que caiba em 3 linhas; se não der, em 4
        for tam in range(150, 88, -6):
            f = ImageFont.truetype(FUTURA, tam, index=4)
            linhas = [l for pt in partes for l in quebra(pt, f, 940, d)]
            if len(linhas) <= maximo and (len(linhas[0]) > 1 or len(partes) > 1):
                escolha = (tam, f, linhas); break
        if escolha:
            break
    tam, f, linhas = escolha or (tam, f, linhas)
    alt = int(tam * 1.08)
    bloco = alt * len(linhas)
    y = (H - bloco) // 2 + 20  # no meio do vídeo, em cima do rosto (pedido dele)
    rot = ImageFont.truetype(FUTURA, 34, index=2)
    r = "G I L B E R T O   S E N A"
    d.text(((W - d.textlength(r, font=rot)) / 2, y - 110), r, font=rot, fill=rgba(PAL['destaque']))
    esp = d.textlength(" ", font=f)
    for l in linhas:
        lw = d.textlength(" ".join(p for p, _ in l), font=f)
        x = (W - lw) / 2
        for p, dourado in l:
            if sum(PAL['fundo']) < 500:
                d.text((x + 4, y + 5), p, font=f, fill=(0, 0, 0, 160))
            d.text((x, y), p, font=f, fill=rgba(PAL['destaque'] if dourado else PAL['texto']))
            x += d.textlength(p, font=f) + esp
        y += alt
    d.rectangle([W / 2 - 80, y + int(tam * 0.42), W / 2 + 80, y + int(tam * 0.42) + 8], fill=rgba(PAL['destaque']))
    img.save(path)


def png_titulo(texto, path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pal = texto.split()
    linhas = quebra([(p, 0) for p in pal], F_TIT, 900, d)
    if len(linhas) == 2:  # duas linhas equilibradas, sem palavra sozinha
        melhor = min(range(1, len(pal)), key=lambda k: abs(d.textlength(" ".join(pal[:k]), font=F_TIT)
                                                          - d.textlength(" ".join(pal[k:]), font=F_TIT)))
        for k in range(1, len(pal)):  # quebra depois de ponto ou vírgula, se as linhas couberem
            l1, l2 = (d.textlength(" ".join(x), font=F_TIT) for x in (pal[:k], pal[k:]))
            if pal[k - 1][-1] in ".,:?!" and max(l1, l2) <= 900:
                melhor = k
        linhas = [[(p, 0) for p in pal[:melhor]], [(p, 0) for p in pal[melhor:]]]
    y = 210
    for l in linhas:
        t = " ".join(p for p, _ in l)
        lw = d.textlength(t, font=F_TIT)
        x = (W - lw) / 2
        d.text((x + 3, y + 4), t, font=F_TIT, fill=(0, 0, 0, 150))
        d.text((x, y), t, font=F_TIT, fill=CREME)
        y += 82
    traco = PAL['fundo'] if PAL['destaque'] == (255, 255, 255) else PAL['destaque']
    d.rectangle([W / 2 - 60, y + 26, W / 2 + 60, y + 32], fill=rgba(traco))
    img.save(path)


# ---- efeitos (pedido dele em 12/nov: "zoom, um efeito de medo, entre outros") ----
VERMELHO = (229, 72, 77, 255)
MEDO = ("medo", "paralis", "quebr", "falenc", "faliu", "morr", "terror", "desesper", "perig", "risco", "crise", "apavor",
        "assust", "pesadel", "prejuiz", "panico", "inadimpl")
DINHEIRO = ("dinheiro", "lucro", "caixa", "imposto", "milh", "bilh", "reais", "fatur", "economi", "honorari", "tribut")
ENFASE = {"nunca", "sempre", "ninguem", "tudo", "verdade", "segredo", "cuidado", "atencao", "jamais", "nada",
          "obrigacao"}
ALERTA = ("erro", "errad", "problema", "falh", "culpa", "golpe", "mentir", "engan")
LUZ = ("ajud", "solucao", "solucoes", "resolv", "caminho", "oportunidad", "cresc", "sucesso", "conquist", "prosper",
       "result", "evolu", "aprend")
FE = ("deus", "proverbi", "salomao", "biblia", "biblic", "jesus", "sabedoria", "senhor", "abencoa", "gratid")
NUM_UNID = ("mil", "milhao", "milhoes", "bilhao", "bilhoes", "reais", "real", "porcento", "anos", "meses", "dias", "vezes",
            "clientes", "empresas", "funcionarios", "horas")


def familia(t):
    n = t["n"]
    if n.startswith(MEDO):
        return "medo"
    if n.startswith(ALERTA):
        return "alerta"
    if n.startswith(DINHEIRO):
        return "dinheiro"
    if n.startswith(FE) or n == "fe":
        return "fe"
    if n.startswith(LUZ):
        return "luz"
    if n in ENFASE:
        return "enfase"
    return None


def cor_palavra(t):
    return PAL["medo"] if familia(t) in ("medo", "alerta") else PAL["destaque"]


def numeros(toks):
    """Números falados viram destaque grande na tela: '40 mil', '600 reais', '20, 30, 40 mil'."""
    pops, i, ultimo = [], 0, -9.0
    while i < len(toks):
        if any(ch.isdigit() for ch in toks[i]["n"]):
            j = i
            while j + 1 < len(toks) and j - i < 5 and (any(ch.isdigit() for ch in toks[j + 1]["n"])
                                                          or toks[j + 1]["n"] in NUM_UNID):
                j += 1
            txt = " ".join(legenda_txt(t).strip(".!?") for t in toks[i:j + 1]).rstrip(",")
            if toks[i]["start"] - ultimo > 2.0 and not (j == i and len(toks[i]["n"]) == 4 and toks[i]["n"].startswith("20")) \
                    or any(u in txt for u in ("mil", "reais", "milh", "%")):
                pops.append((toks[i]["start"], toks[j]["end"] + 0.7, txt)); ultimo = toks[i]["start"]
            i = j + 1
        else:
            i += 1
    return pops


def eventos(toks, bls, total):
    """Escolhe os momentos dos efeitos: medo tem prioridade; zoom de ritmo onde passar de 4 s sem nada."""
    ev, ultimo, n_medo = [], -9.0, 0
    for t in toks:
        f = familia(t)
        if not f:
            continue
        if f == "medo":  # no máximo 3 por vídeo e com 3 s de folga; o resto vira zoom simples
            if n_medo >= 3 or t["start"] - max([a for a, g in ev if g == "medo"] or [-9]) < 3.0:
                f = "enfase"
        folga = 1.2 if f in ("medo", "alerta") else 2.2
        if t["start"] - ultimo >= folga and t["start"] < total - 0.6:
            ev.append((t["start"], f)); ultimo = t["start"]
            n_medo += f == "medo"
    inicios = sorted(b[0]["start"] for b in bls)
    for s in inicios:
        if s > 1.0 and s < total - 1.5 and all(abs(s - a) > 4.0 for a, _ in ev):
            ev.append((s, "ritmo"))
    return sorted(ev)


def filtro_efeitos(ev, juntas, total):
    amp = {k: v * ZOOM_FATOR for k, v in {"medo": 0.17, "alerta": 0.13, "dinheiro": 0.10, "enfase": 0.12, "ritmo": 0.09, "luz": 0.06, "fe": 0.05}.items()}
    bumps = [f"{amp[f]}*if(between(it,{a:.2f},{a+0.18:.2f}),(it-{a:.2f})/0.18,"
             f"if(between(it,{a+0.18:.2f},{a+1.5:.2f}),1-(it-{a+0.18:.2f})/1.32,0))" for a, f in ev]
    z = f"1+0.04*it/{total:.2f}" + "".join("+" + b for b in bumps)
    cadeia = [f"scale=1620:2880:flags=bicubic",
              f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1120x1992:fps=30"]
    medo = [(a, f) for a, f in ev if f == "medo"]
    if medo:
        jan = "+".join(f"between(t,{a-0.05:.2f},{a+1.1:.2f})" for a, _ in medo)
        tremor_x = "+".join(f"if(between(t,{a:.2f},{a+0.9:.2f}),13*sin(t*53),0)" for a, _ in medo)
        tremor_y = "+".join(f"if(between(t,{a:.2f},{a+0.9:.2f}),9*cos(t*61),0)" for a, _ in medo)
        glitch = "+".join(f"between(t,{a:.2f},{a+0.2:.2f})" for a, _ in medo)
        cadeia += [f"crop=1080:1920:x='20+({tremor_x})':y='36+({tremor_y})'",
                   f"hue=s=0.35:enable='{jan}'",
                   f"colorbalance=rs=0.16:rm=0.07:bs=-0.06:enable='{jan}'",
                   f"vignette=angle=PI/3.2:enable='{jan}'",
                   f"rgbashift=rh=-9:bh=9:enable='{glitch}'"]
    else:
        cadeia.append("crop=1080:1920:20:36")
    din = [a for a, f in ev if f == "dinheiro"]
    if din:
        jan = "+".join(f"between(t,{a:.2f},{a+0.35:.2f})" for a in din)
        cadeia += [f"eq=brightness=0.035:saturation=1.12:enable='{jan}'",
                   f"colorbalance=rh=0.08:gh=0.05:bh=-0.08:enable='{jan}'"]
    alerta = [a for a, f in ev if f == "alerta"]
    if alerta:  # erro e problema: pulso vermelho curto nas bordas, sem tremor
        jan = "+".join(f"between(t,{a:.2f},{a+0.45:.2f})" for a in alerta)
        cadeia += [f"colorbalance=rs=0.12:rm=0.05:bs=-0.04:enable='{jan}'", f"vignette=angle=PI/3.5:enable='{jan}'"]
    luz = [a for a, f in ev if f == "luz"]
    if luz:  # ajuda, solução, caminho, crescer: a imagem abre e clareia
        jan = "+".join(f"between(t,{a:.2f},{a+0.8:.2f})" for a in luz)
        cadeia += [f"eq=brightness=0.05:saturation=1.10:gamma=1.05:enable='{jan}'",
                   f"colorbalance=rh=0.05:gh=0.03:bh=-0.02:enable='{jan}'"]
    fe = [a for a, f in ev if f == "fe"]
    if fe:  # Deus, Provérbios, sabedoria: luz quente e suave, mais longa
        jan = "+".join(f"between(t,{a:.2f},{a+1.4:.2f})" for a in fe)
        cadeia += [f"eq=brightness=0.04:contrast=0.96:saturation=1.05:enable='{jan}'",
                   f"colorbalance=rh=0.10:gh=0.06:bh=-0.06:rm=0.04:enable='{jan}'"]
    if juntas:
        jan = "+".join(f"between(t,{j:.2f},{j+0.07:.2f})" for j in juntas)
        cadeia.append(f"eq=brightness=0.35:enable='{jan}'")
    return ",".join(cadeia)


def monta(cid, copy):
    c = SPEC[cid]
    vid = c["vid"]
    wd = f"{WORK}/{cid}"; os.makedirs(wd, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    segs = C.segmentos(vid, c["segs"])
    src, sdr = f"{C.SRC}/{vid}.mov", f"{SDR}/{vid}.mov"
    climas = {  # cor de base pelo assunto do corte
        "neutro": "eq=contrast=1.13:saturation=1.06:gamma=0.95:brightness=0.01,"
                  "colorbalance=rs=0.04:gs=0.01:bs=-0.05:rh=0.02:bh=-0.03,vignette=angle=PI/5",
        "tenso": "eq=contrast=1.18:saturation=0.90:gamma=0.92,"
                 "colorbalance=rs=-0.02:bs=0.05:rm=0.02:bh=0.02,vignette=angle=PI/4",
        "dinheiro": "eq=contrast=1.12:saturation=1.10:gamma=0.96:brightness=0.01,"
                    "colorbalance=rs=0.03:bs=-0.06:rh=0.06:gh=0.03:bh=-0.08,vignette=angle=PI/5",
        "inspirador": "eq=contrast=1.08:saturation=1.10:gamma=1.0:brightness=0.03,"
                      "colorbalance=rs=0.03:bs=-0.04:rh=0.04:gh=0.02:bh=-0.04,vignette=angle=PI/6",
    }
    cor = ("scale=1145:2036:flags=lanczos,crop=1080:1920:(iw-1080)/2:(ih-1920)/2-30,"
           + climas[copy.get("clima", "neutro")] + ",unsharp=5:5:0.35")
    lista, tokens, t_out, juntas_in = [], [], 0.0, []
    for k, (t0, t1, ws) in enumerate(segs):
        zoom = ""  # o zoom agora é o dos efeitos
        dur = t1 - t0
        f = f"{wd}/seg{k:02d}.mov"
        C.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-i", sdr, "-ss", f"{t0:.3f}", "-i", src, "-t", f"{dur:.3f}",
               "-map", "0:v:0", "-map", "1:a:0", "-vf", cor + zoom + ",format=yuv420p,fps=30",
               "-af", f"aresample=48000,afade=t=in:d=0.02,afade=t=out:st={dur-0.04:.3f}:d=0.04",
               "-c:v", "libx264", "-crf", "15", "-preset", "veryfast", "-c:a", "pcm_s16le", "-ac", "2", f])
        lista.append(f)
        if k:
            juntas_in.append(t_out)
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
    pops = numeros(toks)
    copy["numeros_na_tela"] = [txt for _, _, txt in pops]
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
            pop = next((txt for a, b, txt in pops if a - 0.01 <= t["start"] <= b), None)
            png_bloco(textos, wi, p, cor_palavra(t), pop)
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
    capa = f"{wd}/capa.png"; png_capa(copy.get("capa", copy["titulo_na_tela"]), capa)
    ev = eventos(toks, bls, total)
    efx = filtro_efeitos(ev, [j / VEL for j in juntas_in], total)
    copy["efeitos"] = [f"{a:.1f}s {f}" for a, f in ev]

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
          f"[0:v]setpts=PTS/{VEL},fps=30,{efx}[v0];[v0][1:v]overlay=0:0:format=auto:enable='gte(t,{CAPA_DUR-0.2})'[v1];"
          f"[v1][2:v]overlay=0:0:format=auto:enable='gte(t,{CAPA_DUR})'[v2];"
          f"[3:v]format=rgba,fade=t=out:st={CAPA_DUR-0.25}:d=0.25:alpha=1[cp];"
          f"[v2][cp]overlay=0:0:format=auto:eof_action=pass,format=yuv420p[vv]")

    # arquivo novo por dentro: nada do original, data de criação nova
    quando = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=random.randint(5, 600))
    out = f"{OUT}/{copy['arquivo']}"
    C.run(["ffmpeg", "-v", "error", "-y", "-i", f"{wd}/corpo.mov", "-i", f"{wd}/caps.mov", "-loop", "1", "-i", tit, "-loop", "1", "-t", f"{CAPA_DUR}", "-i", capa,
           "-filter_complex", fc, "-map", "[vv]", "-map", "[a]", "-map_metadata", "-1", "-map_chapters", "-1",
           "-metadata", f"creation_time={quando.strftime('%Y-%m-%dT%H:%M:%S.000000Z')}",
           "-metadata", f"title={copy['titulo_na_tela']}",
           "-metadata:s:v:0", "handler_name=VideoHandler", "-metadata:s:a:0", "handler_name=SoundHandler",
           "-fflags", "+bitexact", "-flags:v", "+bitexact", "-flags:a", "+bitexact",
           "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-g", "60", "-bf", "2", "-maxrate", "5M", "-bufsize", "10M",
           "-profile:v", "high", "-level", "4.1", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-movflags", "+faststart", "-t", f"{total:.3f}", out])
    os.makedirs(BASE + "/capas", exist_ok=True)
    C.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.6", "-i", out, "-frames:v", "1", "-q:v", "2",
           BASE + "/capas/" + copy["arquivo"].replace(".mp4", ".jpg")])
    print(f"{cid} -> {copy['arquivo']}: {total:.1f}s (era {t_out:.1f}s), {len(segs)} trecho(s), {len(bips)} bip(s)")
    return round(total, 1)


if __name__ == "__main__":
    copys = json.load(open(sys.argv[1], encoding="utf-8"))
    so = set(sys.argv[2:])
    for cp in copys:
        if not so or cp["id"] in so:
            PAL.clear(); PAL.update(PALETAS[copys.index(cp) % len(PALETAS)])
            cp["paleta"] = PAL["nome"]
            cp["segundos"] = monta(cp["id"], cp)
    json.dump(copys, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
