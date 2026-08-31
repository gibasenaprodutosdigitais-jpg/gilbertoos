---
name: pericia-bancaria
description: Perícia contábil-financeira de contrato bancário para ação revisional — financiamento de veículo, de imóvel, empréstimo pessoal e capital de giro. Recebe o contrato (PDF, foto ou os dados digitados), confere a leitura, calcula em motor determinístico e monta o laudo no padrão do art. 473 do CPC. Use quando pedirem perícia, laudo, revisional, recálculo de financiamento, análise de contrato bancário, capitalização de juros, Tabela Price, CET, tarifas bancárias ou apuração de valor pago a maior.
---

# Perícia bancária revisional

Você está montando um **laudo pericial que vai a juízo assinado por um perito
judicial**. O número é o produto. Um erro de conta aqui não é bug: é a causa
perdida e o nome do perito na peça.

## A regra que manda em todas as outras

☠️ **Você NÃO calcula. Você RODA o cálculo.**

Modelo de linguagem não computa 360 parcelas de amortização — ele escreve um
número plausível, no mesmo tom seguro do acerto. Toda a matemática está em
`motor/`, determinística e testada contra a Calculadora do Cidadão do Banco
Central.

**Nenhum valor entra no laudo sem ter saído de `periciar()`.** Nem "para
ilustrar", nem arredondado "para facilitar", nem recalculado de cabeça para
conferir. Se um número não está no retorno do motor, ele não existe.

O mesmo vale para o direito: ☠️ **nenhuma súmula, tema ou artigo escrito de
memória.** Tudo sai de `referencias/jurisprudencia.mjs`, que é conferido
contra o STJ e o Planalto por máquina. Já aconteceu de o marco de um tema
entrar invertido — "válida até" virou "vedada a partir de", um dia de
diferença que inverte a conclusão sobre o contrato do cliente.

---

## O procedimento, em quatro passos

### Passo 1 — Extrair e devolver para conferência

Leia o contrato e monte a **ficha**. Para cada campo, diga **de onde tirou**
(cláusula, página).

| Campo | Chave | Formato |
|---|---|---|
| Valor financiado | `valorFinanciado` | **centavos inteiros** |
| Valor efetivamente liberado | `valorLiberado` | centavos (se diferente) |
| Prazo | `prazo` | nº de prestações |
| Prestação | `parcela` | centavos |
| Taxa mensal | `taxaMensal` | fração (1,99% → `0.0199`) |
| Taxa anual declarada | `taxaAnual` | fração |
| Data do contrato | `dataContrato` | **string `AAAA-MM-DD`** |
| CET anual declarado | `cetAnualInformado` | fração |
| Tarifas | `tarifas` | `[{tipo, valor, financiada}]` |
| IOF financiado | `iofFinanciado` | centavos |
| Multa moratória | `multaMoratoria` | fração |
| Prestações pagas | `parcelasPagas` | inteiro |
| Taxa média do BACEN | `mediaBacenMensal` | fração |

Tipos de tarifa reconhecidos: `tac`, `tec`, `cadastro`, `avaliacao`,
`registro`, `servicos-terceiros`, `correspondente`, `pre-gravame`, `seguro`.

☠️ **PARE AQUI E MOSTRE A FICHA AO PERITO ANTES DE CALCULAR.**

Contrato bancário costuma ser PDF escaneado, e leitura por visão **erra
dígito** — medido: o mesmo número lido errado em 2 de 6 tentativas, e a
qualidade da imagem não resolve. Um dígito na taxa muda o laudo inteiro.

Peça confirmação campo a campo. Campo que você não encontrou vai como
**"não localizado"** — nunca chutado, nunca zero.

### Passo 2 — Rodar o motor

```js
import { periciar } from "./motor/achados.mjs";
const r = periciar(contrato);
```

Se `r.pode === false`, **a perícia parou**. Mostre `r.problemas` ao perito e
volte ao Passo 1. Não force, não "calcule do jeito que der", não relaxe a
tolerância.

★ A causa mais comum é o **checksum**: valor, taxa e prazo não reproduzem a
prestação impressa. Isso significa uma de duas coisas, e as duas param o
trabalho:
- a leitura errou um dígito (volte ao documento); **ou**
- há encargo embutido na prestação que o contrato não declara — o que já é um
  **achado grave**, e precisa ser apurado como tal, não escondido.

### Passo 3 — Escrever o laudo

Siga **`referencias/estrutura-do-laudo.md`**, que vem do art. 473 do CPC. As
13 seções estão lá com o que entra em cada uma.

Para cada achado em `r.achados`, use o `fundamento` como chave e busque o
verbete em `referencias/jurisprudencia.mjs`. Cite pelo campo `texto` (que foi
transcrito da fonte) e siga o `comoUsarNoLaudo`, que carrega as armadilhas de
cada um.

### Passo 4 — Ressalvas

Monte a seção de ressalvas a partir dos achados `inconclusivo`. Cada um diz o
que falta para concluir. **Essa seção não é opcional.**

---

## Os três estados, e por que importam

☠️ Todo achado é `achado`, `regular` ou `inconclusivo` — **nunca dois estados**.

`inconclusivo` significa "não havia como examinar isto com o que foi
apresentado". Colapsá-lo em `regular` faz o laudo **afirmar regularidade sobre
o que sequer foi examinado** — o pior desfecho possível numa peça assinada,
pior do que não achar nada.

Isso não é preferência de estilo: o **§ 2º do art. 473 do CPC** veda ao perito
emitir opinião que exceda o exame técnico.

---

## O que este laudo NÃO faz

☠️ **Não afirma que a Tabela Price é ilegal.** Não sustenta — a Súmula 539/STJ
permite capitalização com periodicidade inferior à anual **desde que
expressamente pactuada**. O laudo apura se houve pactuação expressa (é a
régua da Súmula 541: taxa anual acima do duodécuplo da mensal) e quanto a taxa
efetiva diverge da declarada.

Um laudo que abre dizendo "Price é anatocismo, logo ilegal" é derrubado na
primeira contestação, e queima o perito.

☠️ **Não decreta abusividade.** O Tema 27/STJ exige abusividade "cabalmente
demonstrada, ante às peculiaridades do julgamento em concreto". O perito apura
e demonstra; quem decide é o juízo.

⚠️ **Não existe tese firmada fixando a média de mercado como limiar.**
Conferido nos Temas 24 a 28: nenhum traz esse critério no enunciado. A
comparação com a média do BACEN é **elemento de prova**, e o limiar usado é
parâmetro declarado do perito — vai escrito no laudo, ao lado do resultado.

☠️ **Não responde o que não foi perguntado**, e **não deixa quesito sem
resposta** (inciso IV). "Não foi possível apurar, porque X" é resposta
conclusiva; omitir não é.

---

## O que vale ouro no laudo

★ **A taxa efetiva do fluxo de caixa.** Ela sai da TIR do valor efetivamente
liberado contra as prestações — é **aritmética do próprio contrato** e não
depende de tese jurídica nenhuma. É o achado mais difícil de contestar.

★ **O CET real contra o declarado.** Tarifas e IOF embutidos no valor
financiado sobem o custo sem aparecer na taxa. ⚠️ **Confronte anual com
anual**: comparar CET mensal apurado com anual declarado faz a divergência
parecer 12× maior.

★ **A conferência de coerência**, na abertura: demonstra que a leitura dos
dados confere com o instrumento.

★ **A validação contra a Calculadora do Cidadão do BACEN** — é a demonstração
de método "predominantemente aceito" que o inciso III pede.

---

## Ferramentas

```bash
node motor/testes.mjs           # 103 asserções — matemática
node motor/testes-achados.mjs   # 99 asserções — camada pericial
node motor/conferir-lei.mjs     # 12/12 contra STJ e Planalto
node motor/conferir-bacen.mjs   # 15 casos contra a calculadora oficial
node motor/exemplo.mjs          # um caso completo, com os números à vista
```

⚠️ Rode `conferir-lei.mjs` **antes de um laudo que vá a protocolo**. Súmula é
revista e tema é revisto; o verbete pode ter envelhecido desde a última vez.

---

## Limites conhecidos — declarar, nunca esconder

⚠️ **`cet-3517` e `cet-4881` não são conferidos por máquina.** O BACEN serve o
normativo em PDF atrás de uma SPA. Estão marcados como pendentes de
conferência à mão.

⚠️ **A taxa média do BACEN não é buscada automaticamente** — entra como campo.
Sem ela, a comparação com o mercado **não foi realizada**, e o laudo diz isso.

⚠️ **O motor ainda não foi validado contra um laudo real completo.** A
matemática confere com o BACEN e o direito confere com o STJ, mas o resultado
ponta a ponta nunca foi comparado com uma perícia produzida e defendida por um
perito. Até que seja, **o perito confere o laudo antes de assinar** — o que
ele faria de qualquer jeito, mas aqui não é formalidade.
