(function(){
  'use strict';
  const root=document.querySelector('#current .audit-v5-carousel');
  if(!root)return;
  const track=root.querySelector('.audit-v5-track');
  const buttons=[...root.querySelectorAll('[data-audit-slide]')];
  const slides=[...root.querySelectorAll('.audit-v5-slide')];
  if(!track||slides.length!==3)return;
  let active=-1,frame=null;
  function setActive(i){
    if(i===active)return;
    active=i;
    buttons.forEach((b,index)=>{
      const selected=index===i;
      b.classList.toggle('is-selected',selected);
      b.setAttribute('aria-pressed',String(selected));
    });
  }
  function move(i){
    i=Math.max(0,Math.min(slides.length-1,i));
    setActive(i);
    const first=slides[0].getBoundingClientRect();
    const target=slides[i].getBoundingClientRect();
    track.scrollBy({left:target.left-first.left-track.scrollLeft,behavior:'smooth'});
  }
  buttons.forEach(b=>b.addEventListener('click',()=>move(Number(b.dataset.auditSlide))));
  track.addEventListener('scroll',()=>{
    if(frame!==null)cancelAnimationFrame(frame);
    frame=requestAnimationFrame(()=>{
      frame=null;
      const first=slides[0].getBoundingClientRect();
      const idx=Math.round(track.scrollLeft/Math.max(1,first.width));
      setActive(Math.max(0,Math.min(slides.length-1,idx)));
    });
  },{passive:true});
  track.addEventListener('keydown',e=>{
    if(e.key==='ArrowRight'||e.key==='ArrowLeft'){
      e.stopPropagation();e.preventDefault();
      move(active+(e.key==='ArrowRight'?1:-1));
    }
  });
  setActive(0);
})();