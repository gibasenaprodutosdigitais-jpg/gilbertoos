const path = require('path');
const { chromium } = require('playwright');

// Kit do participante da Imersão AME: a ficha de diagnóstico, o exercício
// da margem, as decisões dos dois dias e os quatro números. A4, para imprimir
// uma por participante. Com FOTO=1 tira também uma foto de cada folha.
(async () => {
  const dir = __dirname;
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.join(dir, 'kit-do-participante.html'));
  await p.evaluate(() => document.fonts.ready);
  const pdf = path.join(dir, 'Imersao AME - Kit do Participante.pdf');
  await p.pdf({
    path: pdf, format: 'A4', printBackground: true,
    margin: { top: '11mm', bottom: '11mm', left: '13mm', right: '13mm' },
  });
  console.log('PDF ok:', pdf);
  await b.close();
})();
