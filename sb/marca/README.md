# Marca SB · Sena e Bittar

> **19/out/2026: a marca voltou a ser SB.** Com a saída do Will Simões, saiu
> o monograma SBS e voltou o monograma SB original, o das letras S e B com o
> bastão de Asclépio. A marca SBS, a arte dos três e as fotos do Simões estão
> em `../_arquivo-sbs/marca/`, **só como registro. Não usar.**

| Arquivo | Pra quê |
|---|---|
| `sb-original-3d.jpg` | a placa 3D "Sena e Bittar · Consultoria e assessoria para médicos", 1300 × 1018. É a origem da marca. |
| `sb-logo.png` | o monograma SB com fundo transparente, 600 × 599. É o que entra nos documentos e no digital. |
| `sb-gravacao.png` | preto e branco, 1 bit, 2400 × 2396. Pra gravação a laser em modo raster. **Ver a ressalva abaixo.** |
| `sb-marca-dagua.png` | silhueta do monograma em transparência baixa, usada atrás do conteúdo das folhas. |
| **`sb-arte-institucional.jpg`** | **a arte dos dois sócios, 3072 × 2048**, refeita em 19/out/2026 com as fotos reais. Monta com `arte-institucional.html` + `_render-arte.js`. |

## ⚠ A ressalva do tamanho

**O monograma SB que existe tem só 600 px.** Serve bem para documento e tela.
Para placa, gravação, impressão grande ou fachada, **pedir o arquivo original
em alta a quem desenhou a marca** (de preferência em vetor).

O `sb-gravacao.png` foi tirado da silhueta do monograma e ampliado 4 vezes:
sai o contorno inteiro, mas **perde o desenho interno** (a serpente e o bastão
viram parte da massa). Para gravar com detalhe, só com o vetor original.

## A arte institucional

Fotos reais dos dois, originais em `fotos/`:

| Sócio | Arquivo | Resolução | Observação |
|---|---|---|---|
| Gilberto Sena | `sena-original.jpg` | 4480 × 6720 | ensaio profissional |
| Dr. Stanley Bittar | `bittar-original.png` | 768 × 903 | estúdio, terno branco. ⚠ é a menor, e limita o tamanho da peça |

⚠ **Para ampliar a arte além de 3072 × 2048, pedir ao Bittar a foto original
do fotógrafo** (o retrato é de estúdio, então ela existe). É a mesma pendência
da capa do livro.

### O tratamento que faz as fotos parecerem a mesma peça

1. **Recorte igual** nas duas, retrato vertical.
2. **Duotone quente** idêntico: sombra `(14,12,10)`, luz `(214,201,178)`, para
   casar com o ouro da marca e resolver fotos de fotógrafos diferentes.
3. **Alpha que desaparece nas bordas**, com queda forte nas laterais e
   embaixo. Com queda fraca, as fotos aparecem como retângulos colados.
4. **Os nomes ficam abaixo das fotos**, no escuro. Em cima das mãos ficavam
   ilegíveis.

**Os rótulos:** Gilberto Sena, *Gestão, Tributário e Finanças* (o pilar de
Lucratividade passou para ele em 19/out); Dr. Stanley Bittar, *Médico
Estrategista*.
