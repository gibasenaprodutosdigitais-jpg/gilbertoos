// Extrai texto de um PDF para .txt. Uso: node extract-pdf.js <input.pdf> <output.txt>
const fs = require('fs');
const path = require('path');

async function main() {
  const input = process.argv[2];
  const output = process.argv[3];
  if (!input || !output) {
    console.error('Uso: node extract-pdf.js <input.pdf> <output.txt>');
    process.exit(1);
  }
  const buffer = fs.readFileSync(input);
  const mod = require('pdf-parse');
  const pdf = mod.default || mod;

  let text = '';
  let pages = 0;
  try {
    // pdf-parse v1 style
    const data = await pdf(buffer);
    text = data.text;
    pages = data.numpages;
  } catch (e1) {
    // pdf-parse v2 style (class PDFParse)
    try {
      const { PDFParse } = mod;
      const parser = new PDFParse({ data: buffer });
      const result = await parser.getText();
      text = result.text;
      pages = result.total || (result.pages ? result.pages.length : 0);
    } catch (e2) {
      console.error('Falhou:', e1.message, '||', e2.message);
      process.exit(2);
    }
  }
  fs.writeFileSync(output, text, 'utf8');
  const words = text.split(/\s+/).filter(Boolean).length;
  console.log(`OK: ${pages} págs, ${words} palavras -> ${path.basename(output)}`);
}
main();
