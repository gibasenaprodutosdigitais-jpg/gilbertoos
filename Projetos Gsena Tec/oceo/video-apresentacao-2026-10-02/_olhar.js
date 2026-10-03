// tira uma foto em cada instante pedido, pra olhar antes de renderizar tudo
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const TEMPOS = (process.env.T || "2,7,12,18,23,28,33,37,41,46,51,57,63,68").split(",").map(Number);
const OUT = process.env.OUT || '/tmp/oceo-olhar';
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(__dirname, 'video.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
  await p.waitForTimeout(400);
  for (const t of TEMPOS) {
    await p.evaluate((ms) => document.getAnimations().forEach(a => { try { a.pause(); a.currentTime = ms; } catch(e){} }), t * 1000);
    await p.screenshot({ path: path.join(OUT, `t-${String(t).padStart(2,'0')}.png`) });
  }
  await b.close();
  console.log('ok', TEMPOS.length, '->', OUT);
})();
