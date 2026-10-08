
const path=require('path'); const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+path.join(__dirname,'plano-de-mentoria.html'));
await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:path.join(__dirname,'SBS Mentoria Business Medical.pdf'),
  format:'A4',printBackground:true,
  margin:{top:'14mm',bottom:'14mm',left:'15mm',right:'15mm'}});
await b.close();console.log('PDF ok');})();
