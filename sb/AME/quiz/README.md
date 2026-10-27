# Quiz da Imersão AME

Seis perguntas, uma por tela: nome, WhatsApp, Instagram (dele ou do negócio),
nicho, faturamento por mês e a maior dificuldade do negócio hoje.

Existe em duas versões, com as mesmas perguntas e o mesmo visual:

| Versão | Onde | Pra onde vão as respostas |
|---|---|---|
| **Site no computador** | `site/index.html` + `servidor.py` | `respostas.csv`, nesta pasta. Abre no Excel ou no Numbers. Fica fora do GitHub, porque são dados pessoais de terceiros |
| **Online no Claude** | `quiz-ame.html`, publicado em https://claude.ai/artifact/8Rmtdk5U8HtJmkmzASEryn (privado) | quem é da conta dele grava na coleção `inscricoes`; quem é de fora manda pelo WhatsApp, e pra isso falta pôr o número em `WHATSAPP_DESTINO` |

## A mecânica do site (27/out)

Depois de enviar, o quiz leva a pessoa pra uma página conforme o faturamento que ela marcou:

| Faixa | Vai para |
|---|---|
| A · Até R$ 30 mil | `obrigado.html`: agradece e indica o @gilbertosenaoficial |
| B · De R$ 30 mil a R$ 70 mil | `obrigado.html` |
| C · De R$ 70 mil a R$ 120 mil | `venda.html`: a página de vendas do ingresso, de R$ 3.999 por R$ 499 |
| D · Acima de R$ 120 mil | `venda.html` |

Faixas e destinos decididos por ele em 27/out (trocou as faixas antigas, que iam até "acima de R$ 1 milhão").

A regra fica em `DESTINO_POR_FAIXA`, no `site/index.html`. O botão de comprar da página
de vendas usa o link em `LINK_PAGAMENTO`, no `site/venda.html`; enquanto estiver vazio,
o botão avisa que o link está sendo preparado. Desde 27/out está com o link do Mercado Pago que ele mandou. A versão online no Claude ainda não
tem essa mecânica.

⚠ Nos testes, nunca apagar o `respostas.csv` inteiro: já tem resposta de verdade nele.
Tirar só as linhas de teste.

## Google Sheets (27/out)

As respostas também vão pra duas planilhas no Google: "Acima de R$ 70 mil" (faixas C e D)
e "Até R$ 70 mil" (faixas A e B). O código do Apps Script e o passo a passo estão em
`google/`. Ativado por ele em 27/out: o link do App da Web está em `PLANILHA_URL`, no `site/index.html`.
A versão online no Claude não manda pro Google.

## No ar na Vercel (27/out)

**https://imersao-ame.vercel.app** (o quiz), com `/venda.html` e `/obrigado.html`.
Projeto `imersao-ame` na conta Vercel `apliquepoupe`. Sobe só a pasta `site/`:
`servidor.py`, `respostas.csv` e o código do Google ficam de fora.

Na Vercel as respostas vão só pro Google Sheets (lá não existe o servidor local).
No computador, vão pro Google Sheets e pro `respostas.csv`.

Publicar de novo depois de mudar alguma coisa:

```
cd sb/AME/quiz/site
vercel deploy --prod --yes
```

## Ligar o site no computador

```
cd sb/AME/quiz
python3 servidor.py
```

Abre em http://localhost:5180. Pra desligar, Ctrl+C. Só funciona neste
computador: pra receber resposta de quem vem do Instagram, o site precisa
estar publicado num endereço da internet.

Mudou uma pergunta? Mudar nos dois arquivos, `quiz-ame.html` e `site/index.html`.
