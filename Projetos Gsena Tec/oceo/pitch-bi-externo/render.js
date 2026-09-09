const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const htmlPath = path.join(__dirname, 'pitch-bi-externo.html');
  await page.goto('file://' + htmlPath, { waitUntil: 'networkidle' });
  await page.pdf({
    path: path.join(__dirname, 'OCEO - Prova de Conceito BI (pitch externo).pdf'),
    format: 'A4',
    printBackground: true,
    margin: { top: '0mm', bottom: '0mm', left: '0mm', right: '0mm' },
  });
  await browser.close();
  console.log('PDF gerado com sucesso.');
})();
