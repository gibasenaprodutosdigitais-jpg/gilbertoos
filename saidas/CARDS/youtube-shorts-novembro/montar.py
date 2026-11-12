"""Transforma as imagens do Provérbios e da frase do dia em Shorts verticais (YouTube não aceita post de imagem).

9 s, 1080x1920: a imagem inteira no centro, com uma aproximação lenta; atrás, a mesma imagem desfocada e escurecida
preenchendo a tela. Sem música (áudio mudo). Arquivo sem metadado de origem. Saída em videos/ (fora do GitHub).
"""
import os, subprocess, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dados import PROV, FRASE

AQUI = os.path.dirname(os.path.abspath(__file__))
IMG, OUT = AQUI + "/imagens", AQUI + "/videos"
os.makedirs(IMG, exist_ok=True); os.makedirs(OUT, exist_ok=True)
DUR = 9


def um(url, nome):
    img = f"{IMG}/{nome}{os.path.splitext(url)[1]}"
    if not os.path.exists(img):
        urllib.request.urlretrieve(url, img)
    out = f"{OUT}/{nome}.mp4"
    fr = DUR * 30
    fc = ("[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.18[bg];"
          f"[0:v]scale=2000:-2,zoompan=z='1+0.05*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1000x1250:fps=30,"
          "fade=t=in:st=0:d=0.5[fg];"
          f"[bg][fg]overlay=(W-w)/2:(H-h)/2,fade=t=out:st={DUR-0.4}:d=0.4,format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", str(DUR), "-i", img,
                    "-f", "lavfi", "-t", str(DUR), "-i", "anullsrc=r=44100:cl=stereo",
                    "-filter_complex", fc, "-map", "[v]", "-map", "1:a", "-map_metadata", "-1",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-r", "30", "-c:a", "aac", "-b:a", "96k",
                    "-movflags", "+faststart", "-t", str(DUR), out], check=True)
    return out


for dia, url, *_ in PROV:
    print(um(url, f"prov-{dia}"))
for dia, url, _ in FRASE:
    print(um(url, f"frase-{dia}"))
