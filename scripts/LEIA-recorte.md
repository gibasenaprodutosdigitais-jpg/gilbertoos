# Recortar o fundo de uma foto, sem serviço externo

```
swift scripts/recorta-fundo.swift entrada.jpg saida.png
```

Usa o **mesmo motor de recorte de assunto do Preview do macOS**, pela Vision
da Apple. Roda local, não sobe foto pra lugar nenhum, não precisa de conta e
não gasta crédito.

Devolve PNG com fundo transparente, já cortado na borda do assunto.

**Onde isso serviu:** nos três retratos do media kit, em 15/out/2026. Com o
fundo fora, a figura passa a se apoiar na página em vez de morar dentro de um
retângulo, e aí ela funciona em qualquer cor de fundo.

**Quando não usar:** foto de palco. Ali o fundo é a prova, porque é o telão
com o nome do evento e a plateia. Recortar jogaria fora justamente o que
interessa.
