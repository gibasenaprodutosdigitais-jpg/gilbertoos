const { chromium } = require('/Users/gilbertosena/Desktop/GilbertoOS/scripts/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1080, height: 1350 },
    deviceScaleFactor: 2,
  });
  const file = 'file://' + path.join(__dirname, 'carrossel.html');
  await page.goto(file, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1200);

  const slides = await page.$$('.slide');
  for (let i = 0; i < slides.length; i++) {
    const nome = `instagram/slide-${String(i + 1).padStart(2, '0')}.png`;
    await slides[i].screenshot({ path: path.join(__dirname, nome) });
    console.log('ok', nome);
  }
  await browser.close();
})();
