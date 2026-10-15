# Cards — POP e padronização

8 cards, 1080x1350 (o formato que o Instagram mais entrega). Funcionam soltos,
um por dia, ou em sequência como carrossel.

**Direção de arte: Blueprint.** O assunto é a planta de como o trabalho é
feito, então a peça fala a língua de quem projeta antes de construir: papel
azul, grade técnica, linha de cota com seta, carimbo de projeto no rodapé e
prancha numerada.

O azul aqui vem do assunto, não do hábito. A skill de direção de arte avisa
que o Gilberto está saturado de azul, e o aviso é justo. Neste caso a planta
É o conceito da peça, e trocar a cor desmontaria a ideia.

| | |
|---|---|
| Fundo | `#10314F` |
| Tinta | `#DCE8F2` — 10,71:1 |
| Cota | `#E09B55` — 5,71:1 |
| Títulos e corpo | Gill Sans |
| Etiquetas e números | Menlo |

O laranja original da direção (`#F2A65A`) tinha 85% de saturação, que dá cara
de cor de sistema. Baixei para 69%, dentro da faixa que o validador pede.

## O retrato em marca d'água

`retrato-dagua.png` é a foto dele tratada como desenho de planta: cinza
convertido em azul da tinta, fundo recortado pela própria luz e as quatro
bordas dissolvidas. Entra à direita de cada prancha, atrás do conteúdo.

As bordas dissolvidas são o que separa marca d'água de foto colada. Sem elas
a imagem lê como um retângulo por cima do desenho técnico, e a direção
desmonta.

## O texto

Sai dos roteiros em `../roteiro.md`, condensado. Os dois arquivos contam a
mesma coisa de propósito: se ele gravar o reels e postar o card, a mensagem
bate.

**Nenhum número de cláusula da ISO 9001 entrou**, pelo mesmo motivo dos
roteiros: os cards de origem citam vários e não existe nada fichado aqui que
confirme.

## Regerar

```
NODE_PATH="../../../scripts/node_modules" node render.js
```

Sai em `instagram/card-01.png` a `card-08.png`.
