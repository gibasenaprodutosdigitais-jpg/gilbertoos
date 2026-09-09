# OCEO — Ideias de produto (backlog bruto)

> Nota de separação: o GilbertoOS é a ilha pessoal de conteúdo/posicionamento
> do Gilberto (ver `CLAUDE.md` da raiz). O OCEO é outro projeto — o sistema
> de gestão empresarial do Grupo Sena. Este arquivo existe **fora** de
> `_memoria/` e `conhecimento/` de propósito, pra não misturar com a base
> que alimenta carrossel/reels/ideias. Guardado aqui a pedido direto do
> Gilberto em 19/jul/2026, pra não perder as ideias até ele levar pro time
> técnico do OCEO.

## Ideias registradas — 19/jul/2026

### 1. Centro de custos financeiros (separação PF x PJ)

A maioria dos empresários não consegue separar as finanças da empresa das
finanças pessoais. O sistema deve fazer essa separação **por eles**, de
forma automática. A clareza visual disso no sistema deve fazer o próprio
empresário perceber, na prática, que não pode misturar as duas contas — é
a base de uma boa gestão, tanto pessoal quanto da empresa. Aprofundado no
Pilar 2 (05/ago/2026): o sistema não só sinaliza o gasto pessoal, mostra o
**impacto real** dele no caixa livre e no ponto de equilíbrio. Detalhado em
`pilar-2-gestao-financeira.md`.

### 2. Dashboard de resultados com alertas de consequência

O dashboard de resultados deve ter:
- **Gráficos separados por área** (não tudo misturado numa visão só).
- **Alertas mostrando a consequência** caso o empresário não siga as
  orientações que o próprio sistema deu.

### 3. Princípio de uso: o sistema orienta, não decide

Mesmo com os alertas de consequência, **a decisão final é sempre do
empresário**. O sistema mostra o risco e a consequência prevista, mas não
trava a operação nem decide por ele — só informa com clareza pra ele decidir
com mais consciência.

### 4. Escopo híbrido completo do sistema

O OCEO deve cobrir o ciclo inteiro do negócio, em blocos:

- **Operacional** — início das operações, contratações, parcerias,
  fornecedores.
- **Financeiro / Contábil** — custos, despesas, parte contábil e
  financeira, ponto de equilíbrio, margem de contribuição, lucro líquido,
  EBITDA, valor do negócio (valuation).
- **Jurídico**.
- **Marketing e Vendas** — tráfego pago, com funil de atendimento.
- **Investimentos** — sugestões de aplicação (B3, forex, criptoativos,
  mini dólar, mini índice etc.), com riscos e possibilidades apuradas no
  **fechamento mensal dos resultados**.

**Ponto levantado na conversa (não é ideia do Gilberto, é observação a
verificar com o time técnico/jurídico do OCEO):** sugestão de investimento
(B3, forex, cripto) é atividade regulada pela CVM. O Gilberto já tem
habilitação de **Agente Autônomo de Investimento (AAI)** pela ANCORD (ver
`_memoria/quem-e-gilberto.md`), o que dá lastro pra esse módulo — mas vale
definir formalmente se a sugestão do sistema é educacional/genérica ou
recomendação personalizada, porque a exigência regulatória muda.
**Aprofundado no Pilar 5 (05/ago/2026)**: confirmado que recomendação por
perfil comportamental do investidor cai na definição de consultoria de
valores mobiliários da CVM (Resolução 19/2021), e que a licença AAI do
Gilberto só cobre uma corretora por vez pra renda variável — não cobre
"linkar XP e BTG" simultaneamente como recomendação personalizada.
Decidido: rota educacional/genérica — pilar renomeado pra **Educação
Pré-Investimento**. Detalhado em `pilar-5-educacao-pre-investimento.md`.

### 5. Análise comportamental no módulo de RH

O módulo de **Recursos Humanos** deve incluir **análise comportamental**
aplicada a:
- Entrevistas.
- Contratações.
- Departamento pessoal.

**Casa definida (05/ago/2026):** virou o setor RH dentro do Pilar 1
(Contabilidade/BI), junto com Contábil, Fiscal, DP e Legalização — atração,
seleção, entrevista virtual por IA, análise comportamental e apoio na
negociação de salário/comissão/bônus. Detalhado em
`pilar-1-contabilidade-bi.md`.

### 6. Contabilidade consultiva (Pilar 1) — 05/ago/2026

Aplicação direta do princípio #3 ("o sistema orienta, não decide") ao módulo
de Contabilidade/BI: o OCEO **não substitui** o escritório de contabilidade
do cliente nem compete em preço com ele. O empresário continua pagando o
contador normalmente. O sistema dá **visibilidade** sobre o que já é
serviço de terceiro — status da folha, guias pagas/pendentes, licenças a
vencer — e alerta quando algo foge do prazo ou do esperado, sem processar
por baixo. Objetivo final: o empresário poder **questionar o próprio
contador com informação clara na mão**, não só ver o dado passivamente —
o sistema traduz o alerta técnico numa pergunta de cobrança que o
empresário sabe fazer. Detalhado em `pilar-1-contabilidade-bi.md`.

### 7. Fundo de reserva atrelado ao ponto de equilíbrio (Pilar 2) — 05/ago/2026

Parte do resultado financeiro da empresa deve ser direcionada
automaticamente pra um fundo de reserva, com meta padrão de **3 meses de
ponto de equilíbrio** — fixado assim pelo mercado-alvo (PME R$ 50.000+/mês
de faturamento) — segurança financeira do negócio, não só acúmulo de caixa
sem propósito. Detalhado em `pilar-2-gestao-financeira.md`.

### 8. Jurídico consultivo (Pilar 3) — 05/ago/2026

Mesmo modo operante do Pilar 1: o OCEO não substitui advogado com OAB pra
executar (ajuizar ação, representar em juízo) — funciona como **advogado
consultivo interno full-time**, pra geração e análise de contrato, busca de
oportunidade legal de redução de custo tributário/financeiro na estrutura
do negócio, e esclarecimento jurídico simples do dia a dia. Estratégico
porque PME pequena/média não tem e não contrata advogado hoje. Detalhado em
`pilar-3-juridico.md`.

### 9. Marketing e vendas como agência interna (Pilar 4) — 05/ago/2026

Preenche o bloco "Marketing e Vendas" já esboçado no item 4 original: o
OCEO faz social media (copy, carrossel, imagem, publicação manual/
programada) da empresa **e** do empresário, programa tráfego pago junto às
plataformas, e atende via agente de IA do funil até o fechamento — mesmo
quando o negócio fecha fisicamente, o fechamento entra no sistema. Regra
de quando sair do escopo: campanha específica → assessoria externa; dia a
dia e lead orgânico → o pilar cobre sozinho. Detalhado em
`pilar-4-marketing-vendas.md`.

### 10. Educação Pré-Investimento, ex-"renda passiva" (Pilar 5) — 05/ago/2026

Renomeado de "Criação de Renda Passiva" pra **Educação Pré-Investimento**
(decisão do Gilberto, 05/ago/2026) — o nome novo reflete o escopo real
depois do achado regulatório: **era o pilar de maior risco dos cinco**,
porque recomendação individualizada por perfil ativa a exigência de
registro como consultor de valores mobiliários na CVM (Resolução
19/2021), e a licença AAI do Gilberto não cobre recomendar múltiplas
corretoras (XP + BTG) ao mesmo tempo — só uma por vez pra renda variável.
**Decidido: rota educacional/genérica** — só ativa depois que o fundo de
reserva do Pilar 2 está completo, orienta (sem individualizar por CNPJ/CPF
nem vincular corretora como parceira) que destinar uma parcela do caixa
livre (referência: mínimo 10%) costuma ser um caminho considerado, com
Fibonacci e outras ferramentas técnicas via IA sobre dado de mercado
público. Detalhado em `pilar-5-educacao-pre-investimento.md`.

---

*Lista em aberto — continuar adicionando conforme o Gilberto for ditando
novas ideias.*
