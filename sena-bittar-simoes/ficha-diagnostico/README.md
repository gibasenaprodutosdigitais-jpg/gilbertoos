# Ficha de diagnóstico do consultório

Aplicada no primeiro encontro da mentoria, antes de qualquer plano. Sai da
seção 4 do `plano-de-mentoria.md`.

**Entregável:** `Sena, Bittar e Simões - Ficha de Diagnostico.pdf`, 7 páginas A4.
Capa, identificação, uma página por pilar e a folha de fecho com a linha de
partida.

## Estrutura

| Página | O que tem |
|---|---|
| 1 | Faixa de abertura, aviso de sigilo, identificação e perfil do profissional |
| 2 a 5 | As 21 perguntas, divididas pelos quatro pilares |
| 6 | Linha de partida dos quatro indicadores, documentos a entregar, as três decisões do trimestre e assinaturas |

A pergunta 21 só vale para quem faz estética. Ela existe porque a
classificação do procedimento decide a conta de imposto do consultório, e é
a única zona cinzenta entre os quatro públicos. Ver a seção 8 do plano.

## A marca

Os arquivos da marca vivem em `../marca/` desde a troca de nome em
06/out/2026. A ficha usa dois deles:

- **`../marca/sbs-logo.png`** — o monograma SBS recortado do render 3D,
  centralizado acima do título da faixa de abertura.
- **`../marca/sbs-marca-dagua.png`** — o mesmo monograma em silhueta
  azulada, com a opacidade de 9,5% gravada no arquivo, a 580px no meio de
  cada folha.

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

Grafite `#1C1C1E` nas faixas, ouro `#C9A24B` no acento, tinta `#F2F0EC` sobre
o escuro. Escolha do Gilberto em 06/out/2026, de seis opções. Medido: ouro
sobre grafite dá 7,09:1, e o ouro escuro dos rótulos sobre o branco dá
4,20:1, que serve para a caixa alta em negrito que eles usam.

A linha da marca diz "consultoria e assessoria para médicos". A ficha atende
quatro públicos, então dentista e biomédico recebem um documento que fala em
médicos. Está na lista de decisões da seção 9 do plano.

## Regerar

```
NODE_PATH="../../scripts/node_modules" node render.js
```

`conferir.js` tira uma foto do HTML inteiro em `/tmp/sbficha/tudo.png`, pra
olhar o resultado antes de imprimir.
