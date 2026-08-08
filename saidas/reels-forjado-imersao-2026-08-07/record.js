const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const TOTAL_MS = 3000 + 2600 + 2800 + 2400 + 2800 + 3000 + 3600 + 800; // slides + folga final

(async () => {
  const dir = __dirname;
  const outDir = path.join(dir, 'video');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir);

  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1080, height: 1920 },
    recordVideo: { dir: outDir, size: { width: 1080, height: 1920 } },
  });
  const page = await context.newPage();
  await page.goto('file://' + path.join(dir, 'reels-animado.html'));
  await page.waitForTimeout(TOTAL_MS);

  const video = page.video();
  await page.close();
  await context.close();
  await browser.close();

  const savedPath = await video.path();
  const finalPath = path.join(outDir, 'forjado-reels.webm');
  fs.renameSync(savedPath, finalPath);
  console.log('Vídeo salvo em:', finalPath);
})();
