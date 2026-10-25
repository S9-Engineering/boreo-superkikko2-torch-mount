/* QA del visore locale, da eseguire sul wrapper creato dal render.py di Visualize.
   R04_PLAYWRIGHT_MODULE puo indicare un modulo Playwright installato. */
const {chromium}=require(process.env.R04_PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=path.resolve(__dirname,'..');
const workspace=path.resolve(root,'../..');
const folder=path.join(workspace,'output/visualizzazioni');
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--enable-webgl','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 try{
  const page=await browser.newPage({viewport:{width:780,height:720}}),errors=[];
  page.on('pageerror',e=>errors.push(String(e)));
  await page.goto('file://'+path.join(folder,'boreo-portafarfalla-r04-preview.html'));
  await page.waitForTimeout(300);
  const frame=page.frames().find(f=>f.parentFrame()),canvas=frame.locator('canvas');
  await frame.locator('canvas[data-mode]').waitFor({timeout:30000});
  const check=()=>frame.evaluate(()=>({width:innerWidth,scroll:document.body.scrollWidth,mode:document.querySelector('canvas').dataset.mode,vertices:Number(document.querySelector('canvas').dataset.vertices),webgl_error:document.querySelector('canvas').getContext('webgl').getError()}));
  const report={frammento_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(folder,'boreo-portafarfalla-r04.html'))).digest('hex'),controlli:{iniziale:await check()}};
  const before=await canvas.screenshot(),box=await canvas.boundingBox();
  await page.mouse.move(box.x+140,box.y+140);await page.mouse.down();await page.mouse.move(box.x+195,box.y+165,{steps:3});await page.mouse.up();
  report.controlli.rotazione={pixels_changed:!before.equals(await canvas.screenshot())};
  for(const[label,name]of[['Assemblato','assembled'],['Solo supporto','support'],['Esploso','exploded']]){
   await frame.getByRole('button',{name:label,exact:true}).click();report.controlli[name]=await check();
   await page.screenshot({path:path.join(folder,`boreo-r04-${name}-780.png`),fullPage:true});
  }
  await frame.getByRole('button',{name:'Altra vista',exact:true}).click();report.controlli.cambio_vista=await check();
  await page.emulateMedia({colorScheme:'dark'});report.controlli.dark=await check();await page.screenshot({path:path.join(folder,'boreo-r04-dark.png'),fullPage:true});
  await page.setViewportSize({width:352,height:680});report.controlli.mobile320=await check();await page.screenshot({path:path.join(folder,'boreo-r04-320.png'),fullPage:true});
  report.errori_javascript=errors;report.limite='Anteprima software: nessuna prova di montaggio, resistenza o stampa';
  const passed=!errors.length&&report.controlli.rotazione.pixels_changed&&Object.entries(report.controlli).filter(([k])=>k!=='rotazione').every(([,v])=>v.width===v.scroll&&v.webgl_error===0&&v.vertices>0);
  report.controlli_superati=passed;fs.writeFileSync(path.join(root,'verifiche/anteprima_interattiva.json'),JSON.stringify(report,null,2)+'\n');
  if(!passed)process.exitCode=1;console.log(JSON.stringify(report));
 }finally{await browser.close();}
})();
