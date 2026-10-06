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

Dois arquivos, os dois tirados da foto da fachada que o Gilberto mandou em
06/out/2026:

- **`monograma-sb.png`** é a marca em si, recortada do arquivo que o Gilberto
  mandou em 06/out/2026. O original vinha em fundo branco chapado, e o
  prateado da letra também é claro, então cortar por limiar comeria o metal.
  Recortar por limiar comeria o metal, e preencher só a partir das bordas
  deixava o branco preso dentro dos vazados das letras. O que funcionou foi
  marcar o branco neutro e chapado (mínimo acima de 238, variação entre
  canais abaixo de 7) e apagar só as manchas ligadas maiores que 900 pixels.
  Assim some o fundo de fora e o de dentro dos vazados, e o brilho pontual do
  prateado fica. Entra à esquerda da faixa de abertura, nos dois documentos.
- **`marca-dagua.png`** é o mesmo monograma virado em silhueta grafite, com a
  opacidade de 8,5% **assada no arquivo**. Não use `opacity` no CSS junto com
  `z-index` negativo: isso vira grupo de transparência no PDF e nem todo
  leitor compõe igual.
- **`logo-sena-bittar-simoes.jpg`** foi a capa até 06/out/2026, tirada da foto da
  fachada. O Gilberto pediu pra tirar. Fica no arquivo caso volte a servir.

O recorte usa a própria luz da foto como máscara. O metal é claro, o mármore
é escuro, então um corte duro de luminância separa os dois sem deixar resto
de fundo.

**Se aparecer o arquivo original** (vetor, ou PNG com fundo transparente),
trocar. A capa fica mais limpa e a marca pode ir menor sem perder nitidez.

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
