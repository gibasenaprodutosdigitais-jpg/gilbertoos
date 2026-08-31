// ============================================================================
// CAMADA PERICIAL — dos números do contrato para os achados do laudo
// ============================================================================
// Importa a matemática de `calculo.mjs` e não faz conta própria.
//
// ☠️ TRÊS ESTADOS POR ACHADO, nunca dois:
//      'achado'       — há divergência, com o número que a sustenta
//      'regular'      — conferido e nada a apontar
//      'inconclusivo' — falta dado no contrato pra afirmar qualquer coisa
//    Colapsar 'inconclusivo' em 'regular' faz o laudo AFIRMAR regularidade
//    sobre o que nem foi examinado. Num laudo assinado, isso é o pior
//    desfecho possível — pior que não achar nada.
//
// ⚠️ Nenhum achado carrega texto de lei aqui dentro. Ele carrega uma CHAVE
//    (`fundamento`), e o verbete mora em `referencias/jurisprudencia.mjs`,
//    que é conferido contra a fonte por máquina. Súmula escrita de cabeça
//    dentro do motor é exatamente o erro que a casa já pagou caro.
// ============================================================================

import {
  parcelaPrice,
  tabelaPrice,
  tabelaSAC,
  tabelaJurosSimples,
  anualEfetiva,
  anualNominal,
  taxaEfetivaDoFluxo,
  cet,
  conferirCoerencia,
  dataMaiorOuIgual,
  ehData,
} from "./calculo.mjs";

/** Tolerância relativa para dizer que duas taxas "são a mesma". */
const TOL_TAXA = 0.005; // 0,5% relativo

function proximo(a, b, tol = TOL_TAXA) {
  if (!Number.isFinite(a) || !Number.isFinite(b)) return false;
  if (b === 0) return Math.abs(a) < 1e-9;
  return Math.abs(a - b) / Math.abs(b) <= tol;
}

const achado = (id, titulo, status, extra = {}) => ({
  id,
  titulo,
  status,
  fundamento: null,
  numeros: {},
  observacao: null,
  ...extra,
});

// ============================================================================
// 1. COERÊNCIA — o portão. Nada roda antes disso passar.
// ============================================================================

/**
 * ★ A matemática do Price é o checksum da leitura do contrato: se principal,
 *   taxa e prazo não reproduzem a parcela impressa, ou o OCR trocou um dígito
 *   ou há encargo embutido não declarado.
 *
 *   Os dois casos param a perícia. O primeiro é erro nosso; o segundo é
 *   achado grave — mas nenhum dos dois pode seguir para o cálculo como se
 *   estivesse tudo bem.
 */
export function conferirEntrada(contrato) {
  const problemas = [];
  const exigidos = ["valorFinanciado", "prazo", "parcela", "taxaMensal", "dataContrato"];
  for (const campo of exigidos) {
    if (contrato[campo] === undefined || contrato[campo] === null) {
      problemas.push(`falta o campo obrigatório: ${campo}`);
    }
  }
  for (const campo of ["valorFinanciado", "parcela", "prazo"]) {
    const v = contrato[campo];
    if (v !== undefined && v !== null && !Number.isInteger(v)) {
      problemas.push(`${campo} tem que ser inteiro (centavos, ou nº de parcelas): ${v}`);
    }
  }
  if (contrato.dataContrato && !ehData(contrato.dataContrato)) {
    problemas.push(`dataContrato tem que ser 'AAAA-MM-DD': ${contrato.dataContrato}`);
  }
  if (problemas.length) return { pode: false, problemas, coerencia: null };

  const coerencia = conferirCoerencia({
    principal: contrato.valorFinanciado,
    taxaMensal: contrato.taxaMensal,
    prazo: contrato.prazo,
    parcelaContrato: contrato.parcela,
    toleranciaCentavos: contrato.toleranciaCentavos,
  });

  if (!coerencia.bate) {
    problemas.push(
      "os números não fecham entre si: valor financiado, taxa e prazo não " +
        "reproduzem a parcela do contrato. Ou um deles foi lido errado, ou " +
        "há encargo embutido na parcela que o contrato não declara. " +
        "Conferir no documento antes de calcular.",
    );
  }
  return { pode: coerencia.bate, problemas, coerencia };
}

// ============================================================================
// 2. ACHADOS
// ============================================================================

/** Capitalização: a taxa anual do contrato é a efetiva ou o duodécuplo? */
function acharCapitalizacao(c) {
  const efetiva = anualEfetiva(c.taxaMensal);
  const nominal = anualNominal(c.taxaMensal);
  const numeros = {
    taxaMensal: c.taxaMensal,
    anualEfetivaCalculada: efetiva,
    anualNominalCalculada: nominal,
    anualContratada: c.taxaAnual ?? null,
    excedente: efetiva - nominal,
  };

  if (c.taxaAnual === undefined || c.taxaAnual === null) {
    return achado(
      "capitalizacao",
      "Capitalização de juros",
      "inconclusivo",
      {
        numeros,
        fundamento: "sumula-541",
        observacao:
          "O contrato não informa (ou não foi possível extrair) a taxa anual. " +
          "Sem ela não dá pra dizer se a capitalização mensal foi pactuada de " +
          "forma expressa. A ausência da taxa anual no instrumento é, em si, " +
          "ponto a registrar.",
      },
    );
  }

  if (proximo(c.taxaAnual, efetiva)) {
    return achado("capitalizacao", "Capitalização de juros", "regular", {
      numeros,
      fundamento: "sumula-541",
      observacao:
        "A taxa anual do contrato equivale à capitalização mensal da taxa " +
        "mensal pactuada, e supera o duodécuplo desta. Nesse ponto o contrato " +
        "não apresenta divergência.",
    });
  }

  if (proximo(c.taxaAnual, nominal)) {
    return achado("capitalizacao", "Capitalização de juros", "achado", {
      numeros,
      fundamento: "sumula-541",
      observacao:
        "A taxa anual informada corresponde ao simples duodécuplo da taxa " +
        "mensal, e não à sua capitalização. Ainda assim, o sistema de " +
        "amortização aplicado produz incidência de juros sobre juros: em doze " +
        "meses o custo efetivo alcança o percentual calculado acima, superior " +
        "ao anual declarado no instrumento.",
    });
  }

  return achado("capitalizacao", "Capitalização de juros", "achado", {
    numeros,
    fundamento: "sumula-541",
    observacao:
      "A taxa anual informada não corresponde nem ao duodécuplo nem à " +
      "capitalização da taxa mensal. Divergência a esclarecer: os três " +
      "percentuais estão no quadro acima.",
  });
}

/** Taxa efetiva revelada pelo fluxo de caixa real. */
function acharTaxaEfetiva(c) {
  const liberado = c.valorLiberado ?? c.valorFinanciado;
  const real = taxaEfetivaDoFluxo({
    valorLiberado: liberado,
    parcela: c.parcela,
    prazo: c.prazo,
  });
  const numeros = {
    valorFinanciado: c.valorFinanciado,
    valorLiberado: liberado,
    taxaContratada: c.taxaMensal,
    taxaEfetivaReal: real,
    diferenca: real === null ? null : real - c.taxaMensal,
  };

  if (real === null) {
    return achado("taxa-efetiva", "Taxa efetivamente praticada", "inconclusivo", {
      numeros,
      observacao: "Não foi possível apurar a taxa interna do fluxo com os dados disponíveis.",
    });
  }
  if (proximo(real, c.taxaMensal)) {
    return achado("taxa-efetiva", "Taxa efetivamente praticada", "regular", {
      numeros,
      observacao:
        "A taxa apurada a partir do fluxo de caixa do contrato coincide com a " +
        "taxa mensal pactuada.",
    });
  }
  return achado("taxa-efetiva", "Taxa efetivamente praticada", "achado", {
    numeros,
    observacao:
      "A taxa apurada a partir do fluxo de caixa efetivo (valor liberado " +
      "contra as prestações) diverge da taxa mensal declarada no contrato. " +
      "O cálculo é aritmético e independe de qualquer tese: decorre dos " +
      "próprios valores do instrumento.",
  });
}

/**
 * Qual norma do CET regia o contrato na data em que foi celebrado.
 *
 * ☠️ A Resolução CMN 3.517/2007 foi REVOGADA pela Resolução CMN 4.881/2020,
 *    em vigor desde 01/02/2021. Um laudo sobre contrato de 2023 que invoque
 *    a 3.517 cita norma revogada — e é o tipo de coisa que o assistente
 *    técnico do banco usa pra desqualificar a peça inteira.
 *    Mas o contrário também é erro: contrato de 2015 se rege pela 3.517,
 *    não pela 4.881. Por isso a norma é escolhida PELA DATA DO CONTRATO,
 *    nunca cravada.
 */
function normaCET(dataContrato) {
  return dataMaiorOuIgual(dataContrato, "2021-02-01") ? "cet-4881" : "cet-3517";
}

/** CET: o custo total contra o que o contrato declarou. */
function acharCET(c) {
  const descontos = somarTarifasFinanciadas(c) + (c.iofFinanciado ?? 0);
  const calculado = cet({
    valorFinanciado: c.valorFinanciado,
    descontos,
    parcela: c.parcela,
    prazo: c.prazo,
  });
  const numeros = {
    descontosEmbutidos: descontos,
    valorLiquidoRecebido: calculado.valorLiquido,
    cetMensalCalculado: calculado.mensal,
    cetAnualCalculado: calculado.anual,
    cetAnualInformado: c.cetAnualInformado ?? null,
  };

  if (calculado.mensal === null) {
    return achado("cet", "Custo Efetivo Total (CET)", "inconclusivo", { numeros, fundamento: normaCET(c.dataContrato) });
  }
  if (c.cetAnualInformado === undefined || c.cetAnualInformado === null) {
    return achado("cet", "Custo Efetivo Total (CET)", "inconclusivo", {
      numeros,
      fundamento: normaCET(c.dataContrato),
      observacao:
        "O contrato não informa o CET, ou não foi possível extraí-lo. O valor " +
        "calculado acima está apurado; falta o declarado para confronto. " +
        "A ausência da informação no instrumento é ponto a registrar.",
    });
  }
  if (proximo(calculado.anual, c.cetAnualInformado, 0.02)) {
    return achado("cet", "Custo Efetivo Total (CET)", "regular", {
      numeros,
      fundamento: normaCET(c.dataContrato),
      observacao: "O CET apurado confere com o declarado no instrumento.",
    });
  }
  return achado("cet", "Custo Efetivo Total (CET)", "achado", {
    numeros,
    fundamento: normaCET(c.dataContrato),
    observacao:
      "O CET apurado diverge do declarado no contrato. ⚠️ Confrontar sempre " +
      "anual com anual: comparar o CET mensal apurado com o anual declarado " +
      "faz a divergência parecer doze vezes maior do que é.",
  });
}

/** Taxa do contrato contra a média de mercado publicada pelo BACEN. */
function acharTaxaVsMedia(c) {
  const numeros = {
    taxaContratada: c.taxaMensal,
    mediaBacen: c.mediaBacenMensal ?? null,
    razao: c.mediaBacenMensal ? c.taxaMensal / c.mediaBacenMensal : null,
    modalidade: c.modalidadeBacen ?? null,
    competencia: c.competenciaBacen ?? null,
  };
  if (!c.mediaBacenMensal) {
    return achado("taxa-vs-media", "Taxa contra a média de mercado", "inconclusivo", {
      numeros,
      fundamento: "tema-27",
      observacao:
        "Não foi informada a taxa média praticada pelo mercado na modalidade " +
        "e no mês da contratação. Sem ela não se afirma abusividade — a " +
        "comparação com a média oficial é o critério que a jurisprudência usa.",
    });
  }
  // ⚠️ NÃO EXISTE percentual legal a partir do qual a taxa vira abusiva. A
  //    régua é "destoar substancialmente da média", e quem decide é o juízo,
  //    caso a caso. Por isso o limiar é PARÂMETRO DECLARADO, aparece no laudo
  //    junto com o resultado, e a faixa intermediária é INCONCLUSIVA — não
  //    "regular". Cravar 1,5× como se fosse regra de direito seria a precisão
  //    falsa que a gente acusa no concorrente, dentro de uma peça assinada.
  const limiar = c.limiarAbusividade ?? 1.5;
  const razao = c.taxaMensal / c.mediaBacenMensal;
  const numerosCompletos = { ...numeros, razao, limiarAdotado: limiar };

  if (razao >= limiar) {
    return achado("taxa-vs-media", "Taxa contra a média de mercado", "achado", {
      numeros: numerosCompletos,
      fundamento: "tema-27",
      observacao:
        `A taxa pactuada corresponde a ${razao.toFixed(2)} vez(es) a média ` +
        "divulgada pelo Banco Central para a mesma modalidade e período, " +
        `superando o parâmetro de ${limiar.toFixed(2)}× adotado neste laudo. ` +
        "O parâmetro é critério de trabalho do perito, não percentual legal: " +
        "não há tese firmada que estabeleça a média de mercado como limiar de " +
        "abusividade. A comparação é elemento de prova; a caracterização da " +
        "abusividade é matéria de julgamento, no caso concreto.",
    });
  }
  if (razao > 1) {
    return achado("taxa-vs-media", "Taxa contra a média de mercado", "inconclusivo", {
      numeros: numerosCompletos,
      fundamento: "tema-27",
      observacao:
        `A taxa pactuada supera a média de mercado (${razao.toFixed(2)}×), mas ` +
        `não alcança o parâmetro de ${limiar.toFixed(2)}× adotado neste laudo. ` +
        "O parâmetro é critério de trabalho do perito, não percentual legal: " +
        "não há patamar a partir do qual a taxa se torne abusiva por lei. " +
        "Este perito não classifica a faixa de ofício — os percentuais estão " +
        "apurados acima para apreciação do juízo.",
    });
  }
  return achado("taxa-vs-media", "Taxa contra a média de mercado", "regular", {
    numeros: numerosCompletos,
    fundamento: "tema-27",
    observacao:
      "A taxa pactuada não supera a média divulgada pelo Banco Central para " +
      "a mesma modalidade e período.",
  });
}

/**
 * Tarifas e encargos acessórios.
 * ⚠️ A régua de cada uma é jurídica, e mora em `referencias/`. Aqui só se
 *    aplica o critério objetivo (natureza + data) e se aponta o fundamento.
 */
// ☠️ A DATA DO TEMA 618 É "VÁLIDA ATÉ", NÃO "VEDADA A PARTIR DE".
//    O acórdão diz: "Nos contratos bancários celebrados ATÉ 30/04/2008 (fim
//    da vigência da Resolução CMN 2.303/96) ERA VÁLIDA a pactuação das TAC e
//    TEC". O dia 30/04/2008 fica, portanto, do lado VÁLIDO.
//    A 1ª versão daqui tinha `vedadaAPartirDe: '2008-04-30'` e classificava
//    o próprio dia 30/04 como irregular — e havia um teste fossilizando o
//    erro, porque o teste foi escrito a partir da mesma suposição que o
//    código. Um dia de diferença INVERTE a conclusão sobre o contrato.
//    Corrigido contra o texto do acórdão baixado do STJ, não de memória.
const REGRAS_TARIFA = {
  tac: { rotulo: "Tarifa de Abertura de Crédito (TAC)", fundamento: "tema-618", validaAte: "2008-04-30" },
  tec: { rotulo: "Tarifa de Emissão de Carnê (TEC)", fundamento: "tema-618", validaAte: "2008-04-30" },
  cadastro: {
    rotulo: "Tarifa de Cadastro",
    fundamento: "tema-618",
    exigeConferencia: "válida uma única vez, no início do relacionamento com a instituição",
  },

  // ☠️ MOLDURA INVERTIDA NA 1ª VERSÃO. O Tema 958, item 2.3, declara a
  //    VALIDADE da tarifa de avaliação do bem e do ressarcimento de registro.
  //    A abusividade é a EXCEÇÃO (serviço não efetivamente prestado, ou
  //    onerosidade excessiva). Eu tinha escrito como se a regra fosse a
  //    cobrança indevida — o laudo acusaria justamente o que a Corte validou,
  //    e o assistente técnico do banco derrubaria o ponto citando o mesmo tema.
  avaliacao: {
    rotulo: "Tarifa de avaliação do bem",
    fundamento: "tema-958",
    exigeConferencia:
      "a cobrança é VÁLIDA em regra; só é abusiva se a avaliação não foi " +
      "efetivamente realizada, ou por onerosidade excessiva no caso concreto",
  },
  registro: {
    rotulo: "Ressarcimento de registro do contrato",
    fundamento: "tema-958",
    exigeConferencia:
      "o ressarcimento é VÁLIDO em regra; só é abusivo se o serviço não foi " +
      "efetivamente prestado, ou por onerosidade excessiva no caso concreto",
  },
  "servicos-terceiros": {
    rotulo: "Ressarcimento de serviços prestados por terceiros",
    fundamento: "tema-958",
    exigeConferencia:
      "é abusiva a cláusula que não ESPECIFICA o serviço a ser efetivamente " +
      "prestado — verificar no instrumento se há a especificação",
  },

  // Comissão de correspondente e pré-gravame: válidas ATÉ 24/02/2011, porque
  // a Res.-CMN 3.954/2011 entrou em vigor em 25/02/2011 e a abusividade vale
  // "a partir de" essa data (Temas 958, item 2.2, e 972, item 1).
  correspondente: {
    rotulo: "Comissão de correspondente bancário",
    fundamento: "tema-958",
    validaAte: "2011-02-24",
  },
  "pre-gravame": {
    rotulo: "Ressarcimento de registro do pré-gravame",
    fundamento: "tema-972",
    validaAte: "2011-02-24",
  },

  seguro: {
    rotulo: "Seguro prestamista",
    fundamento: "tema-972",
    exigeConferencia:
      "a irregularidade é a IMPOSIÇÃO da seguradora, não a existência do " +
      "seguro — verificar se houve liberdade de escolha. Perícia contábil não " +
      "prova imposição: o ponto é documental",
  },
};

function acharTarifas(c) {
  const lista = c.tarifas ?? [];
  if (lista.length === 0) {
    return [
      achado("tarifas", "Tarifas e encargos acessórios", "inconclusivo", {
        observacao:
          "Nenhuma tarifa foi informada. Conferir no instrumento e no demonstrativo " +
          "de liberação se houve cobrança de tarifas embutidas no valor financiado.",
      }),
    ];
  }
  return lista.map((t, i) => {
    const regra = REGRAS_TARIFA[t.tipo] ?? {
      rotulo: t.nome ?? "Tarifa não classificada",
      fundamento: null,
    };
    const numeros = {
      valor: t.valor,
      financiada: t.financiada ?? false,
      dataContrato: c.dataContrato,
      proporcaoDoFinanciado: c.valorFinanciado ? t.valor / c.valorFinanciado : null,
    };

    if (regra.validaAte) {
      // "válida ATÉ" inclui o próprio dia: só é achado o que vem DEPOIS dele
      const dentroDaValidade = !dataMaiorOuIgual(c.dataContrato, regra.validaAte) ||
        c.dataContrato === regra.validaAte;
      return achado(`tarifa-${t.tipo}-${i}`, regra.rotulo, dentroDaValidade ? "regular" : "achado", {
        numeros: { ...numeros, validaAte: regra.validaAte },
        fundamento: regra.fundamento,
        observacao: dentroDaValidade
          ? `Contrato celebrado em ${c.dataContrato}, até o marco de ${regra.validaAte} — período em que a pactuação era válida, ressalvado o exame de abusividade no caso concreto.`
          : `Contrato celebrado em ${c.dataContrato}, posterior ao marco de ${regra.validaAte}.`,
      });
    }
    return achado(`tarifa-${t.tipo}-${i}`, regra.rotulo, "inconclusivo", {
      numeros,
      fundamento: regra.fundamento,
      observacao: regra.exigeConferencia
        ? `Depende de verificação documental: ${regra.exigeConferencia}. Não se afirma irregularidade sem esse exame.`
        : "Tarifa não classificada. Requer exame do instrumento.",
    });
  });
}

/** Multa moratória acima do teto. */
function acharMulta(c) {
  if (c.multaMoratoria === undefined || c.multaMoratoria === null) {
    return achado("multa", "Multa moratória", "inconclusivo", {
      fundamento: "cdc-52",
      observacao: "Percentual de multa não informado ou não localizado no instrumento.",
    });
  }
  const status = c.multaMoratoria > 0.02 ? "achado" : "regular";
  return achado("multa", "Multa moratória", status, {
    numeros: { multaContratada: c.multaMoratoria, teto: 0.02 },
    fundamento: "cdc-52",
    observacao:
      status === "achado"
        ? "O percentual de multa por inadimplemento supera o teto legal."
        : "O percentual de multa observa o teto legal.",
  });
}

/** Comissão de permanência cumulada com outros encargos de mora. */
function acharComissaoPermanencia(c) {
  if (!c.comissaoPermanencia) {
    return achado("comissao-permanencia", "Comissão de permanência", "regular", {
      fundamento: "sumula-472",
      observacao: "Não há previsão de comissão de permanência no instrumento examinado.",
    });
  }
  // ☠️ A Súmula 472 tem DOIS comandos, e a 1ª versão só tratava um:
  //    (a) o valor da comissão não pode ultrapassar a soma dos encargos
  //        remuneratórios e moratórios previstos no contrato; e
  //    (b) a cobrança EXCLUI A EXIGIBILIDADE dos juros remuneratórios,
  //        moratórios e da multa contratual.
  //    O verbo não é "vedada a cumulação" — foi assim que eu tinha escrito de
  //    cabeça, e a conferência contra a fonte derrubou. O efeito prático é
  //    diferente: não se trata de anular a comissão, e sim de excluir os
  //    demais encargos e apurar o excesso do teto. São duas contas.
  const cumulados = [
    ["multa contratual", c.multaMoratoria],
    ["juros moratórios", c.jurosMoratorios],
    ["juros remuneratórios", c.jurosRemuneratorios],
  ].filter(([, v]) => Boolean(v));

  const numeros = {
    comissaoPermanencia: c.comissaoPermanencia,
    multaMoratoria: c.multaMoratoria ?? null,
    jurosMoratorios: c.jurosMoratorios ?? null,
    jurosRemuneratorios: c.jurosRemuneratorios ?? null,
    correcaoMonetaria: c.correcaoMonetaria ?? null,
    tetoSomaDosEncargos:
      typeof c.comissaoPermanencia === "number"
        ? (c.jurosRemuneratorios ?? 0) + (c.jurosMoratorios ?? 0) + (c.multaMoratoria ?? 0)
        : null,
  };

  if (cumulados.length === 0) {
    return achado("comissao-permanencia", "Comissão de permanência", "inconclusivo", {
      numeros,
      fundamento: "sumula-472",
      observacao:
        "Há previsão de comissão de permanência, mas os demais encargos de " +
        "mora não foram informados. Sem eles não se apura nem a exclusão de " +
        "exigibilidade nem o teto (soma dos encargos remuneratórios e " +
        "moratórios previstos no contrato).",
    });
  }

  return achado("comissao-permanencia", "Comissão de permanência", "achado", {
    numeros,
    fundamento: "sumula-472",
    observacao:
      "O instrumento prevê comissão de permanência ao lado de " +
      `${cumulados.map(([n]) => n).join(", ")}. A cobrança da comissão exclui ` +
      "a exigibilidade desses encargos, e o valor da própria comissão fica " +
      "limitado à soma dos encargos remuneratórios e moratórios previstos no " +
      "contrato. Os dois pontos estão quantificados no quadro acima.",
  });
}

/** Amortização negativa: o saldo cresce mesmo com o pagamento em dia. */
function acharAmortizacaoNegativa(tabela) {
  if (!tabela.amortizacaoNegativa) {
    return achado("amortizacao-negativa", "Evolução do saldo devedor", "regular", {
      observacao: "A amortização é positiva em todas as prestações: o saldo devedor decresce de forma contínua.",
    });
  }
  const primeira = tabela.linhas.find((l) => l.amortizacao <= 0);
  return achado("amortizacao-negativa", "Evolução do saldo devedor", "achado", {
    numeros: {
      primeiraPrestacao: primeira?.n ?? null,
      jurosDoPeriodo: primeira?.juros ?? null,
      prestacao: primeira?.parcela ?? null,
    },
    observacao:
      "Há amortização negativa: a prestação é insuficiente para cobrir os " +
      "juros do período, de modo que o saldo devedor CRESCE ainda que o " +
      "mutuário pague rigorosamente em dia.",
  });
}

function somarTarifasFinanciadas(c) {
  return (c.tarifas ?? []).reduce((s, t) => s + (t.financiada ? t.valor : 0), 0);
}

// ============================================================================
// 3. CENÁRIOS DE RECÁLCULO
// ============================================================================

function montarCenarios(c) {
  const base = { principal: c.valorFinanciado, prazo: c.prazo };
  const original = tabelaPrice({ ...base, taxaMensal: c.taxaMensal, parcela: c.parcela });

  const cenarios = [
    {
      id: "original",
      rotulo: "Contratado (Tabela Price)",
      descricao: "Reprodução do contrato tal como pactuado, com a taxa e a prestação do instrumento.",
      tabela: original,
    },
    {
      id: "juros-simples",
      rotulo: "Juros simples (desconto racional)",
      descricao: "Mesma taxa mensal, sem incidência de juros sobre juros.",
      tabela: tabelaJurosSimples({ ...base, taxaMensal: c.taxaMensal }),
    },
    {
      id: "sac",
      rotulo: "SAC (amortização constante)",
      descricao: "Mesma taxa mensal, amortização constante e prestação decrescente.",
      tabela: tabelaSAC({ ...base, taxaMensal: c.taxaMensal }),
    },
  ];

  // ☠️ Este cenário só entra quando a taxa anual declarada NÃO é nem o
  //    duodécuplo nem a capitalização da mensal.
  //
  //    O gabarito impresso pegou o erro: quando a anual é o duodécuplo,
  //    anual/12 é, por definição, a própria taxa mensal — o cenário saía
  //    numericamente IDÊNTICO ao de juros simples, centavo a centavo. Duas
  //    colunas com o mesmo número num laudo pericial não são redundância
  //    inofensiva: é o perito parecendo não saber o que calculou, e é a
  //    primeira coisa que o assistente técnico do banco aponta.
  //    (E quando a anual é a efetiva, anual/12 devolveria o contrato original.)
  if (
    c.taxaAnual != null &&
    !proximo(c.taxaAnual, anualNominal(c.taxaMensal)) &&
    !proximo(c.taxaAnual, anualEfetiva(c.taxaMensal))
  ) {
    cenarios.push({
      id: "taxa-nominal",
      rotulo: "Taxa anual declarada, sem capitalizar",
      descricao:
        "Aplicação da taxa anual efetivamente declarada no instrumento, " +
        "dividida por doze, sem capitalização mensal.",
      tabela: tabelaJurosSimples({ ...base, taxaMensal: c.taxaAnual / 12 }),
    });
  }

  if (c.mediaBacenMensal) {
    cenarios.push({
      id: "media-bacen",
      rotulo: "Taxa média de mercado (BACEN)",
      descricao: "Substituição da taxa pactuada pela média divulgada pelo Banco Central na modalidade e no período.",
      tabela: tabelaPrice({ ...base, taxaMensal: c.mediaBacenMensal }),
    });
  }

  return { original, cenarios };
}

// ============================================================================
// 4. APURAÇÃO
// ============================================================================

function apurar(c, original, cenarios) {
  const pagas = Math.min(c.parcelasPagas ?? 0, c.prazo);
  return cenarios
    .filter((ce) => ce.id !== "original")
    .map((ce) => {
      const difTotal = original.totalPago - ce.tabela.totalPago;

      // ☠️ SAC tem prestação DECRESCENTE: a "diferença por prestação" contra
      //    ele não existe — muda a cada mês. O gabarito impresso mostrou o
      //    estrago: saía "diferença por prestação −R$ 491,87" e "pago a maior
      //    −R$ 5.047,83", como se o cliente tivesse pago a MENOS num cenário
      //    que, no total, é R$ 4.449 mais barato. Número que se contradiz
      //    dentro da mesma tabela é o que faz o juiz devolver o laudo.
      //    Em sistema de prestação variável o campo vem nulo, e o laudo diz
      //    por quê em vez de imprimir um número sem sentido.
      const variavel = ce.tabela.linhas[0].parcela !== ce.tabela.linhas[ce.tabela.prazo - 2]?.parcela;
      const difParcela = variavel ? null : original.parcela - ce.tabela.parcela;

      const pagoOriginal = original.linhas.slice(0, pagas).reduce((s, l) => s + l.parcela, 0);
      const pagoCenario = ce.tabela.linhas.slice(0, pagas).reduce((s, l) => s + l.parcela, 0);

      return {
        cenario: ce.id,
        rotulo: ce.rotulo,
        prestacaoVariavel: variavel,
        parcelaOriginal: original.parcela,
        parcelaCenario: variavel ? null : ce.tabela.parcela,
        primeiraPrestacaoCenario: ce.tabela.linhas[0].parcela,
        ultimaPrestacaoCenario: ce.tabela.linhas[ce.tabela.prazo - 1].parcela,
        diferencaPorParcela: difParcela,
        totalOriginal: original.totalPago,
        totalCenario: ce.tabela.totalPago,
        diferencaTotal: difTotal,
        jurosOriginal: original.totalJuros,
        jurosCenario: ce.tabela.totalJuros,
        parcelasPagas: pagas,
        pagoAMaiorAteAqui: pagoOriginal - pagoCenario,
        aCompensarNoSaldo: difTotal - (pagoOriginal - pagoCenario),
        observacao: variavel
          ? "Sistema de prestação decrescente: não há diferença única por " +
            "prestação. Nas primeiras prestações este cenário é mais oneroso " +
            "que o contratado, e a economia se realiza ao longo do contrato — " +
            "por isso o valor apurado no período já decorrido pode ser " +
            "negativo enquanto a diferença no contrato inteiro é favorável."
          : null,
      };
    });
}

// ============================================================================
// 5. ENTRADA ÚNICA
// ============================================================================

/**
 * Roda a perícia inteira sobre um contrato já CONFERIDO por humano.
 *
 * ⚠️ Não aceita contrato incoerente: devolve `{ pode: false }` com os
 *    problemas. O agente deve devolver isso ao perito e parar — nunca
 *    calcular "do jeito que der".
 */
export function periciar(contrato) {
  const porta = conferirEntrada(contrato);
  if (!porta.pode) {
    return { pode: false, problemas: porta.problemas, coerencia: porta.coerencia };
  }

  const { original, cenarios } = montarCenarios(contrato);

  const achados = [
    acharCapitalizacao(contrato),
    acharTaxaEfetiva(contrato),
    acharCET(contrato),
    acharTaxaVsMedia(contrato),
    ...acharTarifas(contrato),
    acharMulta(contrato),
    acharComissaoPermanencia(contrato),
    acharAmortizacaoNegativa(original),
  ];

  return {
    pode: true,
    coerencia: porta.coerencia,
    contrato,
    achados,
    resumoAchados: {
      achado: achados.filter((a) => a.status === "achado").length,
      regular: achados.filter((a) => a.status === "regular").length,
      inconclusivo: achados.filter((a) => a.status === "inconclusivo").length,
    },
    cenarios,
    apuracao: apurar(contrato, original, cenarios),
    fundamentosUsados: [...new Set(achados.map((a) => a.fundamento).filter(Boolean))],
  };
}
