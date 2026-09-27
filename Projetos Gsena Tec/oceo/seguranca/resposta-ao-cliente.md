# "Meus dados estão seguros aí dentro?"

Como responder numa reunião, sem jargão e sem prometer o que não existe.

> **Versão impressa:** `OCEO - Seguranca de Dados (guia de reuniao).pdf` —
> uma página, com a identidade do OCEO, pra levar na reunião. Mudou algo
> aqui? Atualize `guia-reuniao.html` e rode `node render.js`.

> Regra: **não vender o que ainda não está pronto.** A lista do que falta
> está no `README.md` desta pasta. Se a pergunta for sobre um item de lá, a
> resposta certa é "ainda não, está no roteiro" — isso constrói mais
> confiança do que improviso.

---

## A resposta curta

> "Seu dado fica isolado do de qualquer outro cliente, a senha é guardada de
> um jeito que nem nós conseguimos ler, e todo movimento dentro do sistema
> fica registrado numa trilha que acusa se alguém mexeu — **inclusive se
> formos nós.**"

O peso está na última parte. Todo fornecedor diz que protege o dado contra
gente de fora. Quase nenhum se dispõe a provar contra si mesmo.

---

## Se ele perguntar "como assim, inclusive vocês?"

> "Cada lançamento guarda uma assinatura do lançamento anterior. Se alguém
> abrir o banco por fora e mudar um número, essa cadeia quebra — e o sistema
> aponta exatamente qual registro foi mexido. Quem tem a senha do servidor
> consegue alterar. O que ele não consegue é alterar sem deixar rastro."

Se puder mostrar a tela: `prova-adulteracao-detectada.png`. Uma folha de
R$ 18.000 alterada pra R$ 4.000 direto no banco, e o portal acusando o
registro exato.

## Se ele perguntar "e se eu quiser provar isso lá na frente?"

> "Todo fechamento a gente te manda um número de 64 caracteres que resume
> todos os lançamentos do período. Ele não revela nenhum dado — é só um
> resumo. Se daqui a dois anos alguém questionar o histórico, refaz a conta:
> se der o mesmo número, nada foi tocado."

*(Ainda não é automático — hoje é gerado sob demanda. Está no roteiro virar
entregável de fechamento mensal.)*

## Se ele perguntar sobre blockchain

> "A gente usa a criptografia que está por trás da blockchain, que é o que
> prova que nada foi adulterado. O que a gente não faz é espalhar seu dado
> por uma rede de computadores — isso não protegeria nada, porque blockchain
> garante que o registro não mudou, não que ele seja secreto. E tem um
> problema pior: como na blockchain nada pode ser apagado, a gente ficaria
> impedido de eliminar seu dado quando você exigisse, que é um direito seu
> pela LGPD."

Esse é o momento de virar o jogo: quem oferece blockchain pra guardar dado
contábil ou não entendeu a tecnologia, ou está usando a palavra como
argumento de venda. Motivos completos em `decisao-blockchain.md`.

## Se ele perguntar "e se outro cliente ver meus números?"

> "Cada empresa é uma caixa separada. Se alguém tentar abrir a sua empresa
> sem ter acesso, o sistema responde 'não encontrado' — nem confirma que ela
> existe aqui dentro. Nem a lista de clientes do OCEO dá pra descobrir de
> fora."

## Se ele perguntar sobre acesso do sócio ou do investidor

> "Dá pra liberar como leitor: vê todos os números, não altera nada. Os
> botões de ação nem aparecem pra ele."

## Se ele perguntar "e se vazar?"

Resposta honesta, sem enfeite:

> "Nenhum sistema no mundo promete que não vaza — quem promete isso está
> mentindo. O que dá pra prometer é o que a gente faz pra reduzir o risco e
> o que a gente faz se acontecer. A parte técnica já está construída; o
> plano formal de comunicação está sendo fechado com nosso jurídico agora."

**Não prometer notificação em prazo nenhum enquanto o item do `lgpd.md` não
estiver fechado com o advogado.**

---

## O que não falar

- **"É seguro."** Vazio. Substituir por o quê, especificamente.
- **"Usamos blockchain."** Não usamos, e é uma decisão consciente e
  defensável — não uma falta.
- **"É impossível invadir."** Não é, e o cliente sabe.
- **Sigla e nome de algoritmo.** Ninguém compra por causa de SHA-256.
  O que vende é "acusa se alguém mexer, inclusive se formos nós".

*Escrito em 27/set/2026.*
