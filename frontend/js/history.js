// js/history.js

// ===============================================================
// === HISTORY PANEL INTEGRATION — 2026‑01‑17 =====================
// ===============================================================


// ---------------------------------------------------------------
// Fetch version history from backend
// ---------------------------------------------------------------
async function fetchVersions(docId) {
  const res = await fetch(`${window.API}/history/versions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ doc_id: docId })
  });

  if (!res.ok) {
    console.error("Failed to fetch versions");
    return { versions: [], count: 0 };
  }

  return res.json();
}


// ---------------------------------------------------------------
// Fetch audit log from backend
// ---------------------------------------------------------------
async function fetchAuditLog(docId) {
  const res = await fetch(`${window.API}/history/audit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ doc_id: docId })
  });

  if (!res.ok) {
    console.error("Failed to fetch audit log");
    return { entries: [], count: 0 };
  }

  return res.json();
}


// ---------------------------------------------------------------
// Render version history list
// ---------------------------------------------------------------
async function loadVersionHistory(docId) {
  const data = await fetchVersions(docId);
  const listEl = document.getElementById("versionList");
  listEl.innerHTML = "";

  if (!data.versions || data.versions.length === 0) {
    const li = document.createElement("li");
    li.textContent = "No versions yet";
    listEl.appendChild(li);
    return;
  }

  data.versions.forEach((versionPath, index) => {
    const li = document.createElement("li");
    li.textContent = `Version ${index + 1}`;

    const btn = document.createElement("button");
    btn.textContent = "Revert";
    btn.style.marginLeft = "10px";
    btn.onclick = () => revertToVersion(docId, versionPath);

    li.appendChild(btn);
    listEl.appendChild(li);
  });
}


// ---------------------------------------------------------------
// Render audit log list
// ---------------------------------------------------------------
async function loadAuditLog(docId) {
  const data = await fetchAuditLog(docId);
  const listEl = document.getElementById("auditList");
  listEl.innerHTML = "";

  if (!data.entries || data.entries.length === 0) {
    const li = document.createElement("li");
    li.textContent = "No audit entries yet";
    listEl.appendChild(li);
    return;
  }

  data.entries.forEach((entry) => {
    const li = document.createElement("li");

    const ts = entry.timestamp || entry.time || "";
    const action = entry.action || entry.type || "action";

    li.textContent = `[${ts}] ${action}`;
    listEl.appendChild(li);
  });
}


// ---------------------------------------------------------------
// Revert to a specific version
// ---------------------------------------------------------------
async function revertToVersion(docId, versionPath) {
  const res = await fetch(`${window.API}/history/revert`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ doc_id: docId, version_path: versionPath })
  });

  if (!res.ok) {
    toast.error("Failed to revert");
    return;
  }

  toast.success("Reverted to selected version");

  await window.loadPdf(docId);
  await window.loadVersionHistory(docId);
  await window.loadAuditLog(docId);
}


// ---------------------------------------------------------------
// Undo last redaction
// ---------------------------------------------------------------
async function undoLastRedaction(docId) {
  const res = await fetch(`${window.API}/history/undo_last`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ doc_id: docId })
  });

  if (!res.ok) {
    toast.error("Nothing to undo");
    return;
  }

  toast.success("Undo successful");

  await window.loadPdf(docId);
  await window.loadVersionHistory(docId);
  await window.loadAuditLog(docId);
}


// ---------------------------------------------------------------
// UI Wiring: panel toggle, tabs, undo button
// ---------------------------------------------------------------
window.addEventListener("DOMContentLoaded", () => {

  const historyPanel = document.getElementById("historyPanel");
  const toggleBtn = document.getElementById("toggleHistoryBtn");
  const undoBtn = document.getElementById("undoBtn");

  const tabs = document.querySelectorAll(".history-tab");
  const sections = {
    versions: document.getElementById("historyVersions"),
    audit: document.getElementById("historyAudit"),
  };


  // Panel toggle
  if (toggleBtn && historyPanel) {
    toggleBtn.addEventListener("click", () => {
      historyPanel.classList.toggle("open");
    });
  }

  // Undo button
  if (undoBtn) {
    undoBtn.addEventListener("click", async () => {
      if (!window.currentDocId) {
        toast.error("Upload a document first");
        return;
      }
      await undoLastRedaction(window.currentDocId);
    });
  }

  // Tab switching
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {

      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");

      const tabName = tab.dataset.tab;

      Object.keys(sections).forEach(name => {
        sections[name].classList.toggle("active", name === tabName);
      });
    });
  });

});
