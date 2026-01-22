// js/loading.js

// ===============================================================
// === PHASE 2 — GLOBAL LOADING ENGINE — 2026‑01‑17 ===============
// Provides:
//   loading.show("message")
//   loading.hide()
// ===============================================================

const loading = {
  el: document.getElementById("loadingOverlay"),
  textEl: null,

  init() {
    this.textEl = this.el.querySelector(".loading-text");
  },

  show(message = "Processing…") {
    if (!this.textEl) this.init();
    this.textEl.innerText = message;
    this.el.classList.add("show");
  },

  hide() {
    this.el.classList.remove("show");
  }
};

// 🔥 Make loading globally accessible
window.loading = loading;
