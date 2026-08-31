// ============================================================================
// GABARITO IMPRESSO — `node motor/exemplo.mjs`
// ============================================================================
// Roda um contrato realista e despeja tudo no terminal, com os números à
// vista. Existe porque bateria verde prova que o código faz o que o teste
// mandou, não que o NÚMERO está certo. Aqui é onde se confere com o olho —
// e é assim que a casa já pegou o que teste unitário não pegou.
// ============================================================================

import { emCentavos, formatarBRL, formatarTaxa, parcelaPrice, anualEfetiva, anualNominal } from "./calculo.mjs";
import { periciar } from "./achados.mjs";

// Financiamento de veículo típico: R$ 60.000 em 48 meses a 1,99% a.m.,
// com TAC e IOF embutidos no valor financiado.
const valorFinanciado = emCentavos(60000);
const taxaMensal = 0.0199;
const prazo = 48;

const contrato = {
  identificacao: "Contrato de financiamento de veículo nº 000.000-0 (EXEMPLO)",
  valorFinanciado,
  prazo,
  taxaMensal,
  taxaAnual: 0.0199 * 12, // o contrato declara o DUODÉCUPLO: 23,88% a.a.
  parcela: parcelaPrice(valorFinanciado, taxaMensal, prazo),
  dataContrato: "2021-03-15",
  valorLiberado: emCentavos(57500), // R$ 2.500 não chegaram na mão do cliente
  tarifas: [
    { tipo: "tac", valor: emCentavos(1500), financiada: true },
    { tipo: "avaliacao", valor: emCentavos(400), financiada: true },
    { tipo: "seguro", valor: emCentavos(600), financiada: true },
  ],
  iofFinanciado: emCentavos(1000),
  cetAnualInformado: 0.2688,
  multaMoratoria: 0.03,
  parcelasPagas: 18,
  mediaBacenMensal: 0.0142, // média BACEN da modalidade no mês (exemplo)
};

const r = periciar(contrato);

const linha = (c = "─") => console.log("  " + c.repeat(74));
const titulo = (t) => {
  console.log("");
  linha("━");
  console.log(`  ${t}`);
  linha("━");
};

console.log("");
console.log(`  ${contrato.identificacao}`);

if (!r.pode) {
  titulo("PERÍCIA NÃO PODE SER REALIZADA");
  for (const p of r.problemas) console.log(`  ✗ ${p}`);
  console.log("");
  process.exit(1);
}

// ————————————————————————————————————————————————————— entrada conferida

titulo("1. DADOS DO CONTRATO");
const d = [
  ["Valor financiado", formatarBRL(contrato.valorFinanciado)],
  ["Valor efetivamente liberado", formatarBRL(contrato.valorLiberado)],
  ["Prazo", `${contrato.prazo} prestações`],
  ["Prestação", formatarBRL(contrato.parcela)],
  ["Taxa mensal pactuada", formatarTaxa(contrato.taxaMensal)],
  ["Taxa anual declarada", formatarTaxa(contrato.taxaAnual, 2)],
  ["  ↳ duodécuplo da mensal", formatarTaxa(anualNominal(contrato.taxaMensal), 2)],
  ["  ↳ capitalização da mensal", formatarTaxa(anualEfetiva(contrato.taxaMensal), 2)],
  ["Data do contrato", contrato.dataContrato],
  ["Prestações pagas", String(contrato.parcelasPagas)],
];
for (const [k, v] of d) console.log(`  ${k.padEnd(34)} ${v.padStart(20)}`);

console.log("");
console.log(
  `  Conferência de coerência: prestação calculada ${formatarBRL(r.coerencia.parcelaCalculada)} ` +
    `× contrato ${formatarBRL(r.coerencia.parcelaContrato)} → ${r.coerencia.bate ? "confere" : "NÃO CONFERE"}`,
);

// ————————————————————————————————————————————————————— achados

titulo(
  `2. ACHADOS  —  ${r.resumoAchados.achado} com divergência · ` +
    `${r.resumoAchados.regular} regulares · ${r.resumoAchados.inconclusivo} inconclusivos`,
);

const marca = { achado: "▲", regular: "·", inconclusivo: "?" };
for (const a of r.achados) {
  console.log("");
  console.log(`  ${marca[a.status]} ${a.titulo}  [${a.status}]${a.fundamento ? `  ← ${a.fundamento}` : ""}`);
  for (const [k, v] of Object.entries(a.numeros ?? {})) {
    if (v === null || v === undefined) continue;
    // ⚠️ Razão e limiar são MÚLTIPLOS, não percentuais: formatados como taxa
    //    saíam "razao 140,1408 %" ao lado de "limiarAdotado 150,0000 %",
    //    como se fossem dois percentuais comparáveis. São "1,40×" e "1,50×".
    const ehMultiplo = /razao|limiar/i.test(k);
    const mostra =
      typeof v !== "number"
        ? String(v)
        : ehMultiplo
          ? `${v.toFixed(2).replace(".", ",")}×`
          : Number.isInteger(v) && Math.abs(v) > 999
            ? formatarBRL(v)
            : Number.isInteger(v)
              ? String(v)
              : formatarTaxa(v);
    console.log(`      ${k.padEnd(28)} ${mostra}`);
  }
  if (a.observacao) {
    const palavras = a.observacao.split(" ");
    let l = "     ";
    for (const p of palavras) {
      if ((l + " " + p).length > 76) {
        console.log(l);
        l = "     ";
      }
      l += " " + p;
    }
    console.log(l);
  }
}

// ————————————————————————————————————————————————————— cenários

titulo("3. CENÁRIOS DE RECÁLCULO");
console.log("");
console.log(
  "  " +
    "Cenário".padEnd(34) +
    "Prestação".padStart(14) +
    "Total pago".padStart(16) +
    "Juros".padStart(14),
);
linha();
for (const c of r.cenarios) {
  console.log(
    "  " +
      c.rotulo.padEnd(34) +
      formatarBRL(c.tabela.parcela).padStart(14) +
      formatarBRL(c.tabela.totalPago).padStart(16) +
      formatarBRL(c.tabela.totalJuros).padStart(14),
  );
}

// ————————————————————————————————————————————————————— apuração

titulo("4. APURAÇÃO");
console.log("");
for (const a of r.apuracao) {
  console.log(`  ${a.rotulo}`);
  console.log(`      diferença por prestação      ${formatarBRL(a.diferencaPorParcela)}`);
  console.log(`      diferença no contrato        ${formatarBRL(a.diferencaTotal)}`);
  console.log(`      pago a maior em ${String(a.parcelasPagas).padStart(2)} prestações ${formatarBRL(a.pagoAMaiorAteAqui)}`);
  console.log(`      a compensar no saldo         ${formatarBRL(a.aCompensarNoSaldo)}`);
  console.log("");
}

titulo("5. FUNDAMENTOS INVOCADOS (chaves — verbete em referencias/)");
console.log("");
console.log(`  ${r.fundamentosUsados.join(" · ")}`);
console.log("");
