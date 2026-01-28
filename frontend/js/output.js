// js/output.js

// ===============================================================
// === PHASE 2 — TOAST NOTIFICATIONS — 2026‑01‑17 =================
// ===============================================================

async function confirmOutputSettings() {
  if (!window.currentDocId) {
    toast.error("Upload a document first");
    return;
  }

  const filename = document.getElementById("outputFileInput").value.trim();
  const saveToOutput = document.getElementById("saveToOutputCheckbox").checked;
  const statusEl = document.getElementById("outputInfoStatus");

  if (!filename) {
    toast.error("Enter an output filename");
    return;
  }

  try {
    loading.show("Saving output settings…");

    const res = await fetch(`${window.API}/output_settings`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        doc_id: window.currentDocId,
        output_filename: filename,
        save_to_output: saveToOutput
      })
    });

    if (!res.ok) throw new Error("Failed to save output settings");

    const data = await res.json();

    if (data.success) {
      toast.success("Output settings saved");
      statusEl.innerText =
        `Output: ${filename} (${saveToOutput ? "saved to /output" : "download only"})`;
    } else {
      toast.error("Failed to save output settings");
      statusEl.innerText = "Error: " + JSON.stringify(data);
    }

  } catch (err) {
    console.error(err);
    toast.error("Failed to save output settings — server error");
    statusEl.innerText = "Server error.";
  } finally {
    loading.hide();
  }
}

// ⭐ Make it globally accessible for app.js
window.sendOutputInfo = confirmOutputSettings;
