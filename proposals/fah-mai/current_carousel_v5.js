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
    // offsetWidth and scrollLeft share the same unzoomed CSS pixel space.
    // getBoundingClientRect uses *scaled* pixels in the A4 storybook, which
    // would otherwise select the wrong screenshot at smaller desktop sizes.
    track.scrollTo({left:i*slides[0].offsetWidth,behavior:'smooth'});
  }
  buttons.forEach(b=>b.addEventListener('click',()=>move(Number(b.dataset.auditSlide))));
  track.addEventListener('scroll',()=>{
    if(frame!==null)cancelAnimationFrame(frame);
    frame=requestAnimationFrame(()=>{
      frame=null;
      const idx=Math.round(track.scrollLeft/Math.max(1,slides[0].offsetWidth));
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