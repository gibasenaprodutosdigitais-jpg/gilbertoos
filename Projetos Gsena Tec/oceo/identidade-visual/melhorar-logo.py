# -*- coding: utf-8 -*-
"""
Melhora a logo OCEO (fonte: referencias/LOGO OCEO.png) e exporta em JPG:
  - reducao leve de ruido + nitidez (unsharp mask) pra limpar o render 3D
  - contraste/saturacao realcados (cromo mais vivo, dourado mais rico)
  - crop apertado ao conteudo
  - fundo novo em gradiente grafite quente (marca) + halo dourado suave
    atras do aro, colado por blend "screen" (sem serrilhado de recorte)
  - sombra de chao sutil + vinheta + upscale final com nitidez de saida
"""
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageChops

BASE = "referencias/LOGO OCEO.png"
OUT  = "OCEO - Logo (melhorada).jpg"

# paleta neutra e quente — evita "esverdear" quando o dourado mistura no fundo
BG_CENTER = (26, 24, 21)
BG_EDGE   = (5, 5, 6)
GLOW      = (255, 196, 92)

src = Image.open(BASE).convert("RGB")

# 1) reducao leve de ruido (preserva borda) + nitidez em 2 escalas + contraste/saturacao
#    (mais moderado que a 1a tentativa, pra nao estourar o brilho do cromo)
src = src.filter(ImageFilter.MedianFilter(3))
fine   = src.filter(ImageFilter.UnsharpMask(radius=1.2, percent=80, threshold=2))
coarse = fine.filter(ImageFilter.UnsharpMask(radius=5, percent=45, threshold=3))
src = coarse
src = ImageEnhance.Contrast(src).enhance(1.06)
src = ImageEnhance.Color(src).enhance(1.10)
src = ImageEnhance.Brightness(src).enhance(1.02)

# trava qualquer estouro de branco que o realce tenha introduzido
arr0 = np.asarray(src).astype(np.float32)
arr0 = np.clip(arr0, 0, 252)   # deixa ~3 níveis de folga antes do 255 puro
src = Image.fromarray(arr0.astype(np.uint8), "RGB")

# 2) crop apertado ao conteudo (tudo que nao e quase-preto)
arr = np.asarray(src).astype(int)
mask = arr.sum(axis=2) > 30 * 3
ys, xs = np.where(mask)
pad = 18
x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad, src.width)
y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad, src.height)
src = src.crop((x0, y0, x1, y1))
W, H = src.size

# 3) canvas final com margem + gradiente radial
MARGIN = int(W * 0.16)
CW, CH = W + MARGIN * 2, H + MARGIN * 2

def radial_gradient(size, c_in, c_out, cx, cy, radius):
    w, h = size
    ys, xs = np.mgrid[0:h, 0:w]
    d = np.sqrt((xs - cx) ** 2 + ((ys - cy) * (w / h * 0.82)) ** 2) / radius
    d = np.clip(d, 0, 1)
    out = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(3):
        out[..., i] = (c_in[i] + (c_out[i] - c_in[i]) * d).astype(np.uint8)
    return Image.fromarray(out, "RGB")

bg = radial_gradient((CW, CH), BG_CENTER, BG_EDGE, CW * 0.5, CH * 0.40, max(CW, CH) * 0.62)

# 3b) halo dourado suave atras do aro
glow = Image.new("RGB", (CW, CH), (0, 0, 0))
gd = ImageDraw.Draw(glow)
gw, gh = int(W * 0.6), int(W * 0.6)
gx, gy = MARGIN + W * 0.5 - gw / 2, MARGIN + H * 0.30 - gh / 2
gd.ellipse([gx, gy, gx + gw, gy + gh], fill=GLOW)
glow = glow.filter(ImageFilter.GaussianBlur(gw * 0.17))
glow = ImageEnhance.Brightness(glow).enhance(0.22)
bg = ImageChops.screen(bg, glow)

# 3c) sombra de chao sob a palavra OCEO
shadow = Image.new("L", (CW, CH), 255)
sd = ImageDraw.Draw(shadow)
sw, sh = int(W * 0.6), int(H * 0.055)
sx, sy = MARGIN + W * 0.5 - sw / 2, MARGIN + H * 0.94 - sh / 2
sd.ellipse([sx, sy, sx + sw, sy + sh], fill=170)
shadow = shadow.filter(ImageFilter.GaussianBlur(sh * 1.6))
bg = Image.composite(bg, ImageEnhance.Brightness(bg).enhance(0.55), shadow.point(lambda p: 255 - (255 - p)))

# 4) cola a arte por "screen" (o preto da fonte some, sem corte serrilhado)
layer = Image.new("RGB", (CW, CH), (0, 0, 0))
layer.paste(src, (MARGIN, MARGIN))
canvas = ImageChops.screen(bg, layer)

# 5) vinheta final suave
vin = radial_gradient((CW, CH), (255, 255, 255), (140, 140, 140),
                       CW * 0.5, CH * 0.5, max(CW, CH) * 0.75).convert("L")
canvas = Image.composite(canvas, ImageEnhance.Brightness(canvas).enhance(0.70), vin)

# 6) upscale pra resolucao alta (aguenta ampliar sem pixelar) + nitidez de saida
#    resample em 2 passos (LANCZOS) fica mais limpo que 1 salto grande direto
TARGET_W = 3200
step_w = min(CW * 2, TARGET_W)
canvas = canvas.resize((step_w, int(CH * step_w / CW)), Image.LANCZOS)
scale = TARGET_W / canvas.width
canvas = canvas.resize((TARGET_W, int(canvas.height * scale)), Image.LANCZOS)
canvas = canvas.filter(ImageFilter.UnsharpMask(radius=2, percent=55, threshold=2))

canvas.convert("RGB").save(OUT, "JPEG", quality=96, subsampling=0, optimize=True)
print("OK ->", OUT, canvas.size)
