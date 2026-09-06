const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const FPS = 30;
const TOTAL_MS = 31000;
const OUT = process.env.OUT || path.join(__dirname, 'frames');
const STRIDE = parseInt(process.env.STRIDE || '1', 10); // render every Nth frame (preview)

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(__dirname, 'reels.html'));

  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
  await page.waitForTimeout(400);

  const total = Math.round(TOTAL_MS / 1000 * FPS); // 930
  let written = 0;
  for (let i = 0; i < total; i++) {
    if (STRIDE > 1 && i % STRIDE !== 0) continue;
    const ms = i * (1000 / FPS);
    await page.evaluate((t) => {
      document.getAnimations().forEach(a => { try { a.pause(); a.currentTime = t; } catch (e) {} });
    }, ms);
    const n = String(i + 1).padStart(4, '0');
    await page.screenshot({ path: path.join(OUT, `f-${n}.png`) });
    written++;
    if (written % 60 === 0) console.log(`  ${written} frames...`);
  }
  await browser.close();
  console.log(`OK ${written} frames -> ${OUT}`);
})();
