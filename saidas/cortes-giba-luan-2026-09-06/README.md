# Cortes — Podcast "Giba e Luan" (GibaCast)

**Data:** 06/set/2026
**Fonte:** 3 episódios do Drive (Meu Drive/Pod GibaCast/Giba e Luan) — baixados em `fonte/` (não versionado).
**Formato de saída:** 1080x1920 (9:16) · 30fps · legenda karaokê queimada · cartela de gancho 1,6s.

Gilberto é o convidado. **Os 3 episódios são multicam** (corta pra quem escuta), então cada janela precisou ser verificada frame a frame pra garantir que a câmera fica nele. Os cortes 3 e 6 (originais) foram descartados por mostrarem muito o Luan e substituídos pelas sacadas 7 e 8, montadas em janelas onde a câmera fica travada no Gilberto.

## Os 6 cortes (`cortes/`)

| # | Arquivo | Gancho | Duração |
|---|---|---|---|
| 1 | `corte-1-golpe-ia.mp4` | CAÍ NUM GOLPE feito por IA | 34s |
| 2 | `corte-2-7-piramides.mp4` | CAÍ EM 7 PIRÂMIDES e nunca arrastei ninguém | 26s |
| 4 | `corte-4-quero-20-mil.mp4` | "QUERO 20 MIL" — tá, e o que você entrega? | 31s |
| 5 | `corte-5-engolia-o-u2.mp4` | SE FOSSEM 4 IGUAIS A MIM eu engolia o U2 | 31s |
| 7 | `corte-7-sacada-40-certificacoes.mp4` | 40 CERTIFICAÇÕES e 7 vezes quebrado | 15s |
| 8 | `corte-8-sacada-certo-e-errado.mp4` | NÃO EXISTE CERTO E ERRADO | 11s |

Sacadas 7 e 8 são cortes curtos, só com a fala do Gilberto (janela verificada como câmera nele o tempo todo).

Legendas prontas pra postar em `legenda.md`.

## Como foi feito
- Transcrição local (faster-whisper large-v3), corte por fronteira de palavra, fades de 30ms nas emendas.
- Legenda karaokê renderizada em PIL (este ffmpeg não tem libass/drawtext) e composta por cima; palavra falada em dourado.
- Script: `edit/build_cortes.py` (config dos 6 cortes, segmentos, ganchos e correções de transcrição no topo do arquivo).
- Re-render de um corte: `<video-use venv python> edit/build_cortes.py <1..6>`.

`fonte/`, `edit/work/`, `edit/tx/`, `edit/verify/` e os `.json` de transcrição não são versionados (pesados / regeneráveis).
