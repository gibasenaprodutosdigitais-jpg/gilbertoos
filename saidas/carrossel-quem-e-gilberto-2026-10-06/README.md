# Carrossel: Quem é Gilberto Sena

Refeito a partir dos 6 cards que ele mandou em 06/out/2026, agora com 9.

| O que mudou | |
|---|---|
| Foto da capa | trocada pela do blazer claro, com o relógio à mostra. A antiga era casual e não dizia "chegou lá", que é o arco da história. |
| Três cards novos | **04, criador do GSena Hub e do OCEO**, **06, a base formal** e **07, o ano em que voltou a estudar** |
| Formato | todos em 1080x1350. Os originais misturavam retrato e quadrado |
| Execução | grade única, respiro igual, numeração 01/08 e assinatura no rodapé |

## De onde saiu cada credencial

Os cards 06 e 07 não têm uma linha inventada. Tudo sai de
`conhecimento/certificacoes-gilberto.md` e de `_memoria/quem-e-gilberto.md`,
que foram fichados a partir dos certificados originais em `dados/biblioteca/`.

Instituição e ano aparecem embaixo de cada item de propósito: credencial sem
origem é discurso, credencial com origem é prova.

## O card do criador

GSena Hub e OCEO estão registrados em `Projetos Gsena Tec/README.md`, que
declara o Gilberto **idealizador, criador intelectual e único titular** dos
dois. Daí vem a linha "idealizador e titular dos dois projetos".

O OCEO está descrito pelos cinco pilares, como no material dele. O GSena Hub
aparece só como "plataforma digital do Grupo Sena", porque o próprio
repositório traz o projeto como "a detalhar". **Se ele disser em uma frase o
que o Hub faz, a linha fica específica.**

## Números do card 08

**+ de 500 empresas e empresários** e **+R$ 500 milhões economizados em
impostos.** Confirmado por ele em 06/out/2026.

Ele chegou a pedir "500 mil" no valor economizado; levantei o conflito com o
`posicionamento.md`, que traz 500 milhões, e ele confirmou que o certo são os
milhões.

Sobre a contagem de empresas, os dois números convivem porque medem coisas
diferentes: o `posicionamento.md` fala em **2.000 empresas recuperadas** e
este card fala em **500 empresas e empresários** atendidos, que é o número
registrado na memória do sistema.

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

Sai em `instagram/card-01.png` a `card-09.png`.
