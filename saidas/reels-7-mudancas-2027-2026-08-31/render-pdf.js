const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(__dirname, 'roteiro-print.html'));
  await page.waitForTimeout(300);

  await page.pdf({
    path: path.join(__dirname, 'roteiro-7-mudancas-2027.pdf'),
    format: 'A4',
    printBackground: true,
    margin: { top: '0', bottom: '0', left: '0', right: '0' },
  });

  await browser.close();
  console.log('PDF do roteiro salvo.');
})();
