/*
 * Gera um contrato ou proposta em papel timbrado (.docx editável): logo no topo de cada página,
 * marca d'água no centro, rodapé com contato e número da página.
 *
 *   node scripts/contrato-timbrado.js <entrada.md> <saida.docx> <logo-cabecalho.png> <marca-dagua.png> "<rodapé>"
 *
 * O .md aceita: # título, ## e ### seções, parágrafos com **negrito** e *itálico*, listas "1. ",
 * citações "> " e tabelas com "|". Criado em 12/nov/2026 para o contrato 01 (Business Advisor and Consultant).
 */
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Header, Footer, Table, TableRow, TableCell,
  WidthType, BorderStyle, AlignmentType, PageNumber, ShadingType,
  HorizontalPositionRelativeFrom, VerticalPositionRelativeFrom, HorizontalPositionAlign,
  VerticalPositionAlign, TextWrappingType, convertMillimetersToTwip,
} = require('/Users/gilbertosena/Desktop/GilbertoOS/scripts/node_modules/docx');

const [, , entrada, saida, logoPath, marcaPath, rodape] = process.argv;
const TINTA = '1E2328', CINZA = '6B7078', LINHA = 'B9BDC2', FUNDO = 'F1F2F3';
const FONTE = 'Georgia';
const UTIL = convertMillimetersToTwip(166); // A4 menos 22 mm de cada lado
const EMU_MM = 3.7795; // px por mm a 96 dpi

function tamanho(png) {
  const b = fs.readFileSync(png);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20), data: b };
}

// **negrito**, *itálico*, `código`
function runs(texto, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*\s][^*]*\*|`[^`]+`)/g;
  let i = 0, m;
  while ((m = re.exec(texto))) {
    if (m.index > i) out.push(new TextRun({ text: texto.slice(i, m.index), ...base }));
    const t = m[0];
    if (t.startsWith('**')) out.push(new TextRun({ text: t.slice(2, -2), bold: true, ...base }));
    else if (t.startsWith('`')) out.push(new TextRun({ text: t.slice(1, -1), ...base }));
    else out.push(new TextRun({ text: t.slice(1, -1), italics: true, ...base }));
    i = m.index + t.length;
  }
  if (i < texto.length) out.push(new TextRun({ text: texto.slice(i), ...base }));
  return out;
}

const borda = { style: BorderStyle.SINGLE, size: 4, color: LINHA };
function tabela(linhas) {
  linhas = linhas.filter((l) => !/^\|[\s\-|:]+\|$/.test(l));
  const ncol = linhas[0].trim().replace(/^\||\|$/g, '').split('|').length;
  const pesos = ncol === 2 ? [0.28, 0.72] : Array(ncol).fill(1 / ncol);
  const larg = pesos.map((x) => Math.floor(UTIL * x));
  const rows = linhas.map((l, i) => new TableRow({
    tableHeader: i === 0,
    children: l.trim().replace(/^\||\|$/g, '').split('|').map((c, j) => new TableCell({
      width: { size: larg[j], type: WidthType.DXA },
      shading: i === 0 ? { type: ShadingType.CLEAR, color: 'auto', fill: FUNDO } : undefined,
      margins: { top: 60, bottom: 60, left: 100, right: 100 },
      borders: { top: borda, bottom: borda, left: borda, right: borda },
      children: [new Paragraph({ children: runs(c.trim(), { size: 18, bold: i === 0 ? true : undefined, font: FONTE, color: TINTA }) })],
    })),
  }));
  return new Table({ rows, columnWidths: larg, width: { size: UTIL, type: WidthType.DXA } });
}

function corpo(md) {
  const out = [];
  let tab = [];
  const linhas = md.split('\n').concat(['']);
  for (const bruta of linhas) {
    const s = bruta.trim();
    if (s.startsWith('|')) { tab.push(s); continue; }
    if (tab.length) { out.push(tabela(tab)); out.push(new Paragraph({ text: '' })); tab = []; }
    if (!s || s === '---') continue;
    const p = (filhos, extra = {}) => out.push(new Paragraph({ children: filhos, spacing: { after: 120, line: 290 }, ...extra }));
    if (s.startsWith('# ')) p(runs(s.slice(2), { size: 30, bold: true, font: FONTE, color: TINTA }), { alignment: AlignmentType.CENTER, spacing: { after: 80 } });
    else if (s.startsWith('### ')) p(runs(s.slice(4), { size: 22, bold: true, font: FONTE, color: TINTA }), { spacing: { before: 160, after: 80 } });
    else if (s.startsWith('## ')) p(runs(s.slice(3).toUpperCase(), { size: 22, bold: true, font: FONTE, color: TINTA }), {
      pageBreakBefore: s.slice(3).startsWith('Anexo'), keepNext: true,
      spacing: { before: 280, after: 120 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINHA, space: 2 } },
    });
    else if (s.startsWith('> ')) p(runs(s.slice(2), { size: 20, italics: true, font: FONTE, color: CINZA }), { indent: { left: 400 } });
    else if (/^_{5,}/.test(s)) p([new TextRun({ text: s, font: FONTE, color: TINTA })], { spacing: { before: 360, after: 0 } });
    else p(runs(s, { size: 21, font: FONTE, color: TINTA }), { alignment: AlignmentType.JUSTIFIED });
  }
  return out;
}

const logo = tamanho(logoPath);
const marca = tamanho(marcaPath);
const logoW = 34 * EMU_MM, logoH = logoW * logo.h / logo.w;
const marcaW = 125 * EMU_MM, marcaH = marcaW * marca.h / marca.w;

const cabecalho = new Header({
  children: [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [
        new ImageRun({ type: 'png', data: logo.data, transformation: { width: logoW, height: logoH } }),
        new ImageRun({
          type: 'png', data: marca.data, transformation: { width: marcaW, height: marcaH },
          floating: {
            horizontalPosition: { relative: HorizontalPositionRelativeFrom.PAGE, align: HorizontalPositionAlign.CENTER },
            verticalPosition: { relative: VerticalPositionRelativeFrom.PAGE, align: VerticalPositionAlign.CENTER },
            behindDocument: true, wrap: { type: TextWrappingType.NONE },
          },
        }),
      ],
    }),
    new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINHA, space: 4 } }, children: [] }),
  ],
});

const rodapeEl = new Footer({
  children: [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      border: { top: { style: BorderStyle.SINGLE, size: 4, color: LINHA, space: 4 } },
      children: [new TextRun({ text: rodape, size: 15, font: FONTE, color: CINZA })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [
        new TextRun({ children: ['Página ', PageNumber.CURRENT, ' de ', PageNumber.TOTAL_PAGES], size: 15, font: FONTE, color: CINZA }),
      ],
    }),
  ],
});

const doc = new Document({
  creator: 'Gilberto Sena',
  title: 'Contrato de Prestação de Serviços Empresariais',
  sections: [{
    properties: {
      page: {
        size: { width: convertMillimetersToTwip(210), height: convertMillimetersToTwip(297) },
        margin: { top: convertMillimetersToTwip(42), bottom: convertMillimetersToTwip(25), left: convertMillimetersToTwip(22), right: convertMillimetersToTwip(22), header: convertMillimetersToTwip(10), footer: convertMillimetersToTwip(10) },
      },
    },
    headers: { default: cabecalho },
    footers: { default: rodapeEl },
    children: corpo(fs.readFileSync(entrada, 'utf8')),
  }],
});

Packer.toBuffer(doc).then((b) => { fs.writeFileSync(saida, b); console.log(saida); });
