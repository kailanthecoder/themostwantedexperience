(function(){
  "use strict";
  const sheet=document.getElementById("current");
  if(!sheet)return;
  const evidence=sheet.querySelector(".ps-evidence");
  const screenshot=evidence?.querySelector(".ps-report-image");
  const toggle=[...sheet.querySelectorAll(".ps-source-button")];
  const dots=[...sheet.querySelectorAll("[data-ps-slide]")];
  const back=evidence?.querySelector(".ps-previous");
  const next=evidence?.querySelector(".ps-next");
  if(!screenshot||dots.length!==5||toggle.length!==2)return;
  const items=[
    {name:"Fah Mai Holdings",mode:"Mobile",result:"Performance 61/100, LCP 9.8s",position:"0% 50%"},
    {name:"Fah Mai Holdings",mode:"Desktop",result:"Performance 78/100, LCP 2.0s",position:"25% 50%"},
    {name:"Whisky Bull Auctions",mode:"Desktop",result:"Performance test returned an error",position:"50% 50%"},
    {name:"Platinum Cask",mode:"Mobile",result:"Performance 48/100, LCP 15.8s",position:"75% 50%"},
    {name:"Platinum Cask",mode:"Desktop",result:"Performance 77/100, LCP 2.6s",position:"100% 50%"}
  ];
  let current=0;
  const title=evidence.querySelector(".ps-slide-caption strong");
  const metric=evidence.querySelector(".ps-slide-metric");
  const count=evidence.querySelector(".ps-slide-count");
  function show(index){
    current=(index+items.length)%items.length;
    const item=items[current];
    screenshot.style.setProperty("background-position",item.position,"important");
    screenshot.setAttribute("aria-label",item.name+" "+item.mode+" original PageSpeed Insights screenshot. "+item.result+". Select to view next report.");
    title.textContent=item.name+" · "+item.mode;
    metric.textContent=item.result;
    count.textContent=(current+1)+" / "+items.length;
    for(let i=0;i<dots.length;i++){
      dots[i].classList.toggle("is-selected",i===current);
      dots[i].setAttribute("aria-pressed",String(i===current));
    }
  }
  function switchMode(which){
    const sites=which==="sites";
    sheet.classList.toggle("ps-show-sites",sites);
    for(const button of toggle){
      const selected=button.dataset.psView===which;
      button.classList.toggle("is-selected",selected);
      button.setAttribute("aria-pressed",String(selected));
    }
  }
  toggle.forEach(el=>el.addEventListener("click",()=>switchMode(el.dataset.psView)));
  screenshot.addEventListener("click",()=>show(current+1));
  back.addEventListener("click",()=>show(current-1));
  next.addEventListener("click",()=>show(current+1));
  dots.forEach((dot,i)=>dot.addEventListener("click",()=>show(i)));
  screenshot.addEventListener("keydown",e=>{
    if(e.key==="ArrowLeft"||e.key==="ArrowRight"){
      e.preventDefault();e.stopPropagation();
      show(current+(e.key==="ArrowLeft"?-1:1));
    }
  });
  // All five images are sourced from screenshots provided by the proposal author
  // on 11 November 2026. They are historical snapshots, not live tests.
  show(0);
  switchMode("reports");
})();