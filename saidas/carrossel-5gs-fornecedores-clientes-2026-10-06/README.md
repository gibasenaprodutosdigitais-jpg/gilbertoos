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

## O retrato em marca d'água

**A foto é o retrato de estúdio**, mãos entrelaçadas, fundo quase preto. Ela
sobe do canto inferior direito em todos os nove slides.

| Arquivo | Onde entra | Força |
|---|---|---|
| `retrato-claro.png` | slides de fundo escuro e preto | 17% |
| `retrato-escuro.png` | slides de fundo claro e o dourado | 14% |

### Por que as duas primeiras tentativas falharam

Comecei com a foto dele à mesa com o relatório, e o resultado foi ruim duas
vezes seguidas. O problema nunca foi a opacidade, era a imagem.

Aquela foto é uma **cena**: escritório, estante, mesa, monitor, e uma janela
de cidade bem clara atrás dele. Como marca d'água, tudo isso vira borrão, e
não se reconhece nada. Pior: a janela era a parte mais clara do quadro, então
era ela que virava o desenho, não ele. E no slide 03 o parágrafo caía em cima
do rosto e cortava a cara ao meio.

**O que resolveu foi trocar a origem, não ajustar número.** Retrato de
estúdio tem fundo quase preto, então o recorte por luz devolve só a silhueta
dele, limpa. E ancorar no rodapé põe o rosto numa área onde não há texto,
porque nesses slides o conteúdo é centralizado na vertical.

A lição, para a próxima: marca d'água precisa de silhueta, não de cenário.

## Regerar

```
NODE_PATH="../../scripts/node_modules" node render.js
```

Sai em `instagram/slide-01.png` a `slide-09.png`.
