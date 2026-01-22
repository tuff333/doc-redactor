// js/toast.js

// ======================================================================
// === PHASE 2 — TOAST NOTIFICATIONS — 2026‑01‑17 ========================
// ======================================================================

const toast = {
  show(message, type = "info") {
    const container = document.getElementById("toastContainer");
    if (!container) return;

    const el = document.createElement("div");
    el.className = `toast toast-${type}`;
    el.textContent = message;

    // Remove toast early if clicked
    el.addEventListener("click", () => {
      el.style.animation = "toastFadeOut 0.3s forwards";
      setTimeout(() => el.remove(), 300);
    });

    container.appendChild(el);

    // Auto-remove after animation ends (4 seconds)
    setTimeout(() => {
      el.remove();
    }, 4000);
  },

  success(msg) {
    this.show(msg, "success");
  },

  error(msg) {
    this.show(msg, "error");
  },

  info(msg) {
    this.show(msg, "info");
  }
};

// 🔥 Make toast globally accessible
window.toast = toast;
