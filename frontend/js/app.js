// js/app.js

// ---- Global API (must be first!) ----
window.API = "http://127.0.0.1:8000";

// ---- Global state (must exist before other scripts run) ----
window.currentDocId = null;
window.pdfDoc = null;
window.currentPageNumber = 1;
window.totalPages = 1;
window.pdfScale = 1.5;

// Canvas + contexts (global so other modules can use them)
window.canvas = null;
window.ctx = null;
window.offscreenCanvas = null;
window.offscreenCtx = null;

window.addEventListener("DOMContentLoaded", () => {

  // Initialize canvas references AFTER DOM loads
  window.canvas = document.getElementById('pdfCanvas');
  window.ctx = window.canvas.getContext('2d');

  window.offscreenCanvas = document.createElement('canvas');
  window.offscreenCtx = window.offscreenCanvas.getContext('2d');

  // ---- Helpers ----
  window.updatePageInfo = function () {
    const el = document.getElementById("pageInfo");
    if (!el) return;
    el.innerText = `Page ${window.currentPageNumber} of ${window.totalPages}`;
  };

  // ---- Event wiring ----

  document.getElementById("uploadBtn").addEventListener("click", upload);
  document.getElementById("askBtn").addEventListener("click", ask);
  document.getElementById("redactTextBtn").addEventListener("click", redactText);
  document.getElementById("applySuggestionsBtn").addEventListener("click", applySelectedSuggestions);
  document.getElementById("saveTagsBtn").addEventListener("click", saveManualTags);
  document.getElementById("outputInfoBtn").addEventListener("click", sendOutputInfo);

  document.getElementById("prevPageBtn").addEventListener("click", async () => {
    await prevPage();
    if (typeof drawHighlightsForCurrentPage === "function") {
      drawHighlightsForCurrentPage();
    }
  });

  document.getElementById("nextPageBtn").addEventListener("click", async () => {
    await nextPage();
    if (typeof drawHighlightsForCurrentPage === "function") {
      drawHighlightsForCurrentPage();
    }
  });

  // ---- PDF.js worker setup ----
  if (window['pdfjsLib']) {
    pdfjsLib.GlobalWorkerOptions.workerSrc = "libs/pdf.worker.js";
  }

}); // END DOMContentLoaded
