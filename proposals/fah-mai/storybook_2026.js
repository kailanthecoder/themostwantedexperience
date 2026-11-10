(function(){
'use strict';
const viewport=document.querySelector('.viewport');
const pages=viewport?[...viewport.querySelectorAll('.sheet')]:[];
const rail=document.querySelector('.fm-zoom');
const slider=document.querySelector('.fm-zoom-range');
const out=document.querySelector('.fm-zoom-readout');
const minus=document.querySelector('.fm-zoom-minus');
const plus=document.querySelector('.fm-zoom-plus');
const prev=document.querySelector('.fm-story-prev');
const next=document.querySelector('.fm-story-next');
const counter=document.querySelector('.fm-story-counter');
const tabs=[...document.querySelectorAll('.proposal-sections [data-target]')];
const proposal=document.getElementById('nav-proposal'),examples=document.getElementById('tab-examples');
if(!viewport||!pages.length||!rail||!prev||!next||!slider)return;
const mobile=()=>window.innerWidth<=800;
const perView=()=>mobile()?1:2;
const clamp=x=>Math.max(.75,Math.min(2.5,Math.round(Number(x)*20)/20));
const group=page=>page.dataset.proposalSection||page.id;
let factor=1,index=0,oldMobile=mobile();
try{const stored=Number(sessionStorage.getItem('fahmai_mobile_zoom')||1);if(Number.isFinite(stored))factor=clamp(stored)}catch(e){}
function zoom(centre){
  slider.value=String(factor);
  out.textContent=Number(factor.toFixed(2)).toLocaleString('en-US',{maximumFractionDigits:2})+'×';
  const n=perView(),gap=n===2?16:0,padding=mobile()?18:24;
  const fit=Math.min(1,Math.max(.12,(viewport.clientWidth-padding-gap)/(n*794)));
  pages.forEach(page=>page.style.setProperty('zoom',String(fit*factor),'important'));
  if(centre)requestAnimationFrame(()=>{viewport.scrollLeft=Math.max(0,(viewport.scrollWidth-viewport.clientWidth)/2)});
}
function display(centre){
  const n=perView(),maxStart=Math.max(0,pages.length-n);
  index=Math.max(0,Math.min(index,maxStart));
  pages.forEach((page,i)=>{
    const show=i>=index&&i<index+n;
    page.classList.toggle('is-active',show);
    page.setAttribute('aria-hidden',String(!show));
  });
  prev.disabled=index===0;next.disabled=index>=maxStart;
  const first=index+1,last=Math.min(pages.length,index+n);
  counter.textContent=n===2?first+'–'+last+' / '+pages.length:first+' / '+pages.length;
  counter.title=n===2?'Pages '+first+'–'+last+' of '+pages.length:'Page '+first+' of '+pages.length;
  zoom(centre!==false);
}
function turn(target,fromTab){
  if(target<0||target>=pages.length)return;
  const section=group(pages[target]);
  if(!fromTab){
    if(section==='examples'){
      if(examples?.getAttribute('aria-pressed')!=='true')examples?.click();
    }else{
      const selected=tabs.find(t=>t.getAttribute('aria-selected')==='true');
      if(!selected||selected.dataset.target!==section||proposal?.getAttribute('aria-pressed')!=='true'){
        tabs.find(t=>t.dataset.target===section)?.click();
      }
    }
  }
  index=target;display(true);
  if(mobile()&&section!=='examples'){
    tabs.find(t=>t.dataset.target===section)?.scrollIntoView({behavior:'smooth',inline:'center',block:'nearest'});
  }
  window.scrollTo({top:0,behavior:'smooth'});
}
function updateZoom(x){
  factor=clamp(x);
  try{sessionStorage.setItem('fahmai_mobile_zoom',String(factor))}catch(e){}
  zoom(true);
}
slider.addEventListener('input',()=>updateZoom(slider.value));
minus.addEventListener('click',()=>updateZoom(factor-.25));
plus.addEventListener('click',()=>updateZoom(factor+.25));
prev.addEventListener('click',()=>turn(Math.max(0,index-perView())));
next.addEventListener('click',()=>turn(Math.min(pages.length-perView(),index+perView())));
tabs.forEach(t=>t.addEventListener('click',()=>{
  const found=pages.findIndex(p=>p.id===t.dataset.target);
  if(found>=0){index=found;display(true)}
  if(mobile())t.scrollIntoView({inline:'center',block:'nearest',behavior:'smooth'});
}));
proposal?.addEventListener('click',()=>{
  const selected=tabs.find(t=>t.getAttribute('aria-selected')==='true');
  index=Math.max(0,pages.findIndex(p=>p.id===(selected?.dataset.target||'overview')));
  display(true);
});
examples?.addEventListener('click',()=>{
  index=pages.findIndex(p=>p.id==='examples');display(true);
});
let pinch=null,swipe=null;
viewport.addEventListener('touchstart',e=>{
  if(e.touches.length===2){
    swipe=null;
    pinch={distance:Math.hypot(e.touches[0].clientX-e.touches[1].clientX,e.touches[0].clientY-e.touches[1].clientY),factor};
  }else if(e.touches.length===1&&factor<=1.05){
    swipe={x:e.touches[0].clientX,y:e.touches[0].clientY};
  }
},{passive:true});
viewport.addEventListener('touchmove',e=>{
  if(pinch&&e.touches.length===2){
    const d=Math.hypot(e.touches[0].clientX-e.touches[1].clientX,e.touches[0].clientY-e.touches[1].clientY);
    updateZoom(pinch.factor*d/Math.max(1,pinch.distance));
  }
},{passive:true});
viewport.addEventListener('touchend',e=>{
  if(pinch&&e.touches.length<2)pinch=null;
  if(swipe&&e.changedTouches.length===1){
    const dx=e.changedTouches[0].clientX-swipe.x,dy=e.changedTouches[0].clientY-swipe.y;
    if(Math.abs(dx)>65&&Math.abs(dx)>Math.abs(dy)*1.4){
      turn(Math.max(0,Math.min(pages.length-perView(),index+(dx<0?perView():-perView()))));
    }
    swipe=null;
  }
},{passive:true});
document.addEventListener('keydown',e=>{
  if(e.defaultPrevented||/INPUT|TEXTAREA|SELECT/.test(e.target?.tagName||'')||e.target?.isContentEditable)return;
  if(e.altKey&&e.key==='ArrowRight'){e.preventDefault();next.click()}
  if(e.altKey&&e.key==='ArrowLeft'){e.preventDefault();prev.click()}
});
window.addEventListener('resize',()=>{
  if(oldMobile!==mobile()){oldMobile=mobile();display(true)}
  else zoom(true);
},{passive:true});
window.addEventListener('beforeprint',()=>pages.forEach(p=>p.style.removeProperty('zoom')));
window.addEventListener('afterprint',()=>display(true));
const requested=location.hash.replace('#','');
const initial=pages.findIndex(p=>p.id===requested);
index=initial<0?0:initial;
display(true);
})();