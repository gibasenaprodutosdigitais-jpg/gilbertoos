const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const dir = __dirname;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(dir, 'projecao-semestral.html'));
  await page.pdf({
    path: path.join(dir, 'projecao-semestral-empreenda.pdf'),
    format: 'A4',
    printBackground: true,
    margin: { top: '10mm', bottom: '14mm', left: '10mm', right: '10mm' },
  });
  await browser.close();
  console.log('PDF ok');
})();
