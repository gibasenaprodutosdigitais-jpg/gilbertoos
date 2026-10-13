# Onde paramos

> Estado das frentes abertas. **Atualizado em 13/out/2026.**
>
> Este arquivo existe para a conversa nova começar sabendo o que já foi
> decidido, sem o Gilberto repetir nada. **Ler no início de toda sessão**, e
> **atualizar sempre que uma frente andar ou fechar.** Arquivo de estado, não
> de histórico: o que terminou sai daqui.

---

## O primeiro ato da próxima sessão

**Conferir se a fila publicou** — `posts_list` com status `published`, e
`posts_list_failed` se faltar algum. **Avisar ele do resultado sem ele
precisar perguntar.** O lote roda de 13 a 17/out no Instagram e até 24/out no
YouTube. Em 13/out os posts de 09:00 e 14:00 saíram normalmente.

**A partir de 18/out, o primeiro ato é outro: fazer a análise de cadência.**
Está especificada na seção 3, com as ferramentas, a ordem das métricas e a
linha de base de 13/out para comparar. **É a única coisa com data marcada.**

Fora isso, nada está esperando de mim. **As frentes estão na mão dele ou de
terceiros:** o SBS com os sócios, o livro com o Stanley, o conteúdo agendado.
Duas decisões são dele e não devem ser aplicadas sem aval: **a capa dos Reels**
(preta "por enquanto") e **o topo da escada de posicionamento**.

---

## 1. SBS — Sena, Bittar e Simões

### ★ A esteira foi substituída em 13/out/2026

**O que vale agora está em `sbs/esteira.md`.** Quatro produtos, preço por
tempo de programa:

| Produto | Prazo | Preço |
|---|---|---|
| Imersão presencial | 2 dias | R$ 3.000 a R$ 5.000 por pessoa |
| Choque de Ordem e Caixa | 3 meses | **R$ 35.000** |
| Escala Blindada | 6 meses | **R$ 60.000** |
| Advisory Board e Expansão | 12 meses | **R$ 160.000** |

**Saíram:** a mentoria de 90 dias por R$ 50.000, a continuidade de 6 meses e
a cesta por porte (R$ 105/200/400 mil). Os arquivos continuam na pasta com
aviso de substituído, porque **a metodologia deles segue valendo** — os
quatro pilares, a divisão de autoridade entre os sócios, o roteiro dos
encontros e a anamnese.

⚠ **Ele reafirmou os R$ 50.000 em 12/out e decidiu o contrário em 13/out**,
depois que eu apontei que o programa de 3 meses a R$ 35.000 colidia com a
mentoria de 90 dias a R$ 50.000. **A decisão nova é a que vale.** Não
ressuscitar a antiga.

**O SBS vende direcionamento, não execução.** Ele mandou incluir execução em
13/out e **mandou retirar no mesmo dia**. Vale a segunda. O SBS aponta o que
mudar — regime, equiparação hospitalar, DRE, licenças — e **quem executa é a
equipe do cliente**. Sem BPO, sem assumir contabilidade, sem gerir tráfego.

**A ancoragem é a das três cabeças**, tese dele de 13/out: o cliente não
contrata um consultor, contrata três leituras cruzando antes de chegar na
mesa dele — gestão e imposto, médico e venda, margem e dinheiro.

⚠ **Duas coisas de preço com resposta já escrita em `esteira.md`:**
1. **O de 12 meses custa mais por mês que o de 6** (R$ 13.333 contra
   R$ 10.000). Quem subir do 6 para o 12 vai perguntar. A resposta é que
   muda a natureza: 4 presenciais em vez de 1, e os três passam de mentores
   a conselho, entrando em decisão de abrir unidade e comprar concorrente.
2. **O preço é por tempo, não por porte.** Uma clínica de uma sala paga o
   mesmo que uma rede.

### ⚠ O que não pode ser vendido, mesmo com a esteira nova

**O Simões explica o Smart Money. Não aplica, não indica, não capta.**
Cláusula 3.7 do termo assinado, decidida em 06 e 07/out. O material de origem
propunha ele renegociando dívida e captando crédito; **escrevi a esteira sem
isso de propósito**. Item 9 do `historico-de-decisoes.md`, ainda aberto.

**O caso do Bittar entra como estudo de caso estrutural, sem afirmação
nenhuma** sobre conselho profissional, vigilância sanitária, processo ou
litígio. Decidido por ele em 13/out. A verificação em
`sbs/material/verificacao-stanley-bittar-2026-10-13.md` **serve para saber
onde não pisar, não para citar.**

### Os PDFs estão desatualizados

Os três PDFs em `sbs/` foram gerados da esteira antiga. **Regerar quando ele
pedir**, com `gerar-plano-pdf.py`, que precisa ser ajustado para a esteira
nova.

**Próximo passo: é dos sócios.** A mudança para execução depende da estrutura
dos três, não só da agenda.

## 2. Livro "O Médico e o Executivo"

Coautoria com o **Dr. Stanley Bittar** (grafia correta: **Stanley**, com N).
O título foi ideia do Gilberto. O tema é a quebra da **Stanley's Hair**.

**A parte dele: 88 de 100 páginas**, em 10 capítulos, já no formato ABNT da
editora (Times 12, entrelinha 1,5, margens 3/3/2/2).

- Texto-fonte: `livro-o-medico-e-o-executivo/capitulos/*.md`
- Saída formatada: `livro-o-medico-e-o-executivo/formatado/`
- PDF para análise: `formatado/O Medico e o Executivo - a parte do Gilberto.pdf`
- Plano de redação e contagem: `a-parte-do-gilberto.md`
- Como formatar: `python3 formatar-capitulo.py capitulos/<arquivo>.md`,
  depois `python3 juntar-parte-do-gilberto.py`

### As 12 páginas que faltam não são capítulo novo

Elas estão nos pontos marcados `[LIGAR]` dentro dos capítulos 2, 3 e 5, onde
a voz do executivo se encontra com a do médico. **Dependem dos capítulos do
Stanley**, que ainda não chegaram. Não inventar essa parte.

### Decisões abertas, todas dele

1. **A exageração do currículo na Fiat** fica no livro ou sai?
2. **A admissão de "covardia educada"** no capítulo Recomeço fica?
3. **O Sr. Elmo (Elmo Calçados) pode ser nomeado?** Hoje há proibição de
   nomear registrada em `_memoria/quem-e-gilberto.md`. O caso é o suicídio
   dele no escritório, por aperto financeiro e falta de direção.
4. **"Stanley's Hair" leva apóstrofo** na capa?

### Pendências técnicas

- **O PDF do escopo da editora escreve "Staley" em todo lugar.** Precisa ser
  corrigido na fonte antes de ir para a editora.
- **A capa precisa de originais em resolução maior.** A foto do Stanley é um
  print de story, 719×1280, com área útil de ~460×613. Serve para tela, não
  para impressão. Arquivos em `capa/fotos/`.
- **Falta o acordo de coautoria** com o Stanley.

---

## 3. Conteúdo e publicação (Zernio)

**26 posts agendados** em 12/out/2026. Dia, hora e ID de cada um estão em
`saidas/reels-a-postar-2026-10-12/calendario.md`.

- **Instagram:** 14 Reels, 3 por dia (09:00 / 14:00 / 20:00), de 13 a 17/out.
- **YouTube:** 12 vídeos, 1 por dia (12:00), de 13 a 24/out.

**Conferir se publicaram** com `posts_list` status `published`. Vídeo fica
alguns minutos em `publishing` porque o Instagram transcodifica — é normal.
Se falhar, `posts_list_failed` e `posts_retry`.

O manual completo da Zernio (IDs, fluxo, limites, armadilhas) está na memória
do Claude, não no repositório, porque envolve credencial e conta.

### O Vivaldi que falhou: decidido, não republicar

Um post da série de música clássica (**Vivaldi, "O Verão"**, ID
`6acc2887071048c61ddac918`) falhou em 11/out — o Instagram não processou a
mídia e pediu novo envio. **Nada chegou a ir ao ar.**

**Ele decidiu em 13/out deixar de lado.** O perfil passou a receber conteúdo
de gestão, e um Vivaldi no meio dos Reels de reforma tributária não cabe
mais.

⚠ **Ele continua aparecendo em `posts_list_failed`.** Não é problema novo e
**não perguntar de novo** — a decisão está tomada.

### Capa dos Reels: preta, "por enquanto"

Ele escolheu capa preta em 12/out/2026, depois de eu recomendar o frame do
próprio vídeo. Disse **"por enquanto"**, então a decisão segue aberta.
**Perguntar no próximo lote em vez de assumir.** Dá para trocar nos 14 de uma
vez com `posts_update_post` enquanto estiverem em `scheduled`.

### Dois vídeos fora da fila

- **Victoria's Secret:** ele vai **regravar**. O vídeo diz que a venda foi de
  4 milhões de dólares e o suicídio dois anos depois; o documentado é
  1 milhão, em 1982, e a morte em agosto de 1993. O texto já escrito está em
  `saidas/reels-a-postar-2026-10-12/fora-da-fila.json` e serve para a nova
  gravação.
- **Vídeo do Ricardo:** descartado. Quem fala é outro empresário e o CTA
  manda o seguidor para o perfil dele.

### O canal do YouTube é de gestão e tributário

Ele cancelou subir os Reels de música clássica para lá, porque o algoritmo
recomenda por tema e misturar confunde os dois lados. **Conferir se o assunto
cabe antes de mandar qualquer coisa para o YouTube.**

---

### ★ Análise de cadência — agendada para 18/out/2026

Em 13/out ele trouxe um método de terceiro (cards atribuídos a "Nardon",
marca Advisor News) pedindo 12 posts por dia. **A regra e o que foi aceito e
recusado estão em `_memoria/posicionamento.md`, no bloco do fim.** Duas
coisas ficaram em aberto e são para analisar depois, não agora.

**1. O número da cadência — depende de dado que chega sexta.**

O lote de 13 a 17/out está rodando a **3 posts por dia**, contra a grade
oficial de **3 por semana**. É a primeira vez que ele roda nesse ritmo. **A
partir de 18/out os 14 posts já publicaram e dá para medir.**

Como medir, na ordem da hierarquia de métricas que virou regra:

| Passo | Ferramenta |
|---|---|
| Puxar os 14 posts do lote | `analytics_get_post_timeline` |
| Comparar com a base anterior | `analytics_get_daily_metrics` |
| Horário que performou | `analytics_get_best_time_to_post` |

**O que decide:** encaminhamento (compartilhamento) por post, primeiro. Depois
alcance. **Não decidir por curtida nem por seguidor novo.**

**Caiu um segundo teste no colo, no TikTok.** Em 13/out ele mandou publicar
lá **de 4 em 4 horas sem parar**, e **4 dos 14 caem entre meia-noite e 7h**.
Avisei e ele manteve. Então dá para comparar, no mesmo lote e com o mesmo
conteúdo, **os 4 da madrugada contra os 10 do horário comercial** — e
responder se horário importa no TikTok dele, onde a entrega é por Para Você
e não por seguidor. Calendário em
`saidas/reels-a-postar-2026-10-12/calendario.md`.

A pergunta a responder: **3 por dia rendeu mais encaminhamento TOTAL na
semana, ou só diluiu o mesmo bolo em mais posts?** Se diluiu, voltar a
frequência do feed e jogar o excedente pro Stories.

**Linha de base de 13/out/2026**, para comparar depois:
- Instagram **105.455** seguidores · alcance de 3.000 a 6.267 por post
  (menos de 6% da base) · impressões até 9.471
- TikTok 3.195 · YouTube **2** · Twitter 0

**2. A escada — decisão dele, não minha.**

Eu recusei a "escada do desejo" que termina em **Idolatrado**, porque
contraria o inimigo que ele mesmo declarou (a indústria que vende acesso e
status) e a personalidade de maturidade emocional. Propus terminar em
**Procurado**.

⚠ **Ele ainda não deu o aval.** Em 13/out mandou registrar para análise
futura. **Perguntar quando o assunto voltar; não aplicar a escada nova como
se estivesse decidida, nem a antiga.**

---

## 4. Coisas que eu errei aqui e não devo repetir

- **Escrevi "aos 20 anos" sobre 1997 sem conferir.** Ele tinha 24, e a data de
  nascimento **já estava no repositório**. Agora está em "O básico" de
  `quem-e-gilberto.md`, com tabela de ano e idade. **Calcular, nunca estimar.**
- **Pus idade colada a um fato errado.** "Três motos" é 1999 (26 anos), não
  1997 (24). Conferir a data do fato, não só a idade.
- **Escrevi `#grupo sena`, com espaço.** No Instagram publica `#grupo` e deixa
  "sena" solto. Hashtag nunca tem espaço.
- **Escrevi a reestruturação do SBS inteira sem confirmar o preço.** Deu
  retrabalho e precisou de `git checkout`.
- **Tratei ele por "tu".** Ele pediu "você" em 09/out/2026 e é definitivo.

---

## 5. Empreenda — encerrado e enxugado

A sociedade com a Elaine (**Ecossistema Empreenda**) foi descontinuada em
11/08/2026. Em **12/10/2026 ele mandou eliminar todo o material de plano de
negócios e de projeto, deixando só o jurídico.**

**Sobrou:** `negocios-declinados/juridico/`, 7 pastas. Ver o README de lá.
**Saiu:** `comercial/`, `financeiro/` e o carrossel do Empreenda Business.
Tudo recuperável no histórico do git — o comando está no mesmo README.

⚠ **Há uma cobrança em aberto:** R$ 31.330,37, na proposta de dissolução de
19/08, com **2 pontos pendentes de confirmação dele**. O demonstrativo
financeiro que sustentava esse número foi removido junto; se a cobrança
evoluir, recuperar do git.

**Não retomar, atualizar nem expandir nada da Empreenda.** Se o nome
aparecer num pedido novo, perguntar antes se é sobre o encerramento ou outra
coisa.

---

## 6. ⚠ A pasta .git está com 1,2 GB — pendente

Em 13/out/2026 apagamos 2.073 duplicatas e liberamos 279,3 MB **no disco**.
Entraram no `.gitignore` as sobras de edição de vídeo e o padrão de duplicata
do macOS, então o problema não volta sozinho.

**Mas a sincronia com o celular continua lenta, e por outro motivo:** o
histórico do git guarda um **brandbook de 235,5 MB**, commitado uma vez lá
atrás e depois removido. O arquivo não está mais no repositório; o histórico
não esquece.

**O conserto existe** — reescrever o histórico com `git filter-repo` ou BFG.
A pasta cairia de 1,2 GB para algo perto de 200 MB.

⚠ **Não fazer de passagem.** Reescrever histórico obriga `--force` e **o
celular dele para de sincronizar até alguém baixar o repositório do zero.**
Ele pediu em 13/out para combinar isso em outro momento, provavelmente com o
Cid junto. **Não executar por conta própria.**

---

## 7. Fora deste repositório

O **OCEO** é projeto à parte, em `Projetos Gsena Tec/oceo/`, com CLAUDE.md
próprio e código rodando. **Ler o CLAUDE.md de lá** antes de mexer, e não
tratar como parte do GilbertoOS.
