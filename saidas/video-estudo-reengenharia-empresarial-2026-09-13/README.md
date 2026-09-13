# Vídeo de estudo — Reengenharia Empresarial (mapa executivo do evento)

**Data:** 2026-09-13
**Fonte:** `evento Gilberto para validação dia 27-08 .pdf` (Downloads)
**Formato:** 1920×1080 (16:9) · 30fps · ~10 min · locução (voz do sistema, sem trilha)

## Entregável
- `Estudo - Reengenharia Empresarial (mapa executivo).mp4`

## Para que serve
Material de **ensaio pessoal**, não de postagem. Narra, na ordem, o mapa executivo
inteiro do evento de validação (27/08): objetivo de cada bloco, tese de cada
tópico, a técnica psicológica por trás, e as frases-chave que você planejou
dizer — pra você internalizar o fluxo antes do dia.

## Estrutura (21 cenas)
1. Abertura + visão geral do dia
2. **Bloco 1** (09h–12h30) — 5 tópicos + resumo do fluxo emocional
3. **Bloco 2** (14h–16h30) — 4 tópicos + resumo do fluxo emocional
4. **Pitch da mentoria** (16h30–17h15)
5. **Bloco 3** (18h–19h30) — 3 tópicos
6. Checklist final de preparo (3 pontos ainda em aberto no seu mapa, mais um
   lembrete pra ensaiar as frases-chave em voz alta)

## Nota de conteúdo
As passagens do PDF que eram anotações soltas de voz (o framework de PNL, a
dinâmica do celular, o apadrinhamento e os 5 porquês, a demo da ferramenta
OCEO, o gancho do clube empresarial) foram limpas e incorporadas nos tópicos
certos — não foram descartadas.

Um ponto de atenção que acrescentei no checklist: se a demonstração ao vivo da
ferramenta OCEO (Tópico 3, Bloco 2) usar dado real de um participante da
plateia, vale confirmar autorização dele antes, ou usar um exemplo fictício em
ordem de grandeza parecida.

## Regerar
```
python3 build.py                                    # TTS + timeline.json + video.html + mux.sh
NODE_PATH="../../scripts/node_modules" node render-frames.js
bash mux.sh
```
`frames/` e `audio/*.wav` não são versionados (recriados pelo pipeline acima).

## Trocar a voz
Em `build.py`, `VOICE` (`say -v '?'` lista as PT-BR) e `RATE`.
