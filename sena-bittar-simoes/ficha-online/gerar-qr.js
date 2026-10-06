// QR do link da ficha online, em dois formatos: PNG grande pra impressao
// e SVG pra usar em peca vetorial.
const QR = require('qrcode');
const path = require('path');
const LINK = process.env.LINK || 'https://claude.ai/artifact/8XJKDDjP2FWsxMKp7z9gY7';
const dir = __dirname;
const opts = { errorCorrectionLevel: 'H', margin: 2,
               color: { dark: '#0C1A2E', light: '#FFFFFF' } };
(async () => {
  await QR.toFile(path.join(dir, 'qr-ficha-sbs.png'), LINK, {...opts, width: 1400});
  await QR.toFile(path.join(dir, 'qr-ficha-sbs.svg'), LINK, {...opts, type: 'svg'});
  console.log('QR gerado para', LINK);
})();
