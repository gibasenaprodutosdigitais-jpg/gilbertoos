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
4. `identidade/design-guide.md` — o que é fixo (a marca) e o que não é mais
   (cor e fonte saem do assunto de cada peça)
5. Se o tema for técnico (imposto, reforma) → `conhecimento/` pra não errar
   fato e poder citar. **Nunca inventar número ou regra técnica.**

## Regra de linguagem (crítica)

Escrever como o **Gilberto** escreveria — autoridade + sabedoria, não redator
publicitário. Sem jargão de guru, sem promessa fácil. Ver `tom-de-voz.md`.

## Direção visual: vem da skill `direcao-de-arte`

**Não existe mais paleta fixa** (revogado em 22/set/2026). Antes de desenhar
qualquer coisa, invocar a skill `direcao-de-arte`: ela lê o assunto, propõe
três direções visuais diferentes e só então se monta. Cor, tipografia e
composição saem do **assunto daquele carrossel**, não de um padrão do
Gilberto. Ela também tem validador de contraste e auditoria anti-cara-de-IA.

O que continua fixo, porque não é sobre cor: a logo do leão entra uma vez,
pequena. Autoridade acima de enfeite. Sem foto de banco de imagem, sem emoji
como ícone.

- **Layouts nomeados** (variar pra criar ritmo): CAPA · DECLARAÇÃO · NÚMERO ·
  CONTRASTE · LISTA · RESPIRO · CTA FINAL. Nunca repetir o mesmo tipo em dois
  slides seguidos.

### Foto do Gilberto de fundo (27/ago/2026, agora condicionada à direção)

Quando a direção escolhida comportar foto, usar uma dele
(`identidade/@eubernardocoelho-Gilberto-Sena-104.jpg` ou equivalente) como
fundo só da CAPA e do CTA FINAL, sempre com véu por cima pra o texto ficar
legível. A cor do véu sai da direção escolhida, não é mais fixa em grafite.
Direção de papel, cartaz ou caderno geralmente não comporta foto: nesse caso
não force.

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
