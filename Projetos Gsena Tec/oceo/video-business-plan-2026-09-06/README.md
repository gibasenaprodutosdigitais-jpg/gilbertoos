# OCEO — Vídeo do Business Plan (resumido)

**Data:** 06/set/2026
**Formato:** 1920x1080 (16:9) · 30fps · 43s · sem locução

## Entregáveis
- `oceo-business-plan.mp4` — com base sonora sintetizada (trilha só de guia; trocar por música licenciada antes de uso externo)
- `oceo-business-plan-mudo.mp4` — sem áudio
- `video.html` + `render-frames.js` — fonte (animação em HTML/CSS, renderizada frame a frame com Playwright)
- `bed.wav` — trilha guia (não versionada)

## Roteiro (7 cenas)
1. **Abertura** (0–4s) — marca OCEO + "O sistema orienta. Você decide."
2. **O problema** (4–10s) — a PME administra no escuro; contabilidade caixa-preta, jurídico só reativo, marketing sem controle, caixa parado. Dado: 24 mi de PMEs, 95% das empresas (SEBRAE, 2025).
3. **A solução** (10–15s) — um sistema, cinco frentes, uma mensalidade; "processa de verdade" dentro de casa. Princípio: o sistema orienta, não decide.
4. **Os 5 pilares** (15–28s) — GC, GF, GJ, GM, GI, cada um com escopo curto e o custo de equipe que substitui (R$ 30.834 / 8.790 / 16.122 / 26.037 / 9.604 → R$ 3.500).
5. **Comparativo central** (28–34,5s) — equipe interna equivalente R$ 91.387/mês x OCEO R$ 3.500/mês; economia R$ 87.887/mês, 96,2%, payback ~4 dias, R$ 1,05 mi em 12 meses. Setup R$ 12.500 à parte.
6. **Mercado e modelo** (34,5–39,5s) — ERP global US$ 71–92 bi (~10% a.a.), Totvs/SAP/Oracle 77% do nacional, alvo PME R$ 50 mil+/mês. Modelo: setup R$ 12.500 + R$ 3.500/mês. Badge de premissa (CAC/churn/PE a validar).
7. **Fecho** (39,5–43s) — marca + "Administrar com o número na mão" + www.oceo.com.br + Grupo Sena · Gilberto Sena, CEO.

## Disciplina de dado (mantida na peça)
- **Fato citável:** preço OCEO, escopo dos pilares, salários (CAGED via salario.com.br, encargos ~80%), dados de mercado (SEBRAE, ERP global, share Totvs/SAP/Oracle).
- **Premissa (marcada na tela, cena 6):** CAC, churn e ponto de equilíbrio do plano são estimativas — a validar com operação real antes de investidor.

## Pendências / ajustes possíveis
- **Marca provisória:** o vídeo usa um wordmark tipográfico "OCEO" + marca geométrica (círculo + arco) na paleta do deck (âmbar `#e8a33d` sobre `#0a0d12`). Quando a marca do OCEO for fechada (registro em andamento), regerar com o logo definitivo.
- Trilha: sintetizada. Substituir por faixa licenciada se o vídeo for pra investidor/externo.

## Re-renderizar
```
OUT=/tmp/oceo-frames NODE_PATH="../../../scripts/node_modules" node render-frames.js
ffmpeg -y -framerate 30 -start_number 1 -i /tmp/oceo-frames/f-%04d.png -i bed.wav \
  -c:v libx264 -pix_fmt yuv420p -crf 19 -movflags +faststart -c:a aac -b:a 160k -shortest oceo-business-plan.mp4
```
`frames/` e `bed.wav` não são versionados (regeneráveis).
