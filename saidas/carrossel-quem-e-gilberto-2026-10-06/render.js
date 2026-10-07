const path=require('path'); const {chromium}=require('playwright'); const fs=require('fs');
(async()=>{
  const out=path.join(__dirname,'instagram'); fs.mkdirSync(out,{recursive:true});
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
  await p.goto('file://'+path.join(__dirname,'carrossel.html'));
  await p.evaluate(()=>document.fonts.ready);
  await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode().catch(()=>{}))));
  await p.waitForTimeout(500);
  const n=await p.locator('.card').count();
  for(let i=0;i<n;i++){
    await p.locator('.card').nth(i).screenshot({path:path.join(out,`card-${String(i+1).padStart(2,'0')}.png`)});
  }
  await b.close(); console.log('cards:',n);
})();
