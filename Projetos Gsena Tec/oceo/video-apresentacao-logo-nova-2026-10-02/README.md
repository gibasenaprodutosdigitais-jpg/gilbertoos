# OCEO: vídeo de apresentação com a marca escolhida

**Data:** 02/out/2026 · 1920x1080 · 70,6s

O vídeo de apresentação original, com a marca provisória trocada pela
escolhida (`identidade-visual/LOGO-OCEO.png`). **Nada mais mudou:** mesma
música, mesma sequência, mesmo texto, mesmas cores, mesma duração. O áudio
foi copiado bit a bit do original, sem recodificar.

## Como foi feito

Não dava pra reabrir o projeto do vídeo, que veio pronto em MP4. Então a
troca foi remendo no quadro: em cada momento onde a marca velha aparecia, uma
mancha escura esfumada apaga ela e a marca nova entra por cima, com um brilho
verde próprio pra não quebrar a linguagem da peça.

`remendos.py` gera as cinco imagens de remendo. Elas entram no vídeo assim:

| Remendo | Quando | O que troca |
|---|---|---|
| `p1` | 3,10s a 4,58s | o símbolo dentro da mira da abertura |
| `p2a` | 4,58s a 5,42s | o lockup enquanto a palavra antiga ainda está sendo digitada |
| `p2` | 5,42s a 6,23s | o lockup já parado, com o PRÉ-LANÇAMENTO intacto embaixo |
| `p3` | 11,07s a 12,47s | o símbolo ao lado de "Tudo em um lugar só." |
| `p4a` | 62,75s a 63,90s | o fechamento enquanto a marca antiga entra grande |
| `p4` | 63,90s a 70,60s | o fechamento parado, com assinatura e selo EM BREVE intactos |

Dois remendos por lockup porque a mancha precisa ser mais alta enquanto as
letras antigas estão caindo na tela, e mais baixa depois, pra não comer o
texto que entra embaixo.

## Comando

```
ffmpeg -y -i "Video de Apresentacao do OCEO.mp4" \
  -i remendos/p1.png -i remendos/p2a.png -i remendos/p2.png \
  -i remendos/p3.png -i remendos/p4a.png -i remendos/p4.png \
  -filter_complex "\
[0:v][1:v]overlay=0:0:enable='between(t,3.10,4.58)'[a];\
[a][2:v]overlay=0:0:enable='between(t,4.58,5.42)'[b];\
[b][3:v]overlay=0:0:enable='between(t,5.42,6.23)'[c];\
[c][4:v]overlay=0:0:enable='between(t,11.07,12.47)'[d];\
[d][5:v]overlay=0:0:enable='between(t,62.75,63.90)'[e];\
[e][6:v]overlay=0:0:enable='between(t,63.90,70.60)',format=yuv420p[v]" \
  -map "[v]" -map 0:a -c:v libx264 -crf 18 -preset medium -c:a copy \
  -movflags +faststart "OCEO - Video de Apresentacao (logo nova).mp4"
```

## O que não foi trocado

A marca velha continua aparecendo **em miniatura dentro das maquetes**: no
canto do painel de BI (12,5s a 15,7s), no cartão do Gilberto (por volta de
37s) e na grade de telas do fim (61s a 62,7s). Ali ela tem uns 30 pixels. A
marca nova, que é cromada e tem relevo, vira borrão nesse tamanho. Trocar
exigiria refazer as maquetes.

## Versão descartada

Existe também `video-apresentacao-2026-10-02/`, uma versão refeita do zero em
outra direção de arte. O Gilberto não quis: o pedido era o mesmo vídeo com a
marca nova, não um vídeo novo. Fica como registro.
