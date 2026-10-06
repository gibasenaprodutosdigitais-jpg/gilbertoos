const path = require('path');
const { chromium } = require('playwright');
(async () => {
  const dir = __dirname;
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.join(dir, 'ficha-diagnostico.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({
    path: path.join(dir, 'Sena, Bittar e Simoes - Ficha de Diagnostico.pdf'),
    format: 'A4', printBackground: true,
    margin: { top: '11mm', bottom: '11mm', left: '13mm', right: '13mm' },
  });
  await b.close();
  console.log('PDF ok');
})();
