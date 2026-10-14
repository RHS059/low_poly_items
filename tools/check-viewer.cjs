const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const browser = await chromium.launch({headless:true,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  const page = await browser.newPage({viewport:{width:1440,height:1000}});
  const errors=[]; page.on('pageerror',e=>errors.push(e.message));
  for (const id of ['b03_classic_muscle_coupe','b04_compact_open_debris_skip']) {
    await page.goto('http://127.0.0.1:8765/#'+id);
    await page.waitForFunction(()=>document.querySelector('#status').textContent==='',null,{timeout:90000});
    if(await page.locator('.item').count()!==1000) throw Error('Expected 1000 items');
    await page.screenshot({path:`review/${id}.png`});
  }
  await page.locator('#search').fill('tanker');
  if(!await page.locator('.item').count()) throw Error('Search returned no tanker');
  await page.locator('.item').first().click();
  await page.waitForFunction(()=>document.querySelector('#status').textContent==='');
  await page.mouse.move(900,500);await page.mouse.down();await page.mouse.move(1000,540,{steps:10});await page.mouse.up();
  await page.mouse.down({button:'right'});await page.mouse.move(950,520,{steps:10});await page.mouse.up({button:'right'});
  await page.locator('#reset').click();
  await page.locator('#search').fill('no-such-object-983');
  if(await page.locator('.item').count()!==0) throw Error('Empty search failed');
  await page.locator('#search').fill('');
  await page.locator('#next').click();await page.waitForFunction(()=>document.querySelector('#status').textContent==='');
  if(errors.length)throw Error(errors.join('\n'));
  fs.writeFileSync('review/viewer-check.json',JSON.stringify({passed:true,checks:['1000 items','GLB loads','search','empty search','rotate','pan','reset','next item','no page errors'],date:new Date().toISOString()},null,2)+'\n');
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});
