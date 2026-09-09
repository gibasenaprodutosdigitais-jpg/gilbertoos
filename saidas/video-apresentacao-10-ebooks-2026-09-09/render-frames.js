// Renderiza os frames do video.html (deterministico via window.__seek(t)).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const HERE = __dirname;
  const TL = JSON.parse(fs.readFileSync(path.join(HERE, 'timeline.json'), 'utf8'));
  const OUT = path.join(HERE, 'frames');
  fs.rmSync(OUT, { recursive: true, force: true });
  fs.mkdirSync(OUT, { recursive: true });

  const total = TL.total, fps = TL.fps;
  const nFrames = Math.round(total * fps);

  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: TL.w, height: TL.h }, deviceScaleFactor: 1,
  });
  page.on('console', m => { if (m.type() === 'error') console.log('  [err]', m.text()); });

  await page.goto('file://' + path.join(HERE, 'video.html'), { waitUntil: 'networkidle' });
  await page.waitForFunction(() => window.__ready === true, null, { timeout: 20000 });
  await page.waitForTimeout(600); // fontes/imagens

  const root = page.locator('#root');
  for (let f = 0; f < nFrames; f++) {
    const t = f / fps;
    await page.evaluate(x => window.__seek(x), t);
    await root.screenshot({ path: path.join(OUT, 'f-' + String(f).padStart(5, '0') + '.png') });
    if (f % 60 === 0) console.log(`  ${f}/${nFrames}  (t=${t.toFixed(1)}s)`);
  }
  await browser.close();
  console.log('frames OK:', nFrames);
})();
