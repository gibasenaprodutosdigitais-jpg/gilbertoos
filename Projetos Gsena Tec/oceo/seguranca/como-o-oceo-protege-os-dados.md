# Como o OCEO protege os dados do cliente

Documento de referência. Cada afirmação aqui tem teste automatizado em
`../oceo-core/testes/` — não é promessa, é comportamento verificável.

Como conferir, na máquina:

```
cd "Projetos Gsena Tec/oceo/oceo-core"
python3 testes/test_acesso.py           # login e isolamento entre clientes
python3 testes/test_trilha.py           # a trilha pega adulteração
python3 testes/test_protecao_login.py   # força bruta e recuperação de senha
```

---

## Camada 1 — A senha

**O OCEO não guarda a senha de ninguém.** Guarda um resultado matemático
que vem dela e do qual não se volta atrás.

- **PBKDF2-HMAC-SHA256 com 600 mil iterações.** Em português: transformar a
  senha no valor guardado custa tempo de propósito. Quem roubar o banco e
  tentar adivinhar senha por força bruta vai levar 600 mil vezes mais tempo
  por tentativa.
- **Sal próprio por conta.** Duas pessoas com a mesma senha têm valores
  guardados diferentes. Isso derruba o ataque de tabela pronta, onde o
  invasor já chega com milhões de senhas comuns pré-calculadas.
- **Mínimo de 10 caracteres.** Senha curta é o elo mais fraco de qualquer
  sistema, por melhor que seja o resto.

### O detalhe que quase ninguém faz

E-mail que não existe e senha errada dão **a mesma mensagem** e gastam **o
mesmo tempo**.

Parece detalhe, mas não é: se o erro fosse diferente — ou se a resposta
demorasse mais quando o e-mail existe — daria pra descobrir quem é cliente
do OCEO só testando endereços. Num sistema contábil, a lista de clientes já
é informação sensível por si só.

### A trava de força bruta

Senha boa não adianta se o invasor puder tentar um milhão de vezes.

- **Cinco senhas erradas travam a conta por 15 minutos.** Durante o
  bloqueio, **nem a senha certa entra** — é isso que impede o ataque de
  continuar rodando enquanto o dono não percebe.
- **Vinte falhas do mesmo endereço de rede travam a origem.** Pega o ataque
  que a trava por conta não pegaria: varrer muitas contas diferentes
  tentando uma senha comum em cada.
- **Acertar a senha zera o contador.** Quem errou duas vezes e acertou na
  terceira não fica com o orçamento pela metade.
- **O bloqueio é temporário, nunca permanente.** Passada a janela, a conta
  volta a aceitar login sozinha.

O detalhe que importa: **o bloqueio vale igual para e-mail que não existe.**
Se só a conta real travasse, o próprio bloqueio viraria o jeito de descobrir
quem é cliente do OCEO — o contrário do que a camada 1 protege.

> **Contrapartida honesta:** alguém que conheça o e-mail de um usuário pode
> travar a conta dele por 15 minutos de propósito. É incômodo, não é
> vazamento, e o caminho de recuperação de senha continua aberto. A
> alternativa — não travar — é bem pior.

## Camada 2 — A sessão

- A sessão vive num **cookie `httponly`**. Se alguém conseguir injetar
  script malicioso na página, o script **não consegue ler** a sessão.
  Guardar o acesso em memória do JavaScript seria mais fácil de programar e
  bem mais fácil de roubar.
- **Expira em 12 horas.** Sessão abandonada em computador de escritório não
  fica eterna.
- Sair do sistema **apaga a sessão no servidor**, não só no navegador.

### Recuperação de senha

Antes disso, cliente que esquecia a senha dependia de alguém do Grupo Sena
abrir o banco e mexer — exatamente o que a trilha da camada 4 existe pra
flagrar. Agora o caminho é o próprio usuário.

Como foi construído:

- **Link que vence em 30 minutos** e **só funciona uma vez**.
- **Pedir um link novo invalida o anterior.** Só o último vale.
- **O link não fica legível no banco.** Guarda-se só o resumo dele. Quem
  roubar a base não consegue redefinir a senha de ninguém.
- **A resposta é sempre a mesma**, exista o e-mail ou não. Formulário de
  "esqueci minha senha" que responde "este e-mail não está cadastrado"
  entrega a lista de clientes pra qualquer um.
- **Redefinir derruba todas as sessões abertas daquela conta.** Se a conta
  estava tomada, o invasor perde o acesso no mesmo instante.
- **O token some da barra de endereço** assim que a senha é salva, pra não
  ficar no histórico do navegador.
- A senha nova passa pela **mesma política** da senha original.

> **O que ainda não funciona:** o e-mail não é enviado de verdade. Hoje a
> mensagem é **gravada em arquivo** em `dados/emails/`, porque não há
> serviço de envio contratado. Todo o mecanismo de segurança — o que é
> difícil de acertar — está pronto e testado; o que falta é configuração.
> **Não anunciar recuperação de senha ao cliente antes de ligar o envio.**

## Camada 3 — O isolamento entre clientes

Este é o ponto que decide se o OCEO pode ser vendido pra mais de uma
empresa no mesmo servidor.

Toda rota que toca dado de empresa passa por **duas portas, nesta ordem**:

1. **Quem é você?**
2. **Você pode ver esta empresa?**

A segunda pergunta é feita **inclusive na leitura** — não só quando alguém
tenta alterar algo. É o erro clássico: proteger a escrita e deixar a
consulta aberta.

### 404 e não 403

Tentar abrir a empresa de outro cliente devolve **"não encontrado"**, e não
"acesso negado".

A diferença importa: "acesso negado" confirma que aquela empresa existe no
OCEO. Um concorrente poderia varrer CNPJs e montar a carteira de clientes do
Grupo Sena sem nunca entrar em lugar nenhum. Com "não encontrado", ele não
descobre nada.

### Papéis

| Papel | O que pode |
|---|---|
| `dono` | Tudo, inclusive dar e tirar acesso de outras pessoas |
| `operador` | Lançar e alterar, não mexe em quem acessa |
| `leitor` | Só olha. O portal esconde os botões de ação pra ele |

O `leitor` existe pro caso real: o cliente quer que o sócio ou o investidor
veja os números **sem poder alterar nada**.

## Camada 4 — A trilha auditável

As três camadas acima protegem contra gente de fora. Esta protege contra
**gente de dentro** — inclusive nós.

### Como funciona

Cada fato gravado guarda o **resumo criptográfico (SHA-256) do fato
anterior**. Os registros viram uma corrente: cada elo depende do anterior.

Mexer num registro antigo muda o resumo dele. O registro seguinte continua
apontando pro resumo velho. A corrente quebra naquele ponto exato — e a
conferência diz qual é o ponto.

### A prova

Foi testado de propósito, com o sistema no ar: três lançamentos de folha
gravados, o banco aberto por fora como faria alguém com a senha do servidor,
e uma folha de R$ 18.000 alterada pra R$ 4.000.

O portal acusou na hora:

> **ADULTERADA** — 3 registro(s) conferido(s)
> quebrou no registro 2 — o conteúdo do registro foi alterado depois de gravado

Ver `prova-adulteracao-detectada.png`.

### E se o fraudador for esperto?

Um dos oito testes simula exatamente isso: o fraudador **recalcula o resumo**
do registro que alterou, pra "consertar a prova".

Continua sendo pego. Os registros seguintes ainda apontam pro resumo antigo,
e a quebra só anda uma casa pra frente. Pra encobrir de verdade, ele teria
que reescrever **toda a base**, do ponto da fraude até hoje, sem errar uma
linha — e, se o resumo do período já tiver sido enviado pro cliente, nem
isso resolve.

### O que os oito testes cobrem

1. Trilha intacta é reconhecida como íntegra
2. Cada registro carrega mesmo o elo do anterior
3. **Alterar um valor é detectado, e aponta o registro exato**
4. Apagar um registro do meio é detectado
5. **Recalcular o resumo não salva o fraudador**
6. Inserir um registro inventado é detectado
7. O recibo prova a integridade **sem expor nenhum dado do cliente**
8. A corrente sobrevive ao reinício do servidor

### O resumo do período

A conferência devolve um número de 64 caracteres que **resume todos os
registros do período sem revelar nenhum deles**.

Esse número pode ser enviado ao cliente, guardado em e-mail datado,
registrado em cartório ou publicado. Se meses depois alguém questionar o
histórico, basta refazer a conta: dá o mesmo número, nada foi tocado.

É aqui — e só aqui — que blockchain teria função real no OCEO. Ver
`decisao-blockchain.md`.

---

## Onde isso aparece pro usuário

- **No portal:** bloco "Integridade dos dados", botão **Conferir agora**.
- **Na API:** `GET /api/empresas/{id}/integridade`.

---

## O que este documento não cobre

Segurança de infraestrutura — servidor, rede, backup, criptografia do disco
— ainda não está definida porque o OCEO ainda não está hospedado em produção.
A lista do que falta está no `README.md` desta pasta.

*Escrito em 27/set/2026. Trava de força bruta e recuperação de senha
acrescentadas no mesmo dia.*
