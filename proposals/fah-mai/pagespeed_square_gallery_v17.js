(function(){
  "use strict";
  const section=document.getElementById("current");
  if(!section)return;
  const gallery=section.querySelector(".ps-v17-evidence");
  if(!gallery)return;
  const thumbs=[...gallery.querySelectorAll(".ps-v17-thumb[data-ps-slide]")];
  const main=gallery.querySelector(".ps-v17-main-image");
  const title=gallery.querySelector(".ps-v17-title");
  const result=gallery.querySelector(".ps-v17-result");
  const index=gallery.querySelector(".ps-v17-index");
  if(thumbs.length!==5||!main||!title||!result||!index)return;
  const reports=[
    {brand:"Fah Mai Holdings",device:"Mobile",score:"61/100 performance · 9.8s LCP",img:"./pagespeed-fmh-mobile-v17.png",alt:"Fah Mai Holdings mobile PageSpeed Insights screenshot, performance 61"},
    {brand:"Fah Mai Holdings",device:"Desktop",score:"78/100 performance · 2.0s LCP",img:"./pagespeed-fmh-desktop-v17.png",alt:"Fah Mai Holdings desktop PageSpeed Insights screenshot, performance 78"},
    {brand:"Whisky Bull Auctions",device:"Desktop",score:"Test returned an error; no score available",img:"./pagespeed-whiskybull-desktop-v17.png",alt:"Whisky Bull desktop PageSpeed Insights report displaying a test error"},
    {brand:"Platinum Cask",device:"Mobile",score:"48/100 performance · 15.8s LCP",img:"./pagespeed-platinum-mobile-v17.png",alt:"Platinum Cask mobile PageSpeed Insights screenshot, performance 48"},
    {brand:"Platinum Cask",device:"Desktop",score:"77/100 performance · 2.6s LCP",img:"./pagespeed-platinum-desktop-v17.png",alt:"Platinum Cask desktop PageSpeed Insights screenshot, performance 77"}
  ];
  let selected=0;
  function select(i,focus=false){
    selected=(i+reports.length)%reports.length;
    const report=reports[selected];
    main.src=report.img;
    main.alt=report.alt;
    title.textContent=report.brand;
    result.textContent=report.device+" · "+report.score;
    index.textContent=String(selected+1).padStart(2,"0")+" / 05";
    thumbs.forEach((button,n)=>{
      const active=n===selected;
      button.classList.toggle("is-selected",active);
      button.setAttribute("aria-pressed",String(active));
    });
    if(focus)thumbs[selected].focus({preventScroll:true});
  }
  thumbs.forEach((button,i)=>{
    button.addEventListener("click",()=>select(i));
    button.addEventListener("keydown",event=>{
      if(event.key==="ArrowDown"||event.key==="ArrowRight"){
        event.preventDefault();
        select(i+1,true);
      }else if(event.key==="ArrowUp"||event.key==="ArrowLeft"){
        event.preventDefault();
        select(i-1,true);
      }else if(event.key==="Home"){
        event.preventDefault();
        select(0,true);
      }else if(event.key==="End"){
        event.preventDefault();
        select(reports.length-1,true);
      }
    });
  });
  select(0);
})();