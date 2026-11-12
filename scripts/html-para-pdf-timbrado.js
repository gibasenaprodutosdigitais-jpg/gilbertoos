const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [, , html, header, footer, out] = process.argv;
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + html); await p.waitForTimeout(500);
  await p.pdf({ path: out, format: 'A4', printBackground: true, displayHeaderFooter: true,
    headerTemplate: fs.readFileSync(header, 'utf8'), footerTemplate: fs.readFileSync(footer, 'utf8'),
    margin: { top: '42mm', bottom: '25mm', left: '22mm', right: '22mm' } });
  await b.close(); console.log(out);
})();
