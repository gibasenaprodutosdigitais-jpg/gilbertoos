# Instagram @gilbertosenaoficial: a série de música clássica

Registro das publicações feitas por aqui, pela Zernio. Serve para não repetir
vídeo, para saber o que já foi ao ar e para medir depois.

**Manual de como publicar:** está na memória do Claude, em
`zernio-instagram-conectado`. Aqui fica só o que foi publicado.

---

## Lote 1. 10/out/2026, formato REACT

Orquestra em cima, Gilberto reagindo embaixo. Um a cada 15 minutos, a partir
das 22:49. **Os 12 publicaram, nenhuma falha.**

Capa preta em 11 deles; o primeiro saiu antes da decisão da capa, com o frame
do próprio vídeo.

| # | Obra | Código de origem | Duração |
|---|---|---|---|
| 1 | Bach — Air, BWV 1068 | `DbMgtUwjkqz` | 57s |
| 2 | Mozart — Rainha da Noite | `DbRV1PlEuIx` | 42s |
| 3 | Beethoven — Sonata ao Luar | `DbR0Y3Nk5YD` | 64s |
| 4 | O Fantasma da Ópera | `DbJxnhukryi` | 96s |
| 5 | Satie — Gymnopédie nº 1 | `DbL-kf5DI0-` | 62s |
| 6 | Einaudi — Experience | `DbJnRi0AZBR` | 50s |
| 7 | Queen — Bohemian Rhapsody | `DbYR3krCFNF` | 64s |
| 8 | Bach — Ária cantada | `DbO-l4tgnJw` | 44s |
| 9 | Vivaldi — As Quatro Estações | `DbWRzI1DuRj` | 93s |
| 10 | Wieniawski — Variações Op. 15 | `DbLxIv-AESx` | 90s |
| 11 | Händel/Halvorsen — Passacaglia | `Dbn8lpVjsLH` | 49s |
| 12 | Morricone — Era uma Vez no Oeste | `DbQsrWgmFVR` | 71s |

## Lote 2. agendado para 12/out/2026, formato CENTRALIZADO

Vídeo original centralizado no preto, chamada em cima e CTA embaixo. Sem o
Gilberto em tela. Um a cada hora, da meia-noite às 6h. Todos com capa preta.

| Hora | Obra | Código de origem | Duração |
|---|---|---|---|
| 00:00 | Tom & Jerry e a música clássica | `DcFLfZEDGMw` | 34s |
| 01:00 | Carl Orff — O Fortuna | `DcOJF_MgVhT` | 55s |
| 02:00 | James Last — O Pastor Solitário | `DbWD5kSjlxg` | 42s |
| 03:00 | Happy Birthday — surpresa da orquestra | `DbRqjIEAJ7I` | 36s |
| 04:00 | Ekaterina Shelehova — Earth Melodies | `DbS17uRgIPk` | 96s |
| 05:00 | Chopin — Noturno nº 20 | `DbllYq8AO9Z` | 69s |
| 06:00 | Vivaldi — O Verão, Salut Salon | `DbapFYkCrVy` | 101s |

---

## ⚠ Os cinco que ficaram de fora

Na pasta `seis-download-com @ -001` do Downloads existem **cinco vídeos no
formato centralizado que repetem conteúdo do lote 1**: os códigos
`DbMgtUwjkqz`, `DbRV1PlEuIx`, `DbR0Y3Nk5YD`, `DbJxnhukryi` e `DbL-kf5DI0-`.
Quatro deles com **a legenda palavra por palavra igual** à que já foi ao ar.

**Ele decidiu em 11/out/2026 não publicar esses cinco.** Se um dia forem
usados, reescrever as legendas antes.

## Como eu confiro repetição

O nome do arquivo traz o código do post de origem no Instagram, aquele
pedaço tipo `DbMgtUwjkqz`. **É por ele que eu comparo**, não pelo nome da
obra nem pelo número da frente, que se repetem entre lotes.

---

## ~~Levar os 12 do lote 1 para o YouTube~~ Cancelado

**Ele decidiu em 11/out/2026 não subir esses vídeos para o YouTube.** Nada
foi publicado lá: o trabalho parou nas legendas.

**O que ficou pronto e continua valendo:**

- **O canal está conectado** à Zernio, saudável, com permissão de publicar e
  de ler métricas. ID `6acc3f8b437b757617379afd`, canal
  `UC_St0YFz8RAcHJXlxQ6zcFw`. Ele pagou o plano para isso, então a conta
  continua disponível para quando houver conteúdo que caiba lá.
- **As 12 legendas no formato do YouTube** estão em
  `youtube-legendas.json`, com título, descrição e tags. Servem de modelo
  para qualquer vídeo que vá para lá depois.

**O que pesou na decisão**, e vale lembrar numa próxima: o canal dele é de
**gestão e tributário**, e no YouTube a recomendação é por tema. Misturar
música clássica ali confunde o aprendizado do algoritmo nos dois sentidos.
Isso foi dito a ele antes, e a decisão de não subir veio depois.

### O histórico, que fica



Ele pediu isso em **11/out/2026**, e parou num limite de plano. Retomar
quando ele avisar.

**O que trava:** a Zernio só conecta **2 contas no plano gratuito**, e as
duas já estão ocupadas por Instagram e TikTok. Conectar o YouTube devolve
`402 PAYMENT_REQUIRED`. **Ele vai adicionar forma de pagamento e chamar de
volta.**

**O que já está resolvido:** os 12 vídeos **continuam hospedados na Zernio** e
respondem normalmente. Não precisa subir nada de novo. As URLs estão no
histórico da conversa de 10/out/2026 e seguem o padrão
`https://media.zernio.com/media/<id>_react-0NN.mp4`.

**A ordem quando ele voltar:**

1. `connect_get_connect_url` com `platform: youtube` e
   `profile_id: 6a95ae7c19812bc89ff900d5`.
2. ⚠ **Avisar para escolher a Conta de Marca** na tela do Google, não o Gmail
   pessoal. Escolhendo errado, o erro é `no_youtube_channel`. E não desmarcar
   nenhuma permissão, senão vem `missing_google_permissions`.
3. Reescrever as 12 legendas no formato do YouTube (ver abaixo).
4. Agendar com `posts_create_post`, reaproveitando as URLs já hospedadas.

### ⚠ As legendas precisam ser reescritas

As atuais fecham com "Siga @gilbertosenaoficial" e hashtags de Instagram, que
no YouTube ficam deslocadas. **O YouTube distribui por busca**, então o que
importa lá é outro:

- **Título** por vídeo. É obrigatório; sem ele, a Zernio usa a primeira linha
  da legenda, que não serve.
- **Descrição** com o contexto da obra, do intérprete e do ano.
- **Tags** no campo `tags`, não como hashtag no texto.

Ele ainda não respondeu se quer isso; **eu recomendei que sim.**

### ⚠ Content ID: avisar antes de qualquer expectativa de receita

São gravações de orquestra. No Instagram passam; **no YouTube o Content ID
identifica a gravação e o selo ou a emissora reivindica o vídeo.** Em geral o
vídeo fica no ar, mas **a monetização vai para o reivindicante**, e há casos
de bloqueio em alguns países.

Isso foi dito a ele em 11/out/2026, antes de ele decidir pagar o plano. Não é
impedimento: serve como vitrine. Só não serve como fonte de receita.

**Os vídeos virarão Shorts**, por serem verticais e com menos de 3 minutos.

---

## O que medir quando der

Com 19 publicações em 48 horas, dá para comparar de verdade:

- **React contra centralizado.** Qual formato prende mais nessa audiência.
- **Duração.** Os de 34 a 50 segundos contra os de 90 a 101.
- **Tema.** Piano solo, orquestra, voz, trilha de cinema, desenho animado.
- **Horário.** O lote 1 saiu de madrugada entre 22h49 e 1h47; o lote 2, da
  meia-noite às 6h. Nenhum dos dois em horário comercial.

A Zernio lê as métricas direto do Instagram (`analytics_*`) e tem uma função
que calcula o melhor horário com base no histórico da própria conta
(`analytics_get_best_time_to_post`). **É o próximo passo antes de montar
calendário de verdade**, para parar de chutar horário.
