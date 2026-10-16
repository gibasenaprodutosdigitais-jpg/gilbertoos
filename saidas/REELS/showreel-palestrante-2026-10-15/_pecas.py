from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920
FUNDO  = (16, 22, 30)
PAPEL  = (242, 239, 233)
ACENTO = (217, 152, 139)
FRACO  = (150, 158, 168)

DIN   = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
DIDOT = "/System/Library/Fonts/Supplemental/Hoefler Text.ttc"
A = "/Users/gilbertosena/Desktop/GilbertoOS/saidas/NEGOCIOS-E-MARCA/media-kit-palestrante-2026-10-14/assets"
E = "/Users/gilbertosena/Desktop/GilbertoOS/entrada-videos/palco-e-eventos"
OUT = os.path.dirname(os.path.abspath(__file__))

def f(p, s, idx=0):
    return ImageFont.truetype(p, s, index=idx)

def espacado(d, xy, txt, fonte, cor, esp):
    x, y = xy
    for ch in txt:
        d.text((x, y), ch, font=fonte, fill=cor)
        x += d.textlength(ch, font=fonte) + esp
    return x

def largura_espacada(d, txt, fonte, esp):
    return sum(d.textlength(c, font=fonte) + esp for c in txt) - esp

def cabecalho(d, com_regua=True):
    nome = f(DIN, 78)
    sub  = f(DIN, 34)
    lg = largura_espacada(d, "GILBERTO SENA", nome, 6)
    espacado(d, ((W-lg)/2, 150), "GILBERTO SENA", nome, PAPEL, 6)
    ls = largura_espacada(d, "PALESTRANTE", sub, 14)
    espacado(d, ((W-ls)/2, 248), "PALESTRANTE", sub, ACENTO, 14)
    if com_regua:
        d.rectangle([(W/2-45, 310), (W/2+45, 314)], fill=ACENTO)

def rodape(d, linha):
    ft = f(DIN, 46)
    d.rectangle([(90, 1560), (190, 1564)], fill=ACENTO)
    lg = largura_espacada(d, linha.upper(), ft, 5)
    espacado(d, (90, 1600), linha.upper(), ft, PAPEL, 5)

# --- overlay do cabecalho (alpha, fica a peca inteira) ---
im = Image.new("RGBA", (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
cabecalho(d); im.save(f"{OUT}/ov-cabecalho.png")

# --- lower third do palco (alpha) ---
im = Image.new("RGBA", (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
rodape(d, "Empreenda Summit Alphaville · 2024"); im.save(f"{OUT}/ov-alphaville.png")

# --- cortes de apoio (opacos, com legenda propria) ---
def corte(arquivo, legenda, saida, topo=600, alt=558):
    base = Image.new("RGB", (W, H), FUNDO)
    foto = Image.open(arquivo).convert("RGB")
    r = min(W / foto.width, 980 / foto.height)
    foto = foto.resize((int(foto.width*r), int(foto.height*r)), Image.LANCZOS)
    y = 420 + (980 - foto.height)//2
    base.paste(foto, ((W-foto.width)//2, y))
    d = ImageDraw.Draw(base)
    d.rectangle([((W-foto.width)//2, y-5), ((W+foto.width)//2, y-1)], fill=(140,60,52))
    cabecalho(d); rodape(d, legenda)
    base.save(saida)

corte(f"{A}/dubai-experience-2023.jpg", "Dubai Experience · 2023", f"{OUT}/cut-dubai.png")
corte(f"{A}/pbxp-2023.jpg",            "PBXP Paraíba Business Experience · 2023", f"{OUT}/cut-pbxp.png")
corte(f"{A}/palco-summit-exito.jpg",   "Summit Êxito de Empreendedorismo · 2022", f"{OUT}/cut-summit.png")
corte(f"{A}/imersao-reengenharia.jpg", "Imersão Reengenharia Empresarial · 2026", f"{OUT}/cut-imersao.png")
corte(f"{OUT}/plateia.png",            "Empreenda Summit Alphaville · 2024", f"{OUT}/cut-plateia.png")

# --- cartao de abertura ---
im = Image.new("RGB", (W, H), FUNDO); d = ImageDraw.Draw(im)
logo = Image.open(f"{A}/logo.png").convert("RGBA")
r = 300/logo.width
logo = logo.resize((300, int(logo.height*r)), Image.LANCZOS)
im.paste(logo, ((W-300)//2, 680), logo)
nome = f(DIN, 104); sub = f(DIN, 40)
lg = largura_espacada(d, "GILBERTO SENA", nome, 8)
espacado(d, ((W-lg)/2, 1010), "GILBERTO SENA", nome, PAPEL, 8)
d.rectangle([(W/2-60, 1150), (W/2+60, 1154)], fill=ACENTO)
ls = largura_espacada(d, "PALESTRANTE", sub, 18)
espacado(d, ((W-ls)/2, 1190), "PALESTRANTE", sub, ACENTO, 18)
im.save(f"{OUT}/card-abre.png")

# --- cartao de fecho ---
im = Image.new("RGB", (W, H), FUNDO); d = ImageDraw.Draw(im)
cabecalho(d)
ser = f(DIDOT, 56)
linhas = ["Diretor de Compliance do", "Instituto Êxito de Empreendedorismo"]
y = 450
for L in linhas:
    w = d.textlength(L, font=ser); d.text(((W-w)/2, y), L, font=ser, fill=PAPEL); y += 78
d.rectangle([(W/2-60, 680), (W/2+60, 684)], fill=ACENTO)
num = f(DIN, 72); rot = f(DIN, 30)
dados = [("+15 ANOS", "dentro de empresas"),
         ("+500", "empresas e empresários orientados"),
         ("R$ 500 MI", "economizados em impostos")]
y = 790
for v, r_ in dados:
    lw = largura_espacada(d, v, num, 4)
    espacado(d, ((W-lw)/2, y), v, num, ACENTO, 4)
    rw = d.textlength(r_, font=rot)
    d.text(((W-rw)/2, y+82), r_, font=rot, fill=FRACO)
    y += 150
ct = f(DIN, 44)
for i, L in enumerate(["@gilbertosenaoficial", "gruposena.com.br"]):
    lw = largura_espacada(d, L, ct, 4)
    espacado(d, ((W-lw)/2, 1530 + i*62), L, ct, PAPEL, 4)
im.save(f"{OUT}/card-fecha.png")
print("pecas prontas")
