# YouTube Shorts: gestão e mentalidade

Onze vídeos baixados em **11/out/2026**, do período de 23 a 30/set/2026.
Vieram **sem legenda**: transcrevi os onze e escrevi as legendas do zero, no
formato do YouTube.

**Arquivo das legendas:** `legendas.json`, com título, descrição e tags por
vídeo. **Nada foi publicado ainda.**

---

## O que é cada um

| Código | Seg | O que é | Título |
|---|---|---|---|
| `DdpPf51s27Z` | 64 | **fala dele** | 30% dos empresários vão quebrar em 2027 |
| `DdpZa12MyV-` | 95 | áudio oficial | Simples Nacional: prazo do regime híbrido |
| `Ddtiux7s-vl` | 44 | **fala dele** | O empresário não paga imposto |
| `DdtksOVM9BB` | 58 | react (Suits) | Lealdade não se mede quando está tudo bem |
| `DdwDkUrMMGP` | 99 | react (áudio) | É sempre mais escuro antes de amanhecer |
| `DdzdcnvMc3Q` | 7 | react curto | Não conte o seu sonho |
| `Ddzs4gvsZxL` | 39 | react (filme) | Quem você escolhe revela seu caráter |
| `Dd09OSYs9Bq` | 111 | **entrevista dele** | A empresa não quebra sozinha |
| `Dd4yBWIMDBv` | 51 | react (300) | 300 contra um milhão |
| `Dd6sQUHgl1Y` | 29 | react (Suits) | A primeira impressão é a que fica |
| `Dd1gN9LMirD` | 4 | ⚠ **quebrado** | sem legenda, ver abaixo |

**Os três melhores são os dele falando.** Em especial a entrevista
`Dd09OSYs9Bq`: "a empresa não quebra por si só, quem quebra a empresa é o
empresário", com a história de servente e motoboy e a metáfora da borboleta.

---

## ⚠ Um vídeo fora

`Dd1gN9LMirD` tem **4 segundos, nenhum áudio e está em codec VP9**, não em
H.264. É o único de 720x1280; todos os outros são 1080x1920. A transcrição
falhou nele porque não há faixa de áudio.

**Não serve como Short.** Se for mesmo para usar, precisa ser reconvertido
e, ainda assim, 4 segundos sem som não sustenta uma publicação.

---

## ⚠ Direito autoral: isso pesa mais no YouTube

**Seis dos onze são react de obra de terceiro:** cenas de Suits (NBCUniversal),
de 300 (Warner), de outro filme, e áudio motivacional de outro autor. Um
sétimo usa áudio de coletiva do Comitê Gestor.

No Instagram isso passa. **No YouTube o Content ID é mais agressivo**, e o
que costuma acontecer com esse tipo de material:

- O vídeo fica no ar, mas **a monetização vai para o detentor**.
- Em alguns casos, bloqueio em certos países.
- Reincidência em obra do mesmo detentor pode gerar aviso de direitos
  autorais, que é mais sério que a reivindicação simples.

**Os três em que ele aparece falando não têm esse risco.** Se a intenção for
construir o canal sem passivo, começar por eles é o caminho mais seguro.

Isso foi dito a ele em 11/out/2026.

---

## Como as legendas foram escritas

Formato do YouTube, que é diferente do Instagram porque **lá a distribuição
é por busca**:

- **Título** com a tese do vídeo, em linguagem de quem procura. Não o nome do
  filme: usar o nome da obra convida a reivindicação e ainda faz o vídeo
  competir com o clipe original.
- **Descrição** que abre entregando o conteúdo, não pedindo seguidor.
- **Tags** no campo próprio, de 7 a 8 por vídeo.
- **Assinatura no rodapé** com o Instagram, para mandar tráfego de lá para cá.

Todos os títulos abaixo de 100 caracteres e as tags abaixo de 500, que são os
limites do YouTube.

---

## O que foi publicado, e por quê

**Decisão dele em 11/out/2026:** o objetivo é **construir o canal**, então
publicar só o que serve a esse propósito.

**Os quatro agendados**, um por dia ao meio-dia, horário de Brasília:

| Dia | Título | Por que entrou |
|---|---|---|
| 12/out | 30% dos empresários vão quebrar em 2027 | ele falando, gancho forte, 64s |
| 13/out | A empresa não quebra sozinha | o melhor do lote: tese e história dele |
| 14/out | O empresário não paga imposto | ele falando, curto e direto |
| 15/out | Simples Nacional: prazo do regime híbrido | utilidade e busca, sem risco autoral |

**Os seis react ficaram de fora.** Mostram Harvey Specter e os 300, não ele.
Não constroem autoridade nenhuma para o canal e trazem reivindicação de
direito autoral junto. Para construção de canal, é passivo sem retorno.

Eles continuam com legenda escrita em `legendas.json`, caso ele mude de
ideia.

⚠ **Um por dia ao meio-dia foi escolha minha**, não dele. O YouTube premia
constância, e meio-dia é o intervalo de almoço de quem é o público dele. **É
palpite informado, não dado.** Quando houver histórico no canal,
`analytics_get_best_time_to_post` dá o horário real.

## Para publicar o resto



Conta do YouTube na Zernio: `6acc3f8b437b757617379afd`, canal
`UC_St0YFz8RAcHJXlxQ6zcFw`.

Os vídeos ainda **não foram enviados** para a Zernio. O fluxo está no manual,
na memória do Claude, em `zernio-instagram-conectado`.

⚠ No YouTube, o título vai em `platformSpecificData.title` e as tags no campo
`tags` do post. Sem título explícito, a Zernio usa a primeira linha da
descrição, que aqui não serve.
