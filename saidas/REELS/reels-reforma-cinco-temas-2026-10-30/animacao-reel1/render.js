// Renderiza anim.html quadro a quadro e monta o vídeo com ffmpeg.
//   node render.js            -> video completo + um mp4 por cena
//   node render.js 1.0 5.5    -> so tira print desses instantes (pra conferir)
const path = require('path');
const fs = require('fs');
const { execFileSync } = require('child_process');
const { chromium } = require(path.join(__dirname, '../../../../scripts/node_modules/playwright'));

const FPS = 30;
const aqui = __dirname;
const quadros = path.join(aqui, 'quadros');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.join(aqui, 'anim.html') + '?t=0');
  await page.evaluate(() => document.fonts.ready);
  const tela = await page.$('#tela');

  const instantes = process.argv.slice(2).map(Number);
  if (instantes.length) {
    for (const t of instantes) {
      await page.evaluate(t => window.render(t), t);
      await tela.screenshot({ path: path.join(aqui, `print-${t}.png`) });
    }
    await browser.close();
    return;
  }

  fs.rmSync(quadros, { recursive: true, force: true });
  fs.mkdirSync(quadros);
  const dur = await page.evaluate(() => window.DURACAO);
  const total = Math.round(dur * FPS);
  for (let i = 0; i < total; i++) {
    await page.evaluate(t => window.render(t), i / FPS);
    await tela.screenshot({ path: path.join(quadros, String(i).padStart(5, '0') + '.png') });
  }
  const cenas = await page.evaluate(() => window.CENAS);
  await browser.close();

  const ff = (...a) => execFileSync('ffmpeg', ['-v', 'error', '-y', ...a], { stdio: 'inherit' });
  const enc = ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', '-preset', 'slow'];
  ff('-framerate', String(FPS), '-i', path.join(quadros, '%05d.png'), ...enc, path.join(aqui, 'reel1-animacao-completa.mp4'));
  Object.entries(cenas).forEach(([id, [a, b]], k) => {
    ff('-framerate', String(FPS), '-start_number', String(Math.round(a * FPS)), '-i', path.join(quadros, '%05d.png'),
       '-frames:v', String(Math.round((b - a) * FPS)), ...enc, path.join(aqui, `cena-${k + 1}.mp4`));
  });
  fs.rmSync(quadros, { recursive: true, force: true });
})();
