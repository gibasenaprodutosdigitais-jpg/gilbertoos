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

A foto é a dele à mesa com o relatório. **Duas versões**, e isso não é
capricho: o carrossel alterna fundo escuro, fundo claro e um slide dourado.
Uma versão só sumiria em metade dele.

| Arquivo | Onde entra | Força |
|---|---|---|
| `retrato-claro.png` | slides de fundo escuro e preto | 13% |
| `retrato-escuro.png` | slides de fundo claro e o dourado | 10% |

**O que estava errado nas primeiras versões.** A foto tem uma janela de
cidade atrás dele, bem clara. Como eu recortava a marca pela luz, era a
janela que virava o desenho, não ele. O carrossel ficava com uma mancha
luminosa no canto que não queria dizer nada.

A correção foi cortar fechado no busto e na mão com o relatório, e trocar o
recorte por luz por um duotone da foto inteira. Agora o que aparece é ele
segurando o relatório, que é imagem com sentido num carrossel sobre
fornecedor e cliente.

As quatro bordas são dissolvidas, pelo mesmo motivo de sempre: sem isso a
imagem lê como retângulo colado.

## Regerar

```
NODE_PATH="../../scripts/node_modules" node render.js
```

Sai em `instagram/slide-01.png` a `slide-09.png`.
