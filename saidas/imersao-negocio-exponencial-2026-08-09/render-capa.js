const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const file = path.join(__dirname, 'capa.html');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  await page.goto('file://' + file);
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(__dirname, 'capa.png') });
  await page.pdf({
    path: path.join(__dirname, 'capa.pdf'),
    width: '16.66in',
    height: '10.42in',
    printBackground: true,
    margin: { top: 0, bottom: 0, left: 0, right: 0 },
  });
  await browser.close();
  console.log('Gerado: capa.png');
})();
