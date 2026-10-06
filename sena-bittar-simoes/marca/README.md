# Marca SBS

| Arquivo | Pra quê |
|---|---|
| `sbs-original-3d.png` | o render 3D que o Gilberto mandou, 1579x996, fundo preto. É a origem de tudo aqui. |
| `sbs-logo.png` | recorte com fundo transparente, 1492x679. É o que entra nos documentos e serve pra qualquer uso digital. |
| `sbs-gravacao.png` | preto e branco, 1 bit, 2980x1354. Pra gravação a laser em modo raster. |
| `sbs-gravacao.svg` | o mesmo traçado em vetor. **Ver a ressalva abaixo.** |
| `sbs-marca-dagua.png` | silhueta azulada a 7,5%, usada atrás do conteúdo das folhas. |

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
