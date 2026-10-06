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

`logo-sena-e-bittar.jpg` é o recorte da foto da fachada que o Gilberto
mandou em 06/out/2026. Entra como imagem porque é foto, não arquivo de
marca: tentei recortar do fundo e sobrava mármore nas bordas das letras.

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
