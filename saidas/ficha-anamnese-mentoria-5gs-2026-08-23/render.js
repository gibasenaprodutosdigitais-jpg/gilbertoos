const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const dir = __dirname;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(dir, 'ficha-anamnese-5gs.html'));
  await page.pdf({
    path: path.join(dir, 'ficha-anamnese-5gs.pdf'),
    format: 'A4',
    printBackground: true,
    margin: { top: '16mm', bottom: '16mm', left: '16mm', right: '16mm' },
  });
  await browser.close();
  console.log('PDF ok');
})();
