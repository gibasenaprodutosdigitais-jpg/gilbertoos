const fs=require('fs'), path=require('path');
const {chromium}=require('playwright');
(async()=>{
  const dir=path.join(__dirname,'formatado');
  const out=path.join(dir,'O Medico e o Executivo - a parte do Gilberto.pdf');
  const b=await chromium.launch();
  const p=await b.newPage();
  await p.goto('file://'+path.join(dir,'_caderno.html'));
  await p.evaluate(()=>document.fonts.ready);
  await p.pdf({path:out,format:'A4',printBackground:true,
    displayHeaderFooter:true,
    headerTemplate:'<div style="width:100%;font-family:Times New Roman,serif;'+
      'font-size:11pt;text-align:right;padding:0 2cm 0 0;color:#000">'+
      '<span class="pageNumber"></span></div>',
    footerTemplate:'<span></span>',
    margin:{top:'3cm',bottom:'2cm',left:'3cm',right:'2cm'}});
  await b.close();
  const d=fs.readFileSync(out);
  const n=(d.toString('latin1').match(/\/Type\s*\/Page[^s]/g)||[]).length;
  console.log(n,'paginas  ->',path.basename(out));
})();
