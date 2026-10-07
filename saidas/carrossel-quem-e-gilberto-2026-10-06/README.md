# Carrossel: Quem é Gilberto Sena

Refeito a partir dos 6 cards que ele mandou em 06/out/2026, agora com 8.

| O que mudou | |
|---|---|
| Foto da capa | trocada pela do blazer claro, com o relógio à mostra. A antiga era casual e não dizia "chegou lá", que é o arco da história. |
| Dois cards novos | **05, a base formal** e **06, o ano em que voltou a estudar** |
| Formato | todos em 1080x1350. Os originais misturavam retrato e quadrado |
| Execução | grade única, respiro igual, numeração 01/08 e assinatura no rodapé |

## De onde saiu cada credencial

Os cards 05 e 06 não têm uma linha inventada. Tudo sai de
`conhecimento/certificacoes-gilberto.md` e de `_memoria/quem-e-gilberto.md`,
que foram fichados a partir dos certificados originais em `dados/biblioteca/`.

Instituição e ano aparecem embaixo de cada item de propósito: credencial sem
origem é discurso, credencial com origem é prova.

## Uma coisa a conferir com ele

O card 04 repete o que estava no carrossel original: *"Formado em Gestão
Financeira e Administração"*. **Essa formação não está registrada em lugar
nenhum do repositório.** O que está documentado é Bacharel em Teologia
(SETEAD, 2020) e a pós em Direito Tributário (720h, 2021), mais a menção no
livro dele de que se formou em Direito.

Mantive o texto como ele tinha, porque é afirmação dele. Mas vale conferir
antes de publicar: é o tipo de linha que alguém checa.

## Regerar

```
NODE_PATH="../../scripts/node_modules" node render.js
```

Sai em `instagram/card-01.png` a `card-08.png`.
