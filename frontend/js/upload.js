// js/upload.js

// ===============================================================
// === PHASE 2 — UPLOAD ENGINE — 2026‑01‑17 =======================
// Replaced:
// - alert() → toast.error()
// - status text → toast.success() / toast.error()
// - Added loading overlay
// - Made upload() global (window.upload)
// ===============================================================

window.upload = async function upload() {
  const fileInput = document.getElementById("fileInput");
  const statusEl = document.getElementById("uploadStatus");

  if (!fileInput.files || fileInput.files.length === 0) {
    toast.error("Select a PDF to upload");
    return;
  }

  const file = fileInput.files[0];

  const formData = new FormData();
  formData.append("file", file);

  try {
    loading.show("Uploading PDF…");

    const res = await fetch(`${window.API}/upload`, {
      method: "POST",
      body: formData
    });

    if (!res.ok) throw new Error("Upload failed");

    const data = await res.json();

    if (!data.doc_id) {
      toast.error("Upload failed: invalid server response");
      statusEl.innerText = "Upload failed.";
      return;
    }

    // Save doc ID globally
    window.currentDocId = data.doc_id;

    toast.success("PDF uploaded successfully");
    statusEl.innerText = `Uploaded: ${file.name}`;

    // Load PDF into viewer
    await window.loadPdf(window.currentDocId);

    // Load tags
    if (typeof loadTagsFromServer === "function") {
      await loadTagsFromServer();
    }

    // Load suggestions
    if (typeof loadSuggestions === "function") {
      await loadSuggestions();
    }

    // Load history + audit
    if (typeof window.loadVersionHistory === "function") {
      await window.loadVersionHistory(window.currentDocId);
    }
    if (typeof window.loadAuditLog === "function") {
      await window.loadAuditLog(window.currentDocId);
    }

  } catch (err) {
    console.error(err);
    toast.error("Upload failed — server error");
    statusEl.innerText = "Upload failed. Server error.";
  } finally {
    loading.hide();
  }
};
