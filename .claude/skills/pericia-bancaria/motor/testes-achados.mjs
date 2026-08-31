// ============================================================================
// BATERIA DA CAMADA PERICIAL — `node motor/testes-achados.mjs`
// ============================================================================

import { parcelaPrice } from "./calculo.mjs";
import { periciar, conferirEntrada } from "./achados.mjs";

let ok = 0;
const falhas = [];

function verdade(rotulo, condicao) {
  if (condicao) return ok++;
  falhas.push(rotulo);
}
function eq(rotulo, obtido, esperado) {
  if (obtido === esperado) return ok++;
  falhas.push(`${rotulo}\n     esperado: ${esperado}\n     obtido:   ${obtido}`);
}
const pega = (r, id) => r.achados.find((a) => a.id === id);
const status = (r, id) => pega(r, id)?.status;

// Contrato-base: R$ 60.000 em 48 meses a 1,99% a.m., firmado em 2021.
function contratoBase(extra = {}) {
  const valorFinanciado = 6000000;
  const taxaMensal = 0.0199;
  const prazo = 48;
  return {
    valorFinanciado,
    prazo,
    taxaMensal,
    parcela: parcelaPrice(valorFinanciado, taxaMensal, prazo),
    dataContrato: "2021-03-15",
    ...extra,
  };
}

// ————————————————————————————————————————————————————— o portão

{
  const bom = conferirEntrada(contratoBase());
  verdade("contrato coerente passa o portão", bom.pode);
  eq("contrato coerente não tem problema", bom.problemas.length, 0);

  // ☠️ taxa lida errada pelo OCR: a perícia NÃO pode rodar
  const torto = conferirEntrada(contratoBase({ taxaMensal: 0.0159 }));
  verdade("contrato incoerente é barrado", !torto.pode);
  verdade("e diz por quê", torto.problemas.some((p) => p.includes("não fecham")));
  verdade("periciar() também recusa", periciar(contratoBase({ taxaMensal: 0.0159 })).pode === false);
  verdade("recusa não devolve achados", periciar(contratoBase({ taxaMensal: 0.0159 })).achados === undefined);

  // Campo faltando
  const semData = conferirEntrada(contratoBase({ dataContrato: null }));
  verdade("campo obrigatório faltando é barrado", !semData.pode);
  const dataTorta = conferirEntrada(contratoBase({ dataContrato: "15/03/2021" }));
  verdade("data em formato brasileiro é barrada", !dataTorta.pode);
  const reais = conferirEntrada(contratoBase({ valorFinanciado: 60000.5 }));
  verdade("valor em reais (float) é barrado", !reais.pode);
}

// ————————————————————————————————————————————————————— capitalização

{
  // Contrato declara a anual EFETIVA (26,68% para 1,99% a.m.) → nada a apontar
  const efetiva = periciar(contratoBase({ taxaAnual: Math.pow(1.0199, 12) - 1 }));
  eq("anual efetiva declarada → regular", status(efetiva, "capitalizacao"), "regular");

  // Contrato declara o duodécuplo (23,88%) → achado
  const nominal = periciar(contratoBase({ taxaAnual: 0.0199 * 12 }));
  eq("duodécuplo declarado → achado", status(nominal, "capitalizacao"), "achado");
  verdade("achado mostra os três percentuais",
    pega(nominal, "capitalizacao").numeros.anualEfetivaCalculada >
    pega(nominal, "capitalizacao").numeros.anualNominalCalculada);

  // ☠️ Sem taxa anual no contrato → INCONCLUSIVO, jamais "regular".
  //    Dizer "regular" aqui é o laudo afirmar regularidade sobre o que
  //    sequer foi examinado.
  const ausente = periciar(contratoBase());
  eq("sem taxa anual → inconclusivo", status(ausente, "capitalizacao"), "inconclusivo");

  // Taxa anual que não é nem uma nem outra
  const estranha = periciar(contratoBase({ taxaAnual: 0.45 }));
  eq("anual incompatível → achado", status(estranha, "capitalizacao"), "achado");
}

// ————————————————————————————————————————————————————— taxa efetiva do fluxo

{
  const limpo = periciar(contratoBase());
  eq("sem custo embutido → taxa efetiva regular", status(limpo, "taxa-efetiva"), "regular");

  // R$ 3.000 de tarifas e IOF não chegaram na mão do cliente
  const comCustos = periciar(contratoBase({ valorLiberado: 5700000 }));
  eq("valor liberado menor → achado", status(comCustos, "taxa-efetiva"), "achado");
  verdade("taxa real é maior que a contratada",
    pega(comCustos, "taxa-efetiva").numeros.taxaEfetivaReal > 0.0199);
}

// ————————————————————————————————————————————————————— CET

{
  const semCET = periciar(contratoBase());
  eq("sem CET declarado → inconclusivo", status(semCET, "cet"), "inconclusivo");

  const comTarifas = periciar(
    contratoBase({
      tarifas: [{ tipo: "tac", valor: 150000, financiada: true }],
      iofFinanciado: 100000,
      cetAnualInformado: 0.2688,
    }),
  );
  const n = pega(comTarifas, "cet").numeros;
  eq("CET desconta o que foi embutido", n.descontosEmbutidos, 250000);
  eq("valor líquido recebido", n.valorLiquidoRecebido, 5750000);
  verdade("CET anual calculado supera o declarado", n.cetAnualCalculado > 0.2688);
  eq("CET divergente → achado", status(comTarifas, "cet"), "achado");

  // ☠️ A norma do CET MUDOU: a Res. CMN 3.517/2007 foi revogada pela
  //    4.881/2020, em vigor desde 01/02/2021. Citar a 3.517 num contrato de
  //    2023 é invocar norma revogada dentro de peça assinada — e citar a
  //    4.881 num contrato de 2015 é o erro inverso. A norma sai da DATA.
  eq("contrato de 2021 em diante → Res. 4.881",
    pega(periciar(contratoBase({ dataContrato: "2021-03-15" })), "cet").fundamento, "cet-4881");
  eq("contrato anterior → Res. 3.517",
    pega(periciar(contratoBase({ dataContrato: "2015-06-10" })), "cet").fundamento, "cet-3517");
  eq("o próprio 01/02/2021 já é a norma nova",
    pega(periciar(contratoBase({ dataContrato: "2021-02-01" })), "cet").fundamento, "cet-4881");
  eq("a véspera ainda é a antiga",
    pega(periciar(contratoBase({ dataContrato: "2021-01-31" })), "cet").fundamento, "cet-3517");
  // ⚠️ anual e mensal não podem ser confundidos
  verdade("CET anual >> CET mensal", n.cetAnualCalculado > n.cetMensalCalculado * 10);
}

// ————————————————————————————————————————————————————— tarifas

{
  // ☠️ A FRONTEIRA DO TEMA 618 — conferida contra o texto do acórdão baixado
  //    do STJ, não de memória. O acórdão diz "celebrados ATÉ 30/04/2008 era
  //    VÁLIDA a pactuação": o próprio dia 30/04 fica do lado VÁLIDO.
  //    A 1ª versão classificava 30/04/2008 como achado, e havia um teste aqui
  //    fossilizando o erro — porque o teste nasceu da mesma suposição que o
  //    código. Um dia inverte a conclusão sobre o contrato do cliente.
  const noDia = periciar(
    contratoBase({ dataContrato: "2008-04-30", tarifas: [{ tipo: "tac", valor: 80000 }] }),
  );
  eq("TAC em 30/04/2008 → regular (último dia válido)", status(noDia, "tarifa-tac-0"), "regular");

  const vespera = periciar(
    contratoBase({ dataContrato: "2008-04-29", tarifas: [{ tipo: "tac", valor: 80000 }] }),
  );
  eq("TAC em 29/04/2008 → regular", status(vespera, "tarifa-tac-0"), "regular");

  const diaSeguinte = periciar(
    contratoBase({ dataContrato: "2008-05-01", tarifas: [{ tipo: "tac", valor: 80000 }] }),
  );
  eq("TAC em 01/05/2008 → achado", status(diaSeguinte, "tarifa-tac-0"), "achado");
  verdade("o laudo ressalva o exame de abusividade no período válido",
    pega(noDia, "tarifa-tac-0").observacao.includes("abusividade"));

  const hoje = periciar(contratoBase({ tarifas: [{ tipo: "tec", valor: 5000 }] }));
  eq("TEC em contrato de 2021 → achado", status(hoje, "tarifa-tec-0"), "achado");

  // Tarifas que dependem de prova documental não podem ser afirmadas
  const avaliacao = periciar(contratoBase({ tarifas: [{ tipo: "avaliacao", valor: 40000 }] }));
  eq("tarifa de avaliação → inconclusivo", status(avaliacao, "tarifa-avaliacao-0"), "inconclusivo");
  const seguro = periciar(contratoBase({ tarifas: [{ tipo: "seguro", valor: 120000 }] }));
  eq("seguro prestamista → inconclusivo", status(seguro, "tarifa-seguro-0"), "inconclusivo");
  verdade("e diz o que precisa ser verificado",
    pega(seguro, "tarifa-seguro-0").observacao.includes("liberdade de escolha"));

  const nenhuma = periciar(contratoBase());
  eq("sem tarifa informada → inconclusivo", status(nenhuma, "tarifas"), "inconclusivo");

  // Várias tarifas não colidem de id
  const varias = periciar(
    contratoBase({
      tarifas: [
        { tipo: "tac", valor: 80000 },
        { tipo: "tec", valor: 5000 },
        { tipo: "registro", valor: 30000 },
      ],
    }),
  );
  eq("três tarifas viram três achados",
    varias.achados.filter((a) => a.id.startsWith("tarifa-")).length, 3);
}

// ————————————————————————————————————————————————————— taxa vs média BACEN

{
  eq("sem média informada → inconclusivo",
    status(periciar(contratoBase()), "taxa-vs-media"), "inconclusivo");

  // Abaixo da média
  eq("taxa abaixo da média → regular",
    status(periciar(contratoBase({ mediaBacenMensal: 0.025 })), "taxa-vs-media"), "regular");

  // ☠️ 1,40× a média saía como "regular" — o laudo afirmando normalidade de
  //    uma taxa 40% acima do mercado, com base num limiar de 1,5× que eu
  //    inventei e que não existe em lei nenhuma. Hoje a faixa é inconclusiva
  //    e o limiar adotado é declarado junto com o resultado.
  const cinza = periciar(contratoBase({ mediaBacenMensal: 0.0142 }));
  eq("1,40× a média → inconclusivo", status(cinza, "taxa-vs-media"), "inconclusivo");
  verdade("o limiar adotado aparece no laudo",
    pega(cinza, "taxa-vs-media").numeros.limiarAdotado === 1.5);
  verdade("e o laudo diz que o limiar é critério do perito, não lei",
    pega(cinza, "taxa-vs-media").observacao.includes("não percentual legal"));

  eq("2× a média → achado",
    status(periciar(contratoBase({ mediaBacenMensal: 0.00995 })), "taxa-vs-media"), "achado");

  // O limiar é parâmetro: o perito pode adotar outro e o laudo acompanha
  const rigoroso = periciar(contratoBase({ mediaBacenMensal: 0.0142, limiarAbusividade: 1.2 }));
  eq("limiar próprio muda a conclusão", status(rigoroso, "taxa-vs-media"), "achado");
  eq("e é o limiar informado que sai no laudo",
    pega(rigoroso, "taxa-vs-media").numeros.limiarAdotado, 1.2);
}

// ————————————————————————————————————————————————————— multa e comissão

{
  eq("multa de 3% → achado", status(periciar(contratoBase({ multaMoratoria: 0.03 })), "multa"), "achado");
  eq("multa de 2% → regular", status(periciar(contratoBase({ multaMoratoria: 0.02 })), "multa"), "regular");
  eq("multa não informada → inconclusivo", status(periciar(contratoBase()), "multa"), "inconclusivo");

  const cumulada = periciar(contratoBase({ comissaoPermanencia: true, multaMoratoria: 0.02 }));
  eq("comissão cumulada → achado", status(cumulada, "comissao-permanencia"), "achado");
  // ☠️ O enunciado da Súmula 472 não diz "vedada a cumulação" — diz que a
  //    cobrança EXCLUI A EXIGIBILIDADE dos demais encargos, e limita o valor
  //    da comissão à soma deles. Conferido contra o texto baixado do STJ.
  verdade("o laudo usa o efeito certo (exclui exigibilidade)",
    pega(cumulada, "comissao-permanencia").observacao.includes("exclui a exigibilidade"));
  verdade("e apura também o teto da própria comissão",
    pega(cumulada, "comissao-permanencia").observacao.includes("limitado à soma"));

  // Sem os demais encargos informados não dá pra apurar nem uma coisa nem
  // outra: é inconclusivo, nunca "regular"
  const sozinha = periciar(contratoBase({ comissaoPermanencia: true }));
  eq("comissão sem os encargos informados → inconclusivo",
    status(sozinha, "comissao-permanencia"), "inconclusivo");

  const semPrevisao = periciar(contratoBase());
  eq("sem previsão de comissão → regular", status(semPrevisao, "comissao-permanencia"), "regular");
}

// ————————————————————————————————————————————————————— Tema 958: a moldura

{
  // ☠️ A REGRA É A VALIDADE. O Tema 958, item 2.3, declara VÁLIDAS a tarifa
  //    de avaliação do bem e o ressarcimento de registro; a abusividade é a
  //    exceção (serviço não prestado / onerosidade excessiva). A 1ª versão
  //    tinha a moldura invertida e o laudo acusaria o que a Corte validou.
  const av = periciar(contratoBase({ tarifas: [{ tipo: "avaliacao", valor: 40000 }] }));
  verdade("avaliação: o laudo diz que é válida em regra",
    pega(av, "tarifa-avaliacao-0").observacao.includes("VÁLIDA em regra"));
  verdade("e não afirma irregularidade de ofício",
    pega(av, "tarifa-avaliacao-0").status === "inconclusivo");

  const terceiros = periciar(contratoBase({ tarifas: [{ tipo: "servicos-terceiros", valor: 90000 }] }));
  verdade("serviços de terceiros: a régua é a ESPECIFICAÇÃO",
    pega(terceiros, "tarifa-servicos-terceiros-0").observacao.includes("ESPECIFICA"));

  // Correspondente bancário e pré-gravame: Res.-CMN 3.954/2011, em vigor em
  // 25/02/2011. Válidos ATÉ 24/02, abusivos a partir de 25/02.
  const antes = periciar(
    contratoBase({ dataContrato: "2011-02-24", tarifas: [{ tipo: "correspondente", valor: 50000 }] }),
  );
  eq("correspondente em 24/02/2011 → regular", status(antes, "tarifa-correspondente-0"), "regular");
  const noDia958 = periciar(
    contratoBase({ dataContrato: "2011-02-25", tarifas: [{ tipo: "correspondente", valor: 50000 }] }),
  );
  eq("correspondente em 25/02/2011 → achado", status(noDia958, "tarifa-correspondente-0"), "achado");
  const preGravame = periciar(
    contratoBase({ dataContrato: "2011-02-25", tarifas: [{ tipo: "pre-gravame", valor: 5000 }] }),
  );
  eq("pré-gravame em 25/02/2011 → achado", status(preGravame, "tarifa-pre-gravame-0"), "achado");
  eq("pré-gravame se funda no Tema 972",
    pega(preGravame, "tarifa-pre-gravame-0").fundamento, "tema-972");
}

// ————————————————————————————————————————————————————— referência × motor

{
  // ☠️ Todo fundamento invocado pelo motor tem que EXISTIR na referência
  //    conferida. Chave órfã faria o laudo citar um verbete que ninguém
  //    conferiu — e não quebraria nada, porque a citação só some do rodapé.
  const { VERBETES } = await import("../referencias/jurisprudencia.mjs");
  const conhecidas = new Set(VERBETES.map((v) => v.chave));

  const usadas = new Set();
  const casos = [
    contratoBase({ taxaAnual: 0.0199 * 12, multaMoratoria: 0.03, comissaoPermanencia: true, mediaBacenMensal: 0.01 }),
    contratoBase({ dataContrato: "2015-06-10", tarifas: [{ tipo: "tac", valor: 1 }, { tipo: "tec", valor: 1 }, { tipo: "cadastro", valor: 1 }, { tipo: "avaliacao", valor: 1 }, { tipo: "registro", valor: 1 }, { tipo: "servicos-terceiros", valor: 1 }, { tipo: "correspondente", valor: 1 }, { tipo: "pre-gravame", valor: 1 }, { tipo: "seguro", valor: 1 }] }),
    contratoBase({ dataContrato: "2023-01-10" }),
  ];
  for (const caso of casos) for (const f of periciar(caso).fundamentosUsados) usadas.add(f);

  const orfas = [...usadas].filter((f) => !conhecidas.has(f));
  eq("nenhum fundamento órfão", orfas.join(",") || "nenhum", "nenhum");
  verdade("o motor exercita vários verbetes", usadas.size >= 7);

  // E todo verbete conferível tem texto transcrito da fonte
  const semTexto = VERBETES.filter((v) => v.conferidor !== "manual" && !v.texto).map((v) => v.chave);
  eq("todo verbete conferível tem texto transcrito", semTexto.join(",") || "nenhum", "nenhum");
  verdade("os verbetes manuais declaram a pendência",
    VERBETES.filter((v) => v.conferidor === "manual").every((v) => v.conferenciaManual?.includes("PENDENTE")));
}

// ————————————————————————————————————————————————————— amortização negativa

{
  const normal = periciar(contratoBase());
  eq("contrato normal → saldo decresce", status(normal, "amortizacao-negativa"), "regular");

  // Prestação menor que os juros do 1º mês
  const bolha = periciar({
    valorFinanciado: 10000000,
    prazo: 360,
    taxaMensal: 0.02,
    parcela: 100000,
    dataContrato: "2015-06-10",
    toleranciaCentavos: 1e12, // o portão não é o assunto deste caso
  });
  eq("prestação insuficiente → achado", status(bolha, "amortizacao-negativa"), "achado");
  eq("aponta a primeira prestação afetada", pega(bolha, "amortizacao-negativa").numeros.primeiraPrestacao, 1);
}

// ————————————————————————————————————————————————————— cenários e apuração

{
  const r = periciar(contratoBase({ taxaAnual: 0.0199 * 12, parcelasPagas: 12 }));
  const ids = r.cenarios.map((c) => c.id);
  verdade("cenário original existe", ids.includes("original"));
  verdade("cenário juros simples existe", ids.includes("juros-simples"));
  verdade("cenário SAC existe", ids.includes("sac"));

  // ☠️ REGRESSÃO — quando a anual declarada é o duodécuplo, anual/12 É a taxa
  //    mensal, e o cenário saía IDÊNTICO ao de juros simples, centavo a
  //    centavo. Duas colunas com o mesmo número num laudo é o que o
  //    assistente técnico do banco aponta primeiro. Nenhum teste pegou —
  //    quem pegou foi o gabarito impresso.
  verdade("duodécuplo declarado NÃO gera cenário redundante", !ids.includes("taxa-nominal"));
  {
    const js = r.cenarios.find((c) => c.id === "juros-simples").tabela;
    const outros = r.cenarios.filter((c) => c.id !== "juros-simples");
    verdade("nenhum cenário repete o total de outro",
      !outros.some((c) => c.tabela.totalPago === js.totalPago));
    const totais = r.cenarios.map((c) => c.tabela.totalPago);
    eq("todos os cenários têm total distinto", new Set(totais).size, totais.length);
  }

  // Com a anual EFETIVA declarada, anual/12 devolveria o próprio contrato
  const efetiva = periciar(contratoBase({ taxaAnual: Math.pow(1.0199, 12) - 1 }));
  verdade("anual efetiva NÃO gera cenário redundante",
    !efetiva.cenarios.map((c) => c.id).includes("taxa-nominal"));

  // Só uma anual que não é nem uma nem outra produz um cenário que informa algo
  const estranha = periciar(contratoBase({ taxaAnual: 0.45 }));
  verdade("anual incompatível gera o cenário sem capitalizar",
    estranha.cenarios.map((c) => c.id).includes("taxa-nominal"));
  verdade("e ele é diferente do juros simples",
    estranha.cenarios.find((c) => c.id === "taxa-nominal").tabela.totalPago !==
    estranha.cenarios.find((c) => c.id === "juros-simples").tabela.totalPago);

  const simples = r.apuracao.find((a) => a.cenario === "juros-simples");
  verdade("juros simples custa menos que o contratado", simples.diferencaTotal > 0);
  verdade("apura o pago a maior até aqui", simples.pagoAMaiorAteAqui > 0);
  eq("respeita as parcelas pagas informadas", simples.parcelasPagas, 12);
  verdade("pago a maior + a compensar = diferença total",
    simples.pagoAMaiorAteAqui + simples.aCompensarNoSaldo === simples.diferencaTotal);
  verdade("original não entra na apuração", !r.apuracao.some((a) => a.cenario === "original"));

  // ☠️ REGRESSÃO — o SAC tem prestação decrescente. A "diferença por
  //    prestação" saía −R$ 491,87 ao lado de uma economia total de R$ 4.449:
  //    a mesma tabela dizendo que o cenário é mais caro e mais barato.
  const sac = r.apuracao.find((a) => a.cenario === "sac");
  verdade("SAC é marcado como prestação variável", sac.prestacaoVariavel === true);
  eq("SAC não inventa diferença por prestação", sac.diferencaPorParcela, null);
  eq("SAC não inventa prestação única", sac.parcelaCenario, null);
  verdade("SAC informa primeira e última prestação",
    sac.primeiraPrestacaoCenario > sac.ultimaPrestacaoCenario);
  verdade("SAC explica o valor negativo do período", sac.observacao !== null);
  verdade("SAC continua mais barato no contrato inteiro", sac.diferencaTotal > 0);

  // Price tem prestação fixa: aí a diferença por prestação existe mesmo
  verdade("juros simples tem prestação fixa", simples.prestacaoVariavel === false);
  verdade("e diferença por prestação de verdade", simples.diferencaPorParcela > 0);
  eq("prestação fixa não carrega a ressalva", simples.observacao, null);

  // parcelasPagas não informado ⇒ nada foi pago a maior "até aqui"
  const zerado = periciar(contratoBase({ taxaAnual: 0.0199 * 12 }));
  eq("sem parcelas pagas, o pago a maior é zero",
    zerado.apuracao.find((a) => a.cenario === "juros-simples").pagoAMaiorAteAqui, 0);
  // e não pode passar do prazo
  const demais = periciar(contratoBase({ parcelasPagas: 999 }));
  eq("parcelas pagas não passam do prazo",
    demais.apuracao[0].parcelasPagas, 48);
}

// ————————————————————————————————————————————————————— invariantes do laudo

{
  const r = periciar(contratoBase({ tarifas: [{ tipo: "tac", valor: 80000 }], multaMoratoria: 0.03 }));

  verdade("todo achado tem um dos três estados",
    r.achados.every((a) => ["achado", "regular", "inconclusivo"].includes(a.status)));
  verdade("todo achado tem título", r.achados.every((a) => a.titulo && a.titulo.length > 3));
  verdade("o resumo soma o total",
    r.resumoAchados.achado + r.resumoAchados.regular + r.resumoAchados.inconclusivo === r.achados.length);
  verdade("há inconclusivos de verdade (não colapsados em regular)", r.resumoAchados.inconclusivo > 0);
  verdade("fundamentos usados são listados", r.fundamentosUsados.length > 0);

  // ☠️ nenhum texto de lei mora no motor: fundamento é CHAVE, não citação
  const temCitacao = r.achados.some(
    (a) => a.fundamento && /(súmula|sumula|art\.|tema)\s*\d/i.test(a.fundamento),
  );
  verdade("fundamento é chave, não citação de lei", !temCitacao);
  verdade("as chaves são identificadores simples",
    r.achados.every((a) => a.fundamento === null || /^[a-z0-9-]+$/.test(a.fundamento)));
}

// ————————————————————————————————————————————————————— relatório

console.log("");
if (falhas.length === 0) {
  console.log(`  ✓ ${ok} asserções — camada pericial OK`);
} else {
  console.log(`  ✓ ${ok} passaram`);
  console.log(`  ✗ ${falhas.length} FALHARAM:\n`);
  for (const f of falhas) console.log(`   • ${f}\n`);
}
console.log("");
process.exit(falhas.length === 0 ? 0 : 1);
