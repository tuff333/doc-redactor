// js/chat.js

// ===============================================================
// === PHASE 2 — TOAST NOTIFICATIONS — 2026‑01‑17 =================
// ===============================================================

async function askQuestion() {
  if (!window.currentDocId) {
    toast.error("Upload a document first");
    return;
  }

  const question = document.getElementById("questionInput").value.trim();
  const answerOutput = document.getElementById("answerOutput");

  if (!question) {
    toast.info("Enter a question");
    return;
  }

  // Show temporary loading message
  answerOutput.innerText = "Thinking...";

  try {
    const res = await fetch(`${window.API}/chat`, {   // <-- FIXED: /ask → /chat
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        doc_id: window.currentDocId,
        message: question       // <-- FIXED: question → message
      })
    });

    if (!res.ok) throw new Error("Chat request failed");

    const data = await res.json();
    console.log("FRONTEND RECEIVED:", data);


    if (data.answer) {
      answerOutput.innerText = data.answer;
      toast.success("Answer ready");
    } else {
      answerOutput.innerText = "No answer returned.";
      toast.error("No answer returned");
    }

  } catch (err) {
    console.error(err);
    answerOutput.innerText = "Error: server failure.";
    toast.error("Chat request failed — server error");
  }
}

// Make it globally accessible for app.js
window.ask = askQuestion;
