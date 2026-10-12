# Calendário agendado — 12/out/2026, 19h30

Agendado por mim pela Zernio. **26 posts na fila:** 14 no Instagram e 12 no
YouTube (3 que já estavam + 9 novos).

Ritmo escolhido por ele: **3 por dia no Instagram** (09:00 / 14:00 / 20:00) e
**1 por dia no YouTube** (12:00). Horários de Brasília.

**Capa dos Reels: preta**, decisão dele, "por enquanto". Dá para trocar nos
14 de uma vez com `posts_update_post`, sem perder hora nem legenda — só
enquanto estiverem em `scheduled`.

---

## Instagram — @gilbertosenaoficial

| Dia | Hora | Vídeo | ID |
|---|---|---|---|
| seg 13 | 09:00 | A empresa não quebra por si só | `6acd5d7fd334c5947c3dd8f6` |
| seg 13 | 14:00 | Operação x Operacional | `6acd5df212ed1f1ef7a74055` |
| seg 13 | 20:00 | Palestra Expresso 97 | `6acd5df512ed1f1ef7a74059` |
| ter 14 | 09:00 | 2027 pode quebrar sua empresa | `6acd5df736c1283120888726` |
| ter 14 | 14:00 | Dinheiro é energia | `6acd5dfb36c1283120888738` |
| ter 14 | 20:00 | Metáfora do Formigão | `6acd5dff36c1283120888746` |
| qua 15 | 09:00 | O empresário não paga o imposto | `6acd5e00c34115ec20dab3ac` |
| qua 15 | 14:00 | Caixinha define | `6acd5e0212ed1f1ef7a74075` |
| qua 15 | 20:00 | Áudio do filho | `6acd5e0436c128312088875e` |
| qui 16 | 09:00 | Comitê Gestor / Simples Nacional | `6acd5e0612ed1f1ef7a74148` |
| qui 16 | 14:00 | Rico x Pobre (cortado) | `6acd5e0936c128312088876f` |
| qui 16 | 20:00 | Quantos Gilbertos tem lá fora | `6acd5e0bd334c5947c3e2420` |
| sex 17 | 09:00 | Bitributação intercompany | `6acd5e0d36c1283120888773` |
| sex 17 | 20:00 | Vídeo sobre evolução | `6acd5e102063d15cff15af5f` |

Sexta tem dois, porque catorze não fecha em múltiplo de três. Deixei o slot
das 14:00 vazio em vez de apertar três no último dia.

## YouTube — @gilbertosenaoficial, canal `UC_St0YFz8RAcHJXlxQ6zcFw`

| Dia | Hora | Vídeo | ID |
|---|---|---|---|
| seg 13 | 12:00 | Entrevista: reforma é problema ou oportunidade | `6acc43b0cb32e11718d95738` |
| ter 14 | 12:00 | O empresário não paga o imposto | `6acc43be6a5c6133e801e6cf` |
| qua 15 | 12:00 | Comitê Gestor da Reforma | `6acc43c96a5c6133e801e719` |
| qui 16 | 12:00 | Operação x Operacional | `6acd5e88be45dd484819b504` |
| sex 17 | 12:00 | A história do Formigão | `6acd5e890e911f65c34f7799` |
| sáb 18 | 12:00 | Revisão de financiamento | `6acd5e8910def5466160b5ce` |
| dom 19 | 12:00 | Dinheiro é como o Usain Bolt | `6acd5e8a10def5466160b5d9` |
| seg 20 | 12:00 | A caixinha define | `6acd5e8b0e911f65c34f77a5` |
| ter 21 | 12:00 | Três motos alugadas | `6acd5e8dcf039f7651bd3e69` |
| qua 22 | 12:00 | Quanto mais evolui, mais sensível | `6acd5e8e10def5466160b5e5` |
| qui 23 | 12:00 | Quantos Gilbertos existem lá fora | `6acd5e8f0e911f65c34f77ad` |
| sex 24 | 12:00 | Áudio do filho / legado | `6acd5e900e911f65c34f77b1` |

Os três primeiros já estavam agendados desde 12/out. Os nove novos entram
depois deles, sem buraco e sem sobreposição.

---

## Por que esta ordem

**No Instagram**, manhã é tese e técnica, tarde é conceito, noite é história
e vínculo. Nunca dois de reforma tributária seguidos, e os três mais fortes
abrem a semana: a tese-mãe na segunda de manhã, a joia do expresso na segunda
à noite, a fábula do Formigão na terça à noite.

**No YouTube**, gestão e número primeiro, história e pessoal depois. Lá a
recomendação é por tema, e um canal novo precisa ensinar o algoritmo do que
ele trata antes de pedir vínculo.

---

## Dois erros meus que eu corrigi antes de agendar

**1. `#grupo sena` com espaço**, na legenda do "empresa não quebra por si
só". No Instagram isso publica `#grupo` sozinho e deixa "sena" como texto
solto. Virou `#gruposena`.

**2. "aos 20 anos"** no título de YouTube do expresso. Eu não sei a idade
dele em 1997 e ele nunca disse — eu inventei. O título agora é *"Eu tinha
três motos alugadas e não dirigia nenhuma"*, que está na fala dele e é gancho
melhor.

---

## O que conferir depois

Vídeo fica em `publishing` alguns minutos porque o Instagram transcodifica.
Isso é normal. Conferir com `posts_list` status `published` e, se algo
falhar, `posts_list_failed` + `posts_retry`.
