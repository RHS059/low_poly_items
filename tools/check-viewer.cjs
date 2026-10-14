const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const browser = await chromium.launch({headless:true,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  const page = await browser.newPage({viewport:{width:1440,height:1000}});
  const manifest=JSON.parse(fs.readFileSync('manifest.json','utf8'));
  const expected=manifest.asset_count;const names=new Set(manifest.assets.map(a=>a.name));
  const errors=[]; page.on('pageerror',e=>errors.push(e.message));
  for (const id of ['b03_classic_muscle_coupe','b04_compact_open_debris_skip','b08_american_elm','b10_bottled_drink_vending_machine','b17_running_shoe','b21_wall_window_opening_4m','b21_door_wood_panel'].filter(id=>names.has(id))) {
    await page.goto('http://127.0.0.1:8765/?check='+id+'#'+id);
    await page.waitForFunction(()=>document.querySelector('#status').textContent==='',null,{timeout:90000});
    if(await page.locator('#title').textContent()!==id.replace(/^b\d+_/, '').replaceAll('_',' ')) throw Error('Wrong selected model');
    if(await page.locator('.item').count()!==expected) throw Error('Incorrect asset count');
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
  if(fs.existsSync('argon/manifest.json')) {
    const argon=JSON.parse(fs.readFileSync('argon/manifest.json','utf8'));
    await page.locator('#tab-argon').click();
    await page.waitForFunction(()=>document.querySelector('#status').textContent===''&&document.querySelector('#tab-argon').getAttribute('aria-selected')==='true');
    if(await page.locator('.item').count()!==argon.items.length)throw Error('Argon count mismatch');
    if(!(await page.locator('#download').getAttribute('href')).includes('/argon/exports/'))throw Error('Argon download points to Astra');
    await page.locator('#search').fill('classic muscle coupe');
    await page.locator('.item').first().click();
    await page.waitForFunction(()=>document.querySelector('#status').textContent==='');
    await page.screenshot({path:'review/argon-muscle-coupe.png'});
    const deepLink=page.url();await page.reload();
    await page.waitForFunction(()=>document.querySelector('#status').textContent==='');
    if(await page.locator('#tab-argon').getAttribute('aria-selected')!=='true'||!page.url().includes('#argon/'))throw Error('Argon deep link failed');
    await page.locator('#tab-astra').click();await page.waitForFunction(()=>document.querySelector('#status').textContent==='');
    if((await page.locator('#download').getAttribute('href')).includes('/argon/'))throw Error('Astra download points to Argon');
    await page.locator('#tab-argon').click();await page.locator('#tab-astra').click();
    await page.waitForFunction(()=>document.querySelector('#status').textContent==='');
    if(!page.url().includes('#astra/'))throw Error('Rapid tab switching selected stale model');
    await page.locator('#tab-astra').focus();await page.keyboard.press('ArrowRight');
    await page.waitForFunction(()=>document.querySelector('#status').textContent===''&&document.querySelector('#tab-argon').getAttribute('aria-selected')==='true');
  }
  if(errors.length)throw Error(errors.join('\n'));
  fs.writeFileSync('review/viewer-check.json',JSON.stringify({passed:true,checks:[expected+' items','GLB loads','search','empty search','rotate','pan','reset','next item','no page errors','collection tabs, counts, downloads, deep links, rapid switching and keyboard navigation'],date:new Date().toISOString()},null,2)+'\n');
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});
