# Fichas de diagnóstico do SBS

São três, uma por faixa de cliente da cesta de produtos
(`../cesta-de-produtos.md`). Todas são aplicadas no primeiro encontro, antes
de qualquer plano, e saem da seção 4 do `../plano-de-mentoria.md`.

| Faixa | Arquivo | PDF | Páginas |
|---|---|---|---|
| **A** Clínica | `ficha-diagnostico.html` | `... - Ficha de Diagnostico.pdf` | 6 |
| **B** Hospital dia | `ficha-hospital-dia.html` | `... - Ficha de Diagnostico - Hospital Dia.pdf` | 10 |
| **C** Rede e grandes hospitais | `ficha-rede.html` | `... - Ficha de Diagnostico - Rede e Grandes Hospitais.pdf` | 10 |

As três dividem o mesmo `ficha.css`. Mexer nele mexe nas três.

## O que cada uma tem de diferente

**Faixa A, clínica.** 21 perguntas nos quatro pilares. A 21 só vale para quem
faz estética: a classificação do procedimento decide a conta de imposto, e é
a única zona cinzenta entre os quatro públicos.

**Faixa B, hospital dia.** 32 perguntas. Antes dos quatro pilares entram três
blocos que não existem num consultório: **sala e escala**, **convênio e
glosa** e **corpo clínico**. A linha de partida mede seis indicadores em vez
de quatro, com ocupação de sala e glosa somadas aos do método. A pergunta 32
cobra a descrição do serviço na nota: a redução de 60% de IBS e CBS alcança
serviço hospitalar e ambulatorial pelos arts. 128 a 134 da LC 214/2025, mas
depende da classificação correta na NBS. Fichado em
`../../conhecimento/reforma-tributaria-saude-geral.md`.

**Faixa C, rede e grandes hospitais.** 25 perguntas em oito blocos, e a
natureza muda: não se preenche com o dono sozinho, e parte vem de documento,
não de memória. Tem mapa de unidades para preencher linha a linha, dívida
separada por categoria de urgência, uma lista de **sinais de alerta** que os
mentores marcam durante a conversa sem perguntar em voz alta, e duas
**condições de entrada** com caixa de assinatura.

Os sinais de alerta e as condições de entrada vieram de caso real, fichado em
`../../conhecimento/turnaround-rede-multiunidades-diagnostico-gargalos.md`:
centro de custo separado por unidade, acesso à informação na fonte por
procuração digital e mandato formal de não ingerência. Três ou mais sinais
marcados mudam o trabalho de mentoria para entrada de turnaround.

## A marca

Os arquivos vivem em `../marca/` desde a troca de nome em 06/out/2026. As
fichas usam dois:

- **`../marca/sbs-logo.png`** — o monograma SBS recortado do render 3D,
  centralizado acima do título da faixa de abertura.
- **`../marca/sbs-marca-dagua.png`** — o mesmo monograma em silhueta
  azulada, com a opacidade gravada no arquivo, a 580px no meio de cada folha.

O SBS é largo (2,2:1). Como marca d'água numa folha retrato ele precisa de
mais largura e um pouco mais de corpo que o monograma quadrado que havia
antes, senão vira borrão em vez de marca.

**Não use `opacity` no CSS junto com `z-index` negativo:** isso vira grupo de
transparência no PDF e nem todo leitor compõe igual. A opacidade vai assada
no arquivo de imagem.

Nesta pasta ainda estão `monograma-sb.png`, `marca-dagua.png` e
`logo-sena-e-bittar.jpg`, da época em que a casa era Sena e Bittar. Nenhum é
usado; ficam como histórico.

## Cor

Azul-noite `#0C1A2E` nas faixas, ouro `#C9A24B` no acento, tinta `#F2EFE8`
sobre o escuro. O azul entrou em 06/out/2026, a pedido dele, conforme a
amostra que ele mandou.

## Quebra de página

Cada bloco começa numa folha nova (`.pilar{page-break-before:always}`), o que
dá espaço para escrever à mão. A exceção é a classe `.junto`, usada no bloco
de condições de entrada da faixa C: ele precisa ficar na mesma folha dos
sinais de alerta, porque a frase que fecha os alertas aponta para "as
condições abaixo".

## Regerar

```
NODE_PATH="../../scripts/node_modules" node render.js
```

Gera os três PDFs de uma vez. `conferir.js` tira uma foto do HTML inteiro em
`/tmp/sbficha/tudo.png`, pra olhar antes de imprimir.
