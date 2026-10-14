const fs=require('fs'), path=require('path'), {chromium}=require('playwright');
(async()=>{
  const dir=__dirname;
  const frases=JSON.parse(fs.readFileSync(path.join(dir,'frases.json'),'utf8'));
  const base=fs.readFileSync(path.join(dir,'card.html'),'utf8');
  const browser=await chromium.launch();
  const page=await browser.newPage({viewport:{width:1160,height:1430}});
  for(const f of frases){
    const cls = f.frase.length>72 ? 'longa' : '';
    const html=base.replace('<div id="palco"></div>',`
      <div class="card">
        <div class="foto" style="background-image:url('assets/foto.jpg')"></div>
        <div class="faixa"></div>
        <div class="topo"><div class="dia">${f.rotulo}</div><div class="arroba">@gilbertosenaoficial</div></div>
        <div class="regua"></div>
        <div class="frase ${cls}">${f.frase}</div>
        <img class="logo" src="assets/logo.png" alt="">
      </div>`);
    const tmp=path.join(dir,'_tmp.html'); fs.writeFileSync(tmp,html);
    await page.goto('file://'+tmp); await page.waitForTimeout(400);
    const el=await page.$('.card');
    await el.screenshot({path:path.join(dir,'instagram',`${f.dia}.png`)});
    console.log('ok',f.dia); fs.unlinkSync(tmp);
  }
  await browser.close();
})();
