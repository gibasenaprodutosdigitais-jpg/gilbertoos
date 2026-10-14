# Capa de O Médico e o Executivo

Primeira versão, 09/out/2026.
**Arquivo:** `O Medico e o Executivo - capa.png`, 1890 × 2716 px, que é
**16 × 23 cm a 300 dpi**, a medida comercial de livro de negócios no Brasil.

Regera com:

```
NODE_PATH="../../scripts/node_modules" node _render-capa.js
```

---

## O conceito

O título nomeia duas pessoas e dois mundos. A capa transforma isso em
geometria: **uma linha dourada atravessa a capa inteira**, do fim do título
ao rodapé, e separa os dois retratos. A linha é o livro.

Os dois losangos sobre a linha marcam onde os dois lados se encontram.

## As decisões de arte

**Os dois retratos vão em duotone azul-noite.** Isso não é estilo, é solução
de um problema prático: **foto de autores diferentes, tiradas por fotógrafos
diferentes, nunca combinam em cor.** O duotone iguala os dois e faz a capa
parecer uma peça só.

**As fotos nascem do escuro.** Nenhum recorte, nenhuma silhueta dura: um
degradê come as bordas e o retrato emerge do fundo. Recorte malfeito é o que
mais estraga capa de livro com foto de autor.

**Paleta:** fundo `#0A1018`, tinta `#ECE9E2`, ouro `#C9A24B`. O ouro é o
único acento e aparece só na linha, no "e o" do título e na tarja de cima. É
o mesmo ouro da identidade da Sena, Bittar e Simões, o que amarra o livro à
casa sem transformar a capa em peça institucional.

**Tipografia:** Playfair Display no título e nos nomes, Archivo no resto.
Serifa de alto contraste dá o tom editorial e sério que o assunto pede.

**As duas fotos, e por que estas.**

**Gilberto:** `identidade/WhatsApp Image 2026-07-15 at 18.49.38.jpeg`, de
terno preto sobre fundo escuro, ajustando o relógio. Original em
`fotos/gilberto-original.jpg`. **Trocada a pedido dele em 09/out/2026**, no
lugar do ensaio do `@eubernardocoelho`, que é tecnicamente muito melhor
(4480 × 6720) mas tem terno cinza-claro e expressão severa: do lado do Bittar
sorrindo de preto, as duas metades não pareciam a mesma peça.

**Stanley:** ★ **trocada em 13/out/2026.** Retrato de estúdio, **terno
branco**, braços cruzados, fundo cinza-azulado. Original em
`fotos/bittar-original-2.png`, 768 × 903. A anterior era print de story e
está em `fotos/bittar-original.jpg`.

### ★ O terno branco virou o conceito

A foto nova trouxe um problema aparente e uma solução melhor. **Ele de
branco, o Gilberto de preto.** Em capa de dupla isso costuma quebrar a
unidade.

Aqui faz o contrário: o livro se chama *O Médico e o Executivo*, e **a roupa
passou a nomear os dois mundos sem precisar de símbolo nenhum.** A linha
dourada do meio deixou de ser enfeite e virou a fronteira entre eles.

**A unidade da capa vem do rosto, e é por isso que ela aguenta a roupa
divergir.** Os dois retratos foram equilibrados para o brilho da pele bater:
**medido em 13 pontos de diferença**, dentro da margem em que o olho não
percebe.

### O tratamento, passo a passo

1. **Recorte 3:4 fechado**, cabeça e busto. ⚠ O enquadramento tem que deixar
   as duas cabeças do mesmo tamanho. Na primeira tentativa de 13/out o
   Stanley saiu menor e parecia mais distante que o Gilberto.
2. Nitidez antes e depois da ampliação.
3. **Curva de tom antes do duotone:** levanta os meios para o rosto subir,
   afunda as sombras para o fundo de estúdio escurecer, e **comprime a luz
   alta para o terno branco não estourar.**
4. Duotone azul-noite idêntico nas duas: sombra `(9,16,26)`, luz
   `(169,169,167)`.
5. **Vinheta larga** mais rampa escura no topo. ⚠ Vinheta estreita cria um
   halo oval visível em volta da pessoa, e foi o que aconteceu na primeira
   tentativa de 13/out.
6. **Conferência de densidade:** medir o brilho **dos rostos**, não da
   metade inteira. Com roupas de cores opostas, a média da metade não diz
   nada. **Alvo: menos de 15 pontos de diferença entre as duas peles.**

---

## O único problema que sobrou: resolução

⚠ **A foto nova do Stanley tem 768 × 903.** Melhor que o print de story
anterior, que rendia 460 × 613 úteis, mas depois do recorte fechado sobram
cerca de **534 × 712**, ampliados para 1200 × 1600.

**Para tela isso passa. Para gráfica, não.** Numa capa impressa de 16 × 23 cm
a 300 dpi, aquela metade vai sair visivelmente mole ao lado da outra, e o
olho percebe mesmo sem saber explicar.

**A capa atual serve para aprovar o conceito, para mockup e para divulgação
digital.** Antes de mandar para a editora, é preciso pedir ao Stanley o
arquivo original, não um print, com uma foto assim:

| | O que pedir |
|---|---|
| Enquadramento | do peito para cima, olhando para a câmera |
| Fundo | escuro ou neutro, de estúdio |
| Resolução | o original, acima de 2000 px de altura |
| Expressão | séria, sem sorriso aberto, para casar com a do Gilberto |
| Roupa | sóbria, tom escuro ou cinza |

Chegando o arquivo, é só salvar em `fotos/bittar-original.jpg` e rodar o
tratamento de novo. Fica pronto na mesma hora, e a composição não muda.

---

## O que já foi decidido

**1. ~~Stanley, e não Staley.~~ Confirmado por ele em 09/out/2026: é
Stanley.** O escopo recebido escreve "Staley" do começo ao fim e **precisa
ser corrigido na fonte**. A capa está com Stanley.

**2. ~~A tarja de cima.~~ Decidida em 09/out/2026:** *"Dois caminhos, uma
empresa, e o que ninguém examinou"*. Ele escolheu esta em vez de "A história
real de um império que ruiu", que exporia a queda do coautor logo na capa.
**Foi a escolha certa:** esta diz a mesma coisa sem acusar ninguém, e ainda
amarra com o nome do primeiro capítulo.

**3. ~~O perfil do Instagram.~~ Fechado em 10/out/2026: o oficial é
`@gilbertosenaoficial`, com UM L**, que é o que está conectado à Zernio e o
que recebe as publicações. O conteúdo já gerado em `saidas/` está certo.

---

## Variação que vale testar depois

Capa **sem foto nenhuma**, só tipografia, com a linha dourada dividindo o
título. Muitos dos melhores livros de negócio fazem isso, e tem uma vantagem
concreta: funciona em miniatura de loja virtual, onde dois rostos pequenos
viram borrão. Se ele quiser comparar, eu monto.
