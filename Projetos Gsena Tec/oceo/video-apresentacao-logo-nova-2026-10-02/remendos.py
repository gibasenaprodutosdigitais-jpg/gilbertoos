"""
Remendos pra trocar a marca antiga (circulo com "C", verde neon) pela
escolhida, sem tocar em mais nada do video.

Cada remendo tem duas camadas:
  1. uma mancha escura esfumada que apaga a marca velha. O fundo ali e quase
     preto e quase liso, entao a borda esfumada some.
  2. a marca nova por cima, com um brilho verde proprio, pra nao quebrar a
     linguagem do video.
"""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, os

L, A = 1920, 1080
ID = "/Users/gilbertosena/Desktop/GilbertoOS/Projetos Gsena Tec/oceo/identidade-visual"
CHEIA = Image.open(f"{ID}/LOGO-OCEO.png").convert("RGBA")
MARCA = Image.open(f"{ID}/LOGO-OCEO-mark.png").convert("RGBA")
FUNDO = (9, 13, 11)          # o quase-preto esverdeado do video
BRILHO = (46, 229, 106)      # o verde do video, so pro halo

def por_altura(img, h):
    return img.resize((round(img.width * h / img.height), h), Image.LANCZOS)

def halo(tam, raio, forca=.30):
    """disco de brilho verde, bem suave — e o que o video faz atras da marca"""
    g = Image.new("RGBA", tam, (0, 0, 0, 0))
    d = ImageDraw.Draw(g)
    cx, cy = tam[0] // 2, tam[1] // 2
    d.ellipse([cx - raio, cy - raio, cx + raio, cy + raio],
              fill=BRILHO + (int(255 * forca),))
    return g.filter(ImageFilter.GaussianBlur(raio * .55))

def apagar(camada, forma, pena):
    """
    Mancha de fundo. O miolo e SOLIDO e a pena cresce so pra fora.
    Borrar a mascara inteira deixava a marca velha aparecendo de leve nas
    bordas, que foi o fantasma do primeiro teste.
    """
    def desenhar(folga):
        m = Image.new("L", (L, A), 0)
        d = ImageDraw.Draw(m)
        if forma[0] == "circulo":
            _, cx, cy, r = forma
            r += folga
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
        else:
            _, x0, y0, x1, y1 = forma
            d.rounded_rectangle([x0 - folga, y0 - folga, x1 + folga, y1 + folga],
                                radius=60, fill=255)
        return m
    solido = desenhar(0)
    fora = desenhar(pena).filter(ImageFilter.GaussianBlur(pena * 0.75))
    m = Image.fromarray(np.maximum(np.array(solido), np.array(fora)))
    cor = Image.new("RGBA", (L, A), FUNDO + (255,))
    camada.paste(cor, (0, 0), m)

def remendo(nome, forma, pena, img, altura, centro, raio_halo):
    c = Image.new("RGBA", (L, A), (0, 0, 0, 0))
    apagar(c, forma, pena)
    h = halo((L, A), raio_halo)
    # o halo tem que ficar centrado onde a marca vai
    h = h.transform((L, A), Image.AFFINE,
                    (1, 0, L // 2 - centro[0], 0, 1, A // 2 - centro[1]))
    c = Image.alpha_composite(c, h)
    lg = por_altura(img, altura)
    c.alpha_composite(lg, (centro[0] - lg.width // 2, centro[1] - lg.height // 2))
    c.save(nome)
    print(f"  {nome}  logo {lg.width}x{lg.height} em {centro}")

os.makedirs("rem", exist_ok=True)
# 1) a mira da abertura: so o simbolo, dentro da propria mira
remendo("rem/p1.png", ("circulo", 960, 540, 198), 58, MARCA, 330, (960, 540), 300)
# 2) o lockup da abertura (marca + palavra OCEO)
remendo("rem/p2.png", ("caixa", 404, 420, 1536, 634), 64, CHEIA, 268, (960, 498), 340)
# 3) o simbolo solto do "Tudo em um lugar so"
remendo("rem/p3.png", ("circulo", 1520, 540, 190), 30, MARCA, 236, (1512, 540), 245)
# 4) o fechamento
remendo("rem/p4.png", ("caixa", 404, 364, 1536, 642), 64, CHEIA, 268, (960, 496), 340)

# 4a) o comeco do fechamento: a marca velha entra grande e desce ate o lugar
#     dela. A mancha precisa ser mais alta pra pegar ela grande; a assinatura
#     ainda nao entrou na tela nesse trecho, entao da pra avancar pra baixo.
remendo("rem/p4a.png", ("caixa", 404, 330, 1536, 745), 60, CHEIA, 268, (960, 496), 340)

# 2a) enquanto a palavra OCEO antiga esta sendo digitada, o cursor branco
#     desce abaixo da linha e escapava da mancha. Nesse trecho o
#     PRE-LANCAMENTO ainda nao entrou, entao da pra descer a mancha.
remendo("rem/p2a.png", ("caixa", 404, 416, 1536, 762), 56, CHEIA, 268, (960, 498), 340)
