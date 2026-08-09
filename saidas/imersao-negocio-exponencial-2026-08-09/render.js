const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const file = path.join(__dirname, 'imersao-negocio-exponencial.html');
  const browser = await chromium.launch();

  // Screenshot da página inteira (visualização web)
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.goto('file://' + file);
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(__dirname, 'preview-web.png'), fullPage: true });

  // PDF (mesmo padrão do mapa-treinamento: A4 paisagem, print CSS já embutido)
  await page.emulateMedia({ media: 'print' });
  await page.pdf({
    path: path.join(__dirname, 'imersao-negocio-exponencial.pdf'),
    format: 'A4',
    landscape: true,
    printBackground: true,
    margin: { top: '10mm', bottom: '10mm', left: '10mm', right: '10mm' },
  });

  await browser.close();
  console.log('Gerado: preview-web.png + imersao-negocio-exponencial.pdf');
})();
