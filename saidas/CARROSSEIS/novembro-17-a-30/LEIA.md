# Carrosséis das 18h, 17 a 30/nov/2026

Pedido dele em 12/nov: fechar o mês com um carrossel por dia, **no tema do reel das 12h do mesmo dia**, saindo como
**direcionamento** sobre a fala do reel (o reel conta, o carrossel orienta o que fazer). Texto aprovado e conferido em
`textos.md` (v3; o topo lista o que a conferência mudou).

- **Visual:** direção 3, escolhida por ele: Suíço Internacional, uma cor sólida por tema, Helvetica Neue + Menlo, tudo
  alinhado à esquerda, número da lâmina no canto, lâmina "O QUE FAZER" com etiqueta. Leão só na última lâmina.
  Paletas medidas no `paleta.py` da direção de arte (dias 20 e 25 sem dourado, pra não cair no azul e dourado).
- **Marca d'água** (pedido dele em 12/nov): a medalha da Business Advisor Consult em cinza, grande e bem clara no
  centro de toda lâmina (`marca-dagua-advisor.png`, tirada de
  `saidas/NEGOCIOS-E-MARCA/logo-3d-business-advisor-2026-11-12/opcao-3-medalha-cobre-transparente.png`). Em fundo claro
  entra a 16% escurecendo; em fundo escuro, a 13% clareando.
- **Como refazer:** editar `textos.md` e rodar `python3 gerar.py`, depois
  `NODE_PATH=../../../scripts/node_modules node render.js <pastas>`. Cada pasta tem `carrossel.html`, `legenda.md` e
  `instagram/slide-NN.png`.
- **Situação:** 14 prontos (96 lâminas), aprovados e **agendados na Zernio em 12/nov**, todo dia às 18h (21:00Z) de 17 a 30/11, só no Instagram. Em 13/nov as imagens dos 14 posts foram trocadas pelas versões com marca d'água (legenda e
  horário mantidos).
