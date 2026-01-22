// js/redact-area.js

window.addEventListener("DOMContentLoaded", () => {
  const canvas = window.canvas;
  const ctx = window.ctx;

  if (!canvas) {
    console.error("Canvas not ready yet");
    return;
  }

  let isDrawing = false;
  let startX, startY, endX, endY;

  // ---- Mouse down: start drawing ----
  canvas.addEventListener("mousedown", (e) => {
    if (!window.pdfDoc) return;

    isDrawing = true;

    const rect = canvas.getBoundingClientRect();
    startX = e.clientX - rect.left;
    startY = e.clientY - rect.top;
  });

  // ---- Mouse move: draw rectangle preview ----
  canvas.addEventListener("mousemove", (e) => {
    if (!isDrawing || !window.pdfDoc) return;

    const rect = canvas.getBoundingClientRect();
    endX = e.clientX - rect.left;
    endY = e.clientY - rect.top;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(window.offscreenCanvas, 0, 0);

    ctx.strokeStyle = "red";
    ctx.lineWidth = 2;
    ctx.strokeRect(startX, startY, endX - startX, endY - startY);
  });

  // ---- Mouse up: finalize redaction ----
  canvas.addEventListener("mouseup", async (e) => {
    if (!isDrawing || !window.pdfDoc) return;

    isDrawing = false;

    const rect = canvas.getBoundingClientRect();
    endX = e.clientX - rect.left;
    endY = e.clientY - rect.top;

    // Normalize to 0–1 coordinates
    const x1 = Math.min(startX, endX) / canvas.width;
    const y1 = Math.min(startY, endY) / canvas.height;
    const x2 = Math.max(startX, endX) / canvas.width;
    const y2 = Math.max(startY, endY) / canvas.height;

    await sendRedactionBox(x1, y1, x2, y2);
  });
});

// ---- Send redaction box to backend ----
async function sendRedactionBox(nx1, ny1, nx2, ny2) {
  if (!window.currentDocId) {
    toast.error("Upload a document first");
    return;
  }

  const statusEl = document.getElementById("areaRedactStatus");

  // Convert normalized coords → PDF coords
  const x = nx1;
  const y = ny1;
  const w = nx2 - nx1;
  const h = ny2 - ny1;

  const payload = {
    doc_id: window.currentDocId,
    page: window.currentPageNumber,
    x,
    y,
    w,
    h
  };

  try {
    const res = await fetch(`${window.API}/redact/box`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error("Area redaction failed");

    const data = await res.json();

    toast.success("Area redacted");

    statusEl.innerText = "Area redaction applied.";

    // Refresh UI
    await window.loadPdf(window.currentDocId);
    await window.loadVersionHistory(window.currentDocId);
    await window.loadAuditLog(window.currentDocId);

  } catch (err) {
    console.error(err);
    toast.error("Area redaction failed — server error");
    statusEl.innerText = "Area redaction failed. Server error.";
  }
}
// js/redact-area.js

window.addEventListener("DOMContentLoaded", () => {
  const canvas = window.canvas;
  const ctx = window.ctx;

  if (!canvas) {
    console.error("Canvas not ready yet");
    return;
  }

  let isDrawing = false;
  let startX, startY, endX, endY;

  // ---- Mouse down: start drawing ----
  canvas.addEventListener("mousedown", (e) => {
    if (!window.pdfDoc) return;

    isDrawing = true;

    const rect = canvas.getBoundingClientRect();
    startX = e.clientX - rect.left;
    startY = e.clientY - rect.top;
  });

  // ---- Mouse move: draw rectangle preview ----
  canvas.addEventListener("mousemove", (e) => {
    if (!isDrawing || !window.pdfDoc) return;

    const rect = canvas.getBoundingClientRect();
    endX = e.clientX - rect.left;
    endY = e.clientY - rect.top;

    // redraw page from offscreen, then overlay preview box
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(window.offscreenCanvas, 0, 0);

    ctx.strokeStyle = "red";
    ctx.lineWidth = 2;
    ctx.strokeRect(startX, startY, endX - startX, endY - startY);
  });

  // ---- Mouse up: finalize redaction ----
  canvas.addEventListener("mouseup", async (e) => {
    if (!isDrawing || !window.pdfDoc) return;

    isDrawing = false;

    const rect = canvas.getBoundingClientRect();
    endX = e.clientX - rect.left;
    endY = e.clientY - rect.top;

    // Normalize to 0–1 coordinates
    const x1 = Math.min(startX, endX) / canvas.width;
    const y1 = Math.min(startY, endY) / canvas.height;
    const x2 = Math.max(startX, endX) / canvas.width;
    const y2 = Math.max(startY, endY) / canvas.height;

    await sendRedactionBox(x1, y1, x2, y2);
  });
});

// ---- Send redaction box to backend ----
async function sendRedactionBox(nx1, ny1, nx2, ny2) {
  if (!window.currentDocId) {
    toast.error("Upload a document first");
    return;
  }

  const statusEl = document.getElementById("areaRedactStatus");

  const x = nx1;
  const y = ny1;
  const w = nx2 - nx1;
  const h = ny2 - ny1;

  const payload = {
    doc_id: window.currentDocId,
    page: window.currentPageNumber,
    x,
    y,
    w,
    h
  };

  try {
    loading.show("Applying area redaction…");

    const res = await fetch(`${window.API}/redact/box`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error("Area redaction failed");

    await res.json();

    toast.success("Area redaction applied.");
    statusEl.innerText = "Area redaction applied.";

    // Reload PDF to show the black box
    await window.loadPdf(window.currentDocId);

    if (window.loadVersionHistory) {
      await window.loadVersionHistory(window.currentDocId);
    }
    if (window.loadAuditLog) {
      await window.loadAuditLog(window.currentDocId);
    }

  } catch (err) {
    console.error(err);
    toast.error("Area redaction failed — server error");
    statusEl.innerText = "Area redaction failed. Server error.";
  } finally {
    loading.hide();
  }
}
