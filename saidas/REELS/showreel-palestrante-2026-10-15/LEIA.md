# Showreel de palestrante — 15/out/2026

`Gilberto-Sena-Showreel.mp4` · 58 segundos · 1080x1920 · áudio em −14 LUFS

Feito pra mandar por WhatsApp ou Direct pra quem contrata palestra. Vertical
porque é assim que o contratante abre no celular.

## O que tem dentro

| Quando | O quê |
|---|---|
| 0–3s | abertura: logo, nome, "palestrante" |
| 3–11s | palco do Empreenda Summit Alphaville, 2024 |
| 11–14s | plateia do mesmo evento |
| 14–22s | volta ao palco |
| 22–25s | cartaz do Dubai Experience 2023 |
| 25–28s | cartaz do PBXP 2023 |
| 28–31s | foto do Summit Êxito 2022 |
| 31–46s | palco |
| 46–49s | sala da Imersão Reengenharia 2026 |
| 49–53s | palco |
| 53–58s | fecho: cargo, números e contato |

A fala é contínua do começo ao fim: a história dele de motoboy, a moto
alugada, o pai da namorada que tirou o financiamento, até as três motos e a
ficha de que aquilo já era empreender. **Os cartazes entram por cima da
imagem enquanto a voz continua**, então não tem buraco de áudio nem corte
no meio de frase.

## Por que é de 58 segundos e não de 3 minutos

Porque é o que existe de palco. O acervo inteiro tem **~3 minutos**: dois
minutos do Alphaville em três clipes e um minuto da Imersão. O resto das
gravações longas é ele no carro, que não serve pra showreel.

⚠ **Três dos quatro clipes de palco vêm com legenda queimada de outro
editor** (estilo karaokê, palavra colorida). Só o clipe da história do
motoboy tem a legenda **fora** da imagem, na tarja preta, e por isso é o
único que dá pra usar com a imagem limpa: eu recorto a faixa de 1080x558 do
palco e descarto a tarja.

## Pra melhorar isso de verdade

Precisa de **imagem bruta de palco, sem legenda**, de qualquer evento. Com
3 ou 4 minutos de material limpo dá pra fazer uma peça de 90 segundos com
variação de plano e corte no ritmo da fala.

## Como refazer

As peças gráficas saem de `_pecas.py` (PIL). A montagem é um filtergraph do
ffmpeg com `overlay ... enable='between(t,a,b)'` sobre a base do palco, e as
pontas entram por concat sem reencode. Está tudo descrito no
`_memoria/onde-paramos.md`.
