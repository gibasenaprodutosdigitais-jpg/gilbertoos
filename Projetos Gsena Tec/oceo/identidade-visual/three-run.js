const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const HERE = __dirname;
const OUT = path.join(HERE, '_3d-render');
fs.mkdirSync(OUT, { recursive: true });

const MARKS = [
  ['12-oc', 'Monograma O-C'],
  ['08-bi', 'Painel BI'],
  ['14-chave', 'Pedra-chave'],
  ['13-norte', 'Estrela-norte'],
];
const ANGLES = [ -26, 22 ];

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl', '--enable-accelerated-2d-canvas'],
  });
  const page = await browser.newPage({ viewport: { width: 1400, height: 1400 }, deviceScaleFactor: 1 });
  page.on('console', m => { if (m.type() === 'error') console.log('  [console.error]', m.text()); });

  await page.goto('file://' + path.join(HERE, 'three-3d.html'), { waitUntil: 'load' });
  await page.waitForFunction(() => typeof window.__setup === 'function', null, { timeout: 20000 });

  for (const [slug, name] of MARKS) {
    for (const ang of ANGLES) {
      const svgTxt = fs.readFileSync(path.join(HERE, `logo-${slug}.svg`), 'utf8');
      await page.evaluate(([t, a]) => window.__setup(t, a), [svgTxt, ang]);
      await page.waitForFunction(() => window.__ready === true || window.__err, null, { timeout: 30000 });
      const err = await page.evaluate(() => window.__err);
      if (err) { console.log('ERR', slug, ang, err); continue; }
      const buf = await page.locator('#c').screenshot();
      const f = path.join(OUT, `${slug}_${ang < 0 ? 'a' : 'b'}.png`);
      fs.writeFileSync(f, buf);
      console.log('ok', path.basename(f));
    }
  }
  await browser.close();
})();
