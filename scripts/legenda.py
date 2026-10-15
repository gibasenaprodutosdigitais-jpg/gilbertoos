"""Monta as legendas: corrige o que o Whisper erra nos termos tecnicos,
descarta fragmento de frase vizinha e quebra em virgula, nao no meio."""
import re
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FONTE = "/System/Library/Fonts/HelveticaNeue.ttc"
FONTE_IDX = 9
TAM = 74
MAX_CHARS = 21
MAX_LINHAS = 2
BASE_Y = int(H * 0.745)
ENTRELINHA = 1.14
CONTORNO = 8
PAUSA, MIN_DUR, MAX_DUR = 0.34, 0.55, 3.0

FT = ImageFont.truetype(FONTE, TAM, index=FONTE_IDX)

# O Whisper nao conhece o vocabulario tributario. Legenda errada na tela
# derruba a autoridade mais rapido do que legenda nenhuma.
FRASES = [
    (["spirit", "pain", "man"],      ["split", "payment"]),
    (["spirit", "panman"],           ["split", "payment"]),
    (["split", "pain", "man"],       ["split", "payment"]),
    (["split", "pain"],              ["split", "payment"]),
    (["spirit", "pain"],             ["split", "payment"]),
    (["com", "o", "lativo"],         []),
    (["qual", "é", "a", "líquida"],  ["qual", "é", "a", "alíquota"]),
    (["a", "líquida"],               ["a", "alíquota"]),
    (["cbs", "e", "bs"],             ["CBS", "e", "IBS"]),
    (["címpus", "nacional"],         ["Simples", "Nacional"]),
    (["simples", "híbido"],          ["Simples", "Híbrido"]),
]
PALAVRAS = {
    "sib": "CIB",   # Cadastro Imobiliario Brasileiro: o Whisper ouve SIB
    "ies": "IS", "híbido": "híbrido", "banker": "bunker",
    "reenginharia": "reengenharia", "reenjeiaria": "reengenharia",
    "cbs": "CBS", "ibs": "IBS", "iss": "ISS", "icms": "ICMS",
    "das": "DAS", "crc": "CRC", "cnpj": "CNPJ", "mei": "MEI",
}
PALAVRAO = re.compile(r"(fode|foda|fodas|porra|fuck|merda|caralho|f\*+)", re.I)

def _nu(t):
    return re.sub(r"[^\wÀ-ÿ]", "", t).lower()

def corrigir(words):
    """Aplica as correcoes mantendo os tempos de cada palavra."""
    # o Whisper devolve tokens so de espaco, e eles furam o casamento de frase
    words = [w for w in words if w["text"].strip()]
    out, i = [], 0
    while i < len(words):
        bateu = False
        for alvo, troca in FRASES:
            n = len(alvo)
            if i + n <= len(words) and [_nu(words[i+k]["text"]) for k in range(n)] == alvo:
                ini, fim = words[i]["start"], words[i+n-1]["end"]
                cauda = re.sub(r"^[\wÀ-ÿ]*", "", words[i+n-1]["text"].strip())
                for j, p in enumerate(troca):
                    out.append({"text": p + (cauda if j == len(troca)-1 else ""),
                                "start": ini + (fim-ini)*j/max(1,len(troca)),
                                "end": ini + (fim-ini)*(j+1)/max(1,len(troca))})
                i += n
                bateu = True
                break
        if bateu:
            continue
        w = dict(words[i])
        t = w["text"].strip()
        base = _nu(t)
        if base in PALAVRAS:
            w["text"] = PALAVRAS[base] + re.sub(r"^[\wÀ-ÿ]*", "", t)
        w["text"] = re.sub(r"(\d)\s+%", r"\1%", w["text"])
        out.append(w)
        i += 1
    return out

def recortar(words, ini, fim, tol=0.03):
    """So entra palavra inteira dentro do corte. Fragmento de frase vizinha fica fora."""
    return [{"text": w["text"], "start": w["start"]-ini, "end": w["end"]-ini}
            for w in words if w["start"] >= ini - tol and w["end"] <= fim + tol]

def quebrar(txt):
    linhas, linha = [], ""
    for p in txt.split():
        teste = (linha + " " + p).strip()
        if len(teste) > MAX_CHARS and linha:
            linhas.append(linha); linha = p
        else:
            linha = teste
    if linha:
        linhas.append(linha)
    return linhas

def censurar(t):
    return PALAVRAO.sub(lambda m: m.group(0)[0].upper() + "***", t)

def _texto(ws):
    t = " ".join(" ".join(w["text"].split()) for w in ws).strip()
    t = re.sub(r"(\d)\s+%", r"\1%", t)
    return censurar(t)

def _cabe(ws):
    return len(quebrar(_texto(ws).upper())) <= MAX_LINHAS

def montar(words):
    ws = [w for w in words if w["text"].strip()]
    cues, i = [], 0
    while i < len(ws):
        j = i
        while j + 1 < len(ws):
            if ws[j+1]["start"] - ws[j]["end"] >= PAUSA:
                break
            if ws[j+1]["end"] - ws[i]["start"] > MAX_DUR:
                break
            if not _cabe(ws[i:j+2]):
                break
            j += 1
        # prefere fechar em pontuacao, pra nao cortar no meio da oracao
        corte = j
        for k in range(j, i, -1):
            if ws[k]["text"].strip().endswith((",", ".", "?", "!", ":", ";")):
                corte = k
                break
        txt = _texto(ws[i:corte+1])
        if txt:
            cues.append({"ini": ws[i]["start"], "fim": ws[corte]["end"], "txt": txt})
        i = corte + 1
    for n, c in enumerate(cues):
        if c["fim"] - c["ini"] < MIN_DUR:
            lim = cues[n+1]["ini"] if n+1 < len(cues) else c["ini"] + MIN_DUR
            c["fim"] = min(c["ini"] + MIN_DUR, lim)
    return cues

def desenhar(txt, destino):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    linhas = quebrar(txt.upper())
    alt = int(TAM * ENTRELINHA)
    y = BASE_Y - (len(linhas) - 1) * alt
    for ln in linhas:
        bb = d.textbbox((0, 0), ln, font=FT)
        x = (W - (bb[2] - bb[0])) // 2 - bb[0]
        d.text((x, y + 6), ln, font=FT, fill=(0, 0, 0, 150),
               stroke_width=CONTORNO + 2, stroke_fill=(0, 0, 0, 150))
        d.text((x, y), ln, font=FT, fill=(255, 255, 255, 255),
               stroke_width=CONTORNO, stroke_fill=(0, 0, 0, 255))
        y += alt
    img.save(destino)
