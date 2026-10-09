# Normas de formatação

Passadas pela editora e aplicadas a todos os capítulos.

| Item | Norma |
|---|---|
| Fonte | Times New Roman, 12 |
| Espaçamento | 1,5 |
| Margens | 3 cm superior e esquerda, 2 cm inferior e direita |
| Alinhamento | justificado |
| Recuo de parágrafo | 1,25 cm na primeira linha |
| Numeração de páginas | canto superior direito |
| Extensão por capítulo | 10 páginas, em média |

## Como gerar

```
python3 formatar-capitulo.py capitulos/07-do-zero-ao-grupo-sena.md
NODE_PATH="../scripts/node_modules" node _render-formatado.js
```

O primeiro comando gera, em `formatado/`, o **.docx** que vai para a editora
e um **.html** com as mesmas medidas. O segundo transforma os HTML em PDF com
as margens da norma e imprime a contagem de páginas de cada capítulo.

O formatador tira sozinho o que é nota de trabalho: o bloco de citação do
topo do arquivo e tudo a partir de "Notas de redação". Então o `.md` continua
servindo de oficina sem sujar o que vai para a editora.

## O que o formatador faz com cada coisa

| No markdown | No documento |
|---|---|
| `# Título` | título do capítulo, caixa alta, negrito, 14 |
| `## Seção` | subtítulo em negrito |
| `### Subseção` | subtítulo em negrito itálico |
| parágrafo | justificado, recuo de 1,25 cm, espaçamento 1,5 |
| `> linha` | bloco recuado 2 cm em itálico, usado nas Sacadas do Giba |
| lista e tabela | recuo de 1,25 cm e tabela com grade |

## Uma conta útil

No formato da editora, **uma página comporta cerca de 420 a 450 palavras**.
Foi medido nos capítulos já escritos, não estimado. Serve para planejar:
um capítulo de 10 páginas pede algo entre 4.200 e 4.500 palavras.
