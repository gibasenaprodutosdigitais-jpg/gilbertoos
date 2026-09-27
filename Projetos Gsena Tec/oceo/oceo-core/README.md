# OCEO — núcleo de interligação dos cinco pilares

Este é o **miolo** do OCEO: o código que faz os cinco pilares conversarem
entre si em vez de virarem cinco sistemas separados com cinco cadastros do
mesmo cliente.

> Estado: **fundação funcional**, com banco, login, isolamento entre
> clientes, trilha auditável, API e portal. Ainda faltam as regras internas de cada pilar e as
> integrações externas. O que existe aqui é a estrutura em que esse resto se
> encaixa.

---

## Para ver funcionando em 30 segundos

```bash
cd oceo-core
python3 testes/test_interligacao.py     # os pilares conversam
python3 testes/test_acesso.py           # login, persistência e isolamento
python3 testes/test_trilha.py           # a trilha pega adulteração
python3 api/app.py                      # sobe o portal em http://127.0.0.1:8000
```

No portal: crie uma conta, cadastre a empresa de demonstração, ligue e
desligue pilares e use os botões de "disparar um fato". Cada fato é publicado
em nome de **um** pilar, e quem reage é decidido pelo sistema, não pelo botão.
Tudo fica gravado: feche o servidor, suba de novo e o estado continua lá.

---

## A ideia central

**Nenhum pilar chama outro pilar.** Quem apura o imposto (GC) não sabe que
existe um módulo jurídico. Ele apenas anuncia que fechou a apuração. Quem
tiver interesse reage.

É isso que permite vender, ligar ou desligar um pilar sem quebrar os outros
— e é por isso que o OCEO pode ser vendido por pilar sem virar cinco
produtos desconectados.

```
GC fecha a apuração
   ├─> GF lê e atualiza a DRE
   └─> GJ vê carga alta e aponta a oportunidade tributária

GF forma a reserva de 3 meses
   └─> GI libera a trilha educacional (com o disclaimer obrigatório)

GF sinaliza risco no caixa
   └─> GM segura o aumento de verba de mídia
```

## As regras de negócio estão no código, não só na documentação

O que estava escrito nos documentos dos pilares virou comportamento:

| Regra (origem) | Onde está no código |
|---|---|
| "Pilar 5: pré-requisito é ativação em cadeia com o Pilar 2" | `dominio.DEPENDENCIAS` — o sistema **recusa** ligar o GI sem o GF |
| "Três meses de ponto de equilíbrio é o padrão" | `pilares/reacoes.MESES_DE_RESERVA_PADRAO` — reserva menor não libera a trilha |
| "GI é educacional puro, não recomendação individualizada" (trava CVM) | `reacoes.DISCLAIMER_GI`, anexado a todo alerta do GI |
| "Fiscal (P1) apura e calcula; o Jurídico aponta a redução" | `reacoes.gj_procura_oportunidade` reage ao evento do GC |
| "Relação com o Pilar 1, pra não duplicar escopo" | o GF **consome** a apuração do GC em vez de refazê-la |

Mudar uma dessas regras é mudar uma linha, num lugar só.

---

## Estrutura

```
oceo-core/
├── oceo/                    ← o núcleo, Python puro, sem dependência externa
│   ├── dominio.py           ← vocabulário único: Empresa, Pilar, Evento, Alerta
│   ├── nucleo.py            ← barramento de eventos, assinatura, sistema
│   ├── montagem.py          ← junta as peças (único lugar que sabe montar)
│   └── pilares/reacoes.py   ← quem reage a quê — a interligação em si
│   ├── repositorio.py       ← persistência (SQLite hoje, Postgres depois)
│   ├── acesso.py            ← usuários, senhas, sessões e permissão
│   └── trilha.py            ← corrente de hashes: prova que ninguém adulterou
├── api/app.py               ← FastAPI: a única porta para o mundo de fora
├── portal/index.html        ← portal de demonstração
└── testes/                  ← test_interligacao, test_acesso, test_trilha
```

O núcleo **não depende de nada externo**. Roda com Python puro, em qualquer
máquina, e é testável sem subir servidor. Só a API precisa de FastAPI.

---

## Login e isolamento entre clientes

Toda rota que toca dado de empresa passa por duas portas, nesta ordem:

1. **Quem é você** — sessão por cookie `httponly`, validada a cada chamada.
2. **Você pode ver esta empresa?** — `acesso.exigir_acesso`, inclusive na
   leitura.

Decisões de segurança que valem saber:

- Senha guardada com **PBKDF2-HMAC-SHA256, 600 mil iterações e salt próprio**
  por conta. Duas pessoas com a mesma senha têm hashes diferentes.
- E-mail inexistente e senha errada dão **a mesma mensagem**, e o login gasta
  o mesmo tempo nos dois casos. Não dá para descobrir quem é cliente do OCEO
  testando e-mails.
- Tentar abrir a empresa de outro cliente devolve **404, não 403**: o sistema
  não confirma nem que aquela empresa existe.
- Papéis: `dono`, `operador` e `leitor`. O leitor não altera nada, e o portal
  esconde os botões de ação para ele.

O banco é SQLite, guardado em `dados/oceo.db` (fora do Git). Trocar por
Postgres é escrever outra classe com os mesmos métodos de
`RepositorioSQLite` — nenhuma regra de negócio muda.

---

## Integridade dos dados (a parte útil da blockchain, sem os problemas dela)

> A documentação completa de segurança — decisão sobre blockchain, LGPD e
> como responder ao cliente — está em `../seguranca/`. Aqui fica só o que
> diz respeito ao código.

Cada fato gravado guarda o **resumo criptográfico do fato anterior**
(SHA-256). Os registros formam uma corrente: alterar qualquer um deles
quebra a corrente a partir dali, e a conferência aponta o registro exato.

Isso responde à pergunta que um cliente grande sempre faz — *"como eu sei
que ninguém mexeu no meu histórico?"* — inclusive quando o "alguém" é o
próprio Grupo Sena. Quem tem a senha do banco consegue mudar uma linha; o
que ele **não** consegue é mudar sem que a conferência acuse.

No portal: **Conferir agora**, no bloco "Integridade dos dados".
Na API: `GET /api/empresas/{id}/integridade`.

O `hash_raiz` é um número de 64 caracteres que resume o período inteiro
**sem revelar nenhum dado**. Guardado mês a mês (e-mail datado, cartório, ou
uma blockchain pública), vira prova de que aqueles registros já existiam
naquela data.

### Por que não uma blockchain de verdade

Foi avaliado e descartado para os dados em si, por três motivos técnicos:

1. **Blockchain não esconde nada.** Ela garante que o registro não mudou,
   não que ele seja secreto. O sigilo continua vindo de criptografia e
   controle de acesso — que é onde o esforço tem que estar.
2. **Espalhar o dado é o contrário de protegê-lo.** Uma rede replica cada
   registro em vários nós. Folha, faturamento e apuração do cliente em
   várias cópias é mais superfície de ataque, não menos.
3. **Imutabilidade briga com a LGPD.** O art. 18 dá ao titular o direito de
   eliminação. Se o dado é imutável por construção, não há como cumprir.

A corrente de hashes entrega o que interessa — a prova de não-adulteração —
e deixa o dado onde ele pode ser corrigido e apagado quando a lei manda.
Se um dia fizer sentido publicar a prova numa rede pública, publica-se só o
`hash_raiz`: um número, sem dado de cliente nenhum dentro.

---

## O que falta para virar produto

Em ordem de quem entra primeiro:

1. **As regras de cada pilar por dentro.** O que existe são as reações
   *entre* pilares; falta o trabalho *dentro* de cada um (apuração real,
   conciliação bancária, geração de contrato).
2. **Integrações.** Open Finance (GF), WhatsApp Business API (GM), e a
   entrada dos painéis de BI que já rodam hoje (GC).
3. **Recuperação de senha** por e-mail, e segundo fator para o papel `dono`.
4. **Limite de tentativas de login**, para travar ataque de força bruta.
5. **Postgres** no lugar do SQLite, quando houver mais de um servidor.

## Decisões técnicas e por quê

- **Python.** O produto é pesado em dados (BI, contábil, fiscal) e em agentes
  de IA, que é onde o Python é mais forte. Também é o que já está instalado
  na máquina do Gilberto.
- **Eventos em vez de chamadas diretas.** Um pilar que chama outro cria
  dependência rígida: mexer em um quebra o outro, e não dá para vender
  separado. Com eventos, cada pilar é autônomo.
- **Núcleo sem dependência externa.** Framework envelhece; regra de negócio
  não. O miolo tem que sobreviver à troca de framework.
- **SQLite primeiro.** Vem na stdlib, não exige servidor de banco e deixa o
  teste rodar com banco em memória. A troca por Postgres já está isolada numa
  classe só.
- **Sessão em cookie `httponly`**, e não token no JavaScript: se alguém
  conseguir injetar script na página, não consegue ler a sessão.
