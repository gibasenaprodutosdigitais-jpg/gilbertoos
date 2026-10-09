const fs=require('fs'), path=require('path');
const {chromium}=require('playwright');
(async()=>{
  const dir=path.join(__dirname,'formatado');
  const b=await chromium.launch();
  for (const f of fs.readdirSync(dir).filter(x=>x.endsWith('.html'))){
    const p=await b.newPage();
    await p.goto('file://'+path.join(dir,f));
    await p.evaluate(()=>document.fonts.ready);
    const out=path.join(dir,f.replace('.html','.pdf'));
    await p.pdf({path:out,format:'A4',printBackground:true,
      margin:{top:'3cm',bottom:'2cm',left:'3cm',right:'2cm'}});
    await p.close();
    const d=fs.readFileSync(out);
    const n=(d.toString('latin1').match(/\/Type\s*\/Page[^s]/g)||[]).length;
    console.log(String(n).padStart(3),'paginas  ',f.replace('.html',''));
  }
  await b.close();
})();
