# Provérbios e frase do dia no YouTube (13 a 30/nov/2026)

Pedido dele em 12/nov: programar no YouTube, a partir de 13/11, os mesmos posts do Provérbios e da frase do dia que saem
no Instagram. O YouTube não aceita post de imagem, então cada imagem virou um **Short de 9 s** (a imagem inteira no
centro, aproximação lenta, fundo com a própria imagem desfocada, sem música) — `montar.py`, dados em `dados.py`.

- **36 Shorts agendados na Zernio em 12/nov**, no mesmo horário do Instagram: **5h Provérbios** e **9h frase do dia**,
  de 13 a 30/11. Títulos e descrições em `agenda-youtube.json`.
- Título do Provérbios: a frase curta do segundo parágrafo da legenda (a frase da imagem passa de 100 caracteres).
  Descrição: a frase inteira + "Reflexão autoral inspirada em Provérbios N".
- Vídeos em `videos/` (fora do GitHub). As imagens foram baixadas das URLs publicadas na Zernio.
- Dezembro: falta a foto do Provérbios e as frases; quando vierem, rodar `montar.py` com os dados novos.
