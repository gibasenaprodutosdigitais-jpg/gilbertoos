# OCEO — Pilar 2: Gestão Financeira (rascunho, 05/ago/2026)

> **Código: GF.** ERP financeiro integrado à contabilidade (Pilar 1) e aos
> bancos, pra dar ao empresário clareza sobre a real situação financeira
> da empresa.
>
> **Atualização de preço (05/ago/2026):** mensalidade do OCEO mudou de
> R$ 2.500 pra **R$ 3.500 (simples, mas completo)** — números abaixo ainda usam
> R$ 2.500. Recalculado no material consolidado
> (`oceo-cinco-pilares-2026-08-05.html`).

## Mercado-alvo (decisão do Gilberto, 05/ago/2026)

PME com **faturamento acima de R$ 50.000/mês**. Isso baliza tanto a regra
do fundo de reserva (abaixo) quanto o comparativo de custo — é a faixa de
empresa que já sente falta de gestão financeira de verdade, mas ainda não
tem caixa pra contratar um diretor financeiro próprio.

## Relação com o Pilar 1 — quem faz o quê, pra não duplicar escopo

O setor **Contábil** do Pilar 1 já é o motor: lançamentos, conciliação
bancária, balancete, DRE bruto, margem de contribuição, ponto de
equilíbrio, EBITDA (ver `pilar-1-contabilidade-bi.md`). O Pilar 2 **não
reprocessa isso** — ele é a camada de **leitura, decisão e planejamento**
em cima desse mesmo dado, somando o que vem direto do banco antes mesmo de
virar lançamento formal. Pilar 1 apura o número; Pilar 2 explica o que ele
significa e o que fazer com ele.

## 1. Integração bancária

- Conexão via Open Finance (ou extrato manual como fallback) com as contas
  da empresa
- Leitura de entradas e saídas em tempo real
- Status cruzado: "a receber" x "recebido", "a pagar" x "pago" — contra o
  que a contabilidade (Pilar 1) já lançou
- **Depende de validação técnica**: quais bancos entram na primeira fase,
  custo de integração Open Finance Brasil, compliance regulatório junto ao
  Banco Central — mesma cautela já registrada pra integração RFB no Pilar 1

## 2. Leitura simples do Balanço e Balancete

- Tradução do balanço/balancete técnico pra linguagem que o empresário
  entende — o que cada linha significa no dia a dia do negócio, não só o
  termo contábil
- Comparativo período a período (mês x mês, trimestre, ano)

## 3. DRE explicado

Cada indicador abaixo vem com **explicação em linguagem simples do que
significa e por que importa** — não só o número solto:

- Caixa livre
- Caixa circulante
- Margem de contribuição
- EBITDA
- ROI
- Valor do negócio (valuation)

## 4. Alertas e indicadores de movimentação financeira

- Alerta de entrada/saída fora do padrão histórico
- Indicador de saúde de caixa (ex.: quantos meses de operação o caixa atual
  cobre, no ritmo de queima atual)
- Cruzamento banco x contabilidade: o que entrou/saiu na conta x o que o
  Pilar 1 já apurou — divergência vira alerta

## 5. Transparência PF x PJ — o verdadeiro impacto do gasto pessoal

Aprofunda o princípio já registrado (`ideias-produto.md`, item 1):

- Todo gasto pessoal feito pela conta da empresa é identificado e
  sinalizado
- O sistema mostra o **impacto real** desse gasto: quanto ele tira do caixa
  livre, do fundo de reserva (item 6), ou quanto atrasa o ponto de
  equilíbrio do mês
- Comparativo "com controle/planejamento" x "sem controle" — o sistema
  simula a consequência, mas **não decide por ele** (mesmo princípio já
  registrado, `ideias-produto.md` item 3: o sistema orienta, não decide)

## 6. Política de fundo de reserva

**Decidido (05/ago/2026): três meses de ponto de equilíbrio é o padrão**,
não exemplo — coerente com o mercado-alvo (PME R$ 50.000+/mês de
faturamento).

- Parte do resultado financeiro é direcionada automaticamente pra um fundo
  de reserva da empresa
- Meta padrão: **3 meses de ponto de equilíbrio** acumulados, pra segurança
  do negócio
- Painel mostra: quanto já tem acumulado no fundo, quantos meses de ponto
  de equilíbrio isso cobre hoje, e quanto falta pra bater a meta

## Comparativo de custo — dois perfis

O pilar entrega dois níveis de valor, e vale mostrar os dois no pitch:

**Analista Financeiro** — perfil já usado no comparativo central do
business plan geral (CAGED, base R$ 4.883,27/mês): **R$ 8.789,90/mês**
custo total com encargos. É o piso do argumento — o que qualquer PME já
reconhece como custo de ter alguém cuidando disso.

**Diretor Financeiro (fato citável, CAGED):** R$ 24.106,54/mês médio, via
salario.com.br — piso R$ 1.621,00, teto R$ 57.722,79, base 2.273
profissionais admitidos/desligados no Brasil em regime CLT nos últimos 12
meses (maio/2025–abr/2026). Com o mesmo fator de encargos (~80%): **R$
43.391,77/mês** de custo total. Esse é o teto do argumento: **o pilar
entrega leitura de DRE, ROI, valuation e política de reserva — decisão de
nível diretoria**, não só lançamento operacional. É isso que justifica
comparar com o cargo, não só com o analista.

| Perfil | Salário base | Custo total c/ encargos | x OCEO (R$ 2.500) | Economia |
| --- | --- | --- | --- | --- |
| Analista Financeiro (CAGED) | R$ 4.883,27 | R$ 8.789,90 | R$ 2.500 | R$ 6.289,90 (71,6%) |
| Diretor Financeiro (CAGED) | R$ 24.106,54 | R$ 43.391,77 | R$ 2.500 | R$ 40.891,77 (94,2%) |

**Leitura pro pitch:** uma PME de R$ 50.000+/mês de faturamento não
contrata um Diretor Financeiro — não cabe no caixa. O OCEO entrega esse
nível de clareza (DRE explicado, ROI, valuation, fundo de reserva
estratégico) pelo preço que nem cobre metade de um Analista Financeiro
júnior. É o gap entre "o que a PME precisa" e "o que ela consegue pagar"
que o pilar preenche.

## Premissas em aberto

1. Viabilidade técnica e custo da integração Open Finance — quais bancos
   na primeira fase, e se há custo por transação/conta que afeta a margem
   do OCEO.

## Próximo passo

1. Validar com o time técnico a integração Open Finance (mesmo tipo de
   validação já pendente pra RFB/Sefaz no Pilar 1).
2. Transformar em peça visual (mockup do painel DRE explicado + indicador
   de fundo de reserva), formato equivalente ao Pilar 1.
