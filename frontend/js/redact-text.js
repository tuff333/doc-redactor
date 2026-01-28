// js/redact-text.js

// ===============================================================
// Manual text redaction (simple search + blackout)
// Updated to call POST /redact/text with JSON
// ===============================================================

async function redactText() {
  if (!window.currentDocId) {
    toast.error("Upload a document first");
    return;
  }

  const text = document.getElementById("redactTextInput").value.trim();
  const statusEl = document.getElementById("redactTextStatus");

  if (!text) {
    toast.error("Enter text to redact");
    return;
  }

  try {
    loading.show("Redacting text…");

    // Backend now expects JSON with doc_id + target_text
    const res = await fetch(`${window.API}/redact/text`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        doc_id: window.currentDocId,
        target_text: text
      })
    });

    if (!res.ok) throw new Error("Redaction failed");

    const data = await res.json();

    // We don’t rely on output_file anymore; we just reload the PDF
    toast.success(`Redaction applied`);

    statusEl.innerText = "Redaction applied successfully.";

    // Reload PDF to show updated redactions
    await window.loadPdf(window.currentDocId);

    // === HISTORY PANEL INTEGRATION ===
    if (window.loadVersionHistory) {
      await window.loadVersionHistory(window.currentDocId);
    }
    if (window.loadAuditLog) {
      await window.loadAuditLog(window.currentDocId);
    }

  } catch (err) {
    console.error(err);
    toast.error("Redaction failed — server error");
    statusEl.innerText = "Redaction failed. Server error.";
  } finally {
    loading.hide();
  }
}

window.redactText = redactText;
