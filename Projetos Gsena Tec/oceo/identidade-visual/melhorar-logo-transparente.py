# -*- coding: utf-8 -*-
"""
Gera as versoes TRANSPARENTES melhoradas da logo OCEO (pra colar em slide,
video e documento que ja tem fundo proprio) a partir da mesma arte-fonte
usada no JPG (referencias/LOGO OCEO.png), com o mesmo tratamento de
qualidade: reducao de ruido, nitidez em duas escalas, contraste/saturacao
moderados (sem estourar o especular do cromo).

Sobrescreve os arquivos canonicos da identidade:
  LOGO-OCEO.png        (logo completa: icone + "OCEO")
  LOGO-OCEO-mark.png   (so o icone, sem a palavra)
"""
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

BASE = "referencias/LOGO OCEO.png"

src = Image.open(BASE).convert("RGB")

# 1) mesmo tratamento de qualidade do JPG (moderado, sem estourar branco)
src = src.filter(ImageFilter.MedianFilter(3))
fine   = src.filter(ImageFilter.UnsharpMask(radius=1.2, percent=80, threshold=2))
coarse = fine.filter(ImageFilter.UnsharpMask(radius=5, percent=45, threshold=3))
src = coarse
src = ImageEnhance.Contrast(src).enhance(1.06)
src = ImageEnhance.Color(src).enhance(1.10)
src = ImageEnhance.Brightness(src).enhance(1.02)

rgb = np.asarray(src).astype(np.float32)

# 2) alpha por luminancia (fundo preto -> transparente), com rampa suave
lum = rgb.max(axis=2)  # value do HSV: mais fiel pro brilho do metal que a media
LOW, HIGH = 10.0, 46.0
alpha = np.clip((lum - LOW) / (HIGH - LOW), 0, 1)

# 3) alpha reta (sem descontaminar): todo uso desta logo e sobre fundo
#    escuro (grafite/preto), entao a franja escura da transicao nao aparece;
#    dividir pelo alpha aqui amplificava ruido de cor nas bordas (halo
#    avermelhado) — pior que a franja escura que resolveria.
rgba = np.dstack([rgb, alpha * 255]).astype(np.uint8)
full = Image.fromarray(rgba, "RGBA")

# 4) crop apertado ao conteudo total
a = np.asarray(full)[..., 3]
ys, xs = np.where(a > 6)
pad = 14
x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad, full.width)
y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad, full.height)
full = full.crop((x0, y0, x1, y1))

# 5) upscale 2x (lanczos) pra aguentar ampliacao, com nitidez de saida leve
full = full.resize((full.width * 2, full.height * 2), Image.LANCZOS)
rgb_ch = Image.merge("RGB", full.split()[:3])
rgb_ch = rgb_ch.filter(ImageFilter.UnsharpMask(radius=2, percent=50, threshold=2))
full = Image.merge("RGBA", (*rgb_ch.split(), full.split()[3]))

full.save("LOGO-OCEO.png")
print("OK -> LOGO-OCEO.png", full.size)

# 6) recorta so o icone (acima da palavra "OCEO"): acha o maior vao vazio
#    entre ~35% e ~85% da altura e corta ali
a2 = np.asarray(full)[..., 3]
row_has = (a2 > 10).any(axis=1)
h = full.height
lo, hi = int(h * 0.35), int(h * 0.85)
best_gap, best_at = 0, None
run_start = None
for y in range(lo, hi):
    if not row_has[y]:
        if run_start is None:
            run_start = y
    else:
        if run_start is not None:
            gap = y - run_start
            if gap > best_gap:
                best_gap, best_at = gap, (run_start + y) // 2
            run_start = None
if run_start is not None:
    gap = hi - run_start
    if gap > best_gap:
        best_gap, best_at = gap, (run_start + hi) // 2

cut = best_at if best_at else int(h * 0.66)
mark = full.crop((0, 0, full.width, cut))
ma = np.asarray(mark)[..., 3]
ys, xs = np.where(ma > 6)
pad2 = 10
mx0, mx1 = max(xs.min() - pad2, 0), min(xs.max() + pad2, mark.width)
my0, my1 = max(ys.min() - pad2, 0), min(ys.max() + pad2, mark.height)
mark = mark.crop((mx0, my0, mx1, my1))
mark.save("LOGO-OCEO-mark.png")
print("OK -> LOGO-OCEO-mark.png", mark.size, " (corte em y=%d de %d)" % (cut, h))
