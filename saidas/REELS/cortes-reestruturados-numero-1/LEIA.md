# Cortes reestruturados nº 1 (12/nov/2026)

Pedido dele: pegar todos os cortes que já foram ao ar e refazer, mudando fonte, cor, texto (copy), velocidade e todos os
metadados do arquivo, para agendar de novo no futuro.

## O que já foi ao ar (levantado na Zernio em 12/nov: 275 posts publicados)

110 cortes dele, sem contar os 19 reacts de música clássica (não são fala dele) e as 8 aulas longas de A Base da Gestão.

| Grupo | Quantos | Pasta | Tem a gravação original? |
|---|---|---|---|
| Gravações do carro (v2-c01 a c26) | 26 | `reels-gravacoes-do-carro-2026-10-30` | **Sim** (`entrada-videos/longos/`): dá pra trocar tudo, até a fonte da legenda |
| Assessoria AME (16 reels) | 16 | `sb/AME/divulgacao/reels-sem-imersao-2026-11-08` | Não: legenda e título vêm gravados na imagem |
| 12 novos, lotes 2, 3 e 4 (editados por terceiros) | 29 | `reels-novos`, `reels-lote-2/3/4` | Não: vieram editados, com legenda na imagem |
| Antigos do Instagram e YouTube (10 a 14/out) | 17 | `reels-antigos-amostra-2026-10-14` | Não |
| 7 pecados + bônus, gravações longas 01 a 07 | 18 | `reels-gravacoes-longas-2026-10-14` | A conferir |
| Direita e esquerda (2), nome e sobrenome Sena (2) | 4 | | A conferir |

## O visual nº 1 (testado no c02)

- Velocidade **1,22x**, com a voz no mesmo tom (era 1,08x, depois 1,15x; ele pediu mais rápido duas vezes em 12/nov).
- Cor mais quente e com mais contraste, vinheta leve, enquadramento mais fechado.
- Legenda em **Futura**, maiúsculas e minúsculas, numa faixa escura, com a palavra falada em **dourado** (antes: DIN
  Condensed, tudo em caixa alta, branca com contorno preto).
- **Chamada nova fixa no topo**, com um traço dourado embaixo.
- Arquivo novo por dentro: nenhum metadado do original, data de criação nova, outra codificação, áudio em 44,1 kHz.
- Título, legenda e tags novos, tirados do que ele falou no vídeo (`copys.json`; o campo `era` guarda o título antigo e
  o ID do post que saiu).

## Ajustes pedidos por ele em 12/nov (depois dos testes)

- **Capa** no começo do vídeo (1,4 s): faixa de **60% da tela no meio, cobrindo o rosto**, com a headline grande e
  "GILBERTO SENA" em cima; depois ela some e fica o título pequeno no topo. A mesma imagem sai em `capas/` (jpg) pra
  ir como capa do post. No `copys.json`, o campo `capa` aceita `*palavra*` (cor de destaque) e `|` (quebra de linha).
- **Legenda abaixo do rosto** (a 77% da altura), escondida enquanto a capa está na tela.
- **Cada corte com uma combinação própria de fundo e letra**, em rodízio de 8: grafite e dourado, marinho e amarelo,
  vinho e champanhe, verde-escuro e limão, creme e preto, roxo e laranja, amarelo e preto (destaque em vermelho-escuro), petróleo e coral. Vale pra
  capa, faixa da legenda e destaque.
- **Efeitos pelo sentido da fala** e **cor de base pelo assunto** (campo `clima`: tenso, dinheiro, inspirador ou neutro).

## Efeitos

| Quando ele fala | O efeito |
|---|---|
| medo, quebrar, falência, crise, risco, prejuízo | tremor de câmera, imagem sem cor e avermelhada, bordas escuras, falha de imagem; palavra em vermelho (no máximo 3 por vídeo) |
| erro, problema, culpa, golpe | pulso vermelho curto nas bordas; palavra em vermelho |
| dinheiro, lucro, caixa, imposto, faturamento | brilho dourado rápido |
| ajuda, solução, caminho, crescer, resultado | a imagem abre e clareia |
| Deus, Provérbios, sabedoria, Jesus | luz quente e suave, mais longa |
| nunca, ninguém, tudo, verdade, cuidado | zoom rápido |
| um número ("20, 30, 40 mil", "600 reais") | o número aparece grande, num selo acima da legenda |
| emenda de dois trechos | flash branco |

Além disso: aproximação lenta do começo ao fim, e um zoom de ritmo onde passar de 4 s sem efeito.

Motor: `ferramenta/reestruturar.py` (usa a receita de corte de `reels-gravacoes-do-carro-2026-10-30/ferramenta/`).
Os vídeos ficam em `videos/`, fora do GitHub (só no notebook). A conversão de cor das gravações do iPhone fica no
scratchpad da sessão; se sumir, refazer com `avconvert` (ver a memória do vídeo HDR do iPhone).

## Situação (12/nov)

- ✅ **107 prontos** em `videos/`, com a capa de cada um em `capas/`: os 26 do carro (motor `ferramenta/reestruturar.py`)
  e os 81 publicados de outros lotes (motor `ferramenta/reestruturar_publicado.py`; como a legenda antiga vem gravada
  na imagem, a capa é opaca do topo até 90% da altura e não entra legenda nova). Textos novos em `copys.json` (carro) e
  `copys-publicados.json` (os 81). Os 3 que estavam repetidos no YouTube entraram uma vez só.
- **Amarelo e preto:** o destaque branco sumia no fundo amarelo; passou a vermelho-escuro. Os 13 cortes dessa
  combinação (3 do carro e 10 publicados) foram refeitos em 12/nov.
- ⚠ **8 marcados `segurar`** em `copys-publicados.json`: falam de alíquota da CBS (~9%), "sem alíquota publicada", prazo
  do Simples híbrido ou CT-e "desde janeiro". Conferir na fonte antes de agendar (regra "nada com data depois da data").
- Os 19 reacts de música e as 8 aulas de A Base da Gestão ficaram fora (não são corte de fala dele); confirmar com ele.
- **Agendado até agora:** só o AME-13 ("Tamanho único não serve em ninguém"), que substituiu o vídeo do reel de 15/11
  às 15h. Os outros 106 esperam ele decidir as datas.
