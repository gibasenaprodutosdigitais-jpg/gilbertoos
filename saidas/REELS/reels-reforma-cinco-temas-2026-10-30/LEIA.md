# 5 Reels da reforma (30/out/2026)

## De onde veio

Em 30/out o Gilberto recebeu por WhatsApp 5 vídeos animados do perfil **@reforma_simplific** (TikTok) e pediu pra
recriar com o rosto dele e sem a marca d'água. **Isso não foi feito**: tirar a marca e postar como dele seria pegar o
trabalho de outro criador. Ele escolheu o caminho 1: **só os temas foram aproveitados**. Texto, ganchos e viradas são
novos, na voz dele. **Os vídeos originais não devem ser postados.**

## Números conferidos (30/out)

| Número | Fonte |
|---|---|
| CBS 2027 de 11,3% (TCU, 28/out; conta exata 11,3468%) | [CNN Brasil](https://www.cnnbrasil.com.br/economia/money/macroeconomia/reforma-tributaria-tcu-propoe-aliquota-de-113-para-cbs-em-2027/), [Poder360](https://www.poder360.com.br/poder-economia/tcu-fixa-aliquota-da-cbs-em-113-para-2027/), [Contábeis](https://www.contabeis.com.br/artigos/80433/cbs-2027-tcu-propoe-aliquota-de-11-3/) |
| Senado até 15/12; sem votação, vale o do TCU | mesmas fontes |
| Governo estimava 9,21% | [InvestNews](https://investnews.com.br/economia/aliquota-cbs-tcu-2027/amp/) |
| 18 profissões com 30% (art. 127 da LC 214/2025) e requisitos da sociedade | [modeloinicial.com.br, art. 127](https://modeloinicial.com.br/lei/LCP-214-2025/lei-complementar-214/art-127) |
| Saúde com 60%; médico nos 60% | `conhecimento/reforma-tributaria-medicos.md` |
| Imposto Seletivo: lista, alíquota sem data, cobrança no fim de jan ou início de fev/2027 | `conhecimento/reforma-tributaria-ipi-imposto-seletivo.md` |
| ICMS e ISS caem 10% ao ano de 2029 a 2032 e acabam em 2033 | `conhecimento/reforma-tributaria.md`, seção 4 |

Conta: 11,3 × 0,7 = 7,9 (desconto de 30%); 11,3 × 0,4 = 4,5 (desconto de 60%); 18 × 0,9 = 16,2.

## Cuidados

- **Publicar antes de 15/12/2026.** Os reels 1 e 3 falam do prazo do Senado. Se o Senado mudar a alíquota antes,
  regravar o número.
- **Reel 3:** o texto completo das alíneas do art. 127, § 1º, não foi lido (o site do Planalto bloqueou a leitura).
  Os três requisitos vieram de um resumo da lei. Gilberto confirma antes de gravar. O § 2º diz que juntar
  profissões diferentes da lista não tira o desconto: por isso o roteiro fala em "sócio sem registro no conselho", e
  não em "sócio de outra profissão".
- O vídeo original dizia que basta um sócio de fora da área pra perder o desconto. Isso está simplificado demais.

## Animação do reel 1 (`animacao-reel1/`)

Feita aqui, do zero: nada da animação do @reforma_simplific. Direção "Cartaz de Rua" (papel claro, Impact
gigante, laranja de alerta). 1080x1920, 30s (eram 24s; ele pediu mais lento em 30/out), 30 quadros por segundo.

- `reel1-animacao-completa.mp4`: as 5 cenas em sequência, pra ver o conjunto.
- `cena-1.mp4` a `cena-5.mp4`: cada cena solta, pra entrar por cima da gravação na fala certa.
  1. 9,2% ("o governo vinha falando em uns 9,2%")
  2. 9,2 correndo até 11,3% ("o TCU fez a conta")
  3. 15/12 e "sem voto, vale 11,3%" ("o Senado tem até 15 de dezembro")
  4. Cobertor curto ("cada setor que ganhou desconto puxou um pedaço")
  5. "Reveja o seu preço" com a logo (só se ele mantiver a frase final, que é sugestão)
- A barra da cena 4 é um desenho do mecanismo, não um gráfico: as larguras não são dado.
- Pra mudar texto ou tempo: editar `anim.html` e rodar `node render.js` nesta pasta (uns 5 min). Pra sair com 30s: `ALVO=30 node animacao-comum/render.js animacao-reel1`.

## Animações dos reels 2 a 5 (`animacao-reel2/` a `animacao-reel5/`)

Mesma direção do reel 1. O motor comum fica em `animacao-comum/` (estilo, ajudantes e `render.js`).
Pra refazer uma: `node animacao-comum/render.js animacao-reelN` (com `ALVO=30` na frente pra sair com 30s; uns 6 min cada; **um de cada vez**: os quatro
juntos travaram o Mac em 30/out).

- **Reel 2** (30s): por fora (a nota fiscal) · empresa: a CBS volta como crédito · pessoa física: paga a nota
  inteira · batata quente (indústria → distribuidor → loja → consumidor) · "Quem é o seu cliente?"
- **Reel 3** (30s): −30% · as 18 profissões da lei · barras 11,3% → 7,9% → 4,5% · o diploma não basta (holding
  sócia derruba o desconto) · "Antes de mexer no contrato social, faça a conta" (sugestão)
- **Reel 4** (30s): IPI riscado vira Seletivo · a lista da lei · a alíquota ainda não saiu · a tabela hoje × 2027,
  com a aposta como imposto novo · "O IPI não acaba. Troca de nome."
- **Reel 5** (30s): 2033 · o calendário ano a ano (100, 100, 90, 80, 70, 60%, acabou) · 18% vira 16,2%, não 8% ·
  Eclesiastes 3:1

**Os vídeos prontos estão juntos em `VIDEOS-PRONTOS/`** (fora do GitHub, como todo mp4 deste projeto).
