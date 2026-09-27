# Como o OCEO protege os dados do cliente

Documento de referência. Cada afirmação aqui tem teste automatizado em
`../oceo-core/testes/` — não é promessa, é comportamento verificável.

Como conferir, na máquina:

```
cd "Projetos Gsena Tec/oceo/oceo-core"
python3 testes/test_acesso.py     # login e isolamento entre clientes
python3 testes/test_trilha.py     # a trilha pega adulteração
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

## Camada 2 — A sessão

- A sessão vive num **cookie `httponly`**. Se alguém conseguir injetar
  script malicioso na página, o script **não consegue ler** a sessão.
  Guardar o acesso em memória do JavaScript seria mais fácil de programar e
  bem mais fácil de roubar.
- **Expira em 12 horas.** Sessão abandonada em computador de escritório não
  fica eterna.
- Sair do sistema **apaga a sessão no servidor**, não só no navegador.

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

*Escrito em 27/set/2026.*
