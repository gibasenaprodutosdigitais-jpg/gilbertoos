# Áudio-guia — Imersão Reengenharia Empresarial

**Data:** 2026-09-15
**Fonte:** os 3 PowerPoints finais de palco, baixados do Downloads:
`! Bloco Treinamento_Reengenharia_Empresarial-1.pptx` (Bloco 1, 27 slides),
`2 Bloco Treinamento_Reengenharia_Empresarial-2.pptx` (Bloco 2, 14 slides),
`3 Bloco Treinamento_Reengenharia_Empresarial-3.pptx` (Bloco 3, 10 slides)
**Formato:** MP3 · ~14 min · locução contínua (voz do sistema), sem trilha

## Entregável
- `Audio-guia - Imersao Reengenharia Empresarial.mp3`

## Para que serve
Ensaio pessoal em áudio — pra ouvir repetido (carro, caminhada) e fixar o
fluxo exato dos SEUS slides finais de palco: o que aparece na tela, o que
você fala (das notas do apresentador), e as frases de impacto na íntegra,
prontas pra sair da boca do jeito que estão escritas.

## Estrutura (17 blocos de narração)
1. Bloco 1 (manhã) — abertura + 5 tópicos (Sofisma do Faturamento →
   Armadilha de 2027 → Cegueira Operacional → 3 Ralos → Diagnóstico)
2. Bloco 2 (tarde) — 4 tópicos (Despertar da Tarde → Perguntas da
   Reengenharia/Canvas → Margem Oculta/demo → Faça Você Mesmo) + Pitch
3. Bloco 3 (noite) — 3 tópicos (Preço da Omissão → Cadeira Vazia →
   Aliança da Reengenharia) + fechamento
4. Encerramento — nota de coerência (ver abaixo)

## Nota de coerência entre os slides
Duas pequenas divergências entre os três arquivos que vale igualar antes
do dia 27 (o áudio já avisa no final):
- **"20 anos de estrada" vs "40 anos de estrada"** — aparece dos dois
  jeitos entre o Bloco 2 e o Bloco 3.
- **"10–18%" vs "10–25%" de vazamento** — as notas do Tópico 4 (Bloco 1)
  dizem 10–18%, mas o texto que aparece na tela do mesmo slide diz
  10–25%.

## Regerar
```
python3 build.py
```
`audio/*.wav` e `audio/_concat.txt` não são versionados (regeneráveis).

## Trocar a voz
Em `build.py`, `VOICE` (`say -v '?'` lista as PT-BR) e `RATE`.
