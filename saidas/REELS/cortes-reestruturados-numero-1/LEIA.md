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

- Velocidade **1,08x**, com a voz no mesmo tom.
- Cor mais quente e com mais contraste, vinheta leve, enquadramento mais fechado.
- Legenda em **Futura**, maiúsculas e minúsculas, numa faixa escura, com a palavra falada em **dourado** (antes: DIN
  Condensed, tudo em caixa alta, branca com contorno preto).
- **Chamada nova fixa no topo**, com um traço dourado embaixo.
- Arquivo novo por dentro: nenhum metadado do original, data de criação nova, outra codificação, áudio em 44,1 kHz.
- Título, legenda e tags novos, tirados do que ele falou no vídeo (`copys.json`; o campo `era` guarda o título antigo e
  o ID do post que saiu).

## Efeitos (pedido dele em 12/nov, depois de ver o teste: "acrescentar efeitos como zoom, um efeito de medo, entre outros")

- **Zoom:** aproximação lenta do começo ao fim e um zoom rápido (entra e volta) nas palavras fortes; onde passar de 4 s
  sem nada, um zoom de ritmo no começo da frase.
- **Medo** (medo, paralisar, quebrar, falência, risco, crise, prejuízo...): tremor de câmera, imagem dessaturada e
  avermelhada, vinheta escura e um "glitch" de cor no começo; a palavra acende em **vermelho** na legenda. No máximo
  3 por vídeo, com 3 s de folga; as outras vezes viram zoom simples.
- **Dinheiro** (dinheiro, lucro, caixa, imposto, faturamento, milhões...): brilho dourado rápido.
- **Flash branco** nas emendas, quando o corte junta dois trechos.
- O título do topo quebra em duas linhas equilibradas, de preferência depois de ponto ou vírgula.

Motor: `ferramenta/reestruturar.py` (usa a receita de corte de `reels-gravacoes-do-carro-2026-10-30/ferramenta/`).
Os vídeos ficam em `videos/`, fora do GitHub (só no notebook). A conversão de cor das gravações do iPhone fica no
scratchpad da sessão; se sumir, refazer com `avconvert` (ver a memória do vídeo HDR do iPhone).

## Situação

- ✅ Testes com efeitos: `videos/r1-01-medo-ate-de-pedir-ajuda.mp4` (era "O medo está paralisando o empresário") e
  `videos/r1-02-o-dinheiro-na-conta-nao-e-seu.mp4` (era "Pagar imposto não é ruim. É bom"). Ele aprovou o visual sem
  efeitos em 12/nov ("ficou bom") e pediu os efeitos.
- ⏳ Falta ele aprovar os efeitos; depois, os outros 24 do carro e a decisão sobre os cortes sem gravação original.
- Nada agendado ainda.
