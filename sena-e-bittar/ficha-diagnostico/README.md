# Ficha de diagnóstico do consultório

Aplicada no primeiro encontro da mentoria, antes de qualquer plano. Sai da
seção 4 do `plano-de-mentoria.md`.

**Entregável:** `Sena e Bittar - Ficha de Diagnostico.pdf`, 7 páginas A4.
Capa, identificação, uma página por pilar e a folha de fecho com a linha de
partida.

## Estrutura

| Página | O que tem |
|---|---|
| 1 | Capa com a marca e o aviso de sigilo |
| 2 | Identificação, perfil do profissional e se faz procedimento estético |
| 3 a 6 | As 21 perguntas, divididas pelos quatro pilares |
| 7 | Linha de partida dos quatro indicadores, documentos a entregar, as três decisões do trimestre e assinaturas |

A pergunta 21 só vale para quem faz estética. Ela existe porque a
classificação do procedimento decide a conta de imposto do consultório, e é
a única zona cinzenta entre os quatro públicos. Ver a seção 8 do plano.

## A marca

Dois arquivos, os dois tirados da foto da fachada que o Gilberto mandou em
06/out/2026:

- **`logo-sena-e-bittar.jpg`** é a capa. Entra como foto, com o azul da marca
  em volta, porque é foto de fachada e não arquivo de marca.
- **`marca-dagua.png`** é o monograma recortado do mármore, cinza-azulado e
  sem cor. Entra a 8% de opacidade no meio de cada folha, menos a capa, que
  já tem a marca grande. Só o símbolo: o conjunto inteiro atrás de texto
  manuscrito vira sujeira.

O recorte usa a própria luz da foto como máscara. O metal é claro, o mármore
é escuro, então um corte duro de luminância separa os dois sem deixar resto
de fundo.

**Se aparecer o arquivo original** (vetor, ou PNG com fundo transparente),
trocar. A capa fica mais limpa e a marca pode ir menor sem perder nitidez.

A linha da marca diz "consultoria e assessoria para médicos". A ficha atende
quatro públicos, então dentista e biomédico recebem um documento que fala em
médicos. Está na lista de decisões da seção 9 do plano.

## Regerar

```
NODE_PATH="../../scripts/node_modules" node render.js
```

`conferir.js` tira uma foto do HTML inteiro em `/tmp/sbficha/tudo.png`, pra
olhar o resultado antes de imprimir.
