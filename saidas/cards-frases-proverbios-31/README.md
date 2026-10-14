# Série diária: Sabedoria para empreender

**31 frases, uma para cada dia do mês.** Reflexões autorais do Gilberto
inspiradas nos princípios de Provérbios 31, aplicadas à rotina de quem
empreende. **Não são citações literais da Bíblia**, e o card diz isso em
letras pequenas: *"Reflexão autoral inspirada em Provérbios 31:20"*.

A série **reinicia todo mês**: o card do dia 14 sai todo dia 14. Uma vez
pronta, roda sozinha o ano inteiro.

## Como gerar

```
node render.js        # os 31
node render.js 14     # só o dia 14
```

Precisa de `NODE_PATH` apontando pra `scripts/node_modules`.

## As fotos

Entram em `assets/` com o nome `foto-01.jpg`, `foto-02.jpg` e assim por
diante. O script distribui as fotos pelos dias em rodízio: com 4 fotos, o dia
1 usa a 1, o dia 2 usa a 2, o dia 5 volta pra 1.

**Quanto mais fotos, menos repetição.** Com 31 fotos, nenhum dia repete.

A foto é tratada no próprio card: dessatura parcial, contraste, leve sépia e
um degradê que a dissolve no fundo. **Manda a foto original**, sem filtro e
sem corte, que o tratamento é feito aqui.

Funciona melhor com **retrato vertical, fundo escuro ou neutro, e o rosto
no terço de cima.** A arte reserva a metade esquerda pro texto.

## Os arquivos

| | |
|---|---|
| `frases.json` | as 31 frases com a referência de cada uma |
| `card.html` | o desenho |
| `render.js` | gera os PNG |
| `instagram/` | os cards prontos, `dia-01.png` a `dia-31.png` |
