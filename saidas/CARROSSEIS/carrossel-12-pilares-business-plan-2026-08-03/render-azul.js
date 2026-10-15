const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const dir = __dirname;
  const outDir = path.join(dir, 'instagram-azul');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir);

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 } });
  await page.goto('file://' + path.join(dir, 'carrossel-azul.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);

  const slides = await page.$$('.slide');
  for (let i = 0; i < slides.length; i++) {
    const n = String(i + 1).padStart(2, '0');
    await slides[i].screenshot({ path: path.join(outDir, `slide-${n}.png`) });
    console.log(`slide-${n}.png ok`);
  }

  await browser.close();
})();
