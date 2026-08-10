const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const dir = __dirname;
  const browser = await chromium.launch();

  const files = [
    'contrato-locacao-espaco-kairos-opcao1-caucao-parcelada',
    'contrato-locacao-espaco-kairos-opcao2-caucao-com-nota-promissoria',
  ];

  for (const f of files) {
    const page = await browser.newPage();
    await page.goto('file://' + path.join(dir, f + '.html'));
    await page.pdf({
      path: path.join(dir, f + '.pdf'),
      format: 'A4',
      printBackground: true,
      margin: { top: '18mm', bottom: '18mm', left: '18mm', right: '18mm' },
    });
    await page.close();
    console.log(f + '.pdf ok');
  }

  await browser.close();
})();
