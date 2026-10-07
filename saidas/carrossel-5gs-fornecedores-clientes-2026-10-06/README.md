# 5 G's da Gestão, 5º G: Fornecedores e Clientes

Os 9 slides de 17/jul/2026 refeitos com retrato em marca d'água, a pedido do
Gilberto em 06/out/2026.

**O conteúdo não mudou.** Parti do HTML original, em
`../carrossel-5gs-fornecedores-clientes-2026-07-17 Postado/`, e acrescentei só
a camada da foto. Texto, tipografia, cores e ordem dos slides continuam os
mesmos.

## O retrato em marca d'água

A foto é a dele à mesa com o relatório. **Duas versões**, e isso não é
capricho: o carrossel alterna fundo escuro, fundo claro e um slide dourado.
Uma versão só sumiria em metade dele.

| Arquivo | Onde entra | Força |
|---|---|---|
| `retrato-claro.png` | slides de fundo escuro e preto | 9,5% |
| `retrato-escuro.png` | slides de fundo claro e o dourado | 6,5% |

Na primeira tentativa eu usei 26% e 20%. Ficou foto com texto por cima, e
essa peça é tipografia primeiro. Baixar para menos da metade devolveu a
hierarquia: lê-se a frase, e o retrato aparece depois.

As quatro bordas são dissolvidas, pelo mesmo motivo de sempre: sem isso a
imagem lê como retângulo colado.

## Regerar

```
NODE_PATH="../../scripts/node_modules" node render.js
```

Sai em `instagram/slide-01.png` a `slide-09.png`.
