# Guia visual — conteúdo do Gilberto Sena

> Visual dos posts do Gilberto. O que é fixo é a marca (logo, nome). Cor,
> tipografia e composição **não são mais fixas** — saem do assunto de cada
> peça. Decisão dele, 22/set/2026: ver seção abaixo.

## Marca (o que não muda)

- **Logo:** leão dourado com o "S" formado na juba
  (`identidade/logo-transparente-crop.png`, fundo transparente — usar
  livremente em qualquer fundo, claro ou escuro). Símbolo de força,
  liderança e autoridade.
- **Instagram:** [@gilbertosenaoficial](https://www.instagram.com/gilbertosenaoficial/)
  — **com UM L**, confirmado como o perfil oficial em 10/out/2026. É a conta
  conectada à Zernio e a que recebe as publicações. Existe um perfil antigo
  com dois L que **não** deve aparecer em peça nenhuma.
- **Nome/wordmark:** GILBERTO SENA
- A logo entra pequena, uma vez por peça (ex.: canto do slide de capa e do
  CTA final). Não precisa se repetir gritando em todo slide — marca boa não
  grita o tempo todo.

- **Logo do serviço Business Advisor & Consultant** (escolhida por ele em 12/nov/2026, a opção 3): medalha de cobre
  em 3D, com o leão polido no centro e "GILBERTO SENA" e "BUSINESS ADVISOR & CONSULTANT" gravados em volta, em
  Copperplate. Arquivos (transparente, fundo claro e fundo vinho) em
  `saidas/NEGOCIOS-E-MARCA/logo-3d-business-advisor-2026-11-12/`, começando por `opcao-3-`.

- **Papel timbrado de contrato e proposta** (decidido por ele em 12/nov/2026): a **logo dourada** (a medalha, opção 3)
  pequena no topo de cada página, com um fio fino embaixo; o **leão da opção 1 (aço), bem claro, como marca d'água** no
  centro; rodapé com nome, serviço, Grupo Sena, telefone, site e número da página. Arquivos prontos em
  `saidas/NEGOCIOS-E-MARCA/propostas-de-servicos/timbrado/` (`logo-cabecalho-dourada.png` e `marca-dagua-leao.png`).
  **No contrato 02 (Assessoria Contábil, Tributária e Financeira), ele pediu a logo do Grupo Sena** (12/nov/2026): a
  assinatura horizontal (`identidade/Grupo Sena - Assinatura Horizontal - Preta.png`), recortada em
  `timbrado/logo-cabecalho-grupo-sena.png`, com a mesma marca d'água do leão. O contrato 01 segue com a logo dourada.

## Direção visual — decidida peça por peça (desde 22/set/2026)

**Revogado:** a regra antiga deste guia, que fixava fundo grafite
(`#0F1419`) + destaque dourado (`#C9A227`) como "a cor do Gilberto" em todo
carrossel. Decisão dele, com estas palavras: **não quer mais nenhum padrão
de cor associado a ele** — quer mais originalidade. A logo já basta pra
peça ser dele; a identidade de cada peça vem do **assunto**, não da pessoa.

**Quem decide isso agora:** a skill `direcao-de-arte`
(`~/.agents/skills/direcao-de-arte/`). Antes de desenhar um carrossel/reels
novo, invocar essa skill — ela lê o assunto, propõe três direções visuais
diferentes (nunca repete uma direção usada nas últimas três peças, ver o
`historico.md` dela) e só monta depois de escolhida. Não voltar por
reflexo pra grafite+dourado "porque foi assim antes" — é exatamente esse
reflexo que a decisão de 22/set elimina.

**Exceção: série.** Peças de uma mesma série (ex.: os 5 G's, as aulas de "A Base da Gestão") saem **todas com o
mesmo visual**, escolhido uma vez no começo da série. Pedido dele em 18/out/2026, quando o 5 de 5 dos 5 G's estava
com fundo creme e os outros quatro escuros: *"refaça no mesmo padrão"*.

## O que continua valendo, porque não é sobre cor

- **Autoridade > enfeite.** Sério, premium, editorial — um homem de
  autoridade no mercado financeiro/jurídico falando com empresários, nunca
  post de coach/guru de dinheiro rápido.
- Sem clip-art, sem foto de banco de imagem genérica, sem emoji decorativo.
- Menos é mais. Se ficou com cara de template de IA, está errado — a skill
  `direcao-de-arte` tem um checklist específico pra isso
  (`referencias/tells.md`).

## Uso do logo nos posts

- Slide de capa e CTA final: leão dourado como elemento de marca (watermark
  sutil ou selo), tamanho pequeno a médio — não precisa dominar a tela.
- CTA final costuma fechar com @gilbertosenaoficial visível.
- Contador de slide / wordmark no rodapé ou topo são opcionais agora — a
  skill `direcao-de-arte` decide isso como parte da composição de cada
  direção, não como regra fixa de todo carrossel.

## Decisão consciente de 16/out/2026: a pele dos carrosséis e dos banners

A regra acima manda escolher a direção por peça, e **isso continua valendo**. Mas as peças feitas entre 14 e 16/out
repetem a mesma pele, e não é reflexo:

- **Carrosséis do Instagram:** quase-preto (`#0D0B0A`) com ouro (`#E3C06E`) e Inter, a "pele de 14/out". Foi escolhida
  para **retenção** (contraste alto na miniatura do feed, dois tons de escuro para dar ritmo, contador em ouro) e porque
  segura os 30 e poucos carrosséis da fila como uma série só.
- **Banners do livro, do nome e do Sena:** azul-noite e ouro, porque **a capa é arte que ele mesmo mandou** nesse estilo
  (banner do livro dos 5 Gs) e o resto precisa parecer a mesma peça. O validador `paleta.py` recusa azul-marinho com
  dourado; o banner do Sena usa a foto real dele sobre fundo azul-noite, na linha do banner que ele trouxe.
- **O que continua proibido:** voltar a esta combinação por padrão numa peça nova que não tenha esse motivo.
  Apresentação, media kit, ebook e site seguem escolhendo a direção pelo assunto (ex.: papel creme, petróleo e
  terracota na apresentação Reestruturando com Êxito).
