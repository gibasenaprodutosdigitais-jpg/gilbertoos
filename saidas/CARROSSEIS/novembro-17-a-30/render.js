const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
(async () => {
  const browser = await chromium.launch();
  for (const pasta of process.argv.slice(2)) {
    const dir = path.join(__dirname, pasta), out = path.join(dir, 'instagram');
    fs.mkdirSync(out, { recursive: true });
    const page = await browser.newPage({ viewport: { width: 1080, height: 1350 } });
    await page.goto('file://' + path.join(dir, 'carrossel.html'));
    await page.waitForSelector('body[data-pronto="1"]', { timeout: 20000 });
    const slides = await page.$$('.slide');
    for (let i = 0; i < slides.length; i++)
      await slides[i].screenshot({ path: path.join(out, `slide-${String(i + 1).padStart(2, '0')}.png`) });
    console.log(pasta, slides.length);
    await page.close();
  }
  await browser.close();
})();
