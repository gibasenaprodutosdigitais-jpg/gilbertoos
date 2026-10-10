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

**A foto do Gilberto** é a do ensaio do `@eubernardocoelho`, em
`identidade/`, original de 4480 × 6720. É a melhor que existe no repositório:
expressão séria, mãos entrelaçadas, fundo escuro que já conversa com a capa.

---

## O que falta, e é só isso

**A foto do Dr. Stanley Bittar.** O Instagram não pode ser aberto por aqui:
o login bloqueia e a página volta vazia. **Ele precisa mandar o arquivo.**

Para o duotone ficar igual ao do Gilberto, o ideal é pedir uma foto assim:

| | O que pedir |
|---|---|
| Enquadramento | do peito para cima, olhando para a câmera |
| Fundo | escuro ou neutro, de estúdio |
| Resolução | o original, acima de 2000 px de altura |
| Expressão | séria, sem sorriso aberto, para casar com a do Gilberto |
| Roupa | sóbria, tom escuro ou cinza |

Chegando o arquivo, é só salvar em `fotos/` e rodar o tratamento. Fica
pronto na mesma hora.

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
