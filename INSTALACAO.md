# Instalação — checklist pro Cid (máquina do Gilberto)

> Passo a passo pra deixar o GilbertoOS rodando na máquina do Gilberto amanhã.
> Objetivo: ele abre, **fala por voz**, e o negócio funciona. Ele nunca vê terminal.

## 1. Levar a pasta

- Copiar a pasta `GilbertoOS/` inteira pra máquina dele (pendrive, OneDrive, drive).
- Local sugerido: Área de Trabalho dele.

## 2. Instalar o básico na máquina dele

- [ ] **VS Code** (se não tiver)
- [ ] **Node.js** (LTS) — necessário pros scripts (fichar PDF, renderizar carrossel)
- [ ] **Claude Code** (extensão/CLI) + login numa conta Claude (Pro/Max)
- [ ] **Wispr Flow** — a peça que mata o atrito. Ele fala, não digita.

## 3. Preparar os scripts (uma vez)

Abrir o terminal na pasta `GilbertoOS/scripts/` e rodar:

```
npm install
npx playwright install chromium
```

(Isto instala o extrator de PDF e o motor de render do carrossel. Só precisa
uma vez.)

## 4. Abrir no Claude Code

- Abrir a pasta `GilbertoOS/` no VS Code / Claude Code.
- O `CLAUDE.md` carrega sozinho — o agente já vira "extensão do Gilberto".

## 5. Alimentar o conhecimento

- Largar os PDFs/livros em `dados/biblioteca/`.
- Pedir ao Claude: **"ficha os PDFs da biblioteca"** → ele resume em
  `conhecimento/` e registra no índice.

## 6. Capturar a alma (na reunião)

- Gravar a conversa com o Gilberto (Wispr Flow ou gravador).
- Focar em: **história** (palavras dele) + **opiniões contrárias** + jeito de falar.
- Depois, jogar a transcrição pro Claude preencher `_memoria/quem-e-gilberto.md`
  e `_memoria/posicionamento.md`.

## 7. Primeiro teste na frente dele

- Pedir `/ideias` → mostrar pautas na cara dele.
- Escolher uma → `/carrossel` ou `/reels` → ele vê saindo conteúdo na hora.
- **É esse momento que vende o projeto.**

## 8. Levar no celular (sincronia notebook ↔ iPhone)

A memória do Gilberto tem que ser a mesma no computador e no celular. O elo é
o **GitHub** (o Claude Code no celular roda na nuvem, ligado a um repositório —
não sincroniza a pasta local direto).

- [ ] A pasta já é um **repositório git** (feito). Falta subir pro GitHub:
      abrir o Claude Code na pasta e falar **"salvar"** → ele cria/liga o repo
      **privado** e dá push. (Ou manual: criar repo privado em github.com/new
      e `git remote add origin <URL>` + `git push -u origin main`.)
- [ ] No **iPhone** do Gilberto: instalar o **app do Claude** (iOS 15+), logar
      na mesma conta Pro/Max, abrir o **Claude Code / Cowork** e **conectar o
      repositório do GilbertoOS** (via GitHub OAuth).
- [ ] Instalar o **Wispr Flow no celular** pra ele falar em vez de digitar.

Como fica o fluxo:
- **Notebook:** trabalha na pasta → ao terminar, "salvar" (puxa + commit + push).
- **Celular:** insight de madrugada → fala → o Claude guarda como commit no repo.
- Regra: **sempre puxa antes de subir** (o `/salvar` já faz isso), pra os dois
  aparelhos ficarem iguais.

**Requisitos:** conta Claude Pro/Max, conta GitHub, iOS 15+.

## Ensinar o Gilberto (30 segundos)

Só isto: abrir a pasta no Claude Code, apertar o atalho do Wispr Flow, e falar.
Os comandos: **conversar, carrossel, reels, ideias** — e **salvar** quando
terminar (mas ele já salva sozinho). Ver `LEIA-PRIMEIRO.md`.
