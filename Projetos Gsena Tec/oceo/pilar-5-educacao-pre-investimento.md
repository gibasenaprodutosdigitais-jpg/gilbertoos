# OCEO — Pilar 5: Educação Pré-Investimento (rascunho, 05/ago/2026)

> **Código: GI.** Renomeado de "Criação de Renda Passiva" pra "Educação
> Pré-Investimento" (decisão do Gilberto, 05/ago/2026) — o nome novo já
> reflete o escopo real depois da decisão regulatória abaixo: o sistema
> educa e prepara o empresário pra investir, não promete criar renda nem
> recomenda produto individualizado.
>
> **Preço do OCEO:** R$ 3.500/mês, simples, mas completo. Ver também o
> material consolidado (`oceo-cinco-pilares-2026-08-05.html`).

> Mercado financeiro — só entra em ação depois que a empresa já tem o
> ponto de equilíbrio (Pilar 2) coberto pela reserva.

## Pré-requisito: ativação em cadeia com o Pilar 2

Esse pilar **não corre solto** — só ativa quando o Pilar 2 (Gestão
Financeira) confirma que o fundo de reserva de 3 meses de ponto de
equilíbrio (`pilar-2-gestao-financeira.md`, item 6) já está completo **e**
o caixa livre tem margem sobrando. Antes disso, o sistema não orienta
investimento nenhum — segurança do negócio vem antes de rentabilizar
sobra.

## Ponto de atenção regulatório — o mais sensível dos 5 pilares até agora

Antes de detalhar a funcionalidade, dois achados de pesquisa que **mudaram
como esse pilar precisa ser desenhado**, não só uma ressalva de rodapé
como nos outros pilares:

### 1. CVM já regula justamente isso — robo-advisor com recomendação por perfil

CVM Resolução 19/2021 e 21/2021: **prestação de consultoria de valores
mobiliários por sistema automatizado/algoritmo está sujeita às mesmas
obrigações do consultor humano** — rotular como "sugestão" não isenta a
responsabilidade regulatória. Citação direta da norma: *"a prestação de
serviço de consultoria de valores mobiliários por meio de sistemas
automatizados ou algoritmos está sujeita às obrigações e regras previstas
nesta Instrução e não mitiga as responsabilidades do consultor quanto à
orientação, recomendação e aconselhamento prestados."* Isso é
praticamente a descrição do que foi pedido originalmente: recomendação
personalizada com base em **perfil comportamental do investidor** — é
exatamente o gatilho que a CVM usa pra classificar como consultoria
regulada, independente do rótulo "sugestão, não direcionamento".

### 2. A licença AAI do Gilberto tem uma trava de exclusividade

Agente Autônomo de Investimento (ANCORD/CVM) **só pode estar vinculado a
UMA corretora por vez pra renda variável** (a exclusividade foi
flexibilizada só pra distribuição de cotas de fundos, não pra renda
variável em geral). Isso significa que "linkar este pilar a XP, BTG,
debêntures..." simultaneamente, como recomendação personalizada,
ultrapassaria o que a licença AAI do Gilberto cobre sozinha — AAI não dá
lastro pra representar duas corretoras ao mesmo tempo.

### Decisão (05/ago/2026): educacional/informacional pura — e o pilar muda de nome por causa disso

O sistema mostra dado de mercado, explica tipo de produto, orienta
alocação **de forma genérica — por categoria de perfil de investidor em
geral, não individualizada pro CNPJ/CPF específico daquela empresa** (ex.:
"perfis conservadores costumam considerar X tipo de produto", não "você
deveria alocar R$ X em Y"), e direciona o cliente a abrir conta e decidir
por conta própria ou com profissional. **Não vincula corretora como
parceira nem recebe comissão por indicação** — XP, BTG e outras aparecem
como referência/exemplo de onde o mercado oferece o produto, não como
parceria formal do OCEO. Registro como consultor CVM fica descartado por
ora — não avança sem decisão nova. **"Educação Pré-Investimento" descreve
melhor esse escopo do que "Criação de Renda Passiva"**, que soava como
promessa de resultado — daí a troca de nome.

## Funcionalidades

### 1. Gatilho de ativação

- Dispara quando o Pilar 2 confirma reserva completa (3 meses de ponto de
  equilíbrio) **e** caixa livre com margem
- Regra: havendo margem, o sistema orienta — de forma educacional — que
  destinar uma parcela (referência: **mínimo 10%**) desse caixa livre pra
  investimento costuma ser um caminho considerado; não é valor prescritivo
  vinculado a um produto específico

### 2. Perfil comportamental do investidor — genérico, não individualizado

- Levantamento de perfil (suitability): conservador, moderado, arrojado
- O perfil filtra **categoria de conteúdo educacional mostrado**, não gera
  recomendação individualizada de produto/valor pro CNPJ específico — é a
  linha que mantém isso fora da definição de consultoria de valores
  mobiliários da CVM (seção acima)

### 3. Universo de produtos apontados

- Renda fixa/variável — tipos de produto explicados, com XP, BTG e outras
  citadas como exemplo de onde existem no mercado (sem parceria/comissão)
- Debêntures disponíveis no mercado
- Criptoativos
- Orientação genérica sobre abertura de conta em cada tipo de instituição
  — informacional, o sistema não executa nem intermedeia a operação

### 4. Ferramentas de análise

- Fibonacci e outras ferramentas técnicas de análise já usadas no mercado,
  aplicadas via IA, sobre dado de mercado público — não sobre a posição
  individual do cliente como recomendação de compra/venda
- Toda saída do sistema vem com aviso explícito: **conteúdo educacional,
  não recomendação individualizada de investimento**

## Comparativo de custo — com uma ressalva importante

**Analista de Fundos de Investimento (fato citável, CAGED):** R$
5.335,73/mês médio, via salario.com.br, base 14.937 profissionais
admitidos/desligados no Brasil em regime CLT nos últimos 12 meses. É o CBO
mais próximo — **não existe CAGED pra "Assessor de Investimentos"/AAI
porque esse profissional normalmente não é CLT**: trabalha como autônomo
comissionado pela corretora (é por isso que o próprio Gilberto atua como
AAI, não como funcionário). Então esse comparativo é mais artificial que
os dos outros pilares — vale registrar isso no pitch, não esconder.

Com o mesmo fator de encargos (~80%): **R$ 9.604,31/mês** de custo total,
contra R$ 3.500 do OCEO — economia de R$ 6.104,31 (63,6%). Mas o argumento
de venda real aqui provavelmente não é "substitui um analista CLT" — é
"dá acesso a educação financeira estruturada que a PME hoje simplesmente
não tem, ponto", isso pesa mais que o número de economia.

## Próximo passo

1. Redigir o texto padrão de disclaimer (conteúdo educacional, não
   recomendação individualizada) que aparece em toda saída deste pilar —
   validar a redação exata com o jurídico do OCEO antes de usar em
   produto.
2. Transformar em peça visual, formato equivalente aos demais pilares.
