// Renderiza os frames do video.html. Como cada cena e um cartao estatico
// (so anima fade-in/fade-out), so tira screenshot de verdade nas janelas de
// transicao; o resto do "hold" e copiado do primeiro frame estavel (muito
// mais rapido que renderizar cada um dos milhares de frames no browser).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const HERE = __dirname;
  const TL = JSON.parse(fs.readFileSync(path.join(HERE, 'timeline.json'), 'utf8'));
  const OUT = path.join(HERE, 'frames');
  fs.rmSync(OUT, { recursive: true, force: true });
  fs.mkdirSync(OUT, { recursive: true });

  const fps = TL.fps;
  const FADE_IN = 0.5, FADE_OUT = 0.4;

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: TL.w, height: TL.h }, deviceScaleFactor: 1 });
  page.on('console', m => { if (m.type() === 'error') console.log('  [err]', m.text()); });
  await page.goto('file://' + path.join(HERE, 'video.html'), { waitUntil: 'networkidle' });
  await page.waitForFunction(() => window.__ready === true, null, { timeout: 20000 });
  await page.waitForTimeout(500);

  const root = page.locator('#root');
  const name = f => path.join(OUT, 'f-' + String(f).padStart(5, '0') + '.png');
  let rendered = 0, copied = 0;

  for (const s of TL.scenes) {
    const f0 = Math.round(s.start * fps);
    const f1 = Math.round((s.start + s.dur) * fps); // exclusive
    const fadeInEnd = Math.min(f1, f0 + Math.round(FADE_IN * fps));
    const fadeOutStart = Math.max(f0, f1 - Math.round(FADE_OUT * fps));

    let lastStableFile = null;
    for (let f = f0; f < f1; f++) {
      const t = f / fps;
      if (f < fadeInEnd || f >= fadeOutStart) {
        await page.evaluate(x => window.__seek(x), t);
        await root.screenshot({ path: name(f) });
        rendered++;
        if (f < fadeInEnd) lastStableFile = null; // still transitioning
      } else {
        if (lastStableFile === null) {
          await page.evaluate(x => window.__seek(x), t);
          await root.screenshot({ path: name(f) });
          rendered++;
          lastStableFile = name(f);
        } else {
          fs.copyFileSync(lastStableFile, name(f));
          copied++;
        }
      }
    }
    console.log(`  cena ${s.id}  frames ${f0}-${f1 - 1}`);
  }
  await browser.close();
  console.log(`frames OK — renderizados ${rendered}, copiados ${copied}`);
})();
