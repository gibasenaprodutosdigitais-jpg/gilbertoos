// Abre o carrossel.html e fotografa cada .slide em 1080x1350.
//   NODE_PATH="../../scripts/node_modules" node render.js
const { chromium } = require('/Users/gilbertosena/Desktop/GilbertoOS/scripts/node_modules/playwright');
const path = require('path'); const fs = require('fs');

(async () => {
  const saida = path.join(__dirname, 'instagram');
  fs.mkdirSync(saida, { recursive: true });
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1080, height: 1350 },
                               deviceScaleFactor: 1 });
  await pg.goto('file://' + path.join(__dirname, 'carrossel.html'),
                { waitUntil: 'networkidle' });
  await pg.evaluate(() => document.fonts.ready);
  await pg.waitForTimeout(600);
  const n = await pg.locator('.slide').count();
  for (let i = 0; i < n; i++) {
    const nome = `slide-${String(i + 1).padStart(2, '0')}.png`;
    await pg.locator('.slide').nth(i).screenshot({ path: path.join(saida, nome) });
    console.log('  ' + nome);
  }
  await b.close();
  console.log(`${n} slides em instagram/`);
})();
