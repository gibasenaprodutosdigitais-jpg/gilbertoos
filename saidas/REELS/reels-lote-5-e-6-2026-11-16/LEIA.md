# Lotes 5 e 6 + grade de 5 posts por dia (agendado em 16/nov/2026)

Vieram dos zips "Cortes Editados - 5º lote - 05.11.2026" (vídeos 51 a 57) e "6º lote - 10.11.2026" (58 a 60), que ele
baixou do Drive em 16/11. Cada vídeo veio com um `.txt` de legenda escrito pela equipe (`legendas-que-vieram/`).
Transcrevi os 10 (faster-whisper local) e conferi cada legenda contra a fala. Todos são ele falando (quadros conferidos).

## O que foi feito nos 8 novos (51 a 57 e 59)

- Motor dos cortes já editados (`../cortes-reestruturados-numero-1/ferramenta/reestruturar_publicado.py`, agora com
  `REESTRUTURAR_BASE` e `REESTRUTURAR_SCR` pra gravar na pasta do lote): capa com a headline cobrindo o rosto (do topo
  a 90%, opaca), 1,22x, cor pelo assunto, efeitos pela fala, arquivo sem metadado. Textos em `copys.json`.
- **53: bip no "porra"** (75,9 s do original), regra da casa. A legenda da equipe já não tinha o palavrão.
- Legendas da equipe ajustadas: 51 tirou "Não é não pagar. É pagar o correto" (não dito) e voltou pra "você vai ouvir";
  59 tirou "um filósofo" (inaudível no vídeo). Chamada "Siga @... para mais conteúdos incríveis" trocada pela assinatura.
- Vídeos em `videos/` e capas em `capas/`, fora do GitHub (só no notebook).

## ⚠ Segurados, esperando a palavra dele

- **58 · o dia que bloquearam 1 milhão** (4 min 8 s): passa do limite de 3 min do Reels e do Shorts; ele fala duas vezes
  em "pensar em se matar" e cita a Deolane. A legenda da equipe já trazia o CVV 188. Não registrado na memória dele.
- **60 · deixa de ser fanfarrão e paga seu imposto**: tem a piada de "pôr mais dois peitos na mulher" e "virar ela de
  costas" e o fim "ela vai arrancar um pedaço de você". Risco de imagem pra quem fala com empresário e médico.

## A grade (decisão dele em 16/11)

YouTube e TikTok com 5 por dia, LinkedIn 1 por dia útil (ele aceitou a recomendação; pediu 5), X 5 por dia (pedido dele
no mesmo dia; cada post no X custa ~US$ 0,015 na Zernio, plano por uso).

| Rede | Horários (Brasília) |
|---|---|
| YouTube | 5h Provérbios e 9h frase (Shorts que já estavam), reels 10h, 16h e 19h |
| TikTok | 6h Provérbios, 9h frase, reels 12h e 15h, e 18h (AME até 24/11; depois reel) |
| X (`@gilbertosenaofc`) | 7h Provérbios, 10h frase, e os reels do YouTube 1 h depois (11h, 17h, 20h); texto curto |
| LinkedIn | 8h, dias úteis, os reels mais de negócio |
| Instagram | os 8 novos no reel das 12h de 4 a 11/12 (com a capa) |

Cada vídeo é **um post na Zernio com um horário por rede** (`plano-agendamento.json`, campo `zernio_id`). Provérbios e
frase no TikTok e X: `shorts-tiktok-x.json`. Ao mexer, lembrar a armadilha de mandar `platforms` incompleto.
Os 34 cortes reestruturados escolhidos saíram de `copys.json` e `copys-publicados.json` (fora: AME, os 8 `segurar`, os
7 pecados e direita/esquerda). O texto do c12 tinha "teu/tua/Olha" e virou "seu/sua/Olhe" (também na fonte).

| Vídeo | YouTube | TikTok | X | LinkedIn | Instagram | ID Zernio |
|---|---|---|---|---|---|---|
| g51 · O eco do vazio em 2027 | 17/11 10h | 26/11 18h | 17/11 11h | 17/11 8h | 04/12 12h | `6afb8ffacbd5727c04d3148a` |
| c02-o-medo-paralisa · Tem empresário com medo até de pedir ajuda | 17/11 16h | 27/11 12h | 17/11 17h | - | - | `6afb902e5af9080702079f5a` |
| g55 · Eu tinha aversão à tecnologia | 17/11 19h | 27/11 15h | 17/11 20h | 19/11 8h | 05/12 12h | `6afb9030604e65386a803cd9` |
| 2027-pode-quebrar · Da janela, eu vejo quem vai quebrar | 18/11 10h | 27/11 18h | 18/11 11h | - | - | `6afb903428ded1e3fb71dda4` |
| g52 · Vende pão e quer receber carne? | 18/11 16h | 28/11 12h | 18/11 17h | 20/11 8h | 06/12 12h | `6afb90365af9080702079f80` |
| 05-gestao-automanipulacao · Você está sendo manipulado. Por você | 18/11 19h | 28/11 15h | 18/11 20h | - | - | `6afb90395af9080702079fa3` |
| g54 · Gênios presos na lâmpada | 19/11 10h | 28/11 18h | 19/11 11h | - | 07/12 12h | `6afb903b5af9080702079fb3` |
| l2-14-vendedores-ilusao · Os vendedores de ilusão | 19/11 16h | 29/11 12h | 19/11 17h | - | - | `6afb903d604e65386a803d4e` |
| g57 · Você dá conta de entregar? | 19/11 19h | 29/11 15h | 19/11 20h | 23/11 8h | 08/12 12h | `6afb90795dc948cd4a5150c2` |
| l34-v24 · Nessa mesa, 90% quebraram | 20/11 10h | 29/11 18h | 20/11 11h | - | - | `6afb907d5dc948cd4a5150ec` |
| g53 · Os R$ 1.500 de janela | 20/11 16h | 30/11 12h | 20/11 17h | 18/11 8h | 09/12 12h | `6afb90805dc948cd4a51511b` |
| novo-01-quebrei-7-negocios · Eu quebrei 7 negócios | 20/11 19h | 30/11 15h | 20/11 20h | - | - | `6afb90835dc948cd4a515139` |
| g56 · O erro da Nike | 21/11 10h | 30/11 18h | 21/11 11h | 24/11 8h | 10/12 12h | `6afb9087f5ce185c20026ee8` |
| c10-pagar-imposto-e-bom · Caiu 40 mil na conta. Não é seu. | 21/11 16h | - | 21/11 17h | - | - | `6afb908bb955f4ef1ef9e934` |
| g59 · Não são gênios. São loucos. | 21/11 19h | - | 21/11 20h | - | 11/12 12h | `6afb908e5af908070207a082` |
| bitributacao-intercompany · O mesmo dinheiro tributado 4 vezes | 22/11 10h | - | 22/11 11h | - | - | `6afb90ba8d3a7676b16172c4` |
| 06-reforma-2027-cai-o-sistema · Em 2027 cai o sistema inteiro | 22/11 16h | - | 22/11 17h | - | - | `6afb90bce92afc0ec812613e` |
| l2-16-contador-guia · "Ele só manda a guia" | 22/11 19h | - | 22/11 20h | - | - | `6afb90beda1ee289509e039f` |
| l34-v37 · Nunca sobra dinheiro? Conta 1 | 23/11 10h | - | 23/11 11h | - | - | `6afb90c19d8babda3372c542` |
| novo-03-medo-de-reinvestir · O medo de reinvestir é um chip | 23/11 16h | - | 23/11 17h | - | - | `6afb90c3846775f814dea670` |
| c03-o-contador-nao-faz-sua-parte · O contador não vai fazer a sua parte | 23/11 19h | - | 23/11 20h | - | - | `6afb90c6846775f814dea681` |
| empresa-nao-quebra-por-si-so · Empresa não quebra sozinha | 24/11 10h | 17/11 12h | 24/11 11h | - | - | `6afb90c9f06fdc2ea1fbc131` |
| 07-gestao-diagnostico-errado · Remédio certo pro diagnóstico errado | 24/11 16h | 17/11 15h | 24/11 17h | - | - | `6afb90fdf06fdc2ea1fbc218` |
| l2-20-faturamento-ego · Faturamento é ego. Margem é o que fica | 24/11 19h | 18/11 12h | 24/11 20h | 26/11 8h | - | `6afb9100846775f814dea6e5` |
| l34-v39 · Aluguei um Tiguan por dois dias | 25/11 10h | 18/11 15h | 25/11 11h | - | - | `6afb9103f06fdc2ea1fbc23b` |
| novo-07-dobrar-equipe · Dobrar a equipe não dobra o lucro | 25/11 16h | 19/11 12h | 25/11 17h | 27/11 8h | - | `6afb9107da1ee289509e03e6` |
| c06-voce-ja-esta-quebrado · Você já está quebrado. Só não percebeu | 25/11 19h | 19/11 15h | 25/11 20h | - | - | `6afb9109da1ee289509e03f2` |
| empresario-nao-paga-imposto · Quem paga o imposto é o cliente | 26/11 10h | 20/11 12h | 26/11 11h | - | - | `6afb910bef6b519da2c52a99` |
| l2-18-quanto-maior · Quanto maior, maior o estrago | 26/11 16h | 20/11 15h | 26/11 17h | - | - | `6afb910d93b913bbd3db84f5` |
| novo-10-conta-bloqueada-folha · Conta bloqueada em 2 horas | 26/11 19h | 21/11 12h | 26/11 20h | - | - | `6afb9153a388c1a1f4fbc4f3` |
| c07-operacao-x-operacional · O padeiro e o dono da padaria | 27/11 10h | 21/11 15h | 27/11 11h | - | - | `6afb9155846775f814dea80b` |
| rico-x-pobre · A diferença do rico: paciência | 27/11 16h | 22/11 12h | 27/11 17h | - | - | `6afb9158da1ee289509e05be` |
| novo-11-socios-se-morrer · E se o seu sócio morrer? | 27/11 19h | 22/11 15h | 27/11 20h | 30/11 8h | - | `6afb915aa388c1a1f4fbc529` |
| c08-os-grandes-nao-quebram · Os grandes não quebram. Quem quebra é o pequeno | 28/11 10h | 23/11 12h | 28/11 11h | - | - | `6afb915da388c1a1f4fbc546` |
| c11-o-maior-cliente-sumiu · O maior cliente parou de pagar. Da noite pro dia | 28/11 16h | 23/11 15h | 28/11 17h | - | - | `6afb915fa388c1a1f4fbc554` |
| c12-era-collor · Eu vivi a era Collor. Crise passa | 28/11 19h | 24/11 12h | 28/11 20h | - | - | `6afb9161da1ee289509e05df` |
| c14-network-de-verdade · Network de verdade não é troca de cartão | 29/11 10h | 24/11 15h | 29/11 11h | - | - | `6afb9197a388c1a1f4fbc666` |
| c16-a-culpa-nao-e-do-governo · Não é o governo. É você | 29/11 16h | 25/11 12h | 29/11 17h | - | - | `6afb9199aaca9416200094c4` |
| c17-recuperacao-judicial · Recuperação judicial não é o fim | 29/11 19h | 25/11 15h | 29/11 20h | - | - | `6afb919aa388c1a1f4fbc68c` |
| c21-o-contador-de-600-reais · Fatura 300 mil e paga 600 reais de contador | 30/11 10h | 25/11 18h | 30/11 11h | 25/11 8h | - | `6afb919daaca9416200094d9` |
| c22-a-tabela-de-honorarios · Por que o seu contador cobra 300 reais | 30/11 16h | 26/11 12h | 30/11 17h | - | - | `6afb91a0a388c1a1f4fbc6ac` |
| c24-a-ia-nao-substitui-empatia · O robô que só sabe dizer bom dia | 30/11 19h | 26/11 15h | 30/11 20h | - | - | `6afb91a28b6d0410db321258` |