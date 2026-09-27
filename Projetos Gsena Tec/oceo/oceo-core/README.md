# OCEO — núcleo de interligação dos cinco pilares

Este é o **miolo** do OCEO: o código que faz os cinco pilares conversarem
entre si em vez de virarem cinco sistemas separados com cinco cadastros do
mesmo cliente.

> Estado: **fundação funcional**, com API e portal de demonstração em cima.
> Ainda não tem banco de dados, login nem as regras de cada pilar por
> inteiro. O que existe aqui é a estrutura em que esse resto se encaixa.

---

## Para ver funcionando em 30 segundos

```bash
cd oceo-core
python3 testes/test_interligacao.py     # prova, no terminal, que os pilares conversam
python3 api/app.py                      # sobe o portal em http://127.0.0.1:8000
```

No portal: crie a empresa de demonstração, ligue e desligue pilares e use os
botões de "disparar um fato". Cada fato é publicado em nome de **um** pilar,
e quem reage é decidido pelo sistema, não pelo botão.

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
├── api/app.py               ← FastAPI: a única porta para o mundo de fora
├── portal/index.html        ← portal de demonstração
└── testes/test_interligacao.py
```

O núcleo **não depende de nada externo**. Roda com Python puro, em qualquer
máquina, e é testável sem subir servidor. Só a API precisa de FastAPI.

---

## O que falta para virar produto

Em ordem de quem entra primeiro:

1. **Persistência.** Hoje tudo vive em memória e some quando o servidor cai.
   Trocar por Postgres é substituir o `Sistema` — o resto do código não muda,
   porque todo mundo conversa através dele.
2. **Login e multiusuário.** Hoje qualquer um vê qualquer empresa.
3. **As regras de cada pilar por dentro.** O que existe são as reações
   *entre* pilares; falta o trabalho *dentro* de cada um (apuração real,
   conciliação bancária, geração de contrato).
4. **Integrações.** Open Finance (GF), WhatsApp Business API (GM), e a
   entrada dos painéis de BI que já rodam hoje (GC).
5. **Auditoria.** O barramento já guarda o histórico de fatos; falta expor
   isso como trilha de auditoria para o cliente.

## Decisões técnicas e por quê

- **Python.** O produto é pesado em dados (BI, contábil, fiscal) e em agentes
  de IA, que é onde o Python é mais forte. Também é o que já está instalado
  na máquina do Gilberto.
- **Eventos em vez de chamadas diretas.** Um pilar que chama outro cria
  dependência rígida: mexer em um quebra o outro, e não dá para vender
  separado. Com eventos, cada pilar é autônomo.
- **Núcleo sem dependência externa.** Framework envelhece; regra de negócio
  não. O miolo tem que sobreviver à troca de framework.
- **Uma instância em memória na API.** É proposital, para demonstração. O
  ponto de troca para banco está isolado num lugar só.
