(function(){
  "use strict";
  const viewport=document.querySelector(".viewport");
  const sheets=viewport?[...viewport.querySelectorAll(".sheet")]:[];
  const sectionTabs=[...document.querySelectorAll(".toolbar nav.proposal-sections button[data-target]")];
  const sectionNav=document.querySelector(".toolbar nav.proposal-sections");
  const examplesSwitch=document.getElementById("tab-examples");
  const toolbar=document.querySelector(".toolbar");
  if(!viewport||sheets.length!==12||!sectionTabs.length)return;

  let scheduled=false;
  let previousSection="";
  const isVertical=()=>viewport.dataset.readingMode==="vertical";

  function getVisibleSheet(){
    if(!isVertical()){
      return sheets.find(s=>s.classList.contains("is-active"))||sheets[0];
    }
    const toolbarBottom=toolbar?.getBoundingClientRect().bottom||0;
    const focusY=toolbarBottom+Math.min(220,(window.innerHeight-toolbarBottom)*.42);
    let closest=sheets[0],closestDistance=Infinity;
    for(const sheet of sheets){
      const rect=sheet.getBoundingClientRect();
      if(rect.height<1)continue;
      if(rect.top<=focusY&&rect.bottom>=focusY)return sheet;
      const distance=Math.min(Math.abs(rect.top-focusY),Math.abs(rect.bottom-focusY));
      if(distance<closestDistance){
        closestDistance=distance;
        closest=sheet;
      }
    }
    return closest;
  }

  function update(){
    scheduled=false;
    const sheet=getVisibleSheet();
    const section=sheet?.dataset.chapter||sheet?.dataset.proposalSection||sheet?.id||"overview";
    const vertical=isVertical();
    document.body.dataset.chapterTracking=vertical?"vertical":"spread";
    document.body.dataset.currentChapter=section;

    for(const tab of sectionTabs){
      const selected=tab.dataset.target===section;
      if(selected)tab.dataset.chapterCurrent="true";
      else delete tab.dataset.chapterCurrent;
      if(selected)tab.setAttribute("aria-current","page");
      else tab.removeAttribute("aria-current");
    }
    if(examplesSwitch){
      if(section==="examples")examplesSwitch.dataset.chapterCurrent="true";
      else delete examplesSwitch.dataset.chapterCurrent;
    }

    // When mobile scrolling changes the chapter, reveal its label in the
    // existing one-line horizontal menu, without moving the page vertically.
    if(vertical&&section!==previousSection&&sectionNav){
      const active=sectionTabs.find(t=>t.dataset.target===section);
      if(active&&sectionNav.scrollWidth>sectionNav.clientWidth+8){
        const navRect=sectionNav.getBoundingClientRect();
        const tabRect=active.getBoundingClientRect();
        const next=sectionNav.scrollLeft+(tabRect.left-navRect.left)-(navRect.width-tabRect.width)/2;
        sectionNav.scrollTo({left:Math.max(0,next),behavior:"smooth"});
      }
    }
    previousSection=section;
  }

  function schedule(){
    if(scheduled)return;
    scheduled=true;
    window.requestAnimationFrame(update);
  }

  window.addEventListener("scroll",schedule,{passive:true});
  document.addEventListener("scroll",schedule,{passive:true,capture:true});
  document.scrollingElement?.addEventListener("scroll",schedule,{passive:true});
  window.addEventListener("resize",schedule,{passive:true});
  document.addEventListener("click",schedule,true);
  viewport.addEventListener("scroll",schedule,{passive:true});

  const observer=new MutationObserver(schedule);
  observer.observe(viewport,{attributes:true,attributeFilter:["data-reading-mode"]});
  sheets.forEach(sheet=>observer.observe(sheet,{attributes:true,attributeFilter:["class"]}));
  if("IntersectionObserver" in window){
    const seen=new IntersectionObserver(schedule,{root:null,threshold:[0,.18,.4,.7]});
    sheets.forEach(sheet=>seen.observe(sheet));
  }
  // Some in-app browsers do not consistently dispatch root-document scroll
  // events. A lightweight scroll-position check makes mobile tracking reliable
  // without repeatedly calculating all twelve sheet layouts.
  let lastScrollY=window.scrollY;
  window.setInterval(()=>{
    if(!isVertical())return;
    const nextY=window.scrollY;
    if(Math.abs(nextY-lastScrollY)>1){
      lastScrollY=nextY;
      schedule();
    }
  },180);
  schedule();
})();