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
| Até R$ 30 mil | `obrigado.html`: agradece e indica o @gilbertosenaoficial |
| De R$ 30 mil pra cima (30 a 100 mil decidido por ele em 27/out) | `venda.html`: a página de vendas do ingresso, de R$ 3.999 por R$ 499 |

A regra fica em `DESTINO_POR_FAIXA`, no `site/index.html`. O botão de comprar da página
de vendas usa o link em `LINK_PAGAMENTO`, no `site/venda.html`; enquanto estiver vazio,
o botão avisa que o link está sendo preparado. Desde 27/out está com o link do Mercado Pago que ele mandou. A versão online no Claude ainda não
tem essa mecânica.

⚠ Nos testes, nunca apagar o `respostas.csv` inteiro: já tem resposta de verdade nele.
Tirar só as linhas de teste.

## Ligar o site no computador

```
cd sb/AME/quiz
python3 servidor.py
```

Abre em http://localhost:5180. Pra desligar, Ctrl+C. Só funciona neste
computador: pra receber resposta de quem vem do Instagram, o site precisa
estar publicado num endereço da internet.

Mudou uma pergunta? Mudar nos dois arquivos, `quiz-ame.html` e `site/index.html`.
