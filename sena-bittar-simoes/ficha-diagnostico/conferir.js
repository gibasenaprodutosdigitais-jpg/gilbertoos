const path=require('path'); const {chromium}=require('playwright');
(async()=>{
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:880,height:1200},deviceScaleFactor:2});
  await p.goto('file://'+path.join(__dirname,'ficha-diagnostico.html'));
  await p.evaluate(()=>document.fonts.ready);
  await p.waitForTimeout(300);
  await p.screenshot({path:'/tmp/sbficha/tudo.png',fullPage:true});
  const h=await p.evaluate(()=>document.body.scrollHeight);
  console.log('altura total', h);
  await b.close();
})();
