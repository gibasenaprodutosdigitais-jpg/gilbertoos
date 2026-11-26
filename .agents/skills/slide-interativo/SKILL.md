---
name: slide-interativo
description: Monta um slide de uma página só (one page) em formato de painel, com números grandes, gráficos e cartões clicáveis, a partir de um pedido por escrito ou de uma planilha do Excel, e que se atualiza trocando os dados. É o equivalente ao "Slide Interativo" novo do PowerPoint. Entrega em duas versões, uma página interativa (clica, troca de aba, passa o mouse e vê o detalhe) e um PowerPoint com gráficos nativos editáveis. Use quando o Gilberto disser "/slide-interativo", "slide interativo", "slide de uma página", "one page", "painel num slide", "dashboard no PowerPoint", "transforma essa planilha em slide", "slide com os números", ou mandar um Excel pedindo um resumo visual.
---

# Slide interativo (one page)

O Gilberto viu no PowerPoint o recurso "Slide Interativo": escolhe um formato,
escreve o que quer (ou sobe uma planilha) e sai um slide de uma página, em
formato de painel, clicável e que se atualiza. Ele pediu um comando que faça
isso aqui. **Ele não é técnico: fala simples, uma pergunta por vez, nunca
pede pra ele mexer em arquivo.**

## Regra-mãe: número não se inventa

Todo número do slide vem **da planilha dele, do texto dele ou de um arquivo do
repositório com a fonte anotada**. Se faltar um número, pergunta. Se ele quiser
um modelo pra ver o visual antes de ter os dados, os números de exemplo levam a
etiqueta **"EXEMPLO"** visível no próprio slide, e isso é dito a ele na entrega.

## Passo 1: entender o pedido (uma pergunta por vez, só o que faltar)

1. **O formato do painel** (sugerir o que combina com os dados):
   - **Painel executivo:** 3 a 5 números grandes (faturamento, margem, caixa...)
     + 1 ou 2 gráficos + um destaque.
   - **Comparativo:** antes e depois, plano contra realizado, A contra B.
   - **Linha do tempo:** marcos, metas por mês, cronograma.
   - **Funil:** etapas de venda, captação, conversão.
   - **Resultado de cliente:** o caso, os números de antes e depois e a frase do cliente.
2. **Os dados:** texto que ele mandou, ou planilha (`.xlsx`, `.xls`, `.csv`). Ler
   a planilha com `openpyxl` (ou `pandas`), mostrar a ele **em 3 a 5 linhas o que
   entendeu** (quais colunas, qual período, qual o total) antes de desenhar.
   Planilha de cliente é dado de terceiro: **fica fora do GitHub** (pasta local ou
   `.gitignore`).
3. **Pra quem é** (cliente, sócio, banco, equipe, telão de evento). Muda o tom e
   o que vai em destaque.

## Passo 2: direção visual

Chamar a skill **`direcao-de-arte`**: a cor e a tipografia saem do **assunto**,
não de um padrão fixo. A logo é a da marca certa (Grupo Sena, OCEO, AME, SB...):
procurar em `identidade/`, `sb/AME/logo/` e `Projetos Gsena Tec/oceo/identidade-visual/`.
Painel bom tem **hierarquia**: um número manda, os outros acompanham. Nada de
seis cartões do mesmo tamanho gritando juntos.

## Passo 3: montar as duas versões

Tudo numa pasta própria: dentro de um projeto com `saidas/`, usar
`saidas/NEGOCIOS-E-MARCA/slide-interativo-<assunto>-<AAAA-MM-DD>/`; fora dele,
`./slides-interativos/<assunto>-<AAAA-MM-DD>/`.

**Os dados ficam separados do desenho**, num `dados.json` gerado da planilha. É
isso que faz o slide "se atualizar": chegou planilha nova, roda o `gerar.py` de
novo e as duas versões saem com os números novos, no mesmo desenho.

### A) `slide.html`: a versão interativa
- Uma página 16:9 (1920x1080) que também se ajusta ao celular.
- **Clicável de verdade:** abas ou botões que trocam o período ou a visão
  (mês, trimestre, ano; unidade A e B), cartões que abrem o detalhe ao clicar,
  gráfico que mostra o valor ao passar o mouse ou tocar.
- Gráficos em SVG desenhados à mão ou com Chart.js por CDN de versão fixa
  (`cdnjs.cloudflare.com`, ex.: Chart.js 4.4.1).
- Os dados entram por um bloco `<script id="dados" type="application/json">`
  no topo, gerado do `dados.json`.
- Se ele quiser um link pra mandar a alguém, publicar como Artifact (privado),
  seguindo as regras da ferramenta Artifact.

### B) `slide.pptx`: a versão PowerPoint
- `python-pptx`, slide 16:9, **gráficos nativos** (`add_chart`), não imagem: no
  PowerPoint ele clica no gráfico, "Editar dados" e muda os números.
- Textos em caixas editáveis. Números grandes como texto, não imagem.
- Se o painel tiver abas no HTML, no PowerPoint elas viram slides extras ligados
  por **hiperlink** (clica no botão "Trimestre" e vai pro slide do trimestre), o
  que deixa a apresentação clicável também no PowerPoint.

Esqueleto do gráfico nativo:

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
s = prs.slides.add_slide(prs.slide_layouts[6])
cd = CategoryChartData(); cd.categories = meses; cd.add_series("Faturamento", valores)
g = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.6), Inches(2.4), Inches(7.5), Inches(4.4), cd).chart
g.has_legend = False; g.value_axis.has_major_gridlines = False
```

### C) `preview.png`
Renderizar o HTML com Playwright (`NODE_PATH` em `scripts/node_modules`) pra
conferir e pra mandar no WhatsApp.

## Passo 4: conferir antes de mostrar

- **Olhar o `preview.png`.** Texto estourando o cartão, número cortado, rótulo
  em cima de rótulo, contraste ruim: corrigir.
- **Somar de novo:** total do cartão bate com a soma das linhas da planilha?
  Percentual bate com a conta? Mês certo no rótulo?
- Abrir o `.pptx` gerado de novo com `python-pptx` e confirmar que os gráficos são
  nativos e com os mesmos números do HTML.
- Escrita: "você", nunca "tu"; sem travessão de efeito (`scripts/tiratravessao.py`);
  sem jargão de programador.

## Passo 5: entregar

Mensagem curta: o que o painel mostra (em uma frase), as duas versões e onde
estão, abrir a pasta no Finder (`open -R`), e como atualizar: **"quando tiver a
planilha nova, me manda que eu atualizo no mesmo desenho"**. Deixar um `LEIA.md`
na pasta com a fonte de cada número e o comando de regerar.
