# Onde paramos

> Estado das frentes abertas. **Atualizado em 12/out/2026, 21h.**
>
> Este arquivo existe para a conversa nova começar sabendo o que já foi
> decidido, sem o Gilberto repetir nada. **Ler no início de toda sessão**, e
> **atualizar sempre que uma frente andar ou fechar.** Arquivo de estado, não
> de histórico: o que terminou sai daqui.

---

## 1. SBS — Sena, Bittar e Simões

Os documentos comerciais estão **prontos e em PDF**, aguardando análise dos
sócios. Nada pendente do meu lado.

| Documento | Arquivo |
|---|---|
| Mentoria (90 dias) | `sbs/SBS Mentoria Business Medical.pdf` |
| Continuidade (6 meses e 1 ano) | `sbs/SBS - Proposta de continuidade.pdf` |
| Cesta de produtos (ano fechado) | `sbs/SBS - Cesta de produtos.pdf` |
| Fichas de diagnóstico (3 portes) | `sbs/ficha-diagnostico/*.pdf` |

**O preço da mentoria é R$ 50.000 à vista ou 12x de R$ 5.000.** Isto é
definitivo. Ele mandou reverter uma reestruturação de 6 meses / R$ 100.000
que eu havia escrito ("SBS PRO") e **remover o PRO inteiro**. O que foi
retirado está registrado em `sbs/historico-de-decisoes.md`. **Não ressuscitar
o PRO nem alterar esse preço** sem ele pedir.

**O nome do produto é "SBS Mentoria Business Medical".**

A cesta tem 3 etapas × 3 portes (clínica, hospital dia, rede e grandes
hospitais), com valor separado por etapa e pacote fechado de ano. Os números
estão em `sbs/cesta-de-produtos.md`.

**Próximo passo: é dos sócios.** Eu entro de novo quando ele trouxer retorno
da análise.

---

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

## 5. Fora deste repositório

O **OCEO** é projeto à parte, em `Projetos Gsena Tec/oceo/`, com CLAUDE.md
próprio e código rodando. **Ler o CLAUDE.md de lá** antes de mexer, e não
tratar como parte do GilbertoOS.
