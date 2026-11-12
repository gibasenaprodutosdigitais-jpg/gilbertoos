# Logo 3D: Gilberto Sena, Business Advisor & Consultant (12/nov/2026)

Pedido dele: a logo em 3D do serviço de "business advisor and consultant", sem mais detalhe.
Tratado como **marca pessoal** (o serviço é dele, com o nome dele), não como Grupo Sena, OCEO ou GSena Hub.

**★ Escolhida por ele em 12/nov: a opção 3, a medalha de cobre.** Primeiro ele escolheu a 1 (aço escovado) e,
no mesmo dia, trocou pela 3. Arquivos da escolhida:

- `opcao-3-medalha-cobre-transparente.png`: fundo transparente, serve em fundo claro e escuro
- `opcao-3-medalha-cobre-fundo-claro.png`: com fundo claro pronto, pra documento e proposta
- `opcao-3-medalha-cobre-fundo-vinho.png`: com fundo vinho pronto

Os arquivos da opção 1, incluindo a versão pra fundo escuro feita quando ela era a escolhida, ficaram na pasta.

**12/nov, mais tarde:** pra o papel timbrado do contrato Business Advisor and Consultant, ele pediu **a logo número 1**
(aço escovado). Está em `../propostas-de-servicos/timbrado/`. Mais tarde, no mesmo dia, ele resolveu: **a oficial é a dourada (opção 3)**, que passou a ir no topo do
papel timbrado; a marca d'água continuou sendo o leão da opção 1, bem claro.

## O que tem aqui

Três opções, cada uma em dois arquivos: um com fundo transparente (pra pôr em cima de qualquer coisa) e um com
fundo pronto (pra olhar e usar direto).

| Opção | Material | Arranjo | Letra | Fundo pronto |
|---|---|---|---|---|
| 1 | Aço escovado | Leão em cima, nome embaixo | Didot no nome, Avenir Next no serviço | Branco quente |
| 2 | Mármore branco com veios | Leão à esquerda, nome à direita, em duas linhas | Futura | Quase-preto esverdeado |
| 3 | Medalha de cobre (selo) | Leão polido no centro, nome e serviço gravados em volta | Copperplate | Vinho escuro |

`comparativo-3-opcoes.png` mostra as três lado a lado.

## Como foi feito

O Higgsfield estava sem crédito (plano gratuito, saldo zero) em 12/nov, então o 3D foi montado aqui, em código, em
cima do desenho exato do leão (`identidade/logo-transparente-crop.png`). Por isso o leão sai fiel, traço por traço.
O script é o `gerar-logo-3d.py`: roda com `python3 gerar-logo-3d.py <pasta> [1|2|3]` e refaz tudo em menos de um
minuto. Trocar cor, letra ou espessura é mexer nele.

Resolução: 3600 px nas opções 1 e 3, 5200 x 2400 na 2. Dá pra imprimir em tamanho de cartão, papelaria e banner.
Pra fachada ou placa grande, o certo é mandar o leão vetorizado pra uma gráfica ou um designer modelar.

## Na peça

Só o nome e o nome do serviço. Nenhum número, nenhuma frase, nenhum fato.

## Falta

- Se for usar o nome do serviço em português também, decidir qual vai na peça.
