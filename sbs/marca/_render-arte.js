const path=require('path'); const {chromium}=require('playwright');
(async()=>{
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:1536,height:1024},deviceScaleFactor:2});
  await p.goto('file://'+path.join(__dirname,'arte-institucional.html'));
  await p.evaluate(()=>document.fonts.ready);
  await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode().catch(()=>{}))));
  await p.waitForTimeout(700);
  await p.locator('.arte').screenshot({path:path.join(__dirname,'sbs-arte-institucional-v2.png')});
  await b.close(); console.log('arte pronta, 3072x2048');
})();
