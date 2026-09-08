const { chromium } = require('playwright');
const path = require('path');
const src = process.argv[2] || 'miolo-src.html';
const out = process.argv[3] || 'test-miolo.pdf';
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.join(__dirname, src), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(600);
  await p.pdf({ path: path.join(__dirname, out), format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close();
  console.log(out, 'ok');
})();
