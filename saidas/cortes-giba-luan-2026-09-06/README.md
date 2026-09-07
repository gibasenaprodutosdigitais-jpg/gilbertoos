# Cortes — Podcast "Giba e Luan" (GibaCast)

**Data:** 06/set/2026
**Fonte:** 3 episódios do Drive (Meu Drive/Pod GibaCast/Giba e Luan) — baixados em `fonte/` (não versionado).
**Formato de saída:** 1080x1920 (9:16) · 30fps · legenda karaokê queimada · cartela de gancho 1,6s.

Gilberto é o convidado. Ep. 1 e Ep. 3 são câmera única travada nele — os 6 cortes saíram só desses dois (o Ep. 2 tem corte de câmera que mostra quem escuta, não dava pra fechar no rosto dele).

## Os 6 cortes (`cortes/`)

| # | Arquivo | Gancho | Duração |
|---|---|---|---|
| 1 | `corte-1-golpe-ia.mp4` | CAÍ NUM GOLPE feito por IA | 34s |
| 2 | `corte-2-7-piramides.mp4` | CAÍ EM 7 PIRÂMIDES e nunca arrastei ninguém | 26s |
| 3 | `corte-3-acharam-golpe.mp4` | ACHARAM QUE ERA GOLPE (cabana temática) | 31s |
| 4 | `corte-4-quero-20-mil.mp4` | "QUERO 20 MIL" — tá, e o que você entrega? | 31s |
| 5 | `corte-5-engolia-o-u2.mp4` | SE FOSSEM 4 IGUAIS A MIM eu engolia o U2 | 31s |
| 6 | `corte-6-patrao-enriquece.mp4` | Todo funcionário pensa: "o patrão enriquece às minhas costas" | 30s |

Legendas prontas pra postar em `legenda.md`.

## Como foi feito
- Transcrição local (faster-whisper large-v3), corte por fronteira de palavra, fades de 30ms nas emendas.
- Legenda karaokê renderizada em PIL (este ffmpeg não tem libass/drawtext) e composta por cima; palavra falada em dourado.
- Script: `edit/build_cortes.py` (config dos 6 cortes, segmentos, ganchos e correções de transcrição no topo do arquivo).
- Re-render de um corte: `<video-use venv python> edit/build_cortes.py <1..6>`.

`fonte/`, `edit/work/`, `edit/tx/`, `edit/verify/` e os `.json` de transcrição não são versionados (pesados / regeneráveis).
