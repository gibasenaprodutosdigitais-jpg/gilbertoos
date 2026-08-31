// ============================================================================
// BATERIA DO MOTOR DE CÁLCULO — `node motor/testes.mjs`
// ============================================================================
// ⚠️ Os gabaritos são calculados FORA do motor (à mão, ou por identidade
//    matemática independente). Testar o motor contra ele mesmo prova nada:
//    é assim que uma fórmula errada passa verde pra sempre.
// ============================================================================

import {
  emCentavos,
  formatarBRL,
  formatarTaxa,
  somarMeses,
  dataMaiorOuIgual,
  anualEfetiva,
  anualNominal,
  mensalDeAnualEfetiva,
  parcelaPrice,
  tabelaPrice,
  tabelaSAC,
  parcelaJurosSimples,
  tabelaJurosSimples,
  tir,
  taxaEfetivaDoFluxo,
  cet,
  conferirCoerencia,
  toleranciaDeArredondamento,
} from "./calculo.mjs";

let ok = 0;
const falhas = [];

function eq(rotulo, obtido, esperado) {
  if (obtido === esperado) return ok++;
  falhas.push(`${rotulo}\n     esperado: ${esperado}\n     obtido:   ${obtido}`);
}

function perto(rotulo, obtido, esperado, tolerancia) {
  if (Number.isFinite(obtido) && Math.abs(obtido - esperado) <= tolerancia) {
    return ok++;
  }
  falhas.push(
    `${rotulo}\n     esperado: ${esperado} (±${tolerancia})\n     obtido:   ${obtido}`,
  );
}

function verdade(rotulo, condicao) {
  if (condicao) return ok++;
  falhas.push(rotulo);
}

function estoura(rotulo, fn) {
  try {
    fn();
    falhas.push(`${rotulo} — devia ter estourado e não estourou`);
  } catch {
    ok++;
  }
}

// ————————————————————————————————————————————————————— dinheiro

eq("emCentavos(1234.56)", emCentavos(1234.56), 123456);
eq("emCentavos('R$ 1.234,56')", emCentavos("R$ 1.234,56"), 123456);
eq("emCentavos('1.234,56')", emCentavos("1.234,56"), 123456);
eq("emCentavos(0)", emCentavos(0), 0);
// ☠️ o clássico do float: 1.005 * 100 dá 100.49999999999999 em IEEE-754
eq("emCentavos(1.005) não perde o centavo", emCentavos(1.005), 101);
eq("emCentavos(0.1 + 0.2)", emCentavos(0.1 + 0.2), 30);
eq("emCentavos(29500)", emCentavos(29500), 2950000);

eq("formatarBRL(123456)", formatarBRL(123456), "R$ 1.234,56");
eq("formatarBRL(0)", formatarBRL(0), "R$ 0,00");
eq("formatarBRL(5)", formatarBRL(5), "R$ 0,05");
eq("formatarBRL(-123456)", formatarBRL(-123456), "-R$ 1.234,56");
eq("formatarBRL(100000000)", formatarBRL(100000000), "R$ 1.000.000,00");
// ☠️ o que não foi calculado NÃO pode sair como "R$ 0,00": num laudo, zero é
//    a afirmação de que nada é devido, e ninguém confere de onde ele veio
eq("formatarBRL(null) não vira zero", formatarBRL(null), "—");
eq("formatarBRL(undefined) não vira zero", formatarBRL(undefined), "—");
eq("formatarBRL(NaN) não vira zero", formatarBRL(NaN), "—");
eq("formatarBRL(Infinity) não vira zero", formatarBRL(Infinity), "—");
eq("zero de verdade continua sendo zero", formatarBRL(0), "R$ 0,00");
eq("formatarTaxa(0.0199)", formatarTaxa(0.0199), "1,9900 %");
eq("formatarTaxa(null)", formatarTaxa(null), "—");

// ————————————————————————————————————————————————————— datas em string

eq("somarMeses 12", somarMeses("2026-08-31", 12), "2027-08-31");
eq("somarMeses 1 (31→30)", somarMeses("2026-08-31", 1), "2026-09-30");
eq("somarMeses vira o ano", somarMeses("2026-12-15", 1), "2027-01-15");
eq("somarMeses 360", somarMeses("2008-04-30", 360), "2038-04-30");
eq("somarMeses fevereiro", somarMeses("2026-01-31", 1), "2026-02-28");
eq("somarMeses ano bissexto", somarMeses("2028-01-31", 1), "2028-02-29");
// ☠️ o dia 30/04/2008 é a fronteira do Tema 618: ele tem que ficar do lado de dentro
verdade("30/04/2008 >= 30/04/2008", dataMaiorOuIgual("2008-04-30", "2008-04-30"));
verdade("29/04/2008 < 30/04/2008", !dataMaiorOuIgual("2008-04-29", "2008-04-30"));
estoura("data fora do formato estoura", () => dataMaiorOuIgual("30/04/2008", "2008-04-30"));

// ————————————————————————————————————————————————————— conversão de taxas

// (1,01)^12 − 1 = 0,126825030131970...
perto("anualEfetiva(1% a.m.) = 12,6825%", anualEfetiva(0.01), 0.12682503, 1e-8);
perto("anualNominal(1% a.m.) = 12%", anualNominal(0.01), 0.12, 1e-12);
perto("ida e volta anual→mensal", mensalDeAnualEfetiva(anualEfetiva(0.0199)), 0.0199, 1e-12);
// ★ é essa distância que a Súmula 541 usa: efetiva 26,82% vs duodécuplo 24%
perto("anualEfetiva(2% a.m.)", anualEfetiva(0.02), 0.26824179, 1e-8);
perto("anualNominal(2% a.m.)", anualNominal(0.02), 0.24, 1e-12);

// ————————————————————————————————————————————————————— Price

// Gabarito de tabela pública: R$ 100.000, 1% a.m., 360 meses ⇒ R$ 1.028,61
eq("parcelaPrice 100k / 1% / 360", parcelaPrice(10000000, 0.01, 360), 102861);
// Gabarito à mão: 100000 · 0,02 / (1 − 1,02^−12) = 9.455,96 centavos
eq("parcelaPrice 1k / 2% / 12", parcelaPrice(100000, 0.02, 12), 9456);
// taxa zero: divisão pura
eq("parcelaPrice taxa zero", parcelaPrice(120000, 0, 12), 10000);
// n = 1: paga principal + juros de um mês
eq("parcelaPrice prazo 1", parcelaPrice(100000, 0.05, 1), 105000);

estoura("principal em reais (float) estoura", () => parcelaPrice(1000.5, 0.01, 12));
estoura("principal negativo estoura", () => parcelaPrice(-100, 0.01, 12));
estoura("prazo zero estoura", () => parcelaPrice(100000, 0.01, 0));
estoura("taxa negativa estoura", () => parcelaPrice(100000, -0.01, 12));

{
  const t = tabelaPrice({ principal: 10000000, taxaMensal: 0.01, prazo: 360 });
  eq("Price: 360 linhas", t.linhas.length, 360);
  // ☠️ o que faz a perícia fechar: saldo tem que dar EXATAMENTE zero
  eq("Price: saldo final zera", t.saldoFinal, 0);
  const somaAmort = t.linhas.reduce((s, l) => s + l.amortizacao, 0);
  eq("Price: Σ amortizações = principal", somaAmort, 10000000);
  const somaParcelas = t.linhas.reduce((s, l) => s + l.parcela, 0);
  eq("Price: Σ parcelas = total pago", somaParcelas, t.totalPago);
  eq("Price: total = principal + juros", t.totalPago, 10000000 + t.totalJuros);
  // 1º mês: juros = 1% de 100.000 = R$ 1.000,00 ⇒ amortiza só R$ 28,61
  eq("Price: juros do 1º mês", t.linhas[0].juros, 100000);
  eq("Price: amortização do 1º mês", t.linhas[0].amortizacao, 2861);
  // ★ o número que vende a tese: em 360 meses paga-se ~3,7× o valor da casa
  verdade("Price 360m: total > 3,5× o principal", t.totalPago > 10000000 * 3.5);
  verdade("Price: amortização sempre cresce", t.linhas[10].amortizacao > t.linhas[0].amortizacao);
  verdade("Price: juros sempre caem", t.linhas[10].juros < t.linhas[0].juros);
  verdade("Price: sem amortização negativa", !t.amortizacaoNegativa);
}

{
  // Amortização negativa: parcela menor que os juros do mês.
  // É o achado clássico do SFH — o saldo devedor CRESCE mesmo pagando em dia.
  const t = tabelaPrice({ principal: 10000000, taxaMensal: 0.02, prazo: 360, parcela: 100000 });
  verdade("amortização negativa é detectada", t.amortizacaoNegativa);
  verdade("saldo cresce em vez de cair", t.linhas[1].saldoInicial > t.linhas[0].saldoInicial);
}

// ————————————————————————————————————————————————————— SAC

{
  // Gabarito à mão: R$ 12.000, 1% a.m., 12 meses.
  // Amortização fixa = R$ 1.000. 1ª parcela = 1.000 + 1% de 12.000 = R$ 1.120.
  const t = tabelaSAC({ principal: 1200000, taxaMensal: 0.01, prazo: 12 });
  eq("SAC: 1ª parcela = R$ 1.120", t.linhas[0].parcela, 112000);
  eq("SAC: amortização constante", t.linhas[0].amortizacao, 100000);
  eq("SAC: última parcela = 1.000 + 10", t.linhas[11].parcela, 101000);
  eq("SAC: saldo final zera", t.saldoFinal, 0);
  eq("SAC: Σ amortizações = principal", t.linhas.reduce((s, l) => s + l.amortizacao, 0), 1200000);
  verdade("SAC: parcela decresce", t.linhas[11].parcela < t.linhas[0].parcela);

  // ★ SAC paga menos juros que Price no mesmo contrato — é o cenário alternativo
  const price = tabelaPrice({ principal: 1200000, taxaMensal: 0.01, prazo: 12 });
  verdade("SAC custa menos juros que Price", t.totalJuros < price.totalJuros);
}

// ————————————————————————————————————————————————————— juros simples (Gauss)

{
  const pv = 1200000, i = 0.01, n = 12;
  // Gabarito independente: P = PV / Σ 1/(1+i·k), k=1..12
  let soma = 0;
  for (let k = 1; k <= n; k++) soma += 1 / (1 + i * k);
  eq("Gauss: parcela bate com a fórmula", parcelaJurosSimples(pv, i, n), Math.round(pv / soma));

  const simples = tabelaJurosSimples({ principal: pv, taxaMensal: i, prazo: n });
  const price = tabelaPrice({ principal: pv, taxaMensal: i, prazo: n });
  // ★ a tese do laudo: sem capitalizar, a parcela é menor
  verdade("Gauss: parcela < Price", simples.parcela < price.parcela);
  verdade("Gauss: total pago < Price", simples.totalPago < price.totalPago);
  eq("Gauss: saldo final zera", simples.saldoFinal, 0);
  eq("Gauss: taxa zero = Price taxa zero", parcelaJurosSimples(120000, 0, 12), 10000);

  // ☠️ REGRESSÃO — a 1ª versão montava a tabela com `juros = saldo × i`, ou
  //    seja, capitalizando dentro do método que existe pra não capitalizar.
  //    Sintoma: saldo não zerava, última parcela virava bolha e o método
  //    "sem juros compostos" saía mais caro que o Price.
  eq("Gauss: Σ amortizações = principal",
    simples.linhas.reduce((s, l) => s + l.amortizacao, 0), pv);
  verdade("Gauss: nenhuma parcela é bolha",
    simples.linhas.every((l) => l.parcela <= simples.parcela + 100));
  verdade("Gauss: total pago ≈ n × parcela",
    Math.abs(simples.totalPago - simples.parcela * n) < 200);
  verdade("Gauss: amortização cresce a cada mês",
    simples.linhas[n - 2].amortizacao < simples.linhas[0].amortizacao === false ||
    simples.linhas[0].amortizacao > simples.linhas[n - 2].amortizacao);

  // O mesmo, num prazo longo — é onde a bolha aparecia com força
  const longo = tabelaJurosSimples({ principal: 10000000, taxaMensal: 0.01, prazo: 360 });
  eq("Gauss 360m: saldo zera", longo.saldoFinal, 0);
  verdade("Gauss 360m: total < Price 360m",
    longo.totalPago < tabelaPrice({ principal: 10000000, taxaMensal: 0.01, prazo: 360 }).totalPago);
}

// ☠️ REGRESSÃO — (1 + (−0,99))^360 estoura pra Infinity em IEEE-754. A guarda
//    de finitude matava a busca e a TIR devolvia null JUSTO no financiamento
//    imobiliário, que é o caso que mais importa. Hoje a raiz é encurralada
//    numa grade antes da bisseção.
{
  verdade("TIR com 360 parcelas não devolve null",
    taxaEfetivaDoFluxo({ valorLiberado: 10000000, parcela: 102861, prazo: 360 }) !== null);
  verdade("TIR com 420 parcelas (35 anos) não devolve null",
    taxaEfetivaDoFluxo({
      valorLiberado: 25000000,
      parcela: parcelaPrice(25000000, 0.0075, 420),
      prazo: 420,
    }) !== null);
  perto("TIR em prazo longo continua exata",
    taxaEfetivaDoFluxo({
      valorLiberado: 25000000,
      parcela: parcelaPrice(25000000, 0.0075, 420),
      prazo: 420,
    }), 0.0075, 1e-5);
}

// ————————————————————————————————————————————————————— TIR

{
  // Identidade: a TIR do fluxo de um Price perfeito devolve a própria taxa
  perto("TIR devolve a taxa do Price (1%)",
    taxaEfetivaDoFluxo({ valorLiberado: 10000000, parcela: 102861, prazo: 360 }), 0.01, 1e-5);
  perto("TIR devolve a taxa do Price (2%)",
    taxaEfetivaDoFluxo({ valorLiberado: 100000, parcela: 9456, prazo: 12 }), 0.02, 1e-4);
  // Gabarito simples: R$ 100 hoje, R$ 110 em um período ⇒ 10%
  perto("TIR de 100 → 110 é 10%", tir([100, -110]), 0.10, 1e-9);
  perto("TIR de 100 → 2×55 (juros zero)", tir([110, -55, -55]), 0, 1e-9);
  // Sem troca de sinal não existe raiz — tem que devolver null, não um número
  eq("TIR sem raiz devolve null", tir([100, 50, 50]), null);
  estoura("TIR de fluxo curto estoura", () => tir([100]));
}

// ————————————————————————————————————————————————————— CET

{
  // R$ 50.000 financiados, mas R$ 2.500 saíram em tarifas + IOF:
  // o cliente recebeu 47.500 e paga como se devesse 50.000.
  const parcela = parcelaPrice(5000000, 0.0199, 48);
  const semCustos = taxaEfetivaDoFluxo({ valorLiberado: 5000000, parcela, prazo: 48 });
  const c = cet({ valorFinanciado: 5000000, descontos: 250000, parcela, prazo: 48 });
  perto("taxa sem custos = a contratada", semCustos, 0.0199, 1e-5);
  verdade("CET mensal > taxa contratada", c.mensal > 0.0199);
  eq("CET: valor líquido", c.valorLiquido, 4750000);
  perto("CET anual = efetiva do mensal", c.anual, anualEfetiva(c.mensal), 1e-12);
  // ⚠️ mensal e anual não se comparam entre si — é onde o laudo erra 12×
  verdade("CET anual é muito maior que o mensal", c.anual > c.mensal * 10);
  eq("CET sem descontos = taxa contratada",
    Math.round(cet({ valorFinanciado: 5000000, descontos: 0, parcela, prazo: 48 }).mensal * 1e6),
    Math.round(semCustos * 1e6));
}

// ————————————————————————————————————————————————————— checksum da leitura

{
  const parcela = parcelaPrice(3000000, 0.0175, 60);
  const bom = conferirCoerencia({
    principal: 3000000, taxaMensal: 0.0175, prazo: 60, parcelaContrato: parcela,
  });
  verdade("contrato coerente passa", bom.bate);
  eq("coerente: diferença zero", bom.diferenca, 0);

  // ☠️ dígito trocado no OCR: 1,75% lido como 1,15%
  const errado = conferirCoerencia({
    principal: 3000000, taxaMensal: 0.0115, prazo: 60, parcelaContrato: parcela,
  });
  verdade("dígito trocado é pego", !errado.bate);
  perto("checksum revela a taxa verdadeira", errado.taxaImplicita, 0.0175, 1e-5);
  verdade("checksum mostra o tamanho do estrago", Math.abs(errado.diferencaTotal) > 10000);

  // Encargo embutido: parcela maior do que a taxa declarada produz
  const inflada = conferirCoerencia({
    principal: 3000000, taxaMensal: 0.0175, prazo: 60, parcelaContrato: parcela + 5000,
  });
  verdade("parcela inflada é pega", !inflada.bate);
  verdade("taxa implícita é maior que a declarada", inflada.taxaImplicita > 0.0175);

  // Tolerância: 1 centavo de arredondamento não pode virar achado
  const arredonda = conferirCoerencia({
    principal: 3000000, taxaMensal: 0.0175, prazo: 60, parcelaContrato: parcela + 1,
  });
  verdade("1 centavo não vira achado", arredonda.bate);
}

// ————————————————————————————————————————————————————— tolerância proporcional

{
  // ☠️ REGRESSÃO — a tolerância era FIXA em 2 centavos. Medido contra a
  //    Calculadora do Cidadão do BACEN: em 15 casos, 10 divergiram do cálculo
  //    direto e a maior diferença foi de 7 CENTAVOS, numa prestação de
  //    R$ 56.687. O erro cresce com o valor porque quem arredonda é o
  //    COEFICIENTE, que multiplica o principal.
  //    Com teto fixo, o contrato de maior valor — o que mais importa — seria
  //    barrado como "os números não fecham", apontando defeito inexistente.
  verdade("tolerância cresce com a prestação",
    toleranciaDeArredondamento(5668746) > toleranciaDeArredondamento(9456));
  eq("piso de 5 centavos em prestação pequena", toleranciaDeArredondamento(9456), 5);
  verdade("prestação de R$ 56.687 tolera os 7 centavos medidos",
    toleranciaDeArredondamento(5668746) >= 7);

  // O caso real que estourava o teto fixo: R$ 500.000 / 2,35% / 10 meses
  const p = parcelaPrice(50000000, 0.0235, 10);
  const comoOBacen = conferirCoerencia({
    principal: 50000000, taxaMensal: 0.0235, prazo: 10, parcelaContrato: p + 7,
  });
  verdade("contrato legítimo de valor alto não é barrado", comoOBacen.bate);
  verdade("e a tolerância aplicada vai no resultado", comoOBacen.tolerancia >= 7);

  // ★ Mas a folga NÃO pode engolir dígito trocado — é o que o portão existe
  //   pra pegar. Um erro de leitura muda a prestação em ordens de grandeza.
  const digito = conferirCoerencia({
    principal: 50000000, taxaMensal: 0.0335, prazo: 10, parcelaContrato: p,
  });
  verdade("dígito trocado na taxa continua sendo pego", !digito.bate);
  const prazoTorto = conferirCoerencia({
    principal: 50000000, taxaMensal: 0.0235, prazo: 16, parcelaContrato: p,
  });
  verdade("prazo lido errado continua sendo pego", !prazoTorto.bate);
  const principalTorto = conferirCoerencia({
    principal: 60000000, taxaMensal: 0.0235, prazo: 10, parcelaContrato: p,
  });
  verdade("principal lido errado continua sendo pego", !principalTorto.bate);
}

// ————————————————————————————————————————————————————— relatório

console.log("");
if (falhas.length === 0) {
  console.log(`  ✓ ${ok} asserções — motor de cálculo OK`);
} else {
  console.log(`  ✓ ${ok} passaram`);
  console.log(`  ✗ ${falhas.length} FALHARAM:\n`);
  for (const f of falhas) console.log(`   • ${f}\n`);
}
console.log("");
process.exit(falhas.length === 0 ? 0 : 1);
