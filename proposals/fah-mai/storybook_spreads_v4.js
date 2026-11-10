(function () {
  "use strict";

  const viewport = document.querySelector(".viewport");
  const sheets = viewport ? Array.from(viewport.querySelectorAll(".sheet")) : [];
  const rail = document.querySelector(".fm-zoom");
  const zoomRange = document.querySelector(".fm-zoom-range");
  const zoomOut = document.querySelector(".fm-zoom-minus");
  const zoomIn = document.querySelector(".fm-zoom-plus");
  const zoomLabel = document.querySelector(".fm-zoom-readout");
  const previous = document.querySelector(".fm-story-prev");
  const next = document.querySelector(".fm-story-next");
  const counter = document.querySelector(".fm-story-counter");
  const tabs = Array.from(document.querySelectorAll(".proposal-sections [data-target]"));
  const proposal = document.getElementById("nav-proposal");
  const examples = document.getElementById("tab-examples");
  const toolbar = document.querySelector(".toolbar");
  if (!viewport || !sheets.length || !rail || !zoomRange || !counter || !previous || !next) return;

  const mobile = () => window.innerWidth <= 800;
  const spreadThreshold = 0.85;
  const zoomKeys = { desktop: "fahmai_story_v3_desktop_zoom", mobile: "fahmai_story_v3_mobile_zoom" };
  const clamp = x => Math.min(2.5, Math.max(0.5, Math.round(Number(x) * 20) / 20));
  const storedZoom = isMobile => {
    const fallback = isMobile ? 1 : spreadThreshold;
    try {
      const stored = sessionStorage.getItem(isMobile ? zoomKeys.mobile : zoomKeys.desktop);
      const value = stored === null ? fallback : Number(stored);
      return Number.isFinite(value) && value >= 0.5 ? clamp(value) : fallback;
    } catch (_) { return fallback; }
  };
  let zoomFactor = storedZoom(mobile());
  let pageIndex = 0;
  let lastMobile = mobile();
  let previousMode = "";
  let programmaticScrollUntil = 0;
  let scrollQueued = false;

  const mode = () => mobile() ? "vertical" : zoomFactor > spreadThreshold + 0.001 ? "vertical" : "spread";
  // Group pages by actual reading units rather than an odd/even index rule.
  // The cover stands alone, interior pages form spreads, and Examples always
  // displays its own two pages together. Proposed must not borrow page 1 of Examples.
  const spreadGroups = (() => {
    const groups = [];
    let i = 0;
    while (i < sheets.length) {
      if (i === 0) {
        groups.push([0]);
        i += 1;
      } else if (sheets[i].id === "examples" && sheets[i + 1]?.id === "examples-client") {
        groups.push([i, i + 1]);
        i += 2;
      } else if (sheets[i + 1]?.id === "examples") {
        groups.push([i]);
        i += 1;
      } else {
        const group = [i];
        if (i + 1 < sheets.length && sheets[i + 1].id !== "examples-client") group.push(++i);
        groups.push(group);
        i += 1;
      }
    }
    return groups;
  })();
  const groupAt = page => spreadGroups.find(group => group.includes(page)) || [0];
  const spreadStart = page => groupAt(page)[0];
  const maxSpread = spreadGroups.at(-1)?.[0] ?? 0;
  const pageGroup = sheet => sheet.dataset.proposalSection ||
      (sheet.id === "examples-client" ? "examples" : sheet.id);

  function updateCounter() {
    const isSpread = mode() === "spread";
    if (isSpread) pageIndex = spreadStart(pageIndex);
    pageIndex = Math.min(sheets.length - 1, Math.max(0, pageIndex));
    const last = isSpread ? groupAt(pageIndex).at(-1) + 1 : pageIndex + 1;
    const first = pageIndex + 1;
    counter.textContent = isSpread && last !== first ? first + "–" + last + " / " + sheets.length : first + " / " + sheets.length;
    counter.title = last !== first ? "Pages " + first + "–" + last + " of " + sheets.length : "Page " + first + " of " + sheets.length;
    previous.disabled = pageIndex === 0;
    next.disabled = isSpread ? pageIndex >= maxSpread : pageIndex >= sheets.length - 1;
    zoomRange.setAttribute("aria-valuetext", zoomFactor.toFixed(2) + " times");
    zoomRange.value = String(zoomFactor);
    zoomLabel.textContent = Number(zoomFactor.toFixed(2)).toLocaleString("en-US", { maximumFractionDigits: 2 }) + "×";
  }

  function layout({ resetHorizontal = true } = {}) {
    const readingMode = mode();
    const previousReadingMode = previousMode;
    previousMode = readingMode;
    viewport.dataset.readingMode = readingMode;
    document.documentElement.dataset.storyMode = readingMode;
    const isSpread = readingMode === "spread";
    if (isSpread) pageIndex = spreadStart(pageIndex);
    sheets.forEach((sheet, i) => {
      const show = !isSpread || groupAt(pageIndex).includes(i);
      sheet.classList.toggle("is-active", show);
      sheet.setAttribute("aria-hidden", String(!show));
    });
    updateCounter();
    const documentWidth = 794; // A4 CSS width
    const pageCount = isSpread ? groupAt(pageIndex).length : 1;
    const available = viewport.clientWidth - (mobile() ? 18 : 32) - (isSpread && pageCount === 2 ? 16 : 0);
    const fit = Math.min(1, Math.max(0.16, available / (documentWidth * pageCount)));
    const size = fit * zoomFactor;
    sheets.forEach(sheet => sheet.style.setProperty("zoom", String(size), "important"));

    if (resetHorizontal) requestAnimationFrame(() => {
      const scrollLimit = Math.max(0, viewport.scrollWidth - viewport.clientWidth);
      viewport.scrollLeft = scrollLimit / 2;
    });

    if (previousReadingMode && previousReadingMode !== readingMode) {
      requestAnimationFrame(() => {
        if (readingMode === "vertical") jumpTo(pageIndex, false);
        else window.scrollTo({ top: 0, behavior: "auto" });
      });
    }
  }

  function jumpTo(i, animate = true) {
    if (i < 0 || i >= sheets.length) return;
    const el = sheets[i];
    const header = toolbar?.getBoundingClientRect().height || 0;
    const top = window.scrollY + el.getBoundingClientRect().top - header - 11;
    programmaticScrollUntil = Date.now() + (animate ? 700 : 200);
    window.scrollTo({ top: Math.max(0, top), behavior: animate ? "smooth" : "auto" });
  }

  function selectPage(i, { syncTabs = true, smooth = true } = {}) {
    if (i < 0 || i >= sheets.length) return;
    const group = pageGroup(sheets[i]);
    if (syncTabs) {
      if (group === "examples") {
        if (examples && examples.getAttribute("aria-pressed") !== "true") examples.click();
      } else {
        const selected = tabs.find(t => t.getAttribute("aria-selected") === "true");
        if (!selected || selected.dataset.target !== group || proposal?.getAttribute("aria-pressed") !== "true") {
          tabs.find(t => t.dataset.target === group)?.click();
        }
      }
    }
    pageIndex = i;
    layout();
    if (mode() === "vertical") requestAnimationFrame(() => jumpTo(i, smooth));
    else window.scrollTo({ top: 0, behavior: smooth ? "smooth" : "auto" });
  }

  function scrollActivePage() {
    if (mode() !== "vertical" || Date.now() < programmaticScrollUntil) return;
    const offset = (toolbar?.getBoundingClientRect().height || 0) + Math.min(110, window.innerHeight * 0.19);
    let current = 0;
    for (let i = 0; i < sheets.length; i++) {
      if (sheets[i].getBoundingClientRect().top <= offset) current = i;
      else break;
    }
    if (current !== pageIndex) { pageIndex = current; updateCounter(); }
  }

  window.addEventListener("scroll", () => {
    if (scrollQueued) return;
    scrollQueued = true;
    requestAnimationFrame(() => { scrollQueued = false; scrollActivePage(); });
  }, { passive: true });

  function updateZoom(v) {
    const was = mode();
    zoomFactor = clamp(v);
    try { sessionStorage.setItem(mobile() ? zoomKeys.mobile : zoomKeys.desktop, String(zoomFactor)); } catch (_) {}
    layout();
    if (was !== mode() && mode() === "vertical") requestAnimationFrame(() => jumpTo(pageIndex, false));
  }
  zoomRange.min = "0.5";
  zoomRange.max = "2.5";
  zoomRange.step = "0.05";
  zoomRange.addEventListener("input", () => updateZoom(zoomRange.value));
  zoomOut?.addEventListener("click", () => updateZoom(zoomFactor - 0.25));
  zoomIn?.addEventListener("click", () => updateZoom(zoomFactor + 0.25));

  previous.addEventListener("click", () => {
    const current = spreadGroups.findIndex(group => group[0] === spreadStart(pageIndex));
    const target = mode() === "spread" ? spreadGroups[Math.max(0, current - 1)][0] : pageIndex - 1;
    selectPage(target);
  });
  next.addEventListener("click", () => {
    const current = spreadGroups.findIndex(group => group[0] === spreadStart(pageIndex));
    const target = mode() === "spread" ? spreadGroups[Math.min(spreadGroups.length - 1, current + 1)][0] : pageIndex + 1;
    selectPage(target);
  });

  // The legacy proposal tab controller changes state first, then this controller
  // restores the correct continuous reader/spread and moves to that section.
  tabs.forEach(tab => tab.addEventListener("click", () => {
    const position = sheets.findIndex(sheet => sheet.id === tab.dataset.target);
    if (position !== -1) {
      pageIndex = position;
      layout();
      if (mode() === "vertical") requestAnimationFrame(() => jumpTo(position));
      else window.scrollTo({ top: 0, behavior: "smooth" });
    }
    if (mobile()) tab.scrollIntoView({ block: "nearest", inline: "center", behavior: "smooth" });
  }));

  proposal?.addEventListener("click", () => {
    const selected = tabs.find(tab => tab.getAttribute("aria-selected") === "true");
    const id = selected?.dataset.target || "overview";
    pageIndex = Math.max(0, sheets.findIndex(sheet => sheet.id === id));
    layout();
    if (mode() === "vertical") requestAnimationFrame(() => jumpTo(pageIndex));
    else window.scrollTo({ top: 0, behavior: "smooth" });
  });
  examples?.addEventListener("click", () => {
    pageIndex = Math.max(0, sheets.findIndex(sheet => sheet.id === "examples"));
    layout();
    if (mode() === "vertical") requestAnimationFrame(() => jumpTo(pageIndex));
    else window.scrollTo({ top: 0, behavior: "smooth" });
  });

  // Pinch zoom remains in the same unobtrusive floating control on mobile.
  let pinch = null;
  viewport.addEventListener("touchstart", e => {
    if (e.touches.length === 2) {
      pinch = {
        distance: Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY),
        scale: zoomFactor
      };
    }
  }, { passive: true });
  viewport.addEventListener("touchmove", e => {
    if (pinch && e.touches.length === 2) {
      const distance = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
      updateZoom(pinch.scale * distance / Math.max(1, pinch.distance));
    }
  }, { passive: true });
  viewport.addEventListener("touchend", e => { if (e.touches.length < 2) pinch = null; }, { passive: true });

  document.addEventListener("keydown", e => {
    if (e.defaultPrevented || e.altKey === false || /INPUT|TEXTAREA|SELECT/.test(e.target?.tagName || "") || e.target?.isContentEditable) return;
    if (e.key === "ArrowRight") { e.preventDefault(); next.click(); }
    if (e.key === "ArrowLeft") { e.preventDefault(); previous.click(); }
  });
  window.addEventListener("resize", () => {
    if (mobile() !== lastMobile) {
      lastMobile = mobile();
      zoomFactor = storedZoom(lastMobile);
    }
    layout();
  }, { passive: true });
  window.addEventListener("beforeprint", () => sheets.forEach(sheet => sheet.style.removeProperty("zoom")));
  window.addEventListener("afterprint", () => layout());

  const hash = location.hash.replace("#", "");
  const match = sheets.findIndex(sheet => sheet.id === hash);
  pageIndex = Math.max(0, match);
  layout();
  if (mode() === "vertical" && pageIndex > 0) requestAnimationFrame(() => jumpTo(pageIndex, false));
})();