# Sistema visual — apresentações de palco e aplicativos

> Extensão do `identidade/design-guide.md` (que cobre os posts de Instagram)
> pra dois formatos novos: **decks de palestra/imersão interativos** (web,
> não PowerPoint estático) e **aplicativos**. Usa a mesma base de marca —
> nunca cria uma identidade paralela.

## Quando usar este arquivo em vez do `design-guide.md`

- `design-guide.md` → carrossel e reels (Instagram). Regra de uma cor só.
- Este arquivo → apresentação de palco/imersão em HTML interativo,
  ferramentas internas, protótipos de app, qualquer coisa com navegação,
  estado ou interação (não é só uma imagem estática).

## Base (herdada, não muda)

- Fundo escuro principal `#0F1419`, preto `#0A0A0A`, papel `#F4F1EA`.
- Texto sobre escuro `#F4F1EA`; sobre claro `#151515` (título) / `#454545` (corpo).
- Dourado de marca `#C9A227` — autoridade, solução, avanço.
- Tipografia: **Fraunces** (serifada, títulos/frases de impacto) + **Inter**
  (sans, rótulos/kicker/UI). Leão dourado (`identidade/logo-transparente-crop.png`)
  + wordmark "GILBERTO SENA".

## O que este formato acrescenta

**1. Um segundo acento — coral de risco, só pra isto**
`#E0654F` (coral queimado). Reservado pra sinalizar *problema, risco,
confronto* em decks/apps — nunca no Instagram, onde a regra de uma cor só
continua valendo. Dourado = solução/avanço/autoridade. Coral = alerta/ferida
a expor antes da virada. Um conteúdo pode migrar de coral pra dourado no
meio da apresentação, no exato momento em que a narrativa vira de
"problema" pra "solução" — isso é permitido e é um recurso, não um erro de
consistência.

**2. Cromo de navegação (todo deck/app de palco usa este padrão)**
- Topo-esquerda: leão + wordmark + kicker do módulo atual.
- Topo-direita: contador `NN / TT`, setas ‹ ›, botão de tela cheia.
- Rodapé: barra de progresso com as etapas nomeadas (nome curto, 1-2
  palavras, maiúsculo), o segmento atual preenchido na cor do estado
  (dourado ou coral).
- Navegação: seta direita/esquerda do teclado avança/volta; `F` alterna
  tela cheia. Sem menu, sem scroll — uma decisão por tela.

**3. Estrutura de conteúdo por tópico (4 tipos de tela, repetem)**
- **Marcador**: numeral + nome do tópico, título grande, subtítulo itálico
  discreto.
- **Crença/confronto**: citação grande (o que a pessoa pensa hoje, ou a
  virada que desmonta isso).
- **Dado na empresa**: eyebrow "NA EMPRESA" + rótulo curto + 3 bullets com
  losango dourado/coral — nunca mais que 3 por tela.
- **Ponte**: fecha o bloco e assina a transição pro próximo (troca de cor
  se for virada problema→solução).

**4. Sem foto de banco de imagem, sem 3D fotorrealista**
Sem gerador de imagem/vídeo conectado nesta sessão pra renderizar cenas 3D
(tipo casa em construção). Em vez disso: ícone de linha dourado/tinta
desenhado à mão (mesmo estilo dos carrosséis) ou grade isométrica sutil em
SVG como textura de fundo — nunca clip-art, nunca gradiente arco-íris.
Se um dia o Gilberto autorizar um gerador de imagem/3D, este é o primeiro
lugar onde vale a pena usar (cena figurativa recorrente, tipo a casa da
referência), mas o sistema tem que funcionar bem sem isso.

**5. Movimento**
Transição entre telas: fade + leve deslocamento vertical, ~450ms,
`ease-out-cubic`. Nunca linear. Uma coisa muda por vez na tela — nunca
duas revelações simultâneas.

## Para aplicativos (além do deck)

Mesma paleta e tipografia. Diferença: o app tem estado (o que a pessoa
preencheu, clicou, salvou) — então qualquer protótipo de app deve nascer
pensando em "o que precisa ser lembrado entre uma visita e outra" antes de
desenhar a tela.

## Referência

Site usado como parâmetro de sofisticação (estrutura de navegação, ritmo,
progressão nomeada): `gsena-palestra-reengenharia.vercel.app` — decks de
palco do Gilberto sobre Gestão Empresarial, com cenas 3D de uma casa sendo
construída (dourado) e depois rachando (coral). O padrão de navegação e
tipografia foi absorvido aqui; as cenas 3D specific daquele site não são
replicadas (sem pipeline de imagem 3D nesta sessão) — substituídas por
ícone de linha e textura isométrica sutil, conforme item 4 acima.
