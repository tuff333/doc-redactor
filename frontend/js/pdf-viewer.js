// js/pdf-viewer.js
// ===============================================================
// PDF Viewer with:
// - Canvas rendering
// - Highlight overlay layer
// - Jump-to-page
// - Scroll-to-highlight
// - Redraw highlights on page change
// ===============================================================

// Global highlight registry:
// highlightRects[pageNumber] = [ { x, y, w, h, color } ]
window.highlightRects = {};

window.pdfScale = 1.5;

// ---- Load PDF from backend ----
async function loadPdf(docId) {
  try {
    const url = `${window.API}/view/${docId}`;
    window.pdfDoc = await pdfjsLib.getDocument({ url }).promise;

    window.totalPages = window.pdfDoc.numPages;
    window.currentPageNumber = 1;

    await renderPage(window.currentPageNumber);
    window.updatePageInfo();

    drawHighlightsForCurrentPage();

  } catch (err) {
    console.error("Error loading PDF:", err);
    document.getElementById("uploadStatus").innerText = "Error loading PDF.";
  }
}

// ---- Render a single page ----
async function renderPage(pageNumber) {
  if (!window.pdfDoc) return;

  const page = await window.pdfDoc.getPage(pageNumber);
  const viewport = page.getViewport({ scale: window.pdfScale });

  // Reset transforms before resizing/drawing
  window.ctx.setTransform(1, 0, 0, 1, 0, 0);
  window.offscreenCtx.setTransform(1, 0, 0, 1, 0, 0);

  // Resize canvases
  window.canvas.width = viewport.width;
  window.canvas.height = viewport.height;

  window.offscreenCanvas.width = viewport.width;
  window.offscreenCanvas.height = viewport.height;

  const renderContext = {
    canvasContext: window.offscreenCtx,
    viewport: viewport,
  };

  // Clear offscreen and render page
  window.offscreenCtx.clearRect(0, 0, viewport.width, viewport.height);
  await page.render(renderContext).promise;

  // Clear visible canvas and draw from offscreen
  window.ctx.clearRect(0, 0, viewport.width, viewport.height);
  window.ctx.drawImage(window.offscreenCanvas, 0, 0);

  // Ensure overlay exists
  ensureOverlayLayer(viewport.width, viewport.height);

  // Redraw highlights
  drawHighlightsForCurrentPage();
}

// ---- Ensure overlay layer exists ----
function ensureOverlayLayer(width, height) {
  let overlay = document.getElementById("pdfOverlay");
  if (!overlay) {
    overlay = document.createElement("div");
    overlay.id = "pdfOverlay";
    overlay.style.position = "absolute";
    overlay.style.left = "0";
    overlay.style.top = "0";
    overlay.style.pointerEvents = "none";
    overlay.style.zIndex = "50";
    window.canvas.parentElement.appendChild(overlay);
  }

  overlay.style.width = width + "px";
  overlay.style.height = height + "px";
}

// ---- Draw highlights for current page ----
function drawHighlightsForCurrentPage() {
  const page = window.currentPageNumber;
  const overlay = document.getElementById("pdfOverlay");
  if (!overlay) return;

  overlay.innerHTML = "";

  const rects = window.highlightRects[page] || [];
  rects.forEach(r => {
    const div = document.createElement("div");
    div.style.position = "absolute";
    div.style.left = r.x + "px";
    div.style.top = r.y + "px";
    div.style.width = r.w + "px";
    div.style.height = r.h + "px";
    div.style.background = r.color || "rgba(255, 230, 0, 0.5)";
    div.style.border = "2px solid orange";
    div.style.borderRadius = "3px";
    overlay.appendChild(div);
  });
}

// ---- Add a highlight rectangle ----
window.addPdfHighlight = function (page, x, y, w, h, color = "rgba(255, 230, 0, 0.5)") {
  if (!window.highlightRects[page]) {
    window.highlightRects[page] = [];
  }
  window.highlightRects[page].push({ x, y, w, h, color });

  if (page === window.currentPageNumber) {
    drawHighlightsForCurrentPage();
  }
};

// ---- Clear all highlights ----
window.clearPdfHighlights = function () {
  window.highlightRects = {};
  drawHighlightsForCurrentPage();
};

// ---- Jump to a specific page ----
window.jumpToPage = async function (pageNumber) {
  if (!window.pdfDoc) return;
  if (pageNumber < 1 || pageNumber > window.totalPages) return;

  window.currentPageNumber = pageNumber;
  await renderPage(pageNumber);
  window.updatePageInfo();
};

// ---- Scroll to a highlight ----
window.scrollToHighlight = async function (page, rect) {
  await window.jumpToPage(page);

  setTimeout(() => {
    const overlay = document.getElementById("pdfOverlay");
    if (!overlay) return;

    overlay.scrollIntoView({
      behavior: "smooth",
      block: "center"
    });
  }, 150);
};

// ---- Page navigation ----
async function nextPage() {
  if (!window.pdfDoc) return;
  if (window.currentPageNumber < window.totalPages) {
    window.currentPageNumber++;
    await renderPage(window.currentPageNumber);
    window.updatePageInfo();
  }
}

async function prevPage() {
  if (!window.pdfDoc) return;
  if (window.currentPageNumber > 1) {
    window.currentPageNumber--;
    await renderPage(window.currentPageNumber);
    window.updatePageInfo();
  }
}

// Expose functions globally
window.loadPdf = loadPdf;
window.renderPage = renderPage;
window.nextPage = nextPage;
window.prevPage = prevPage;
window.drawHighlightsForCurrentPage = drawHighlightsForCurrentPage;
