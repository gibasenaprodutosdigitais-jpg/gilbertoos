# OCEO — Business Plan & Pitch de Investimento (gerado 03/ago/2026)

> Nota de separação: como o `ideias-produto.md`, este arquivo fica **fora** de
> `_memoria/` e `conhecimento/` de propósito — é sobre o produto OCEO, não
> sobre o posicionamento pessoal/conteúdo do Gilberto no Instagram.

## O que foi gerado

Documento de 27 páginas (PDF + HTML) em `saidas/oceo-business-plan-2026-08-03/`,
cópia também em `~/Desktop/OCEO - Business Plan e Pitch de Investimento.pdf`.
Cobre: sumário executivo, o problema, a solução, os 11 módulos, diferenciais
de produto, análise de mercado (TAM/SAM/SOM), análise competitiva, modelo de
negócio, comparativo de custo (profissional CLT x sistema), indicadores
financeiros (CAC/LTV/churn/margem), projeções de clientes e receita (3 anos,
3 cenários), DRE simplificado, ponto de equilíbrio, uso dos recursos, roadmap,
equipe, riscos e anexo de premissas.

## Preço do produto (fato, não premissa)

- Setup (implantação): **R$ 12.500** (único)
- Mensalidade: ~~R$ 2.500/mês~~ → **R$ 3.500/mês, modelo híbrido**
  (atualizado 05/ago/2026, decisão do Gilberto — cobre os 5 pilares
  registrados nesta pasta). **"Híbrido" — minha interpretação de trabalho,
  não confirmada com o Gilberto**: mensalidade fixa + repasse de custo
  variável identificado nos pilares (ex.: conversas WhatsApp Business API
  acima da franquia grátis, Pilar 4; verba de mídia paga sempre à parte,
  Pilar 4). Confirmar essa leitura antes de usar em pitch formal. O PDF de
  27 páginas gerado em 03/ago ainda traz o preço antigo (R$ 2.500) e os
  gráficos/comparativos antigos — precisa de nova geração se for usado
  externamente.

## O comparativo central pedido pelo Gilberto: profissional x sistema

- Salário médio de Analista Financeiro CLT no Brasil: R$ 4.883,27/mês (fonte:
  CAGED via salario.com.br, dados mar/2025–fev/2026).
- Custo total do empregador com encargos trabalhistas (~80%: FGTS, INSS
  patronal, 13º, férias+1/3): **R$ 8.789,90/mês**.
- Economia mensal com o OCEO: **R$ 6.289,90 (71,6%)**.
- Payback do setup (R$ 12.500): **≈ 2 meses** de economia acumulada.
- Economia acumulada em 3 anos: **R$ 213.940 (67,6%)**.

## Premissas do modelo que PRECISAM ser validadas com o Gilberto/time OCEO antes de usar externamente

Todas marcadas explicitamente no documento (badge "Premissa do modelo"), mas as
mais sensíveis ao resultado final são:

- **CAC estimado:** R$ 3.000 — não veio de dado real, é um chute de ordem de
  grandeza pra dar forma ao modelo.
- **Churn mensal estimado:** 3% — gera LTV/CAC de ~31,7x, que é
  extraordinariamente alto pra padrão de SaaS (saudável é ~3x). Documento já
  avisa que isso reflete alta troca de custo de ERP, mas precisa validação
  real assim que houver clientes operando 12+ meses.
- **Custo fixo operacional mensal:** R$ 150.000 — usado pra calcular o ponto
  de equilíbrio de ~71 clientes. Número inventado pra ter uma referência, não
  veio de orçamento real do Grupo Sena/OCEO.
- **Cenários de clientes (Ano 1/2/3):** conservador 25/90/240, base 40/150/400,
  otimista 55/210/560 — construídos a partir de 0,01%–0,05% da SAM estimada,
  não de um funil comercial real.
- **Valor da captação e % de equity oferecido:** deixados **em aberto de
  propósito** — não é decisão que a IA deveria tomar; a seção 13 (Uso dos
  Recursos) só tem o framework de alocação percentual, pronto pra receber os
  números reais quando o Gilberto decidir.

## Dados que SÃO reais e citáveis (fonte externa)

- TAM: 24 milhões de pequenos negócios ativos no Brasil, 95% de todas as
  empresas do país (SEBRAE, 2025).
- Mercado global de ERP: US$ 71,6–92,6 bi (2025), CAGR 9–13% até 2031.
- Preços de concorrentes PME: Bling R$250–800, Conta Azul R$220–650, Omie
  R$450–1.800/mês.
- Totvs/SAP/Oracle dominam 77% do mercado nacional de ERP.

## Diferenciais de produto usados no documento (vêm do backlog real do Gilberto)

Puxados de `ideias-produto.md` (histórico do git, arquivo removido do disco em
alguma limpeza mas recuperável via `git show 64bbe9d:outros-projetos/oceo/ideias-produto.md`):
separação automática PF x PJ, alertas de consequência no dashboard, princípio
"o sistema orienta, não decide", escopo híbrido (operacional/financeiro/
jurídico/marketing/investimentos), módulo de sugestão de investimentos
(lastro: AAI/ANCORD do Gilberto, mas com ponto de atenção regulatório CVM
sinalizado), análise comportamental no módulo de RH.

## Mercado-alvo refinado (05/ago/2026, via Pilar 2)

PME com **faturamento acima de R$ 50.000/mês** — balizou a política de
fundo de reserva (3 meses de ponto de equilíbrio) e o comparativo de custo
do Pilar 2 (`pilar-2-gestao-financeira.md`). Vale usar esse recorte no TAM/
SAM/SOM do business plan geral quando for revisado.

## Próximo passo recomendado

Antes de usar este documento com investidores de verdade: validar as 5
premissas listadas acima com números reais do Grupo Sena/OCEO, e decidir o
valor da captação + equity oferecido (seção 13).
