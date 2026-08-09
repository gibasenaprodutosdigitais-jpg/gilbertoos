const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const dir = __dirname;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  await page.goto('file://' + path.join(dir, 'flyer.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  await page.locator('.flyer').screenshot({ path: path.join(dir, 'evento-lideranca-que-transforma.png') });
  await browser.close();
  console.log('ok');
})();
