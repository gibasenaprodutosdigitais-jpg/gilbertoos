/*
 * Refaz os três PDFs desta pasta a partir dos HTML.
 *
 * Ordem certa quando o inventário mudar:
 *   1) editar a lista em gerar_inventario.py
 *   2) python3 gerar_inventario.py      (reescreve os HTML e a contagem do resumo)
 *   3) node render.js                   (refaz os PDFs)
 *
 * O resumo tem que caber em UMA página. Este script avisa se passar disso.
 */
const { chromium } = require('/Users/gilbertosena/Desktop/GilbertoOS/scripts/node_modules/playwright');
const path = require('path');
const fs = require('fs');

const PECAS = [
  ['inventario.html',         'Inventario para Parceria.pdf'],
  ['inventario-resumo.html',  'Inventario para Parceria - Itens e Quantidades.pdf'],
  ['resumo.html',             'Resumo da Parceria - 1 pagina.pdf'],
];

const paginas = (arquivo) =>
  (fs.readFileSync(arquivo).toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;

(async () => {
  const browser = await chromium.launch();
  for (const [html, pdf] of PECAS) {
    const page = await browser.newPage();
    await page.goto('file://' + path.join(__dirname, html), { waitUntil: 'networkidle' });
    const destino = path.join(__dirname, pdf);
    await page.pdf({ path: destino, format: 'A4', printBackground: true });
    await page.close();
    const n = paginas(destino);
    const alerta = (html === 'resumo.html' && n > 1) ? '  <-- ESTOUROU: o resumo tem que ser 1 página' : '';
    console.log(`${pdf}  (${n} pág.)${alerta}`);
  }
  await browser.close();
})();
