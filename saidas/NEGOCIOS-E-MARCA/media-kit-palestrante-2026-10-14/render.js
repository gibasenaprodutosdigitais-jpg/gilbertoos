const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const outDir = path.join(__dirname, 'paginas');
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  await page.goto('file://' + path.join(__dirname, 'media-kit.html'));
  await page.waitForTimeout(2500);
  const secs = await page.$$('.pagina');
  for (let i = 0; i < secs.length; i++) {
    const n = String(i + 1).padStart(2, '0');
    await secs[i].screenshot({ path: path.join(outDir, `pagina-${n}.png`) });
  }
  await page.pdf({ path: path.join(__dirname, 'Gilberto-Sena-Media-Kit.pdf'),
                   format: 'A4', printBackground: true, margin: {top:0,right:0,bottom:0,left:0} });
  await browser.close();
  console.log(`${secs.length} paginas + PDF`);
})();
