const path = require('path');
const { chromium } = require('playwright');

// Regera as peças da Imersão AME de uma vez: os PDFs de imprimir e as
// artes de divulgação em PNG. O kit do participante tem o render dele,
// dentro da própria pasta.
const PDFS = [
  ['programacao/programacao.html', 'programacao/Imersao AME - Programacao.pdf',
   { format: 'A4', margin: { top: '12mm', bottom: '12mm', left: '14mm', right: '14mm' } }],
  ['cracha/cracha.html', 'cracha/Imersao AME - Crachas.pdf', { format: 'A4', preferCSSPageSize: true }],
  ['certificado/certificado.html', 'certificado/Imersao AME - Certificado.pdf', { preferCSSPageSize: true }],
];
const ARTES = [
  ['divulgacao/divulgacao.html', '', 1080, 1350, 'divulgacao/imersao-ame-feed.png'],
  ['divulgacao/divulgacao.html', '?story', 1080, 1920, 'divulgacao/imersao-ame-story.png'],
];

(async () => {
  const dir = __dirname;
  const b = await chromium.launch();
  for (const [html, pdf, opt] of PDFS) {
    const p = await b.newPage();
    await p.goto('file://' + path.join(dir, html));
    await p.evaluate(() => document.fonts.ready);
    await p.pdf({ path: path.join(dir, pdf), printBackground: true, ...opt });
    await p.close();
    console.log('PDF ok:', pdf);
  }
  for (const [html, q, w, h, png] of ARTES) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.goto('file://' + path.join(dir, html) + q);
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(dir, png) });
    await p.close();
    console.log('PNG ok:', png);
  }
  await b.close();
})();
