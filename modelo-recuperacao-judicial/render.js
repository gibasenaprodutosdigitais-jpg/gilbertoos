const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const dir = __dirname;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(dir, 'modelo-peticao-recuperacao-judicial.html'));
  await page.pdf({
    path: path.join(dir, 'modelo-peticao-recuperacao-judicial.pdf'),
    format: 'A4',
    printBackground: true,
    margin: { top: '18mm', bottom: '18mm', left: '18mm', right: '18mm' },
  });
  await browser.close();
  console.log('PDF ok');
})();
