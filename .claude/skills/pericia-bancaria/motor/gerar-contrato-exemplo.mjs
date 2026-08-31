// ============================================================================
// GERADOR DE CONTRATO DE EXEMPLO — `node motor/gerar-contrato-exemplo.mjs`
// ============================================================================
// Escreve um contrato bancário fictício em `exemplos/` e imprime o GABARITO
// no terminal: quais achados a perícia TEM que encontrar naquele documento.
//
// ★ POR QUE COM GABARITO: é o padrão que já pegou defeito nesta casa mais de
//   uma vez. Um documento de teste sem gabarito só prova que o código não
//   quebra; com gabarito, ele prova que o código ACHOU O QUE DEVIA ACHAR.
//
// ⚠️ O QUE ISTO **NÃO** TESTA, e precisa ficar dito: PDF escaneado de verdade,
//    layout de banco real e a nomenclatura que cada instituição usa para as
//    mesmas tarifas. Isso só um contrato real resolve — e até lá é limitação
//    declarada, não coberta.
//
// ☠️ Tudo aqui é FICTÍCIO. Nomes, CPF, CNPJ e números são inventados. Nenhum
//    banco real é nomeado: um documento que imita instrumento de instituição
//    identificável não deve existir nem como exemplo.
// ============================================================================

import { writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import { parcelaPrice, emCentavos, formatarBRL, formatarTaxa, somarMeses, anualEfetiva, anualNominal } from "./calculo.mjs";
import { periciar } from "./achados.mjs";

const AQUI = dirname(fileURLToPath(import.meta.url));
const SAIDA = join(AQUI, "..", "exemplos");

// ————————————————————————————————————————————————————— o caso

const valorBem = emCentavos(72000);
const entrada = emCentavos(15000);
const tac = emCentavos(1450);
const avaliacao = emCentavos(380);
const registro = emCentavos(295);
const seguro = emCentavos(1180);
const iof = emCentavos(1195);

const valorLiberado = valorBem - entrada; // o que foi pago ao vendedor
const valorFinanciado = valorLiberado + tac + avaliacao + registro + seguro + iof;
const taxaMensal = 0.0212;
const prazo = 48;
const parcela = parcelaPrice(valorFinanciado, taxaMensal, prazo);
const dataContrato = "2022-09-14";

const contrato = {
  identificacao: "Cédula de Crédito Bancário nº 4471-0092281/22 (EXEMPLO FICTÍCIO)",
  valorFinanciado,
  valorLiberado,
  prazo,
  taxaMensal,
  // ARMADILHA 1: o contrato declara o DUODÉCUPLO (25,44%), não a efetiva (28,60%)
  taxaAnual: anualNominal(taxaMensal),
  parcela,
  dataContrato,
  tarifas: [
    { tipo: "tac", valor: tac, financiada: true },                 // ARMADILHA 2
    { tipo: "avaliacao", valor: avaliacao, financiada: true },     // inconclusivo
    { tipo: "registro", valor: registro, financiada: true },       // inconclusivo
    { tipo: "seguro", valor: seguro, financiada: true },           // inconclusivo
  ],
  iofFinanciado: iof,
  // ARMADILHA 3: CET declarado abaixo do real (as tarifas embutidas não entraram)
  cetAnualInformado: 0.2860,
  multaMoratoria: 0.03, // ARMADILHA 4: acima do teto de 2% do CDC
  comissaoPermanencia: true,
  jurosMoratorios: 0.01,
  parcelasPagas: 22,
  mediaBacenMensal: 0.0168,
};

// ————————————————————————————————————————————————————— o documento

const brl = (c) => formatarBRL(c).replace("R$ ", "");
const pct = (f, casas = 2) => (f * 100).toFixed(casas).replace(".", ",");
const dataBR = (d) => d.split("-").reverse().join("/");

const doc = `
========================================================================
                  CÉDULA DE CRÉDITO BANCÁRIO
                    (DOCUMENTO FICTÍCIO — EXEMPLO)
========================================================================

Nº do instrumento .......: 4471-0092281/22
Data de emissão .........: ${dataBR(dataContrato)}
Praça de emissão ........: Belo Horizonte / MG

EMITENTE (devedor)
  Nome ..................: JOÃO DA SILVA SANTOS
  CPF ...................: 000.000.000-00
  Endereço ..............: Rua Exemplo, 100 — Belo Horizonte / MG

CREDOR
  Instituição financeira consignada no campo próprio deste instrumento.

------------------------------------------------------------------------
QUADRO I — CARACTERÍSTICAS DA OPERAÇÃO
------------------------------------------------------------------------

  Finalidade ..............: Aquisição de veículo automotor
  Valor do bem ............: R$ ${brl(valorBem)}
  Recursos próprios .......: R$ ${brl(entrada)}
  Valor liberado ao
    vendedor do bem .......: R$ ${brl(valorLiberado)}

  VALOR TOTAL FINANCIADO ..: R$ ${brl(valorFinanciado)}

  Prazo ...................: ${prazo} (quarenta e oito) meses
  Sistema de amortização ..: Tabela Price (prestações fixas)
  Vencimento da 1ª parcela : ${dataBR(somarMeses(dataContrato, 1))}
  Vencimento da última ....: ${dataBR(somarMeses(dataContrato, prazo))}

  VALOR DA PRESTAÇÃO ......: R$ ${brl(parcela)}

------------------------------------------------------------------------
QUADRO II — ENCARGOS
------------------------------------------------------------------------

  Taxa de juros mensal ....: ${pct(taxaMensal, 2)}% a.m.
  Taxa de juros anual .....: ${pct(contrato.taxaAnual, 2)}% a.a.
  Custo Efetivo Total .....: ${pct(contrato.cetAnualInformado, 2)}% a.a.

------------------------------------------------------------------------
QUADRO III — TARIFAS E DESPESAS FINANCIADAS
------------------------------------------------------------------------

  Tarifa de Abertura de Crédito (TAC) .........: R$ ${brl(tac)}
  Tarifa de avaliação do bem ..................: R$ ${brl(avaliacao)}
  Ressarcimento de registro do contrato .......: R$ ${brl(registro)}
  Seguro prestamista ..........................: R$ ${brl(seguro)}
  IOF .........................................: R$ ${brl(iof)}
                                                 ----------------
  Total de despesas incorporadas ao principal .: R$ ${brl(tac + avaliacao + registro + seguro + iof)}

------------------------------------------------------------------------
QUADRO IV — INADIMPLEMENTO
------------------------------------------------------------------------

  Multa moratória .........: ${pct(contrato.multaMoratoria, 0)}% sobre o valor da prestação
  Juros de mora ...........: ${pct(contrato.jurosMoratorios, 0)}% ao mês
  Comissão de permanência .: incidente durante o período de inadimplência,
                             cumulativamente aos encargos acima.

------------------------------------------------------------------------
DECLARAÇÃO
------------------------------------------------------------------------

  O EMITENTE declara ter recebido via deste instrumento e ter tomado
  conhecimento prévio de todas as suas condições.

  ____________________________________
  JOÃO DA SILVA SANTOS

========================================================================
DOCUMENTO FICTÍCIO, GERADO PARA TESTE DE SOFTWARE PERICIAL.
NÃO REPRESENTA OPERAÇÃO REAL NEM INSTITUIÇÃO FINANCEIRA EXISTENTE.
========================================================================
`;

mkdirSync(SAIDA, { recursive: true });
const arquivo = join(SAIDA, "contrato-veiculo-exemplo.txt");
writeFileSync(arquivo, doc, "utf-8");

// ————————————————————————————————————————————————————— o gabarito

// ⚠️ O id do achado de tarifa carrega o ÍNDICE da tarifa no array
//    (`tarifa-<tipo>-<i>`), não um contador por tipo. Escrevi o gabarito com
//    "-0" em todas e ele acusou três ausências — que eram erro do gabarito,
//    não do motor. É exatamente para isso que ele existe.
const ESPERADO = [
  ["capitalizacao", "achado", "a taxa anual declarada é o duodécuplo (25,44%), não a capitalização (28,63%)"],
  ["taxa-efetiva", "achado", "R$ 4.500 de tarifas e IOF embutidos: o liberado é menor que o financiado"],
  ["cet", "achado", "o CET declarado ignora as despesas incorporadas ao principal"],
  ["taxa-vs-media", null, "1,26× a média — faixa cinzenta, o motor não classifica de ofício"],
  ["tarifa-tac-0", "achado", "TAC em contrato de 2022, posterior a 30/04/2008 (Tema 618)"],
  ["tarifa-avaliacao-1", "inconclusivo", "válida em regra; depende de prova de que a avaliação ocorreu"],
  ["tarifa-registro-2", "inconclusivo", "válido em regra; depende de prova da prestação do serviço"],
  ["tarifa-seguro-3", "inconclusivo", "depende de prova de imposição da seguradora (Tema 972)"],
  ["multa", "achado", "3% supera o teto de 2% do art. 52, § 1º do CDC"],
  ["comissao-permanencia", "achado", "cumulada com multa e juros de mora (Súmula 472)"],
  ["amortizacao-negativa", "regular", "a prestação cobre os juros: o saldo decresce"],
];

const r = periciar(contrato);

console.log("");
console.log(`  Contrato de exemplo gravado em:`);
console.log(`  ${arquivo}`);
console.log("");
console.log("  ── GABARITO — o que a perícia TEM que encontrar ──");
console.log("");

if (!r.pode) {
  console.log("  ✗ o motor recusou o contrato de exemplo:");
  for (const p of r.problemas) console.log(`    · ${p}`);
  process.exit(1);
}

let ok = 0;
const erros = [];
for (const [id, esperado, porque] of ESPERADO) {
  const achou = r.achados.find((a) => a.id === id);
  const real = achou?.status ?? "AUSENTE";
  const bate = esperado === null ? achou !== undefined : real === esperado;
  if (bate) ok++;
  else erros.push(`${id}: esperado ${esperado}, obtido ${real}`);
  const marca = bate ? { achado: "▲", regular: "·", inconclusivo: "?" }[real] ?? "·" : "✗";
  console.log(`  ${marca} ${id.padEnd(22)} ${real.padEnd(14)} ${porque}`);
}

console.log("");
console.log("  ── números que o laudo deve apresentar ──");
console.log("");
const linhas = [
  ["valor financiado", formatarBRL(contrato.valorFinanciado)],
  ["valor liberado", formatarBRL(contrato.valorLiberado)],
  ["prestação", formatarBRL(contrato.parcela)],
  ["taxa mensal contratada", formatarTaxa(contrato.taxaMensal)],
  ["taxa anual declarada", formatarTaxa(contrato.taxaAnual, 2)],
  ["taxa anual capitalizada", formatarTaxa(anualEfetiva(contrato.taxaMensal), 2)],
];
const te = r.achados.find((a) => a.id === "taxa-efetiva")?.numeros;
const ce = r.achados.find((a) => a.id === "cet")?.numeros;
if (te) linhas.push(["taxa efetiva do fluxo", formatarTaxa(te.taxaEfetivaReal)]);
if (ce) linhas.push(["CET anual apurado", formatarTaxa(ce.cetAnualCalculado, 2)]);
for (const a of r.apuracao) {
  linhas.push([`economia — ${a.rotulo.slice(0, 28)}`, formatarBRL(a.diferencaTotal)]);
}
for (const [k, v] of linhas) console.log(`  ${k.padEnd(38)} ${v.padStart(16)}`);

console.log("");
if (erros.length) {
  console.log(`  ✗ ${erros.length} divergência(s) contra o gabarito:`);
  for (const e of erros) console.log(`    · ${e}`);
} else {
  console.log(`  ✓ ${ok}/${ESPERADO.length} — a perícia encontrou tudo que o documento esconde`);
}
console.log("");
process.exit(erros.length === 0 ? 0 : 1);
