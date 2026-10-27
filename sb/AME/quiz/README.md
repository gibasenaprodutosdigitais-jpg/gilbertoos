# Quiz da Imersão AME

Seis perguntas, uma por tela: nome, WhatsApp, Instagram (dele ou do negócio),
nicho, faturamento por mês e a maior dificuldade do negócio hoje.

Existe em duas versões, com as mesmas perguntas e o mesmo visual:

| Versão | Onde | Pra onde vão as respostas |
|---|---|---|
| **Site no computador** | `site/index.html` + `servidor.py` | `respostas.csv`, nesta pasta. Abre no Excel ou no Numbers. Fica fora do GitHub, porque são dados pessoais de terceiros |
| **Online no Claude** | `quiz-ame.html`, publicado em https://claude.ai/artifact/8Rmtdk5U8HtJmkmzASEryn (privado) | quem é da conta dele grava na coleção `inscricoes`; quem é de fora manda pelo WhatsApp, e pra isso falta pôr o número em `WHATSAPP_DESTINO` |

## Ligar o site no computador

```
cd sb/AME/quiz
python3 servidor.py
```

Abre em http://localhost:5180. Pra desligar, Ctrl+C. Só funciona neste
computador: pra receber resposta de quem vem do Instagram, o site precisa
estar publicado num endereço da internet.

Mudou uma pergunta? Mudar nos dois arquivos, `quiz-ame.html` e `site/index.html`.
