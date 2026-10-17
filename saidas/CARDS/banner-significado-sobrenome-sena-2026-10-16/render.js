const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 } });
  await page.goto('file://' + path.join(__dirname, 'banner.html'));
  await page.waitForTimeout(800);
  await page.evaluate(() => document.fonts.ready);
  const el = await page.$('.banner');
  await el.screenshot({ path: path.join(__dirname, 'banner-sena.png') });
  await browser.close();
  console.log('ok');
})();
