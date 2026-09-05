# OCEO — Pilar 1 (GC): o painel de BI já existe e já roda pra cliente real

> Complementa `pilar-1-contabilidade-bi.md`. Resolve parte do "Próximo passo
> 4" de lá ("transformar em peça visual — comparativo de custo + mockup do
> painel"): não é mockup teórico, é print de um painel Power BI que o Grupo
> Sena já construiu e já opera para um cliente real — uma rede de franquias
> de serviço com múltiplas unidades (holding + ~24 unidades operacionais).
> Extraído em 06/12/2023, 9 páginas. Isso é evidência de capacidade
> instalada, não uma promessa de produto.

## Por que isso importa pro pitch do OCEO

O Pilar 1 descreve um módulo que faz apuração contábil/fiscal/DP de verdade
e devolve painel gerencial pro empresário. A pergunta óbvia de qualquer
investidor ou cliente é "vocês já fizeram isso, ou é só plano?". A resposta
concreta é: **sim, já fizemos — para uma rede de franquias com holding e
mais de vinte unidades, cobrindo balancete, financeiro, DRE e fluxo de
caixa por unidade, todos os meses, em tempo real.** O que falta não é
construir a capacidade — é empacotar essa capacidade, que hoje vive dentro
da operação do Grupo Sena para um cliente específico, como produto que
qualquer empresário possa assinar.

## Os 9 painéis, o que cada um mostra e a função que cobre no Pilar 1

| # | Painel | O que mostra | Granularidade | Função do Pilar 1 que evidencia |
|---|---|---|---|---|
| 1 | Volume de Compras — Balancetes | Fluxo de volume de compras ao longo do ano, por razão social (gráfico de fluxo/Sankey) | Mensal, por empresa do grupo | "Controle de custos e despesas por centro de custo" |
| 2 | Pagamento a Fornecedores — Balancete | Tabela dinâmica de pagamentos por razão social e mês, com filtro por conta contábil (ICMS, ISS, PIS, COFINS, Simples Nacional, depreciações etc.) | Mensal, por conta contábil e empresa | "Lançamentos contábeis automáticos" + "Balancete... em tempo real" |
| 3 | Receita Contabilizada — Balancetes | Fluxo de receita contabilizada ao longo do ano, por razão social | Mensal, por empresa do grupo | "Controle de entradas (receita/faturamento) por categoria" |
| 4 | Pagamento a Fornecedores — Financeiro (visão fornecedor/cliente) | Ranking de maiores pagamentos por fornecedor/credor, incluindo linhas de imposto (COFINS, IRPJ, CSLL, ISSQN) lançadas como "fornecedor" | Mensal, por fornecedor/credor | "Conciliação de contas a pagar x movimentação real" |
| 5 | Contabilização de Notas Fiscais | Barras de valor de crédito por razão social ao longo dos meses | Mensal, por empresa | "Conciliação bancária (extrato x lançamento)" |
| 6 | DRE Financeiro | Cards de KPI (Receita Total do Ano, Custo Total, Despesa Total, Distribuição de Lucro, Aporte dos Sócios) + tabela por categoria x mês | Anual (cards) e mensal (tabela), consolidado do grupo | "Balancete e DRE gerencial em tempo real" — é literalmente a funcionalidade central do pilar, já rodando |
| 7 | Sobra de Caixa por Unidade | Fluxo de sobra/consumo de caixa por unidade ao longo do ano | Mensal, por unidade operacional | "Margem de contribuição, ponto de equilíbrio" (insumo direto) |
| 8 | Distribuição de Lucros por Unidade | Fluxo de distribuição de lucro por unidade ao longo do ano | Mensal, por unidade operacional | "Controle de retiradas (pró-labore, distribuição de lucro)" |
| 9 | Volume de Compras por Fornecedor — NFE | Ranking dos maiores fornecedores por nota fiscal eletrônica emitida + tabela detalhada mês a mês | Mensal, por fornecedor emitente de NF-e | "Comparativo automático: o que o OCEO apurou x o que o escritório externo reportou" (base de dados pra esse comparativo) |

## Leitura consolidada

- **Cobertura já validada:** dos itens listados em `pilar-1-contabilidade-bi.md` na seção "Contábil — apuração e conciliação", pelo menos seis já têm painel real funcionando: balancete/DRE gerencial, controle de entradas por categoria, controle de custos/despesas por centro de custo, controle de retiradas, conciliação de contas a pagar, e a base de dado que sustenta comparativo com o escritório externo.
- **O que ainda não aparece nesses 9 painéis** (e continua como próximo passo do Pilar 1, não resolvido por este material): módulo de Fiscal com consulta direta à RFB, módulo de DP com folha e eSocial, módulo de RH, e o Departamento de Legalização. Este conjunto de painéis prova a camada **Contábil**, não as outras três camadas do pilar (Fiscal, DP/RH, Legalização).
- **Ferramenta usada:** Microsoft Power BI, publicado via link de compartilhamento (`app.powerbi.com/view?r=...`). Pra virar produto OCEO de verdade, essa ferramenta provavelmente precisa ser embutida (embed) dentro do próprio sistema, não um link avulso do Power BI — ponto técnico a resolver antes de virar módulo comercial, não só um dado de marketing.

## Cuidado de uso

⚠️ Estes 9 painéis vêm de um cliente real do Grupo Sena (rede de franquias,
identificada nos arquivos originais). Pra qualquer uso **externo** deste
material (pitch de investidor, material de venda do OCEO), **generalizar o
nome do cliente e nunca expor valor exato de faturamento, nome de
fornecedor pessoa física ou fragmento de documento** — os PDFs originais
trazem nomes individuais de fornecedores com início de CPF, o que não deve
circular fora do uso interno do Grupo Sena. Uso interno (planejamento do
produto OCEO, como este documento) pode manter a referência ao caso real,
mas sem reproduzir os números linha a linha aqui.

## Próximo passo

1. Confirmar com o Gilberto se este painel real pode ser usado, generalizado, como peça de prova em pitch de investidor do OCEO (ver aviso acima).
2. Mapear, painel por painel, qual desses 9 já pode virar tela do produto OCEO "como está" e qual precisa ser redesenhado pra fazer sentido pra qualquer cliente (não só pra uma rede de franquia com holding).
3. Resolver a questão técnica de embed do Power BI vs. dashboard nativo do OCEO.
4. Estender a mesma lógica de painel pras outras três camadas do Pilar 1 (Fiscal, DP/RH, Legalização), que ainda não têm painel real equivalente a este.
