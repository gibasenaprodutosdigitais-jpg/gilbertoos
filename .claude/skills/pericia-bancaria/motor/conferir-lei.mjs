// ============================================================================
// CONFERIDOR DE FONTE PRIMÁRIA
//   node motor/conferir-lei.mjs            → confere as referências
//   node motor/conferir-lei.mjs --baixar   → imprime o texto oficial de cada uma
// ============================================================================
// ☠️ TEXTO DE LEI ESCRITO DE CABEÇA É FONTE DE FATO — E FATO É ONDE IA ERRA.
//    O modelo acerta o julgamento e erra o número, a data e o dispositivo.
//    Esta obra já provou isso antes mesmo do conferidor existir: o marco do
//    Tema 618 foi implementado como "vedada A PARTIR de 30/04/2008" quando o
//    acórdão diz "válida ATÉ 30/04/2008" — um dia de diferença que INVERTE a
//    conclusão sobre o contrato do cliente. E havia teste fossilizando o erro.
//
// ⚠️ As fontes servem LATIN-1 (ISO-8859-1). Decodificar como UTF-8 estraga
//    todo acento e nenhuma âncora casa.
// ⚠️ O HTML quebra linha DENTRO da frase: normalizar espaço antes de comparar.
// ⚠️ O STJ marca o termo buscado com <span class=highlightBrs> NO MEIO do
//    texto: tem que tirar tag antes de comparar, não depois.
// ⚠️ `scon.stj.jus.br` devolve 403. O host que responde é `processo.stj.jus.br`.
// ============================================================================

import { VERBETES } from "../referencias/jurisprudencia.mjs";

const UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
  "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36";

const MOSTRAR = process.argv.includes("--baixar");

// ————————————————————————————————————————————————————— rede

async function baixar(url, tentativas = 3) {
  let ultimoErro;
  for (let i = 0; i < tentativas; i++) {
    try {
      const r = await fetch(url, {
        headers: { "User-Agent": UA, "Accept-Language": "pt-BR,pt;q=0.9" },
        signal: AbortSignal.timeout(45000),
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const buf = Buffer.from(await r.arrayBuffer());
      // O charset vem no cabeçalho; na dúvida, latin-1 (é o que essas fontes servem)
      const ct = r.headers.get("content-type") ?? "";
      const enc = /utf-?8/i.test(ct) ? "utf-8" : "latin1";
      return new TextDecoder(enc).decode(buf);
    } catch (e) {
      ultimoErro = e;
      // sites de tribunal derrubam conexão sozinhos; sem repetir, a fonte
      // "some" em dias aleatórios e parece que o verbete está errado
      await new Promise((r) => setTimeout(r, 1500 * (i + 1)));
    }
  }
  throw ultimoErro;
}

// ————————————————————————————————————————————————————— texto

const ENTIDADES = {
  "&nbsp;": " ", "&aacute;": "á", "&eacute;": "é", "&iacute;": "í",
  "&oacute;": "ó", "&uacute;": "ú", "&acirc;": "â", "&ecirc;": "ê",
  "&ocirc;": "ô", "&atilde;": "ã", "&otilde;": "õ", "&ccedil;": "ç",
  "&agrave;": "à", "&Aacute;": "Á", "&Eacute;": "É", "&Iacute;": "Í",
  "&Oacute;": "Ó", "&Uacute;": "Ú", "&Ccedil;": "Ç", "&Atilde;": "Ã",
  "&amp;": "&", "&quot;": '"', "&lt;": "<", "&gt;": ">", "&#39;": "'",
};

function limpar(html) {
  let t = html;
  t = t.replace(/<script[\s\S]*?<\/script>/gi, " ");
  t = t.replace(/<style[\s\S]*?<\/style>/gi, " ");
  t = t.replace(/<[^>]*>/g, " "); // tira tag ANTES de comparar (highlightBrs)
  for (const [e, c] of Object.entries(ENTIDADES)) t = t.split(e).join(c);
  t = t.replace(/&#(\d+);/g, (_, n) => String.fromCharCode(Number(n)));
  return t.replace(/\s+/g, " ").trim(); // quebra dentro da frase vira espaço
}

/** Comparação tolerante a acento, caixa e pontuação — nunca a NÚMERO. */
function normalizar(s) {
  return normalizarComMapa(s).texto;
}

/**
 * Normaliza guardando, para cada caractere do resultado, de onde ele veio.
 *
 * ☠️ Sem o mapa não dá pra recortar o texto ORIGINAL a partir de uma busca
 *    feita no texto normalizado: a normalização muda o comprimento (NFD
 *    separa o acento, o filtro colapsa espaço), então o índice encontrado
 *    aponta pra outro lugar na string original. Foi exatamente o que
 *    aconteceu no CDC: a busca por "dois por cento do valor da prestação"
 *    ACHOU o trecho e o recorte devolveu um pedaço do § 2º, algumas centenas
 *    de caracteres adiante — texto real, da lei certa, do dispositivo errado.
 *    Num laudo isso vira citação errada com cara de citação conferida.
 */
function normalizarComMapa(s) {
  let texto = "";
  const mapa = [];
  let espacoPendente = false;

  for (let i = 0; i < s.length; i++) {
    const bruto = s[i].normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
    const c = bruto === "" ? "" : /[\w\s/%.-]/.test(bruto[0]) ? bruto[0] : " ";
    if (c === "") continue;
    if (/\s/.test(c)) {
      espacoPendente = texto.length > 0;
      continue;
    }
    if (espacoPendente) {
      texto += " ";
      mapa.push(i);
      espacoPendente = false;
    }
    texto += c;
    mapa.push(i);
  }
  return { texto, mapa };
}

// ————————————————————————————————————————————————————— extratores por fonte

const EXTRATORES = {
  /** Súmula do STJ: o enunciado mora no <div class="blocoVerbete">. */
  "stj-sumula": (html) => {
    const blocos = [...html.matchAll(/<div class="blocoVerbete">([\s\S]*?)<\/div>/g)];
    if (!blocos.length) return null;
    let t = limpar(blocos[0][1]);
    // o "ramo do direito" vem grudado na frente do enunciado
    t = t.replace(/^[A-ZÀ-Ú\s\-]{6,}?\s(?=[A-ZÀ-Ú][a-zà-ú])/, "");
    return t;
  },

  /** Tema repetitivo do STJ: a página traz "Tese Firmada". */
  "stj-tema": (html) => {
    const t = limpar(html);
    const m = t.match(/Tese\s+Firmada:?\s*(.+?)(?:Anotações|Informações|Legislação|Precedentes|Situação|Tema\s+\d{2,}\/STF)/i);
    return m ? m[1].trim() : t;
  },

  /**
   * Planalto: recorta a vizinhança da âncora dentro da lei inteira.
   * O recorte usa o MAPA de índices — buscar no normalizado e cortar no
   * original com o mesmo número devolve o dispositivo errado.
   */
  planalto: (html, verbete) => {
    const t = limpar(html);
    const { texto, mapa } = normalizarComMapa(t);
    const i = texto.indexOf(normalizar(verbete.ancoras[0]));
    if (i < 0) return null; // não achou: é o conferidor que tem que reclamar
    // ⚠️ A janela acompanha o tamanho do verbete. Fixa em 400 caracteres, ela
    //    cortava o art. 473 do CPC no meio e o § 2º ficava de fora — o
    //    conferidor então acusava "divergência" num verbete correto, que é o
    //    falso positivo que ele mesmo avisa ser o caso mais comum.
    const folga = Math.max(500, (verbete.texto?.length ?? 0) + 300);
    const inicio = mapa[Math.max(0, i - 300)] ?? 0;
    const fim = mapa[Math.min(mapa.length - 1, i + folga)] ?? t.length;
    return t.slice(inicio, fim);
  },
};

// ————————————————————————————————————————————————————— execução

const alvos = VERBETES.filter((v) => v.fonte && EXTRATORES[v.conferidor]);
const manuais = VERBETES.filter((v) => !EXTRATORES[v.conferidor]);

console.log("");
console.log(`  Conferindo ${alvos.length} verbetes contra a fonte primária...`);
console.log("");

let conferidos = 0;
const divergencias = [];
const inacessiveis = [];

for (const v of alvos) {
  let html;
  try {
    html = await baixar(v.fonte);
  } catch (e) {
    inacessiveis.push({ v, erro: String(e.message ?? e) });
    console.log(`  ⚠ ${v.chave.padEnd(14)} fonte não respondeu — ${e.message ?? e}`);
    continue;
  }

  const oficial = EXTRATORES[v.conferidor](html, v);
  if (!oficial) {
    inacessiveis.push({ v, erro: "não achei o trecho na página" });
    console.log(`  ⚠ ${v.chave.padEnd(14)} página respondeu, mas não achei o trecho`);
    continue;
  }

  if (MOSTRAR) {
    console.log(`  ── ${v.chave} ─────────────────────────────────────────`);
    console.log(`  ${oficial.slice(0, 1400)}`);
    console.log("");
    continue;
  }

  const alvo = normalizar(oficial);
  const faltando = v.ancoras.filter((a) => !alvo.includes(normalizar(a)));

  if (faltando.length === 0) {
    conferidos++;
    console.log(`  ✓ ${v.chave.padEnd(14)} confere com a fonte`);
  } else {
    divergencias.push({ v, faltando, oficial });
    console.log(`  ✗ ${v.chave.padEnd(14)} DIVERGE — ${faltando.length} âncora(s) não encontrada(s)`);
    for (const f of faltando) console.log(`      não achei: "${f}"`);
  }
}

if (MOSTRAR) process.exit(0);

// ————————————————————————————————————————————————————— relatório

console.log("");
if (manuais.length) {
  console.log(`  ── ${manuais.length} verbete(s) SEM conferência por máquina ──`);
  for (const v of manuais) {
    console.log(`  · ${v.chave.padEnd(14)} ${v.conferenciaManual ?? "PENDENTE — conferir à mão"}`);
    if (v.fonte) console.log(`      ${v.fonte}`);
  }
  console.log("");
}

if (divergencias.length) {
  console.log("  ⚠️ ANTES DE MEXER NO VERBETE: nas rodadas anteriores desta casa,");
  console.log("     quase toda 'divergência' era o PADRÃO errado, não a referência.");
  console.log("     Ler o texto oficial (--baixar) antes de alterar qualquer coisa.");
  console.log("");
  for (const d of divergencias) {
    console.log(`  ── ${d.v.chave} — texto oficial ──`);
    console.log(`  ${d.oficial.slice(0, 900)}`);
    console.log("");
  }
}

const total = alvos.length;
console.log(
  `  ${conferidos}/${total} conferidos por máquina · ` +
    `${divergencias.length} divergentes · ${inacessiveis.length} inacessíveis · ` +
    `${manuais.length} manuais`,
);
console.log("");

// Fonte fora do ar é hiccup de rede, não defeito da referência: não reprova.
process.exit(divergencias.length === 0 ? 0 : 1);
