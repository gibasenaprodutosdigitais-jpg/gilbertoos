const { chromium } = require('/Users/gilbertosena/Desktop/GilbertoOS/scripts/node_modules/playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(__dirname, 'guia-reuniao.html'),
                  { waitUntil: 'networkidle' });
  await page.pdf({
    path: path.join(__dirname, 'OCEO - Seguranca de Dados (guia de reuniao).pdf'),
    format: 'A4', printBackground: true,
    margin: { top: '0mm', bottom: '0mm', left: '0mm', right: '0mm' },
  });
  await page.setViewportSize({ width: 794, height: 1123 });
  await page.screenshot({ path: '/tmp/guia.png', fullPage: true });
  await browser.close();
  console.log('PDF gerado.');
})();
