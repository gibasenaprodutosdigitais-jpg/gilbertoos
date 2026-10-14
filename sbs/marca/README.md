# Marca SBS

| Arquivo | Pra quê |
|---|---|
| `sbs-original-3d.png` | o render 3D que o Gilberto mandou, 1579x996, fundo preto. É a origem de tudo aqui. |
| `sbs-logo.png` | recorte com fundo transparente, 1492x679. É o que entra nos documentos e serve pra qualquer uso digital. |
| `sbs-gravacao.png` | preto e branco, 1 bit, 2980x1354. Pra gravação a laser em modo raster. |
| `sbs-gravacao.svg` | o mesmo traçado em vetor. **Ver a ressalva abaixo.** |
| `sbs-marca-dagua.png` | silhueta azulada a 7,5%, usada atrás do conteúdo das folhas. |
| **`sbs-arte-institucional.jpg`** | **a arte dos três sócios, 3072 × 2048.** Refeita em 14/out/2026 com as fotos reais. Monta com `arte-institucional.html` + `_render-arte.js`. |
| `sbs-arte-institucional-v1-IA.jpg` | ⚠ a versão anterior. **Os três rostos eram gerados por IA.** Guardada só como referência de layout. **Não usar.** |

## A ressalva do vetor

O render é brilhante e tem sombra entre as fitas que se cruzam. Traçar isso
automaticamente dá um contorno com ondulação, e em alguns pontos as fitas se
fundem em vez de passar uma por cima da outra, que é justamente a graça do
monograma.

O `.png` de gravação resolve bem em laser raster, que é o caso mais comum. Se
a gravação for em vetor (fresa, corte, baixo-relevo profundo), **pedir o
arquivo vetorial original** a quem desenhou a marca, ou mandar um designer
redesenhar por cima. Traçado automático não substitui isso.

## Como foi feito o recorte

O fundo do render é preto chapado e a borda da letra é dura, então a forma
sai de um corte de luminância em 70, com máscara sólida e pena de borda. Não
usei o brilho como transparência: foi o que deixou a primeira tentativa com
cara de lavada.


---

## ★ A arte institucional foi refeita em 14/out/2026

**A versão anterior tinha três rostos inventados por IA.** Numa peça que leva
o nome de três pessoas reais e vende consultoria para médicos, isso queima
autoridade no dia em que um cliente compara a arte com os sócios ao vivo.

**A nova usa as fotos reais dos três.** Originais em `fotos/`:

| Sócio | Arquivo | Resolução | Observação |
|---|---|---|---|
| Gilberto Sena | `sena-original.jpg` | 4480 × 6720 | ensaio profissional, o melhor dos três |
| Dr. Stanley Bittar | `bittar-original.png` | 768 × 903 | estúdio, terno branco |
| Will Simões | `will-original.jpg` | **399 × 501** | ⚠ o menor, e é ele que limita o tamanho da peça |

⚠ **A arte está em 3072 × 2048 por causa da foto do Will.** Para ampliar
além disso, **pedir a ele uma foto maior**: do peito para cima, fundo escuro,
acima de 2000 px de altura.

### O tratamento que faz os três parecerem a mesma peça

1. **Recorte igual** nos três, proporção 560 × 780.
2. **Duotone quente** idêntico: sombra `(14,12,10)`, luz `(214,201,178)`.
   Escolhido para casar com o ouro da marca, e resolve o problema de três
   fotos de fotógrafos diferentes nunca combinarem em cor.
3. **Alpha que desaparece nas bordas**, com queda forte nas laterais e
   embaixo. ⚠ **Na primeira tentativa a queda era fraca e as três fotos
   apareceram como retângulos colados.**
4. **Conferência de densidade:** o brilho dos três rostos é medido.
   **Ficou em 11 pontos de diferença.** Alvo: menos de 18.
   O Will precisou de ganho de 1,14 para alcançar os outros dois.

### Dois defeitos que eu só vi olhando a arte pronta

**Os nomes estavam em cima das mãos** de cada um, ilegíveis. Foram para baixo
das fotos, no escuro.

**O til do "SIMÕES" estava cortado** pela linha acima. Resolvido com
entrelinha maior, não com fonte menor.
