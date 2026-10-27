# Imersão AME · 14 e 15 de novembro de 2026

**AME: Administração, Marketing e Escala.** Medicina · Odontologia · Estética.
A imersão de dois dias da SB (Sena e Bittar) em São Paulo, no espaço da Rede
Vivax de Televisão. O nome é decisão do Gilberto, de 26/out/2026; até ali ela
se chamava Imersão SB. A SB continua sendo quem realiza.

**Preço:** de R$ 3.999 por R$ 499, os dois dias, 50 vagas (decidido em 26/out; o jurídico liberou o "de").

| Pasta | O que tem |
|---|---|
| `logo/` | a logo em todos os formatos (ver abaixo) |
| `cronograma/` | o cronograma hora a hora, em Word e PDF. Os arquivos daqui são de 21/out, com o nome e o preço antigos. O que vale é o doc, já com o nome AME e o preço novo: no doc https://claude.ai/artifact/5i1kFD51t9amxdeZfpmjmH |
| `kit-do-participante/` | o caderno que cada participante recebe no credenciamento (ver abaixo) |
| `programacao/` | a programação dos dois dias pro participante, 2 folhas A4. É o cronograma sem a parte interna (oferta, conta da sala, pendências) |
| `cracha/` | crachás de 10 x 14 cm, 4 por folha A4: os dois que conduzem, equipe, e participante com o nome em branco |
| `certificado/` | certificado de participação, A4 deitado, com o nome em branco e carga horária de 20 horas |
| `divulgacao/` | a arte de divulgação: `imersao-ame-feed.png` (Instagram, 1080 x 1350) e `imersao-ame-story.png` (story e status, 1080 x 1920) |
| `ficha-online/` | a ficha de diagnóstico pelo celular, com a logo da AME e a pergunta do hot seat. Link e regras no README de lá |
| `fontes/` | a Montserrat, a fonte da logo, usada em todas as peças |

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

## Regerar programação, crachás, certificado e artes

`NODE_PATH="../../scripts/node_modules" node render.js` dentro desta pasta.
