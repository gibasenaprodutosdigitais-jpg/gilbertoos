#!/usr/bin/env python3
"""Move os selos de registro pra leitura/, deixa o fundo branco transparente,
e carimba o selo na folha de rosto (pág. 2) de cada e-book pronto."""
import os, glob, pymupdf
from PIL import Image

ROOT="/Users/gilbertosena/Desktop/GilbertoOS"
DL=os.path.expanduser("~/Downloads")
LEIT=f"{ROOT}/leitura"
OUT=f"{ROOT}/E-boocks prontos"
TMP=f"{ROOT}/saidas/ebook-seja-rico-montado-2026-09-08/_selos"
os.makedirs(TMP, exist_ok=True)

# slug do arquivo -> título (nome do PDF pronto)
M={
 "de-motoboy-a-executivo":"De Motoboy a Executivo",
 "a-startap-unicornio":"A Startap Unicornio",
 "no-controle-das-emocoes":"No Controle Das Emocoes",
 "entenda-suas-financas":"Entenda Suas Financas",
 "estrategia-da-gestao":"Estrategia da Gestao",
 "o-segredo-das-financas":"O Segredo Das Financas",
 "os-pilares-de-um-homem-prospero":"Os Pilares de um Homem Prospero",
 "quite-suas-dividas-ja":"Quite Suas Dividas Ja",
 "posicionese-ou-morra":"Posicione-se ou Morra",
 "seja-rico-ou-pobre":"Seja Rico ou Pobre",
}

def transparent_png(src, dst):
    im=Image.open(src).convert("RGBA")
    px=im.load()
    for y in range(im.height):
        for x in range(im.width):
            r,g,b,a=px[x,y]
            if r>238 and g>238 and b>238:
                px[x,y]=(r,g,b,0)
    im.save(dst)

for slug,title in M.items():
    matches=glob.glob(f"{DL}/{glob.escape(slug)}.docx*_pt.jpg")
    if not matches:
        print("!! selo não encontrado:", slug); continue
    src=matches[0]
    jpg=f"{LEIT}/Selo - {title}.jpg"
    if not os.path.exists(jpg):
        Image.open(src).convert("RGB").save(jpg, quality=92)
    png=f"{TMP}/{slug}.png"
    transparent_png(src, png)

    pdf=f"{OUT}/{title} - Gilberto Sena.pdf"
    if not os.path.exists(pdf):
        print("!! pdf não encontrado:", pdf); continue
    d=pymupdf.open(pdf)
    pg=d[1]  # folha de rosto
    W,H=pg.rect.width, pg.rect.height
    im=Image.open(png); ar=im.height/im.width
    w=37; h=w*ar                       # ~13mm de largura, discreto
    # bloco de conteúdo = maior retângulo de FUNDO CREME (não o branco da página)
    box=None
    for dr in pg.get_drawings():
        r=dr.get("rect"); f=dr.get("fill")
        if r and f and 0.80 < min(f) < 0.985 and r.width > W*0.6 and r.height > H*0.3:
            if box is None or r.height > box.height: box=r
    if box is None:
        box=pymupdf.Rect(30, 40, W-40, H*0.75)
    right = min(box.x1, W-40) - 14
    bottom = box.y1 - 18
    x1 = right - w; y1 = bottom - h
    pg.insert_image(pymupdf.Rect(x1,y1,x1+w,y1+h), filename=png, keep_proportion=True, overlay=True)
    tmp=pdf+".tmp"
    d.save(tmp, garbage=4, deflate=True); d.close()
    os.replace(tmp, pdf)
    print(f"carimbado: {title}")
