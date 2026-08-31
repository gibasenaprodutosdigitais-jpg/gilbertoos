// ============================================================================
// MOTOR DE CÁLCULO — perícia contábil-financeira de contrato bancário
// ============================================================================
// Matemática pura. Sem dependência, sem I/O, sem data do relógio.
// Roda em Node e no navegador sem alteração.
//
// ☠️ DINHEIRO É INTEIRO EM CENTAVOS. Nunca float.
//    Um resíduo de float faz o saldo devedor nunca zerar e a última parcela
//    sair com um centavo fantasma que o advogado do banco usa pra dizer que
//    a perícia não fecha.
//
// ☠️ DATA É STRING 'AAAA-MM-DD'. Nunca `new Date`.
//    `new Date('2008-04-30')` é meia-noite UTC e no Brasil volta 29/abr —
//    um contrato do próprio dia 30/04/2008 mudaria de lado no Tema 618.
//
// ⚠️ TAXA é fração decimal (0.0199 = 1,99%), nunca percentual.
// ============================================================================

// ————————————————————————————————————————————————————— dinheiro

/** Reais (número ou string "1.234,56") → centavos inteiros. */
export function emCentavos(valor) {
  if (typeof valor === "number") {
    if (!Number.isFinite(valor)) throw new Error(`valor não é número: ${valor}`);
    // toFixed(4) antes do round mata o erro de float de 1.005 * 100 = 100.49999
    return Math.round(Number((valor * 100).toFixed(4)));
  }
  if (typeof valor !== "string") throw new Error(`valor inesperado: ${valor}`);
  const limpo = valor
    .replace(/\s/g, "")
    .replace(/R\$/gi, "")
    .replace(/\./g, "")
    .replace(",", ".");
  const n = Number(limpo);
  if (!Number.isFinite(n)) throw new Error(`não consegui ler o valor: ${valor}`);
  return Math.round(Number((n * 100).toFixed(4)));
}

/** Centavos inteiros → número em reais (só para exibição, nunca para conta). */
export function emReais(centavos) {
  return centavos / 100;
}

/**
 * Centavos inteiros → "R$ 1.234,56".
 *
 * ☠️ null/undefined/NaN saem como "—", NUNCA como "R$ 0,00". O que não foi
 *    calculado não pode aparecer como zero: num laudo, "R$ 0,00" é uma
 *    afirmação de que nada é devido, e ninguém confere se aquele zero veio
 *    de uma conta ou de um campo vazio. Já saiu "diferença por prestação:
 *    R$ 0,00" para o SAC, onde a resposta certa é "não se aplica".
 */
export function formatarBRL(centavos) {
  if (centavos === null || centavos === undefined || !Number.isFinite(centavos)) {
    return "—";
  }
  const neg = centavos < 0;
  const abs = Math.abs(Math.round(centavos));
  const inteiro = String(Math.floor(abs / 100)).replace(
    /\B(?=(\d{3})+(?!\d))/g,
    ".",
  );
  const cent = String(abs % 100).padStart(2, "0");
  return `${neg ? "-" : ""}R$ ${inteiro},${cent}`;
}

/** Fração → "1,9900 % a.m." (4 casas: taxa de contrato tem 4 casas). */
export function formatarTaxa(fracao, casas = 4) {
  if (fracao === null || fracao === undefined || !Number.isFinite(fracao)) {
    return "—";
  }
  return `${(fracao * 100).toFixed(casas).replace(".", ",")} %`;
}

// ————————————————————————————————————————————————————— datas (string pura)

const DATA = /^\d{4}-\d{2}-\d{2}$/;

export function ehData(s) {
  return typeof s === "string" && DATA.test(s);
}

/** Compara duas datas 'AAAA-MM-DD'. Lexicográfico é suficiente nesse formato. */
export function dataMaiorOuIgual(a, b) {
  if (!ehData(a) || !ehData(b)) throw new Error(`data inválida: ${a} / ${b}`);
  return a >= b;
}

/** Soma meses a 'AAAA-MM-DD', preservando o formato. Dia 31 vira o último do mês. */
export function somarMeses(data, meses) {
  if (!ehData(data)) throw new Error(`data inválida: ${data}`);
  const [a, m, d] = data.split("-").map(Number);
  const total = (a * 12 + (m - 1)) + meses;
  const anoNovo = Math.floor(total / 12);
  const mesNovo = (total % 12) + 1;
  const ultimoDia = new Date(Date.UTC(anoNovo, mesNovo, 0)).getUTCDate();
  const diaNovo = Math.min(d, ultimoDia);
  return `${String(anoNovo).padStart(4, "0")}-${String(mesNovo).padStart(2, "0")}-${String(diaNovo).padStart(2, "0")}`;
}

// ————————————————————————————————————————————————————— conversão de taxas

/** Mensal → anual EFETIVA (capitalizada): (1+i)^12 − 1. */
export function anualEfetiva(mensal) {
  return Math.pow(1 + mensal, 12) - 1;
}

/** Mensal → anual NOMINAL (duodécuplo, sem capitalizar): i × 12. */
export function anualNominal(mensal) {
  return mensal * 12;
}

/** Anual efetiva → mensal equivalente: (1+i)^(1/12) − 1. */
export function mensalDeAnualEfetiva(anual) {
  return Math.pow(1 + anual, 1 / 12) - 1;
}

// ————————————————————————————————————————————————————— Price

/**
 * Parcela do Sistema Francês (Tabela Price), em centavos inteiros.
 *   PMT = PV · i / (1 − (1+i)^−n)
 */
export function parcelaPrice(principal, taxaMensal, prazo) {
  exigirContrato(principal, taxaMensal, prazo);
  if (taxaMensal === 0) return Math.round(principal / prazo);
  const fator = taxaMensal / (1 - Math.pow(1 + taxaMensal, -prazo));
  return Math.round(principal * fator);
}

/**
 * Tabela de amortização do Price.
 * Reproduz o que o banco faz de verdade: parcela arredondada ao centavo,
 * juros arredondados ao centavo a cada mês, e a ÚLTIMA parcela ajustada
 * para zerar o saldo. É esse ajuste que faz a tabela fechar em centavos —
 * sem ele sobra resíduo e a perícia parece errada quando está certa.
 */
export function tabelaPrice({ principal, taxaMensal, prazo, parcela }) {
  exigirContrato(principal, taxaMensal, prazo);
  const pmt = parcela ?? parcelaPrice(principal, taxaMensal, prazo);
  return amortizar({ principal, taxaMensal, prazo, parcelaDe: () => pmt });
}

/** Tabela SAC: amortização constante, parcela decrescente. */
export function tabelaSAC({ principal, taxaMensal, prazo }) {
  exigirContrato(principal, taxaMensal, prazo);
  const amortConstante = Math.round(principal / prazo);
  let saldo = principal;
  return amortizar({
    principal,
    taxaMensal,
    prazo,
    parcelaDe: (k, saldoAtual) => {
      const juros = Math.round(saldoAtual * taxaMensal);
      return (k === prazo ? saldoAtual : amortConstante) + juros;
    },
  });
}

/**
 * Juros simples — método de Gauss (desconto racional simples).
 *   PV = Σ P / (1 + i·k),  k = 1..n   ⇒   P = PV / Σ 1/(1+i·k)
 *
 * ⚠️ A nomenclatura é disputada na literatura revisional. O que está
 *    implementado aqui é o desconto racional simples, que é a formulação
 *    mais citada nos laudos como "método de Gauss". O laudo deve dizer
 *    QUAL fórmula usou — não basta o nome.
 */
export function parcelaJurosSimples(principal, taxaMensal, prazo) {
  exigirContrato(principal, taxaMensal, prazo);
  if (taxaMensal === 0) return Math.round(principal / prazo);
  let soma = 0;
  for (let k = 1; k <= prazo; k++) soma += 1 / (1 + taxaMensal * k);
  return Math.round(principal / soma);
}

/**
 * Tabela do método de juros simples.
 *
 * ☠️ NÃO usa `juros = saldo × i` como o Price. Esse é o erro que derruba o
 *    laudo inteiro: calcular a parcela sem capitalizar e depois montar a
 *    tabela capitalizando é se contradizer dentro da própria peça — o saldo
 *    não zera, a última parcela vira uma bolha e o "método sem capitalização"
 *    acaba custando MAIS caro que o Price. Passou verde na 1ª rodada aqui.
 *
 *    No desconto racional simples, a parcela k traz para o presente o valor
 *    P/(1+i·k) — e é ISSO que amortiza. O juros do período é o resto.
 *    Assim Σ amortizações = Σ P/(1+i·k) = PV, e a tabela fecha por definição.
 */
export function tabelaJurosSimples({ principal, taxaMensal, prazo }) {
  exigirContrato(principal, taxaMensal, prazo);
  const pmt = parcelaJurosSimples(principal, taxaMensal, prazo);

  const linhas = [];
  let saldo = principal;
  let totalJuros = 0;
  let totalPago = 0;

  for (let k = 1; k <= prazo; k++) {
    const saldoInicial = saldo;
    let amortizacao = Math.round(pmt / (1 + taxaMensal * k));
    let parcela = pmt;

    if (k === prazo) {
      amortizacao = saldoInicial; // fecha o centavo do arredondamento
      parcela = amortizacao + (pmt - Math.round(pmt / (1 + taxaMensal * k)));
    }
    const juros = parcela - amortizacao;

    saldo = saldoInicial - amortizacao;
    totalJuros += juros;
    totalPago += parcela;
    linhas.push({ n: k, saldoInicial, juros, amortizacao, parcela, saldoFinal: saldo });
  }

  return {
    linhas,
    principal,
    taxaMensal,
    prazo,
    parcela: pmt,
    totalPago,
    totalJuros,
    saldoFinal: saldo,
    amortizacaoNegativa: false,
  };
}

/** Núcleo compartilhado das tabelas. Não exportado: sempre via um sistema. */
function amortizar({ principal, taxaMensal, prazo, parcelaDe }) {
  const linhas = [];
  let saldo = principal;
  let totalJuros = 0;
  let totalPago = 0;
  let amortizacaoNegativa = false;

  for (let k = 1; k <= prazo; k++) {
    const saldoInicial = saldo;
    const juros = Math.round(saldoInicial * taxaMensal);
    let parcela = parcelaDe(k, saldoInicial);
    let amortizacao = parcela - juros;

    // Última parcela: quita o saldo exatamente. Sem isso sobra resíduo.
    if (k === prazo) {
      amortizacao = saldoInicial;
      parcela = amortizacao + juros;
    }

    if (amortizacao <= 0 && k < prazo) amortizacaoNegativa = true;

    saldo = saldoInicial - amortizacao;
    totalJuros += juros;
    totalPago += parcela;
    linhas.push({ n: k, saldoInicial, juros, amortizacao, parcela, saldoFinal: saldo });
  }

  return {
    linhas,
    principal,
    taxaMensal,
    prazo,
    parcela: linhas[0]?.parcela ?? 0,
    totalPago,
    totalJuros,
    saldoFinal: saldo,
    amortizacaoNegativa,
  };
}

function exigirContrato(principal, taxaMensal, prazo) {
  if (!Number.isInteger(principal) || principal <= 0) {
    throw new Error(`principal tem que ser centavos inteiros positivos: ${principal}`);
  }
  if (!Number.isFinite(taxaMensal) || taxaMensal < 0) {
    throw new Error(`taxa mensal inválida: ${taxaMensal}`);
  }
  if (!Number.isInteger(prazo) || prazo <= 0) {
    throw new Error(`prazo tem que ser inteiro positivo: ${prazo}`);
  }
}

// ————————————————————————————————————————————————————— TIR / CET

/**
 * Taxa interna de retorno de um fluxo de caixa, por BISSEÇÃO.
 *
 * Bisseção e não Newton-Raphson de propósito: Newton é mais rápido e
 * DIVERGE em fluxo mal-comportado, devolvendo NaN ou uma raiz absurda sem
 * avisar. Aqui a taxa achada vira a tese central do laudo — vale trocar
 * velocidade por uma resposta que sempre converge ou admite que não achou.
 *
 * Convenção do fluxo, do ponto de vista do TOMADOR:
 *   fluxo[0] = + valor efetivamente liberado
 *   fluxo[k] = − parcela paga no mês k
 *
 * Devolve a taxa por período (mensal, se o fluxo for mensal) ou null.
 */
export function tir(fluxo, { minimo = -0.99, maximo = 10, passos = 200 } = {}) {
  if (!Array.isArray(fluxo) || fluxo.length < 2) {
    throw new Error("fluxo precisa de ao menos duas posições");
  }
  const vpl = (taxa) =>
    fluxo.reduce((soma, valor, k) => soma + valor / Math.pow(1 + taxa, k), 0);

  // ☠️ Não dá pra abrir a bisseção direto em [mínimo, máximo]: num contrato de
  //    360 parcelas, (1 + (−0,99))^360 = 10^720, que em IEEE-754 é Infinity.
  //    A guarda de finitude então matava a busca e a TIR voltava `null` —
  //    ou seja, o financiamento imobiliário, que é o caso que mais importa,
  //    era exatamente o único que não calculava.
  //    Por isso a raiz é ENCURRALADA primeiro, numa grade que descarta o que
  //    estourou, e só depois bisseccionada no par que trocou de sinal.
  const grade = [
    -0.99, -0.95, -0.9, -0.75, -0.5, -0.25, -0.1, -0.05, -0.01, -0.001, 0,
    0.001, 0.0025, 0.005, 0.0075, 0.01, 0.0125, 0.015, 0.0175, 0.02, 0.025,
    0.03, 0.04, 0.05, 0.075, 0.1, 0.15, 0.2, 0.3, 0.5, 0.75, 1, 1.5, 2, 3, 5,
    7.5, 10,
  ].filter((t) => t >= minimo && t <= maximo);

  const pontos = [];
  for (const t of grade) {
    const v = vpl(t);
    if (Number.isFinite(v)) pontos.push({ t, v });
  }
  if (pontos.length < 2) return null;

  let a = null;
  let b = null;
  let va = 0;
  for (let i = 0; i < pontos.length; i++) {
    if (pontos[i].v === 0) return pontos[i].t;
    if (i > 0 && pontos[i - 1].v > 0 !== pontos[i].v > 0) {
      a = pontos[i - 1].t;
      va = pontos[i - 1].v;
      b = pontos[i].t;
      break;
    }
  }
  if (a === null) return null; // sem troca de sinal: não há raiz na faixa

  for (let i = 0; i < passos; i++) {
    const meio = (a + b) / 2;
    const vm = vpl(meio);
    if (vm === 0) return meio;
    if (va > 0 === vm > 0) {
      a = meio;
      va = vm;
    } else {
      b = meio;
    }
  }
  return (a + b) / 2;
}

/**
 * Taxa efetiva REAL do contrato: a que o fluxo de caixa revela, e não a
 * que está escrita na cláusula. É o achado mais forte da perícia, porque
 * não depende de tese jurídica nenhuma — é aritmética do próprio contrato.
 *
 * @param valorLiberado   centavos que o cliente realmente recebeu
 * @param parcela         centavos (fixa) OU array de centavos (variável)
 * @param prazo           nº de parcelas (ignorado se parcela for array)
 */
export function taxaEfetivaDoFluxo({ valorLiberado, parcela, prazo }) {
  const parcelas = Array.isArray(parcela)
    ? parcela
    : Array.from({ length: prazo }, () => parcela);
  const fluxo = [valorLiberado, ...parcelas.map((p) => -p)];
  return tir(fluxo);
}

/**
 * CET — Custo Efetivo Total (Res. CMN 3.517/2007).
 * Mesma TIR, mas o valor liberado é líquido de tudo que foi financiado e
 * não chegou na mão do cliente (tarifas, IOF, seguro embutido).
 *
 * ⚠️ Devolve mensal E anual. O contrato costuma informar o CET anual —
 *    comparar mensal com anual faz a divergência parecer 12× maior do que é.
 */
export function cet({ valorFinanciado, descontos = 0, parcela, prazo }) {
  const liquido = valorFinanciado - descontos;
  const mensal = taxaEfetivaDoFluxo({ valorLiberado: liquido, parcela, prazo });
  if (mensal === null) return { mensal: null, anual: null, valorLiquido: liquido };
  return { mensal, anual: anualEfetiva(mensal), valorLiquido: liquido };
}

/**
 * Quanto de diferença é ARREDONDAMENTO, e não erro de leitura.
 *
 * ☠️ TOLERÂNCIA FIXA EM CENTAVOS ESTÁ ERRADA, e isso foi MEDIDO contra a
 *    Calculadora do Cidadão do BACEN: em 15 casos, 10 divergiram do nosso
 *    cálculo direto, e a maior diferença foi de 7 CENTAVOS — numa prestação
 *    de R$ 56.687. O erro não é constante: ele CRESCE COM O VALOR, porque
 *    quem arredonda é o coeficiente de financiamento, e o coeficiente é
 *    multiplicado pelo principal.
 *
 *    Com o teto fixo de 2 centavos que estava aqui, um contrato de valor alto
 *    e perfeitamente legítimo seria barrado como "os números não fecham" — a
 *    perícia pararia sozinha, apontando um defeito que não existe, e no
 *    contrato de maior valor, que é justamente o que mais importa.
 *
 * ⚠️ Não se persegue o algoritmo do BACEN: nenhuma hipótese de arredondamento
 *    (round/ceil/trunc em 6 a 9 casas) reproduziu as 18 respostas dele. E não
 *    adiantaria — cada banco arredonda do seu jeito, e a prestação do laudo é
 *    a IMPRESSA NO CONTRATO, nunca a que a gente calcula. O que se precisa
 *    aqui é só separar arredondamento de dígito trocado.
 *
 *    Maior divergência relativa medida: 5,5 × 10⁻⁶. A folga de 5 × 10⁻⁵ é
 *    ~10× isso, e continua ordens de grandeza abaixo do efeito de um dígito
 *    errado na taxa, no prazo ou no principal.
 */
export function toleranciaDeArredondamento(parcela) {
  return Math.max(5, Math.round(Math.abs(parcela) * 5e-5));
}

/**
 * Checksum da leitura do contrato.
 *
 * ★ A própria matemática do Price denuncia leitura errada: se principal,
 *   taxa e prazo NÃO reproduzem a parcela impressa no contrato, então ou
 *   um dos três foi lido errado (OCR de PDF escaneado troca dígito), ou
 *   há encargo embutido na parcela que o contrato não declarou.
 *
 *   Os dois casos precisam parar a perícia. Nenhum deles pode virar laudo.
 */
export function conferirCoerencia({ principal, taxaMensal, prazo, parcelaContrato, toleranciaCentavos }) {
  const calculada = parcelaPrice(principal, taxaMensal, prazo);
  const diferenca = parcelaContrato - calculada;
  const tolerancia = toleranciaCentavos ?? toleranciaDeArredondamento(calculada);
  const bate = Math.abs(diferenca) <= tolerancia;

  // Se não bate, qual taxa reproduziria a parcela do contrato?
  const taxaImplicita = bate
    ? taxaMensal
    : taxaEfetivaDoFluxo({ valorLiberado: principal, parcela: parcelaContrato, prazo });

  return {
    bate,
    parcelaCalculada: calculada,
    parcelaContrato,
    diferenca,
    taxaInformada: taxaMensal,
    taxaImplicita,
    // quanto a diferença representa no contrato inteiro
    diferencaTotal: diferenca * prazo,
    tolerancia,
  };
}
