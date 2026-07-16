---
name: carrossel
description: >
  Vira uma ideia em carrossel pronto pro Instagram do Gilberto — HTML
  estilizado renderizado em PNG 1080x1350 + legenda pronta. Na voz do Gilberto
  e no visual dele. Use quando ele disser "/carrossel", "faz um carrossel",
  "post pro instagram", "transforma isso em carrossel".
---

# /carrossel — carrossel pro Instagram do Gilberto

Pega um tema → entrega slides prontos pra postar + legenda. Tudo na voz do
Gilberto e no visual de autoridade dele.

## Antes de criar (ler sempre)

1. `_memoria/tom-de-voz.md` — como o Gilberto fala (a linguagem dos slides
   segue isto ESTRITAMENTE)
2. `_memoria/quem-e-gilberto.md` — autoridade, história, o que ele domina
3. `_memoria/posicionamento.md` — o ângulo e os pilares de conteúdo
4. `identidade/design-guide.md` — cores, fonte, sobriedade do visual dele
5. Se o tema for técnico (imposto, reforma) → `conhecimento/` pra não errar
   fato e poder citar. **Nunca inventar número ou regra técnica.**

## Regra de linguagem (crítica)

Escrever como o **Gilberto** escreveria — autoridade + sabedoria, não redator
publicitário. Sem jargão de guru, sem promessa fácil. Ver `tom-de-voz.md`.

## Estilo visual base (quando o design-guide for vago)

Sóbrio e premium: fundo escuro OU claro + off-white + **UMA** cor de destaque
(dourado/azul do guia). Nunca cores brigando. Cara de quem entende de dinheiro,
não de coach de Instagram.

- **Tipografia:** Inter. Capa 88-100px/900, letter-spacing -0.035em. H2
  60-72px/800. Corpo 20-24px/500. Kicker 13-15px/700 UPPERCASE, spacing 0.24em.
- **Elementos:** régua fina na cor de destaque, wordmark/nome top-left +
  contador top-right, border-top translúcida no rodapé.
- **Layouts nomeados** (variar pra criar ritmo): CAPA · SOLO · DUO · NÚMERO ·
  CITAÇÃO · CTA FINAL. Nunca dois slides seguidos com o mesmo fundo.

## Estrutura (5 a 10 slides)

- Slide 1: `CAPA` — título impactante (máx 8 palavras)
- Internos: um insight por slide, 2-3 layouts diferentes, frases naturais
- Último: `CTA FINAL` — @handle do Gilberto + convite

## Workflow

1. **Texto primeiro.** Escrever os slides na voz dele. Pra capa, oferecer 3
   opções de título. **CHECKPOINT: mostrar o texto e esperar aprovação antes
   do visual.**
2. **Visual.** Criar um único `carrossel.html` com todos os slides como
   `<div class="slide">` (inline CSS, Google Fonts como única dependência
   externa). Aplicar cores/tipografia do design-guide, mínimo 2 layouts.
3. **Render.** Criar `render.js` na mesma pasta (Playwright: abre o HTML e tira
   screenshot de cada `.slide` em 1080x1350). Reutilizar `node_modules` de
   `scripts/` quando possível:
   `NODE_PATH="../../scripts/node_modules" node render.js`
   Se o Playwright não estiver instalado, avisar o Cid (setup de máquina).
4. **Mostrar** slide 1, 2 e o CTA renderizados. Aprovado → gerar o resto.
5. **Legenda automática** (sempre, sem pedir): salvar `legenda.md` — hook +
   contexto + "arraste pro lado" + assinatura do Gilberto + 10-15 hashtags
   (tributário / empresário / o nicho dele).

## Saída

```
saidas/carrossel-<tema>-<AAAA-MM-DD>/
  texto.md
  carrossel.html
  render.js
  instagram/  slide-01.png … slide-NN.png
  legenda.md
```

## Regras

- 1080x1350 (4:5) sempre
- Autoridade > enfeite. Se ficou com cara de coach, refazer.
- Nunca inventar fato técnico — checar `conhecimento/` ou perguntar ao Gilberto
- Não repetir layout entre slides
- Legenda sempre gerada ao final
