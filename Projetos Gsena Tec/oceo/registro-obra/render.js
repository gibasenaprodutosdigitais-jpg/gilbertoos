const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const HERE = __dirname;
  const src = 'file://' + path.join(HERE, 'oceo-obra-literaria.html');
  const out = path.join(HERE, 'OCEO - A Obra Completa (registro de obra literaria).pdf');

  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(src, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1200); // fontes
  await page.pdf({
    path: out,
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true,
    displayHeaderFooter: false,
  });
  await browser.close();
  console.log('OK ->', out);
})();
