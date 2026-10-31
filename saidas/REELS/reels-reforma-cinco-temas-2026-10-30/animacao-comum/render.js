// Renderiza o anim.html de uma pasta quadro a quadro e monta os vídeos com ffmpeg.
//   node render.js ../animacao-reel2           -> video completo + um mp4 por cena
//   node render.js ../animacao-reel2 1.0 5.5   -> so tira print desses instantes
//   ALVO=30 node render.js ../animacao-reel2   -> estica tudo por igual ate durar 30s (pedido dele em 30/out)
const path = require('path');
const fs = require('fs');
const { execFileSync } = require('child_process');
const { chromium } = require(path.join(__dirname, '../../../../scripts/node_modules/playwright'));

const FPS = 30;
const pasta = path.resolve(process.argv[2]);
const nome = path.basename(pasta).replace('animacao-', '');
const quadros = path.join(pasta, 'quadros');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.join(pasta, 'anim.html') + '?t=0');
  await page.evaluate(() => document.fonts.ready);
  const tela = await page.$('#tela');

  const instantes = process.argv.slice(3).map(Number);
  if (instantes.length) {
    for (const t of instantes) {
      await page.evaluate(t => window.render(t), t);
      await tela.screenshot({ path: path.join(pasta, `print-${t}.png`) });
    }
    await browser.close();
    return;
  }

  fs.rmSync(quadros, { recursive: true, force: true });
  fs.mkdirSync(quadros);
  const dur = await page.evaluate(() => window.DURACAO);
  const alvo = Number(process.env.ALVO) || dur;
  const ritmo = dur / alvo;  // < 1 deixa mais lento
  const total = Math.round(alvo * FPS);
  for (let i = 0; i < total; i++) {
    await page.evaluate(t => window.render(t), (i / FPS) * ritmo);
    await tela.screenshot({ path: path.join(quadros, String(i).padStart(5, '0') + '.png') });
  }
  const cenas = await page.evaluate(() => window.CENAS);
  await browser.close();

  const ff = (...a) => execFileSync('ffmpeg', ['-v', 'error', '-y', ...a], { stdio: 'inherit' });
  const enc = ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', '-preset', 'slow'];
  ff('-framerate', String(FPS), '-i', path.join(quadros, '%05d.png'), ...enc, path.join(pasta, `${nome}-animacao-completa.mp4`));
  Object.entries(cenas).forEach(([id, [a0, b0]], k) => {
    const a = a0 / ritmo, b = b0 / ritmo;
    ff('-framerate', String(FPS), '-start_number', String(Math.round(a * FPS)), '-i', path.join(quadros, '%05d.png'),
       '-frames:v', String(Math.round((b - a) * FPS)), ...enc, path.join(pasta, `cena-${k + 1}.mp4`));
  });
  fs.rmSync(quadros, { recursive: true, force: true });
})();
