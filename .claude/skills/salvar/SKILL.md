---
name: salvar
description: >
  Guarda e sincroniza o GilbertoOS no GitHub (puxa o que veio do celular +
  commit + push). É o que faz a memória do Gilberto ser a mesma no notebook e
  no celular. Use quando ele disser "salvar", "guarda isso", "sincroniza",
  "/salvar", "backup", ou ao fim de uma sessão que mudou memória/gerou conteúdo.
---

# /salvar — guardar e sincronizar

Uma função só: garantir que tudo do Gilberto está no GitHub e que o notebook e
o celular estão com **a mesma memória**. Feito pra quem nunca usou git — falar
simples, sem termo técnico.

## Regra de ouro da sincronia (por que é diferente)

O Gilberto usa isto no **notebook** e no **celular** (Claude Code no app do
iPhone, ligado ao mesmo repositório). Então **sempre puxar antes de subir** —
senão o que ele falou de madrugada no celular não aparece no computador.

Ordem certa: **`git pull --rebase` → `git add .` → `git commit` → `git push`.**

## Workflow

### Primeira vez (repositório ainda não ligado ao GitHub)

Detectar com `git remote get-url origin`. Se não houver remoto:

1. Dizer simples:
   > "Vou ligar o teu sistema ao GitHub — é o cofre que sincroniza o notebook
   > com o celular. Você já tem um repositório criado, ou crio agora?"
2. **Se já tem URL:** `git init` (se preciso), `git add .`,
   `git commit -m "Setup inicial do GilbertoOS"`, `git branch -M main`,
   `git remote add origin <URL>`, `git push -u origin main`.
3. **Se não tem:** checar `gh --version`.
   - Tem `gh`: `git init`, commit inicial, `gh repo create gilbertoos --private --source=. --push`.
   - Não tem: instruir a instalar o `gh` (https://cli.github.com/) ou criar o
     repo **privado** em github.com/new e voltar com a URL.

   > Sempre **privado** — é a cabeça e a memória do Gilberto.

### Salvamentos seguintes (já ligado)

1. **Puxar primeiro:** `git pull --rebase origin main`.
   - Se vier mudança do celular, avisar simples: "Puxei o que você guardou no
     celular." Se der conflito, resolver com bom senso (preferir manter as duas
     contribuições) e avisar; nunca descartar trabalho dele sem falar.
2. `git status`. Sem mudança local nova → "Já está tudo sincronizado." e parar.
3. `git add .` → `git commit -m "<mensagem>"`. Gerar a mensagem sozinho a partir
   do que mudou (1 linha: "Adiciona reflexão sobre X", "Cria carrossel sobre Y",
   "Atualiza a memória do Gilberto"). Não obrigar o Gilberto a escrever nada.
4. `git push`.
5. Confirmar humano: "Guardado e sincronizado. Já está no notebook e no celular."

## Regras

- **Sempre pull antes de push** (sincronia de duas mãos — celular ↔ notebook).
- Repositório **privado**, sempre.
- Nunca `--force`, `reset --hard` ou destrutivo sem o Gilberto pedir e confirmar.
- Se o push falhar por divergência, puxar com `--rebase` e tentar de novo; se
  travar, explicar em linguagem humana, sem jargão.
- Configurar `user.name`/`user.email` no `git config --global` na primeira vez
  se não estiverem setados.
- Nunca subir `node_modules/`, `.env` ou segredos (o `.gitignore` cuida disso).
