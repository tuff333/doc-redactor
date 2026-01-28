// js/redact-suggestions.js

// ===============================================================
// Smart Suggestions UI
// - Dropdown + multi-select
// - Color-coded labels
// - Keyboard navigation
// - Exact PDF highlight (canvas overlay)
// - Jump to page + scroll to highlight
// - "Redact This" + "Redact Selected"
// ===============================================================

window.suggestions = [];
let currentSuggestionIndex = -1;

// Label → color map
const LABEL_COLORS = {
  EMAIL: "#ff6b6b",
  PHONE: "#4dabf7",
  CREDIT_CARD: "#f59f00",
  SSN: "#e64980",
  DATE: "#51cf66",
  ADDRESS: "#845ef7",
  LICENSE: "#ffa94d",
  PASSPORT: "#fcc419",
  HEALTH_CARD: "#20c997",
  POSTAL_CODE: "#228be6",
  SENSITIVE: "#868e96"
};

function getLabelColor(label) {
  return LABEL_COLORS[label] || LABEL_COLORS.SENSITIVE;
}

// ---------------------------------------------------------------
// Load suggestions from backend
// ---------------------------------------------------------------
async function loadSuggestions(docId) {
  if (!docId) return;

  const container = document.getElementById("suggestionsContainer");
  if (!container) return;

  container.innerHTML = "Loading suggestions…";

  try {
    const res = await fetch(`${window.API}/redact/suggest`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ doc_id: docId })
    });

    if (!res.ok) throw new Error("Failed to load suggestions");

    const data = await res.json();
    window.suggestions = data.suggestions || [];

    renderSuggestionsUI();
  } catch (err) {
    console.error(err);
    container.innerHTML = "Failed to load suggestions.";
  }
}

// ---------------------------------------------------------------
// Render UI: dropdown + multi-select + buttons
// ---------------------------------------------------------------
function renderSuggestionsUI() {
  const container = document.getElementById("suggestionsContainer");
  container.innerHTML = "";

  if (!window.suggestions.length) {
    container.innerText = "No suggestions found.";
    return;
  }

  // === Dropdown (single focus) ===
  const dropdown = document.createElement("select");
  dropdown.id = "suggestionDropdown";
  dropdown.style.width = "100%";
  dropdown.style.marginBottom = "8px";

  const defaultOpt = document.createElement("option");
  defaultOpt.value = "";
  defaultOpt.textContent = "Select a suggestion…";
  dropdown.appendChild(defaultOpt);

  window.suggestions.forEach((s, idx) => {
    const opt = document.createElement("option");
    opt.value = String(idx);
    const pageLabel = s.page ? `P${s.page}` : "?";
    opt.textContent = `[${pageLabel}] [${s.label}] ${s.text}`;
    opt.style.color = getLabelColor(s.label);
    dropdown.appendChild(opt);
  });

  dropdown.addEventListener("change", () => {
    const idx = parseInt(dropdown.value, 10);
    if (!isNaN(idx)) {
      focusSuggestion(idx);
    }
  });

  container.appendChild(dropdown);

  // === Multi-select list ===
  const multi = document.createElement("select");
  multi.id = "suggestionMulti";
  multi.multiple = true;
  multi.size = Math.min(10, window.suggestions.length);
  multi.style.width = "100%";
  multi.style.marginBottom = "8px";

  window.suggestions.forEach((s, idx) => {
    const opt = document.createElement("option");
    opt.value = String(idx);
    const pageLabel = s.page ? `P${s.page}` : "?";
    opt.textContent = `[${pageLabel}] [${s.label}] ${s.text}`;
    opt.style.color = getLabelColor(s.label);
    multi.appendChild(opt);
  });

  multi.addEventListener("change", () => {
    const idx = parseInt(multi.value, 10);
    if (!isNaN(idx)) {
      focusSuggestion(idx);
      dropdown.value = String(idx);
    }
  });

  container.appendChild(multi);

  // === Buttons row ===
  const btnRow = document.createElement("div");
  btnRow.style.display = "flex";
  btnRow.style.gap = "8px";
  btnRow.style.marginTop = "8px";

  const btnRedactThis = document.createElement("button");
  btnRedactThis.innerText = "Redact This";
  btnRedactThis.onclick = async () => {
    const idx = parseInt(dropdown.value, 10);
    if (isNaN(idx)) {
      toast.error("Select a suggestion first");
      return;
    }
    await redactSelectedSpans([window.suggestions[idx]]);
  };

  const btnRedactSelected = document.createElement("button");
  btnRedactSelected.innerText = "Redact Selected";
  btnRedactSelected.onclick = async () => {
    const selected = Array.from(multi.selectedOptions).map(opt =>
      window.suggestions[parseInt(opt.value, 10)]
    );
    if (!selected.length) {
      toast.error("Select one or more suggestions");
      return;
    }
    await redactSelectedSpans(selected);
  };

  btnRow.appendChild(btnRedactThis);
  btnRow.appendChild(btnRedactSelected);
  container.appendChild(btnRow);

  // === Keyboard navigation ===
  setupSuggestionKeyboardNav(dropdown, multi);
}

// ---------------------------------------------------------------
// Focus a suggestion: highlight + jump/scroll
// ---------------------------------------------------------------
function focusSuggestion(index) {
  currentSuggestionIndex = index;
  const s = window.suggestions[index];
  if (!s) return;

  highlightSuggestionOnPdf(s);
}

// ---------------------------------------------------------------
// Highlight on PDF using exact normalized coords
// ---------------------------------------------------------------
function highlightSuggestionOnPdf(suggestion) {
  if (!window.pdfDoc || !window.canvas) return;
  if (!suggestion.page || suggestion.x == null || suggestion.y == null ||
      suggestion.w == null || suggestion.h == null) {
    toast.info("No exact location for this suggestion");
    return;
  }

  const page = suggestion.page;

  // Clear previous highlights
  if (window.clearPdfHighlights) {
    window.clearPdfHighlights();
  }

  const canvas = window.canvas;
  const x = suggestion.x * canvas.width;
  const y = suggestion.y * canvas.height;
  const w = suggestion.w * canvas.width;
  const h = suggestion.h * canvas.height;

  const color = hexToRgba(getLabelColor(suggestion.label), 0.35);

  if (window.addPdfHighlight) {
    window.addPdfHighlight(page, x, y, w, h, color);
  }

  if (window.scrollToHighlight) {
    window.scrollToHighlight(page, { x, y, w, h });
  }

  toast.info(`Focused [P${page}] ${suggestion.label}: ${suggestion.text}`);
}

function hexToRgba(hex, alpha) {
  if (!hex) return `rgba(255, 230, 0, ${alpha})`;
  const h = hex.replace("#", "");
  const bigint = parseInt(h, 16);
  const r = (bigint >> 16) & 255;
  const g = (bigint >> 8) & 255;
  const b = bigint & 255;
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

// ---------------------------------------------------------------
// Keyboard navigation: Up/Down, Enter, R
// ---------------------------------------------------------------
function setupSuggestionKeyboardNav(dropdown, multi) {
  document.addEventListener("keydown", async (e) => {
    if (!window.suggestions.length) return;

    const container = document.getElementById("suggestionsContainer");
    if (!container) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      if (currentSuggestionIndex < window.suggestions.length - 1) {
        currentSuggestionIndex++;
      } else {
        currentSuggestionIndex = 0;
      }
      dropdown.value = String(currentSuggestionIndex);
      multi.value = String(currentSuggestionIndex);
      focusSuggestion(currentSuggestionIndex);
    }

    if (e.key === "ArrowUp") {
      e.preventDefault();
      if (currentSuggestionIndex > 0) {
        currentSuggestionIndex--;
      } else {
        currentSuggestionIndex = window.suggestions.length - 1;
      }
      dropdown.value = String(currentSuggestionIndex);
      multi.value = String(currentSuggestionIndex);
      focusSuggestion(currentSuggestionIndex);
    }

    if (e.key === "Enter") {
      if (currentSuggestionIndex >= 0) {
        const opt = Array.from(multi.options).find(
          o => parseInt(o.value, 10) === currentSuggestionIndex
        );
        if (opt) opt.selected = !opt.selected;
      }
    }

    if (e.key.toLowerCase() === "r") {
      const selected = Array.from(multi.selectedOptions).map(opt =>
        window.suggestions[parseInt(opt.value, 10)]
      );
      if (selected.length) {
        await redactSelectedSpans(selected);
      }
    }
  });
}

// ---------------------------------------------------------------
// Call backend /redact/multiple
// ---------------------------------------------------------------
async function redactSelectedSpans(spans) {
  if (!window.currentDocId) {
    toast.error("Upload a document first");
    return;
  }

  try {
    loading.show("Applying redactions…");

    const res = await fetch(`${window.API}/redact/multiple`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        doc_id: window.currentDocId,
        spans
      })
    });

    if (!res.ok) throw new Error("Redaction failed");

    const data = await res.json();
    toast.success(`Applied ${data.applied || data.total_hits || spans.length} redactions`);

    await window.loadPdf(window.currentDocId);

    if (window.loadVersionHistory) {
      await window.loadVersionHistory(window.currentDocId);
    }
    if (window.loadAuditLog) {
      await window.loadAuditLog(window.currentDocId);
    }

  } catch (err) {
    console.error(err);
    toast.error("Redaction failed");
  } finally {
    loading.hide();
  }
}

// ---------------------------------------------------------------
// Expose loader
// ---------------------------------------------------------------
window.loadSuggestions = loadSuggestions;
