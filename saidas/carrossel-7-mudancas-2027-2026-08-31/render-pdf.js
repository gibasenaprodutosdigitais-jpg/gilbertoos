const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(__dirname, 'carrossel.html'));
  await page.addStyleTag({ content: '@media print { .slide { page-break-after: always; } } body { background: white !important; }' });
  await page.waitForTimeout(300);

  await page.pdf({
    path: path.join(__dirname, 'carrossel-7-mudancas-2027.pdf'),
    width: '1080px',
    height: '1350px',
    printBackground: true,
    margin: { top: 0, bottom: 0, left: 0, right: 0 },
  });

  await browser.close();
  console.log('PDF do carrossel salvo.');
})();
