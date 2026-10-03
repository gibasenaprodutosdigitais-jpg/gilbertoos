# OCEO: vídeo de apresentação (versão Gilberto)

**Data:** 02/out/2026 · **Formato:** 1920x1080 · 30fps · 71s · sem locução e sem trilha

Segunda versão do vídeo de apresentação. A primeira (`Video de Apresentacao
do OCEO.mp4`, verde néon) usava a marca provisória do círculo com "C" e um
texto de redator publicitário. Esta usa a marca escolhida e o texto sai da
cabeça do Gilberto.

## O que mudou da versão verde pra esta

| | Versão verde | Esta |
|---|---|---|
| Marca | círculo com "C", verde néon | `LOGO-OCEO.png`, a escolhida (cromada e dourada) |
| Cor | verde néon sobre preto | papel sujo, tinta preta, laranja sinal |
| Texto | promessa de agência | a tese do Gilberto, com a analogia dele |
| Fecho | "O CEO que faltava na sua empresa" | "Simples. Mais completo.", a assinatura oficial |

O verde saiu por um motivo prático: prata e ouro brigam com verde néon. A
marca escolhida pediu outro mundo.

## Direção de arte

**Cartaz de Rua**, escolhida pelo Gilberto. Papel sujo `#E8E4DC`, tinta
`#0A0A0A`, laranja sinal `#CC4A1E`. Impact nas palavras, Helvetica Neue nas
linhas pequenas.

A assinatura da peça: a palavra é maior que a tela e a borda corta ela. O
acento aparece num lugar só, o quadrado que fecha cada palavra.

Três atos pelo fundo: escuro no problema, papel na solução, escuro na marca.
O papel entra junto com a palavra SABEDORIA, que é onde a peça vira.

O laranja passou de `#FF4D00` (o valor da direção) pra `#CC4A1E` porque o
validador de paleta apontou saturação de 100%, que dá cara de cor de sistema
em vez de cor de marca.

## Roteiro

Está em `roteiro.md`, com a origem de cada frase e de cada número.

## Disciplina de dado

Tudo que a peça afirma está registrado no repositório:

- Preço (R$ 3.500/mês, setup R$ 12.500) está no `CLAUDE.md` do OCEO.
- R$ 91.387/mês da equipe equivalente vem do business plan (salários CAGED
  mais encargos), marcado lá como fato citável.
- Escopo dos cinco pilares sai dos arquivos `pilar-1` a `pilar-5`.
- A analogia de Salomão é gancho dele, em
  `conhecimento/sabedoria-de-salomao.md` no GilbertoOS.
- Credenciais do retrato: pós-graduação em Direito Tributário e perícia
  financeira, ambas em `_memoria/quem-e-gilberto.md`.

**Ficou de fora:** "+15 anos dentro das empresas" e "+500 empresas
orientadas", que apareciam na versão verde. Nenhum dos dois está registrado.
Se o Gilberto confirmar, entram e a peça é regerada.

## Trilha

Não tem. A versão verde usa uma faixa com vocal em inglês que briga com
texto em português na tela, e cuja licença ninguém conferiu. Pra uso externo,
entrar com faixa licenciada.

## Re-renderizar

```
OUT=/tmp/oceo-frames TOTAL_MS=71000 NODE_PATH="../../../scripts/node_modules" node render-frames.js
ffmpeg -y -framerate 30 -start_number 1 -i /tmp/oceo-frames/f-%04d.png \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart oceo-apresentacao.mp4
```

`_olhar.js` tira foto só dos instantes que você pedir (`T=12,23,51 node
_olhar.js`), pra conferir uma mudança sem renderizar os 2130 quadros.

Os quadros não são versionados.
