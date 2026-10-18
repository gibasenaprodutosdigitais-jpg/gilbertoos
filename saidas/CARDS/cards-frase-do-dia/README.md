# Série semanal: frase do dia

**Uma frase por dia, todos os dias, inclusive fim de semana** (desde 18/out/2026; antes era só segunda a sexta).
Nenhuma frase repete: conferir `ja-usadas.md` antes de montar.

Irmã da série de Provérbios: mesma paleta e a mesma faixa de ouro na lateral.
A composição é invertida de propósito, pra o seguidor reconhecer qual é qual
sem ler. **Na de Provérbios ele pensa, de lado. Aqui ele aponta pra quem lê, e
a frase vem por cima.**

## Como gerar

```
node render.js
```

Precisa de `NODE_PATH` apontando pra `scripts/node_modules`.

## A foto

`assets/foto.jpg`, já tratada: a figura foi recortada do topo da cabeça até
abaixo das mãos e assentada numa tela 4:5 com folga preta em cima, que é onde
o texto entra. **As duas mãos apontando precisam aparecer inteiras**, é o
gancho da imagem.

Pra trocar a foto, manda a original e eu refaço o assentamento. Não dá pra
simplesmente substituir o arquivo: o enquadramento é calculado.

## Os arquivos

| | |
|---|---|
| `frases.json` | as 5 frases, uma por dia útil |
| `card.html` | o desenho |
| `render.js` | gera os PNG |
| `jpg/` | os cards prontos pra postar |
