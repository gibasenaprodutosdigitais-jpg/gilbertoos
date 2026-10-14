const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const dir = __dirname;
  const frases = JSON.parse(fs.readFileSync(path.join(dir,'frases.json'),'utf8'));
  const base = fs.readFileSync(path.join(dir,'card.html'),'utf8');
  const only = process.argv[2] ? parseInt(process.argv[2],10) : null;
  const fotos = fs.readdirSync(path.join(dir,'assets')).filter(f=>/^foto-\d+\.(jpg|jpeg|png)$/i.test(f)).sort();
  if (!fotos.length) { console.error('sem fotos em assets/ (foto-01.jpg, foto-02.jpg, ...)'); process.exit(1); }

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport:{width:1160,height:1430}, deviceScaleFactor:1 });

  for (const f of frases) {
    if (only && f.dia !== only) continue;
    const foto = fotos[(f.dia - 1) % fotos.length];
    const n = f.frase.length;
    const cls = n > 92 ? 'longa' : (n < 66 ? 'curta' : '');
    const html = base.replace('<div id="palco"></div>', `
      <div class="card">
        <div class="foto" style="background-image:url('assets/${foto}')"></div>
        <div class="halo"></div>
        <div class="faixa"></div>
        <div class="topo"><div class="num">${String(f.dia).padStart(2,'0')}</div>
          <div class="rotulo">Sabedoria<br>para empreender</div></div>
        <div class="regua"></div>
        <div class="bloco">
          <div class="frase ${cls}">${f.frase}</div>
          <div class="fonte">Reflexão autoral inspirada em <b>${f.ref}</b>.</div>
        </div>
        <div class="rodape"><img src="assets/logo.png" alt=""><div class="arroba">@gilbertosenaoficial</div></div>
      </div>`);
    const tmp = path.join(dir, '_tmp.html');
    fs.writeFileSync(tmp, html);
    await page.goto('file://' + tmp);
    await page.waitForTimeout(400);
    const el = await page.$('.card');
    const out = path.join(dir,'instagram',`dia-${String(f.dia).padStart(2,'0')}.png`);
    await el.screenshot({ path: out });
    console.log('ok dia', f.dia);
    fs.unlinkSync(tmp);
  }
  await browser.close();
})();
