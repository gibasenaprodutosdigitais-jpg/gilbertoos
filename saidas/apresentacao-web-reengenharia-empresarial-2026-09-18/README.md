# Apresentação web — Reengenharia Empresarial (Bloco 1 · Manhã)

**Data:** 2026-09-18
**Formato:** página HTML interativa (não PowerPoint) — navegação por teclado,
tela cheia, contador de slide, barra de progresso por tópico.

## Por que web em vez de PowerPoint

O Gilberto pediu uma apresentação "mais sofisticada", usando como parâmetro
`gsena-palestra-reengenharia.vercel.app` (um deck de palco dele sobre Gestão
Empresarial, com cenas 3D de uma casa sendo construída). Essa referência tem
um padrão de navegação e ritmo que o PowerPoint não reproduz (contador,
tela cheia, barra de progresso nomeada, transição suave). Este deck absorve
esse padrão de navegação — sem tentar copiar as cenas 3D fotorrealistas
(nenhum gerador de imagem/3D está autorizado nesta sessão). No lugar, usa
ícone de linha dourado/coral e uma grade isométrica sutil de fundo.

O sistema visual usado aqui está registrado em
`identidade/sistema-apresentacoes-apps.md` (novo, complementa o
`design-guide.md` que cobre só os posts de Instagram).

## Conteúdo

Extraído dos 3 blocos de slides reais que o Gilberto apresentou em 16–17/set
(`Downloads/1-2-3 Bloco Treinamento_Reengenharia_Empresarial-*.pptx`) — este
primeiro recorte cobre só o **Bloco 1 (manhã)**, os 5 tópicos:
Sofisma do Faturamento → Armadilha de 2027 → Cegueira Operacional →
3 Ralos Invisíveis → Diagnóstico, terminando na ponte pro Bloco 2.

18 telas. Acento coral = confronto/risco (todo o bloco da manhã, que é
100% quebra de crença). Acento dourado = abertura (capa) e fechamento
(ponte pra tarde) — a virada de cor sinaliza a virada de tom.

## Como abrir

Abrir `index.html` direto no navegador (duplo clique, ou arrastar pro
Chrome). Não precisa de servidor.

- `→` ou `espaço`: avança · `←`: volta · `F`: tela cheia
- Botões no canto superior direito fazem o mesmo

## Isto é um rascunho pra aprovação

Só o Bloco 1 (manhã) está pronto, seguindo o mesmo padrão usado antes com
o deck de PowerPoint (Tópico 1 primeiro, aprovar, depois seguir). Depois do
seu retorno, os Blocos 2 (tarde) e 3 (noite) entram no mesmo arquivo,
completando a apresentação inteira — o Bloco 3 provavelmente vira dourado
de novo (fechamento/aliança), fazendo o arco de cor completo:
dourado → coral (manhã) → dourado (virada) → coral parcial (tarde,
confronto residual) → dourado (noite, decisão e fechamento).

## Editar conteúdo

Todo o conteúdo está no array `SLIDES` dentro de `index.html` — cada slide
é um objeto com `type`, `accent`, `title`/`quote`/`bullets` etc. Adicionar
telas é só adicionar objetos no array na posição certa.
