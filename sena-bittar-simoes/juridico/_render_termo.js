
const path=require('path'); const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+path.join(__dirname,'termo-de-compromisso-sbs.html'));
await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:path.join(__dirname,'SBS - Termo de Compromisso e NDA.pdf'),
  format:'A4',printBackground:true,
  margin:{top:'14mm',bottom:'14mm',left:'15mm',right:'15mm'}});
await b.close();console.log('PDF ok');})();
