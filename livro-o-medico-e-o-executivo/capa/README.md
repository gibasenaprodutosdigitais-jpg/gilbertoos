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

**Stanley:** foto que ele mandou em 09/out/2026, original em
`fotos/bittar-original.jpg`. Terno preto, gravata, fundo de evento.

**O que as duas têm em comum é o que faz a capa funcionar:** terno escuro,
olhando para a câmera, expressão aberta. Em capa de dupla isso importa mais
que a qualidade de cada foto isolada.

### O tratamento, passo a passo

1. Recorte 3:4, cabeça e busto.
2. Nitidez antes e depois da ampliação.
3. **No caso do Stanley**, desfoque pesado fora de uma elipse no rosto: o
   fundo do evento tinha um cartaz com texto grande, que lia como erro de
   arte. Blur de 48 px resolve.
4. Duotone azul-noite idêntico nas duas.
5. Vinheta radial mais rampa escura no topo, para as duas nascerem do mesmo
   preto.
6. **Conferência de densidade:** o brilho médio das duas é medido e
   equilibrado. É o que impede uma metade de parecer colada na outra.

---

## O único problema que sobrou: resolução

⚠ **A foto do Stanley é um print de story, de 719 × 1280.** Depois do recorte
sobram cerca de 460 × 613 px de imagem útil, ampliados para 1200 × 1600.

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

**3. ~~O perfil do Instagram.~~ Resolvido em 09/out/2026: é
`@gilbertosenaoficiall`, com DOIS L.** O registro anterior, de julho, dizia o
contrário. A memória foi corrigida. **Atenção:** os 61 arquivos de conteúdo
já gerados em `saidas/` estão com um L.

---

## Variação que vale testar depois

Capa **sem foto nenhuma**, só tipografia, com a linha dourada dividindo o
título. Muitos dos melhores livros de negócio fazem isso, e tem uma vantagem
concreta: funciona em miniatura de loja virtual, onde dois rostos pequenos
viram borrão. Se ele quiser comparar, eu monto.
