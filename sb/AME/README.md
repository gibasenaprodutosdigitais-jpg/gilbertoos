# Imersão AME · 14 e 15 de novembro de 2026

**AME: Administração, Marketing e Escala.** Medicina · Odontologia · Estética.
A imersão de dois dias da SB (Sena e Bittar) em São Paulo, no espaço da Rede
Vivax de Televisão. O nome é decisão do Gilberto, de 26/out/2026; até ali ela
se chamava Imersão SB. A SB continua sendo quem realiza.

| Pasta | O que tem |
|---|---|
| `logo/` | a logo em todos os formatos (ver abaixo) |
| `cronograma/` | o cronograma hora a hora, em Word e PDF. Ainda com o nome antigo, "Imersão SB". O original fica no doc https://claude.ai/artifact/5i1kFD51t9amxdeZfpmjmH |
| `kit-do-participante/` | o caderno que cada participante recebe no credenciamento (ver abaixo) |

## A logo

| Arquivo | Pra quê |
|---|---|
| `ame-logo-fundo-azul.jpg` | com o fundo azul-escuro. Pra mandar no WhatsApp |
| `ame-logo-transparente.png` | sem fundo, dourado e prata. Pra fundo escuro, foto e vídeo |
| `ame-logo-transparente-fundo-claro.png` | sem fundo, com o prata em azul-marinho. Pra fundo branco |
| `ame-simbolo.png` | só as letras AME, sem as linhas de baixo. Pra selo pequeno |
| `ame-logo-original.jpeg` | a que chegou pelo WhatsApp, com "Assessoria Médica Empresarial" |

A original veio do WhatsApp, pequena (1536 px) e comprimida. As versões foram
ampliadas a partir dela, sem ganhar detalhe. **Pra banner e palco, pedir o
arquivo original a quem desenhou.** As duas linhas de baixo foram refeitas
aqui em Montserrat, a fonte da logo.

## O kit do participante

`Imersao AME - Kit do Participante.pdf`, 8 folhas A4, uma por participante
(50). É a mesma ficha de diagnóstico da clínica (`../ficha-diagnostico/`),
adaptada pra sala: o participante preenche sozinho às 9h15 do dia 1 e leva
pra casa. Tem a capa e a identificação, os quatro pilares (21 perguntas), o
exercício da margem de três procedimentos (dia 1, 13h45), as decisões de cada
dia e os quatro números pra acompanhar a partir de segunda.

Regerar: `NODE_PATH="../../../scripts/node_modules" node render.js` dentro de
`kit-do-participante/`.
