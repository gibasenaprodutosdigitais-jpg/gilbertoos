# 5 G's da Gestão, 5º G: Fornecedores e Clientes

Os 9 slides de 17/jul/2026 refeitos com retrato em marca d'água, a pedido do
Gilberto em 06/out/2026.

Parti do HTML original, em
`../carrossel-5gs-fornecedores-clientes-2026-07-17 Postado/`. Tipografia,
cores e ordem dos slides continuam os mesmos. Mudaram duas coisas: entrou a
camada da foto e saíram os travessões.

## Os travessões

O texto de julho usava travessão como pausa de efeito em cinco lugares, que é
o tique que o `motor/texto.py` marca e que denuncia texto gerado. Ficaram
assim:

| Antes | Agora |
|---|---|
| não nascem do nada — se cultivam | não nascem do nada. Elas se cultivam |
| têm ciclo — identificação, integração | têm ciclo: identificação, integração |
| não se evita — se mapeia, se responde | não se evita. Mapeia, responde |
| A conta é simples — poucos fazem | A conta é simples. Poucos fazem |
| Não é sorte — é o exemplo | Não foi sorte. É o exemplo |

Nos títulos o travessão virou ponto médio, que separa sem fingir pausa:
*Pilar 1 · Governança de Relacionamentos* e *Riscos · Método TRI*.

O travessão antes de "Gilberto Sena", na citação do slide 06, fica: ali ele
marca autoria, que é o uso certo.

## A cor saiu da foto

A versão de julho era preto, creme e dourado. Aqui a paleta é tirada da
própria fotografia que entra em marca d'água:

| | | De onde veio |
|---|---|---|
| Fundo escuro | `#241C19` | o marrom profundo do terno e da sala |
| Fundo preto | `#1A1411` | o mesmo, mais fechado |
| Papel | `#EDE7E0` | o claro quente do ambiente |
| Acento | `#A87339` | o bronze da madeira da mesa |
| Bloco cheio (slide 07) | `#B98A48` | o mesmo bronze, mais claro |

**Por que isso resolveu.** As duas primeiras tentativas falharam porque a
foto brigava com a peça: imagem quente de escritório por trás de um design
preto, creme e dourado. Baixar a opacidade só tornava a briga mais fraca,
nunca a resolvia.

Com a paleta vinda da foto, ela deixa de ser corpo estranho e passa a ler
como textura do próprio material. É a mesma família de cor, então não há o
que brigar.

Contraste medido: tinta clara sobre o marrom dá 13,63:1; o bronze dá 4,12:1
sobre o escuro e 3,30:1 sobre o papel, que é o que permite usá-lo nos dois,
já que o carrossel alterna fundo claro e escuro.

## O retrato em marca d'água

A foto dele à mesa com o relatório, em duotone, subindo do canto inferior
direito. Clara a 15% sobre os fundos escuros, escura a 12% sobre o papel e o
bronze. As quatro bordas dissolvidas.

## Regerar

```
NODE_PATH="../../scripts/node_modules" node render.js
```

Sai em `instagram/slide-01.png` a `slide-09.png`.
