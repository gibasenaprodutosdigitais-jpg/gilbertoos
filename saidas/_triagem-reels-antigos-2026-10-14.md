# Reels antigos do Drive: o que dá pra postar

> Levantado em **14/out/2026**. Pasta de origem no Drive: *Gilberto Reels antigos*.
> **Nada foi agendado ainda.** Os aprovados já estão cortados e tratados em
> `saidas/reels-antigos-amostra-2026-10-14/aprovados/`.

---

## Os números que você pediu

| | |
|---|---|
| Reels na pasta do Drive | **198** |
| Já postados (detectados por tamanho do arquivo) | 23 |
| Nunca postados | 175 |
| Recorte que eu revisei (só 2026, sua escolha) | **50** |
| **Aprovados, cortados e com texto pronto** | **7** |
| Esperando uma confirmação sua | 1 |
| Liberados por você em 14/out | e-commerce, com o 9,9% na fala |
| Declinados | 42 |

Dos 42 declinados, **1 tem roteiro bom demais pra jogar fora** e entra como
regravação.

E os carrosséis, do levantamento de ontem: **38 existem, 31 estão prontos**
(ver `_inventario-carrosseis-2026-10-14.md`). Todos já com a pele nova.

---

## Por que 42 de 50 caíram

Quando eu abri os vídeos um por um, apareceu um padrão que a transcrição
sozinha não mostra. **A maior parte do seu 2026 não é você falando. São
reacts.** Clipe de outra pessoa em cima, você comentando embaixo.

Contei: **16 são reacts** sobre Wolf of Wall Street, Silvio Santos, Elon Musk,
Tony Robbins, Michael Caine, o filme do McDonald's, Tom e Jerry.

Isso não serve pra republicar, por três motivos:

1. **O material central não é seu.** Repostar filme e programa de TV em escala
   é pedir strike de direitos autorais nas duas contas.
2. **O valor do post era o clipe, não você.** Quem salvou, salvou pelo trecho
   do filme.
3. **Contraria o seu próprio posicionamento.** Qualquer contador reposta Wolf
   of Wall Street. Isso é exatamente o genérico do qual você quer distância.

O segundo grupo que caiu: **13 arquivos que não são reels.** São cards
estáticos, citações e flyers de evento, a maioria sem nenhuma faixa de áudio,
de 4 a 23 segundos. O Drive guardou como vídeo, mas é imagem.

O terceiro: **4 peças com o banner "17/09 Alphaville" queimado no quadro.**
Não é overlay que eu removo, está gravado no vídeo, do primeiro ao último
frame. Anuncia um evento que já passou.

---

## Os 7 aprovados

Já cortados, com áudio normalizado em -14 LUFS, padronizados em 1080x1920 e
com a taxa limitada pra subirem rápido na sua internet. Texto pronto pra
Instagram, YouTube e TikTok em `aprovados/textos.json`.

| # | Nome / assunto | Tempo | O que eu fiz |
|---|---|---|---|
| 01 | **Transportadora: CT-e tem que destacar CBS e IBS** | 70s | nada, estava pronto |
| 02 | **E-commerce: split payment e a compra acima de 50 dólares** | 67s | nada, estava pronto |
| 03 | **O sucesso dos maus é o silêncio dos bons** | 78s | cortei de 2m45 pra 1m18, fechando na frase do René Silva |
| 04 | **O fim do IPI é escudo da Zona Franca de Manaus** | 18s | cortei antes do banner do evento e apaguei o botão "inscrição no link da bio" |
| 05 | **Automanipulação: o empresário que acredita no próprio Instagram** | 66s | cortei o convite do evento de 27/ago |
| 06 | **Em 2027 não cai um imposto novo, cai o sistema inteiro** | 35s | cortei o card do evento no fim |
| 07 | **Nem toda queda é calvície: o diagnóstico errado** | 75s | cortei o convite da Regenera no fim |

**O mais forte do grupo é o 03.** É o único em que você assume uma briga com
nome e sobrenome, e é a sua tese de posicionamento inteira em 78 segundos.

**O 04 é o mais curto e provavelmente o que mais roda.** 18 segundos, uma
informação técnica fechada, sem CTA.

### ✅ 14/out: o 08 saiu, a pedido dele

*"o reels número 8 reflexão pode tirar pois o bom domingo a todos já passou o
contexto"*. Ele tem razão: o vídeo abre com "pessoal, bom domingo a todos", o
que prende a peça a um dia da semana e a uma data. Arquivo e texto removidos.

### ✅ 14/out: os 7 foram tratados de imagem e som

Ele pediu primeiro para 1, 5 e 6, depois mandou rodar nos outros. Todos vinham
em VP9 com taxa muito baixa, o 01 em **702 kbps a 1080x1920**, e áudio entre
**47 e 77 kbps**.

| | Vídeo antes | Vídeo depois | Áudio antes | Áudio depois |
|---|---|---|---|---|
| 01 transportadora | 702 kbps | 2.624 kbps | 50 kbps | 192 kbps |
| 02 e-commerce | 849 kbps | 2.755 kbps | 56 kbps | 192 kbps |
| 03 silêncio dos bons | 910 kbps | 3.480 kbps | 70 kbps | 193 kbps |
| 04 fim do IPI | 790 kbps | 2.166 kbps | 77 kbps | 192 kbps |
| 05 automanipulação | 1.160 kbps | 5.048 kbps | 65 kbps | 194 kbps |
| 06 cai o sistema | 1.434 kbps | 5.044 kbps | 47 kbps | 191 kbps |
| 07 diagnóstico errado | 1.304 kbps | 4.670 kbps | 53 kbps | 192 kbps |

**Ruído de fundo:** o 01 caiu de −27 para −34 dB, e o 05 de −22 para −32 dB.
Os outros já eram limpos.

**Imagem:** remoção de ruído de compressão, correção de banding nos degradês,
nitidez adaptativa e um leve ganho de contraste e cor. O 05 era **576x1024** e
subiu pra 1080x1920.

**Som:** corte de graves de sala, redução de ruído por FFT, controle de
sibilância, compressão leve e nivelamento em dois passos. **Os sete fecharam
em −14,0 LUFS exatos**, que é o alvo do Instagram.

⚠ **Um erro meu, pego e corrigido.** No 04 eu tinha apagado por filtro o botão
"inscrição no link da bio", mas deixei o filtro ligado no vídeo inteiro. Ele
estava comendo a última linha de texto de dois cards anteriores. O botão só
entra aos 15,9s, então o filtro agora liga só a partir dali. **Só vi isso
olhando o quadro.**

**A prova de que a limpeza não comeu a fala:** transcrevi de novo o áudio
tratado e comparei. No 05, o trecho que o Whisper errava antes ("tem empresa
dela que está num patamar") agora sai certo: "acredita que ela está em um
patamar de segurança". O som ficou mais limpo e mais inteligível, não mais
abafado.

---

## 2 pra você regravar

**"Ninguém quer estar num ônibus que vai pra esquina, quer estar num foguete
que vai pra lua."** (09/set, sobre contratar e reter gente boa)

É o melhor roteiro de gestão dos 50. O vídeo é inaproveitável porque o banner
do 17/09 ocupa o terço central de todos os quadros. Mas o texto não tem
nenhuma referência de data. Regrava em 60 segundos e vira um dos melhores
reels do perfil.

**"Teoria sem prática não vale nada, doutor Eurico."** (26/ago, sua resposta ao
professor da FGV que disse que o empresário deveria economizar acabando com os
tributaristas). É a sua melhor peça de autoridade do ano e está presa num
vídeo de 3 minutos em baixa resolução com convite de evento no fim. Cortada
pra 70 segundos, vira outra coisa.

Os dois roteiros estão em `aprovados/regravar.md`, já enxugados pro tempo de
Reels.

---

## ✅ Decidido em 14/out: o e-commerce vai inteiro

Você disse: *"o e-commerce continua e o 9,9 pode deixar a fala"*. **O reel sobe
com o número no áudio.** A legenda segue sem percentual, porque você autorizou
a fala e não pediu o número escrito.

Se alguém puxar o assunto nos comentários, a referência do repositório é CBS
de 8,8%, IBS de 17,7% e total perto de 26,5%, com a alíquota final ainda em
aberto.

## Uma coisa ainda esperando você

**O reel do "fundo do poço".** Tem um de 14/set em que você conta ter
dormido em abrigos e carregado seu filho pela mão enquanto segurava a
esperança. Essa é, palavra por palavra, a história do Chris Gardner, do filme
À Procura da Felicidade. **Eu não aprovei esse.** Se for a sua história de
verdade, eu aprovo na hora e ela vira conteúdo forte. Se for narração do
filme, publicar na sua voz te cria um problema que você não precisa.

---

## Os 42 declinados, por motivo

**Reacts a material de terceiro (16):** Wolf of Wall Street · Silvio Santos ·
Elon Musk sobre dinheiro · Tony Robbins · Michael Caine · o filme do McDonald's ·
Tom e Jerry · cena de luta · monge · samurais · "perde um pouco" · Johnny
Walker · notícia do PT · metáfora da água · "a coisa difícil e a coisa certa" ·
"quem perde o caráter perde tudo"

**Banner do 17/09 queimado no quadro (4):** ônibus ou foguete *(vai pra
regravação)* · simples ou lucro presumido · sua resposta ao Eurico Santi da
FGV · independência no 7 de setembro

A do Eurico Santi dói deixar de fora. São 3 minutos bons, você defendendo a
classe inteira dos tributaristas contra um professor da FGV. Mas são 3
minutos, em 576x1024, e o último terço é convite do evento. **Esse também vale
regravar**, mais curto.

**Card, citação ou flyer, não é reel (13):** PIS/Cofins malha fiscal · Ativo x
Passivo · Simples puro ou híbrido · Saúde = Gestão · "o IPI não morreu" ·
"uma decisão pode mudar tudo" · "fui forjado pelos momentos que passei" ·
"o dinheiro nunca foi só uma ferramenta" · dois flyers do Clube Êxito ·
três cards sem fala

**Série de viagem da Nova Zelândia (4):** Waitomo e vilarejo hobbit · Mount
Cook · duas de estrada. Todas com chamada da agência de turismo no fim.

**Motivacional genérico, sem nada seu (3):** "um sábio disse" · clipe musical ·
ilustração do leão

**Assunto vencido (1):** Simples Híbrido com a janela de setembro, que fechou
em 30/set

---

## O que eu recomendo

Esses 8 **não formam uma grade**, formam um reforço. Você já tem 40 posts de
vídeo agendados até 24/out e 31 carrosséis esperando fila.

Encaixa os 8 como respiro entre os carrosséis a partir de 21/out, um por
semana. Assim eles não competem com o material novo e cada um pega um público
diferente.

E a lição que vale mais que os 8: **em 2026 você produziu muito mais react do
que conteúdo próprio.** Os reels que sobreviveram à peneira são todos os que
você gravou sozinho, falando do que sabe. É onde está o seu diferencial, e é o
que o acervo prova.
