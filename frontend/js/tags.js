// js/tags.js

// ---- Load tags (auto + manual) from backend ----
async function loadTagsFromServer() {
  if (!window.currentDocId) return;

  const div = document.getElementById("tagsDisplay");
  div.innerHTML = "";

  try {
    loading.show("Loading tags…");

    const res = await fetch(`${window.API}/tags/get`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        doc_id: window.currentDocId,
        tag: ""   // backend requires tag field in TagRequest
      })
    });

    if (!res.ok) throw new Error("Failed to load tags");

    const data = await res.json();

    const auto = data.auto || [];
    const manual = data.manual || [];

    // Auto tags
    const autoTitle = document.createElement("div");
    autoTitle.innerHTML = "<strong>Auto tags:</strong> ";
    div.appendChild(autoTitle);

    auto.forEach(tag => {
      const chip = document.createElement("span");
      chip.className = "tag-chip";
      chip.innerText = tag;
      chip.onclick = () => toggleTag(tag);
      div.appendChild(chip);
    });

    // Manual tags
    const manualTitle = document.createElement("div");
    manualTitle.innerHTML = "<br><strong>Manual tags:</strong> ";
    div.appendChild(manualTitle);

    manual.forEach(tag => {
      const chip = document.createElement("span");
      chip.className = "tag-chip manual";
      chip.innerText = tag;
      chip.onclick = () => toggleTag(tag);
      div.appendChild(chip);
    });

  } catch (err) {
    console.error(err);
    div.innerText = "Error loading tags.";
    toast.error("Failed to load tags");
  } finally {
    loading.hide();
  }
}

// ---- Save manual tags ----
async function saveManualTags() {
  if (!window.currentDocId) {
    toast.error("Upload a document first");
    return;
  }

  const manual = document.getElementById("manualTagsInput").value.trim();
  if (!manual) return;

  try {
    loading.show("Saving tags…");

    await fetch(`${window.API}/tags/add`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        doc_id: window.currentDocId,
        tag: manual
      })
    });

    await loadTagsFromServer();
    toast.success("Tag added");

  } catch (err) {
    console.error(err);
    toast.error("Failed to save manual tags");
  } finally {
    loading.hide();
  }
}

// ---- Toggle a tag (auto or manual) ----
async function toggleTag(tag) {
  if (!window.currentDocId) return;

  try {
    loading.show("Updating tag…");

    await fetch(`${window.API}/tags/remove`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        doc_id: window.currentDocId,
        tag: tag
      })
    });

    await loadTagsFromServer();
    toast.success("Tag removed");

  } catch (err) {
    console.error(err);
    toast.error("Failed to toggle tag");
  } finally {
    loading.hide();
  }
}
