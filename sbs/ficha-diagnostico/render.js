const path = require('path');
const { chromium } = require('playwright');

// As tres fichas da esteira: clinica, hospital dia e rede. Mesma identidade,
// mesmo ficha.css, mesma margem de impressao.
const FICHAS = [
  ['ficha-diagnostico.html',  'Sena, Bittar e Simoes - Ficha de Diagnostico.pdf'],
  ['ficha-hospital-dia.html', 'Sena, Bittar e Simoes - Ficha de Diagnostico - Hospital Dia.pdf'],
  ['ficha-rede.html',         'Sena, Bittar e Simoes - Ficha de Diagnostico - Rede e Grandes Hospitais.pdf'],
];

(async () => {
  const dir = __dirname;
  const b = await chromium.launch();
  for (const [html, pdf] of FICHAS) {
    const p = await b.newPage();
    await p.goto('file://' + path.join(dir, html));
    await p.evaluate(() => document.fonts.ready);
    await p.pdf({
      path: path.join(dir, pdf),
      format: 'A4', printBackground: true,
      margin: { top: '11mm', bottom: '11mm', left: '13mm', right: '13mm' },
    });
    await p.close();
    console.log('PDF ok:', pdf);
  }
  await b.close();
})();
