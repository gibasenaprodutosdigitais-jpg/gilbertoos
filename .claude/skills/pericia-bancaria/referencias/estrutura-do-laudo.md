# Estrutura do laudo pericial

> Esta é a **régua do documento**. Ela não veio de um modelo pessoal de
> perito — veio do **art. 473 do CPC**, conferido contra o Planalto por
> `motor/conferir-lei.mjs` (verbete `cpc-473`). Um laudo no padrão da norma é
> mais defensável do que o modelo de qualquer perito, e não depende do gosto
> de ninguém.

O art. 473 lista quatro requisitos obrigatórios, e eles viram as seções
centrais do documento:

| Inciso | Exige | Seção |
|---|---|---|
| I | exposição do objeto da perícia | **2** |
| II | análise técnica realizada pelo perito | **6** |
| III | indicação do método, esclarecendo-o e demonstrando ser aceito | **5** |
| IV | resposta conclusiva a **todos** os quesitos | **9** |

E dois parágrafos que mandam no tom:

- **§ 1º** — fundamentação em **linguagem simples e com coerência lógica**,
  indicando **como** o perito alcançou suas conclusões. Daí a seção 12
  (origem dos parâmetros) e a exigência de mostrar a conta, não só o resultado.
- **§ 2º** — ☠️ **é vedado ao perito emitir opiniões pessoais que excedam o
  exame técnico.** É a base normativa de tudo que segue: os três estados do
  achado, a recusa a decretar abusividade, e a proibição de responder o que
  não foi perguntado.

---

## As seções

### 1. Identificação
Processo, vara, partes, quem nomeou, o perito, data. Se for parecer
extrajudicial (parte contratante, sem processo), **dizer isso** — parecer de
assistente técnico e laudo de perito nomeado não são a mesma peça, e apresentar
um como o outro compromete quem assina.

### 2. Objeto da perícia — *inciso I*
Uma frase do que se pediu para apurar. ⚠️ Se os quesitos pedirem menos do que
o motor calculou, o excedente **não vira seção nova**: vai para "documentos e
elementos adicionais", ou fica de fora. O § 2º veda ultrapassar os limites da
designação.

### 3. Documentos examinados
Lista do que foi efetivamente lido, com identificação. ☠️ **Não listar
documento que não foi examinado**, mesmo que exista nos autos.

### 4. Dados do contrato
A **ficha conferida** — valor financiado, valor liberado, prazo, prestação,
taxa mensal, taxa anual, data, tarifas, IOF, CET declarado, seguro, encargos
de mora. Cada campo com a **origem** (cláusula, página).

★ Fecha com a **conferência de coerência**: a prestação calculada a partir de
valor, taxa e prazo confere com a impressa no instrumento. É o que demonstra
que a leitura dos dados está correta, e é uma frase forte de abrir laudo.

### 5. Metodologia — *inciso III*
O inciso exige **declarar o método e demonstrar que é aceito**. Então:

- as fórmulas efetivamente usadas, escritas (Price, SAC, desconto racional
  simples, TIR);
- ⚠️ para o método de juros simples, dizer **qual formulação** — "método de
  Gauss" é nome disputado na literatura, e nome não é método;
- a convenção de arredondamento (centavo, com ajuste na última prestação);
- ★ a validação: o cálculo confere com a **Calculadora do Cidadão do Banco
  Central**, ferramenta oficial e pública. É a demonstração de aceitação que o
  inciso III pede, e o assistente técnico do banco não a derruba.

### 6. Análise técnica — *inciso II*
Um bloco por achado, na ordem que o motor devolve. Cada bloco tem:

1. o que foi examinado;
2. **os números**, em quadro;
3. o que eles demonstram;
4. o fundamento (verbete de `referencias/jurisprudencia.mjs`, citado pelo
   texto conferido — **nunca parafraseado**).

☠️ **Três estados, e o `inconclusivo` nunca vira `regular`.** Dizer "regular"
sobre o que não foi examinado é o pior desfecho possível num laudo assinado —
pior que não achar nada. `inconclusivo` diz **o que falta** para concluir.

### 7. Quadro comparativo dos cenários
Tabela: contratado × juros simples × SAC × média de mercado. Prestação, total
pago, juros totais.

⚠️ Em sistema de prestação **variável** (SAC), não existe "diferença por
prestação" — informar a primeira e a última, e dizer por quê.

### 8. Apuração de valores
Diferença por prestação, diferença no contrato inteiro, valor pago a maior no
período já decorrido, valor a compensar no saldo. ⚠️ Separar **pago** de **a
vencer**: são pedidos diferentes (repetição × revisão do saldo).

### 9. Resposta aos quesitos — *inciso IV*
☠️ **A resposta é conclusiva e individual, quesito por quesito.** Quesito sem
resposta é laudo incompleto e é motivo de devolução.

- "Não foi possível apurar, porque X" **é** uma resposta conclusiva. Omitir
  não é.
- Quesito que pede juízo de direito ("a cláusula é abusiva?") se responde no
  plano técnico: apura-se o que dá para apurar e **declina-se a matéria de
  direito**, por força do § 2º.
- Não responder o que não foi perguntado.

### 10. Conclusão
Síntese em linguagem simples (§ 1º): o que se apurou, quanto, e com que grau
de certeza. **Sem adjetivo e sem opinião.**

### 11. Ressalvas e limitações
☠️ **Seção obrigatória neste laudo, não opcional.** Entram aqui:
- o que dependia de documento que não foi apresentado;
- os achados `inconclusivos` e o que os destravaria;
- as premissas adotadas (ex.: taxa média de mercado, limiar de comparação);
- ⚠️ se a taxa média do BACEN não foi informada, dizer que **a comparação com
  o mercado não foi realizada** — e não deixar o silêncio sugerir que foi.

### 12. Origem dos parâmetros
Quadro de procedência, com três níveis. Misturá-los é mentir:

| Nível | Significa |
|---|---|
| **literal** | copiado do contrato ou da fonte oficial e conferido |
| **derivado** | calculado a partir de dados do contrato, com a conta escrita |
| **estimado** | não consta do contrato; premissa do perito, e **declarada como tal** |

### 13. Encerramento
Local, data, nome, título profissional e registro. ⚠️ Perícia contábil exige
**contador registrado no CRC**; se quem assina não for, a peça é parecer
técnico, não laudo contábil, e tem que se apresentar assim.

---

## Proibições que valem para o documento inteiro

☠️ **Nenhum número no laudo pode vir do modelo de linguagem.** Todo valor sai
do motor. Se um número não está no retorno de `periciar()`, ele **não entra no
laudo** — nem "para ilustrar", nem arredondado "para facilitar".

☠️ **Nenhuma citação de lei escrita de memória.** Súmula, tema e artigo saem de
`referencias/jurisprudencia.mjs`, que é conferido contra a fonte. Verbete não
conferido não se cita.

☠️ **Não decretar abusividade.** O perito apura e demonstra; a caracterização é
matéria de julgamento (§ 2º do art. 473, e Tema 27/STJ: abusividade
"cabalmente demonstrada ante as peculiaridades do julgamento em concreto").

☠️ **Não afirmar que a Tabela Price é ilegal.** Não sustenta: a Súmula 539
permite capitalização expressamente pactuada. O que o laudo faz é **apurar se
houve pactuação expressa** e quanto a taxa efetiva diverge da declarada.

☠️ **"R$ 0,00" nunca representa o que não foi calculado.** O que não foi
apurado aparece como "não apurado", com o motivo.
