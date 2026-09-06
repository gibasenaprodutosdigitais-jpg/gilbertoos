# Reels — 10 e-books do Gilberto (pasta leitura)

**Data:** 2026-09-06
**Formato:** 1080x1920 (9:16) · 30fps · 31s

## Entregáveis
- `reels-10-ebooks.mp4` — com base sonora sintetizada (guia; trocar por som do Instagram)
- `reels-10-ebooks-mudo.mp4` — sem áudio
- `legenda.md` — legenda + hashtags

## Estrutura da animação
1. Intro (0–3,6s): selo do leão + título "10 e-books. Um assunto só: parar de decidir no escuro."
2. 10 capas (3,6–23,6s): cada capa entra girando em 3D, com numeral, título e uma linha-lição; sai encaixando de lado.
3. Mosaico (23,6–27s): as 10 capas montam a grade sobre um "10" gigante.
4. CTA (27–31s): selo + @gilbertosenaoficial + "comenta qual você quer primeiro".

## Como re-renderizar
As capas ficam em `../../leitura/`. Recriar a pasta local de assets:

```
mkdir -p assets
cp ../../leitura/*.png assets/
cp ../carrossel-10-ebooks-leitura-2026-09-06/assets/grupo-sena-icone-gold.png assets/
cp "../../identidade/@eubernardocoelho-Gilberto-Sena-104.jpg" assets/gilberto.jpg
```

Depois:

```
OUT=/tmp/reels-frames NODE_PATH="../../scripts/node_modules" node render-frames.js
ffmpeg -y -framerate 30 -start_number 1 -i /tmp/reels-frames/f-%04d.png -i bed.wav \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart -c:a aac -b:a 160k -shortest reels-10-ebooks.mp4
```

`assets/` não é versionado (as capas originais já estão em `leitura/`).
`bed.wav` também não — é gerado; comando no histórico da sessão.
