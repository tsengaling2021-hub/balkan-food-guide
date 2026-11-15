// Run: node shanghai-nanjing-2026/qa-static.mjs
// Checks actual files, not public deployment or browser interaction.
import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const root=dirname(fileURLToPath(import.meta.url));
const pages=['index.html','day2-preview.html','day2-option1.html'];
const errors=[];
const files=new Map();
for(const page of pages){
 const p=resolve(root,page);
 if(!existsSync(p)){errors.push('Missing page: '+page);continue;}
 files.set(page,readFileSync(p,'utf8'));
}
for(const [page,html] of files){
 // Ignore JS string literals containing generated HTML: those are not DOM links.
 const staticHtml=html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,'');
 const ids=new Set([...html.matchAll(/\bid=["']([^"']+)["']/g)].map(m=>m[1]));
 for(const m of staticHtml.matchAll(/\b(?:href|src)=["']([^"']+)["']/g)){
  const url=m[1];if(!url||/^(?:https?:|data:|mailto:|tel:|javascript:)/i.test(url))continue;
  const [target,fragment]=url.split('#');const name=target||page;
  if(name.startsWith('/'))continue;
  const targetPath=resolve(root,dirname(page),decodeURIComponent(name));
  if(!existsSync(targetPath)){errors.push(page+' -> missing '+url);continue;}
  if(fragment){
   const targetHtml=name===page||!target?html:readFileSync(targetPath,'utf8');
   if(!new RegExp('\\bid=["\\\']'+fragment.replace(/[.*+?^\x24{}()|[\]\\]/g,'\\$&')+'["\\\']').test(targetHtml))
    errors.push(page+' -> missing anchor '+url);
  }
 }
}
const index=files.get('index.html')||'';
for(let d=19;d<=30;d++)if(!new RegExp('id=["\\\']day'+d+'["\\\']').test(index))errors.push('Missing date anchor day'+d);
const preview=files.get('day2-preview.html')||'';
for(let n=3;n<=8;n++)if(!new RegExp('id=["\\\']spot'+n+'["\\\']').test(preview))errors.push('Missing Shanghai option anchor spot'+n);
console.log('Checked '+files.size+' pages; '+errors.length+' errors');
for(const e of errors)console.error('FAIL '+e);
if(errors.length)process.exitCode=1;
