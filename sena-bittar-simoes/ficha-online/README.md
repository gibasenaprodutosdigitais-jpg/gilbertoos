# Ficha de diagnóstico online

**Link:** https://claude.ai/artifact/8XJKDDjP2FWsxMKp7z9gY7

A mesma ficha do papel, respondida pelo celular. O profissional abre, responde
e envia; a resposta cai num banco que o Gilberto consegue ler daqui, sem
ninguém reencaminhar nada.

| Arquivo | Pra quê |
|---|---|
| `anamnese-sbs.html` | a fonte da página. Editar aqui e republicar pela mesma URL. |
| `qr-ficha-sbs.png` | QR em 1400px, cor da marca. Pra imprimir, pôr em card ou mandar. |
| `qr-ficha-sbs.svg` | o mesmo QR em vetor, pra peça impressa de qualidade. |
| `gerar-qr.js` | regera os dois. `LINK=... node gerar-qr.js` troca o destino. |

## Antes de mandar pra alguém

**A página nasce privada.** Só o Gilberto abre. Para o médico conseguir
responder, abrir a página e compartilhar pelo menu Share. Enquanto isso não
for feito, quem receber o link vê uma tela de acesso negado.

## Como a resposta chega

Quem está logado no claude.ai e tem acesso à página grava direto no banco.
Para qualquer outra pessoa, o formulário continua funcionando, e no envio a
página mostra as respostas em texto com um aviso para copiar e mandar no
WhatsApp. Nada do que foi digitado se perde nos dois casos.

Para ler as respostas, é só pedir aqui: elas ficam na coleção `respostas`.

## O que a ficha online tem a mais que o papel

- A pergunta 21 só aparece para quem marca que faz procedimento estético
- Campo de contato, que no papel não existia
- Botão de copiar as respostas, útil quando a pessoa quer guardar o que escreveu
