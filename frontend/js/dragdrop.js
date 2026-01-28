// js/dragdrop.js

// ======================================================================
// === PHASE 2 — DRAG & DROP UPLOAD — 2026‑01‑17 =========================
// This module adds:
// - Sidebar drop zone (Option B)
// - Full‑screen overlay (Option C)
// - Drag enter / leave detection
// - Auto‑upload on drop
// - Smooth, professional UX
//
// It integrates with your existing upload.js logic by:
// - Setting fileInput.files programmatically
// - Calling upload() automatically
//
// No existing files are modified here — this module is fully standalone.
// ======================================================================


// ---------------------------------------------------------------
// DOM references
// ---------------------------------------------------------------
const dropZone = document.getElementById("dropZone");
const dropOverlay = document.getElementById("dropOverlay");
const fileInput = document.getElementById("fileInput");


// ---------------------------------------------------------------
// Utility: show overlay
// ---------------------------------------------------------------
function showOverlay() {
  dropOverlay.classList.add("show");
}

// Utility: hide overlay
function hideOverlay() {
  dropOverlay.classList.remove("show");
}


// ---------------------------------------------------------------
// Highlight sidebar drop zone
// ---------------------------------------------------------------
function highlightDropZone() {
  dropZone.classList.add("dragover");
}

function unhighlightDropZone() {
  dropZone.classList.remove("dragover");
}


// ---------------------------------------------------------------
// Handle dropped files
// ---------------------------------------------------------------
async function handleDroppedFiles(files) {
  if (!files || files.length === 0) return;

  // Assign dropped file to the hidden file input
  const file = files[0];
  const dataTransfer = new DataTransfer();
  dataTransfer.items.add(file);
  fileInput.files = dataTransfer.files;

  // Trigger existing upload logic
  await upload();
}


// ---------------------------------------------------------------
// Global drag events (for full‑screen overlay)
// ---------------------------------------------------------------
window.addEventListener("dragenter", (e) => {
  e.preventDefault();
  showOverlay();
});

window.addEventListener("dragover", (e) => {
  e.preventDefault();
});

window.addEventListener("dragleave", (e) => {
  // Only hide if leaving the window entirely
  if (e.clientX <= 0 || e.clientY <= 0 ||
      e.clientX >= window.innerWidth || e.clientY >= window.innerHeight) {
    hideOverlay();
  }
});

window.addEventListener("drop", async (e) => {
  e.preventDefault();
  hideOverlay();
  await handleDroppedFiles(e.dataTransfer.files);
});


// ---------------------------------------------------------------
// Sidebar drop zone events
// ---------------------------------------------------------------
dropZone.addEventListener("dragenter", (e) => {
  e.preventDefault();
  highlightDropZone();
});

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  highlightDropZone();
});

dropZone.addEventListener("dragleave", (e) => {
  e.preventDefault();
  unhighlightDropZone();
});

dropZone.addEventListener("drop", async (e) => {
  e.preventDefault();
  unhighlightDropZone();
  hideOverlay();
  await handleDroppedFiles(e.dataTransfer.files);
});


// ---------------------------------------------------------------
// Clicking the drop zone triggers file input
// ---------------------------------------------------------------
dropZone.addEventListener("click", () => {
  fileInput.click();
});