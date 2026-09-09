# Vídeo de apresentação — 10 e-books de Gilberto Sena

**Data:** 2026-09-09
**Formato:** 1920×1080 (16:9) · 30 fps · ~79 s
**Áudio:** locução PT-BR (voz do sistema `Luciana`) + cama musical sutil

## Entregável
- `Apresentacao 10 e-books - Gilberto Sena.mp4` — vídeo final

## Estrutura
1. **Intro** (0–6,5 s): leão dourado + "A biblioteca de Gilberto Sena" + "10 e-books. / Um assunto só: parar de decidir no escuro."
2. **10 obras** (~6,5–71,5 s): uma cena por e-book — capa em leve perspectiva 3D deslizando de fora, numeral dourado, **PILAR · <tema>**, título (Fraunces), régua, tag de diálogo com o clássico, frase-força. Locução curta por obra.
   - 01 A Startup Unicórnio — **EMPREENDER**
   - 02 De Motoboy a Executivo — **LIDERANÇA**
   - 03 Entenda Suas Finanças — **LEITURA DO NEGÓCIO**
   - 04 Estratégia da Gestão — **ESTRATÉGIA**
   - 05 No Controle das Emoções — **EMOÇÃO**
   - 06 O Segredo das Finanças — **MATEMÁTICA DO DINHEIRO**
   - 07 Os Pilares de um Homem Próspero — **CARÁTER**
   - 08 Posicione-se ou Morra — **POSICIONAMENTO**
   - 09 Quite Suas Dívidas Já — **DÍVIDA**
   - 10 Seja Rico ou Pobre — **MENTALIDADE**
3. **Fecho** (~71,5–79 s): as 10 capas em fila sobre um "10" gigante + leão + @gilbertosenaoficial + "comenta qual você quer primeiro".

## Identidade
Fundo grafite `#0F1419`, dourado `#C9A227` (kicker, numeral, régua, CTA), texto `#F4F1EA`,
Fraunces (títulos/numeral) + Inter (resto). Leão dourado top-left em toda cena de obra.
Segue `identidade/design-guide.md`.

## Regerar
```
python3 build.py            # gera locução (say), timeline.json, video.html, mux.sh
NODE_PATH="../../scripts/node_modules" node render-frames.js
bash mux.sh
```
`frames/` e `audio/*.wav` não são versionados (recriados por `build.py` + `render-frames.js`).
As capas ficam em `leitura/` (copiadas para `assets/` pelos comandos de setup no build).

## Trocar a voz da locução
Em `build.py`, `VOICE` (`say -v '?'` lista as PT-BR: Luciana, Rocko, Reed, Sandy…) e `RATE`.
