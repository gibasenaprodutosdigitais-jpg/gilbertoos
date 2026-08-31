// ============================================================================
// GABARITO EXTERNO — `node motor/conferir-bacen.mjs`
// ============================================================================
// Confere o motor contra a CALCULADORA DO CIDADÃO do Banco Central.
//
// ★ POR QUE ISSO EXISTE: as baterias de `testes.mjs` provam que o código faz
//   o que o teste mandou — e o teste foi escrito por quem escreveu o código,
//   a partir da mesma suposição. Contra erro de FATO isso é cego por
//   construção (foi assim que a data do Tema 618 passou verde invertida).
//   A calculadora do BACEN é oficial, pública e INDEPENDENTE do nosso código:
//   é a única coisa aqui que pode discordar de nós.
//
// ★ E vale no laudo: "o cálculo confere com a Calculadora do Cidadão do Banco
//   Central" é uma frase que o assistente técnico do banco não derruba.
//
// ☠️ EXIGE COOKIE DE SESSÃO (JSESSIONID). Sem ele o BACEN responde HTTP 200
//    com o FORMULÁRIO VAZIO — "deu certo" sem resposta nenhuma. Uma leitura
//    ingênua veria 200 e concluiria que a conferência passou.
// ⚠️ Serve latin-1, como o STJ e o Planalto.
// ⚠️ A taxa vai em formato brasileiro ("1,99"), e o valor com ponto de milhar.
// ============================================================================

import { parcelaPrice, emCentavos, formatarBRL, toleranciaDeArredondamento } from "./calculo.mjs";

const UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
  "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36";
const BASE = "https://www3.bcb.gov.br/CALCIDADAO/publico";
const FORM = `${BASE}/exibirFormFinanciamentoPrestacoesFixas.do?method=exibirFormFinanciamentoPrestacoesFixas`;
const CALC = `${BASE}/calcularFinanciamentoPrestacoesFixas.do`;

// Casos escolhidos pra cobrir a faixa que aparece em contrato de verdade:
// veículo curto, empréstimo pessoal, imóvel longo, e taxas de 0,49% a 4,50%.
const CASOS = [
  { rotulo: "veículo 60k / 1,99% / 48m", valor: 60000, taxa: "1,99", meses: 48 },
  { rotulo: "imóvel 100k / 1,00% / 360m", valor: 100000, taxa: "1,00", meses: 360 },
  { rotulo: "imóvel 250k / 0,75% / 420m", valor: 250000, taxa: "0,75", meses: 420 },
  { rotulo: "pessoal 1k / 2,00% / 12m", valor: 1000, taxa: "2,00", meses: 12 },
  { rotulo: "pessoal 15k / 4,50% / 24m", valor: 15000, taxa: "4,50", meses: 24 },
  { rotulo: "consignado 30k / 1,75% / 60m", valor: 30000, taxa: "1,75", meses: 60 },
  { rotulo: "capital de giro 500k / 2,35% / 36m", valor: 500000, taxa: "2,35", meses: 36 },
  { rotulo: "taxa baixa 80k / 0,49% / 180m", valor: 80000, taxa: "0,49", meses: 180 },
  { rotulo: "prazo curto 20k / 3,00% / 6m", valor: 20000, taxa: "3,00", meses: 6 },

  // ★ Casos DUROS, achados numa varredura de 15: são os que mais divergem do
  //   nosso arredondamento. Ficam aqui de propósito — bateria que só carrega
  //   caso fácil passa sempre e não avisa nada. O pior medido foi 7 centavos.
  { rotulo: "duro · 500k / 2,35% / 10m", valor: 500000, taxa: "2,35", meses: 10 },
  { rotulo: "duro · 500k / 2,35% / 24m", valor: 500000, taxa: "2,35", meses: 24 },
  { rotulo: "duro · 500k / 2,05% / 72m", valor: 500000, taxa: "2,05", meses: 72 },
  { rotulo: "duro · 37,8k / 1,15% / 24m", valor: 37800, taxa: "1,15", meses: 24 },
  { rotulo: "duro · 37,8k / 2,79% / 10m", valor: 37800, taxa: "2,79", meses: 10 },
  { rotulo: "duro · 64,2k / 3,21% / 24m", valor: 64200, taxa: "3,21", meses: 24 },
];

const brl = (n) =>
  n.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

/** Abre a sessão e devolve o cookie. Sem isso o cálculo volta vazio. */
async function abrirSessao() {
  const r = await fetch(FORM, { headers: { "User-Agent": UA }, signal: AbortSignal.timeout(30000) });
  const bruto = r.headers.getSetCookie?.() ?? [];
  const cookie = bruto.map((c) => c.split(";")[0]).join("; ");
  if (!cookie) throw new Error("o BACEN não devolveu cookie de sessão");
  return cookie;
}

async function perguntarAoBacen(cookie, { valor, taxa, meses }) {
  const corpo = new URLSearchParams({
    method: "calcularFinanciamentoPrestacoesFixas",
    opcao: "",
    meses: String(meses),
    taxaJurosMensal: taxa,
    valorPrestacao: "",
    valorFinanciado: brl(valor),
  });
  const r = await fetch(CALC, {
    method: "POST",
    headers: {
      "User-Agent": UA,
      Cookie: cookie,
      Referer: FORM,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: corpo,
    signal: AbortSignal.timeout(45000),
  });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  const html = new TextDecoder("latin1").decode(Buffer.from(await r.arrayBuffer()));

  const m = html.match(/name="valorPrestacao"[^>]*value="([\d.,]+)"/);
  if (!m || !m[1]) {
    // ☠️ é aqui que a sessão perdida se denuncia: 200, formulário, valor vazio
    throw new Error("o BACEN respondeu sem o valor da prestação (sessão perdida?)");
  }
  return emCentavos(m[1]);
}

// ————————————————————————————————————————————————————— execução

console.log("");
console.log("  Conferindo o motor contra a Calculadora do Cidadão (BACEN)...");
console.log("");

let cookie;
try {
  cookie = await abrirSessao();
} catch (e) {
  console.log(`  ⚠ não consegui abrir sessão no BACEN — ${e.message}`);
  console.log("    (fonte fora do ar não reprova o motor; tentar de novo depois)");
  console.log("");
  process.exit(0);
}

let iguais = 0;
const arredondamentos = [];
const divergentes = [];
const falhas = [];

console.log(
  "  " + "Caso".padEnd(34) + "Nosso motor".padStart(15) + "BACEN".padStart(15) + "  ",
);
console.log("  " + "─".repeat(70));

for (const caso of CASOS) {
  const nosso = parcelaPrice(emCentavos(caso.valor), Number(caso.taxa.replace(",", ".")) / 100, caso.meses);
  let deles;
  try {
    deles = await perguntarAoBacen(cookie, caso);
  } catch (e) {
    falhas.push({ caso, erro: e.message });
    console.log(`  ${caso.rotulo.padEnd(34)}${formatarBRL(nosso).padStart(15)}${"—".padStart(15)}  ⚠ ${e.message}`);
    continue;
  }

  // ⚠️ Igualdade exata NÃO é a régua certa aqui, e isso foi medido: em 15
  //    casos, 10 divergiram do BACEN — a maior por 7 centavos, numa prestação
  //    de R$ 56.687. Nenhuma hipótese de arredondamento (round/ceil/trunc em
  //    6 a 9 casas do coeficiente) reproduziu as 18 respostas dele.
  //    E não adianta perseguir: cada banco arredonda do seu jeito, e a
  //    prestação do laudo é a IMPRESSA NO CONTRATO, não a que a gente calcula.
  //    O que esta ferramenta tem que provar é que a FÓRMULA é a mesma — e
  //    fórmula errada não erra centavos, erra reais.
  const delta = Math.abs(nosso - deles);
  const folga = toleranciaDeArredondamento(deles);
  const marca = delta === 0 ? "✓" : delta <= folga ? "≈" : "✗";

  if (delta === 0) iguais++;
  else if (delta <= folga) arredondamentos.push({ caso, nosso, deles, delta });
  else divergentes.push({ caso, nosso, deles, delta });

  console.log(
    `  ${caso.rotulo.padEnd(34)}${formatarBRL(nosso).padStart(15)}${formatarBRL(deles).padStart(15)}` +
      `  ${marca}${delta ? ` ${delta} centavo(s)` : ""}`,
  );
}

console.log("");
if (divergentes.length) {
  console.log("  ✗ DIVERGÊNCIA DE FÓRMULA contra fonte oficial — não usar em laudo.");
  console.log("    Fórmula errada não erra centavos, erra reais. Conferir a conta.");
  for (const d of divergentes) {
    console.log(`    ${d.caso.rotulo}: ${d.delta} centavos`);
  }
} else {
  console.log(`  ✓ fórmula confere com a calculadora oficial do BACEN em ${CASOS.length - falhas.length} caso(s)`);
  console.log(`    ${iguais} ao centavo exato · ${arredondamentos.length} dentro da folga de arredondamento`);
}
if (arredondamentos.length) {
  const maior = Math.max(...arredondamentos.map((a) => a.delta));
  console.log("");
  console.log(`  ≈ maior diferença de arredondamento: ${maior} centavo(s).`);
  console.log("    ⚠️ Isso NÃO é defeito: o BACEN arredonda o coeficiente de um jeito");
  console.log("       que não reproduzimos, e cada banco usa o seu. Num laudo, a");
  console.log("       prestação é a IMPRESSA NO CONTRATO — esta ferramenta só prova");
  console.log("       que a fórmula é a mesma.");
}
if (falhas.length) {
  console.log(`  ⚠ ${falhas.length} caso(s) não puderam ser conferidos (rede/fonte)`);
}
console.log("");

process.exit(divergentes.length === 0 ? 0 : 1);
