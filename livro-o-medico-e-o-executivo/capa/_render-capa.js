const path=require('path'); const {chromium}=require('playwright');
(async()=>{
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:945,height:1358},deviceScaleFactor:2});
  await p.goto('file://'+path.join(__dirname,'capa.html'));
  await p.evaluate(()=>document.fonts.ready);
  await p.waitForTimeout(400);
  await p.locator('.capa').screenshot({path:path.join(__dirname,'O Medico e o Executivo - capa.png')});
  await b.close();
  console.log('capa pronta, 1890x2716 (16x23cm a 300dpi)');
})();
