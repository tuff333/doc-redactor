# backend/app/services/multiple_redaction_service.py
# ---------------------------------------------------------
# Unified redaction engine:
# - Accepts either spans OR plain text terms
# - Applies blackout rectangles using PyMuPDF
# ---------------------------------------------------------

import fitz
from fastapi import HTTPException
from .pdf_service import get_pdf_bytes, update_pdf_bytes


def redact_multiple(doc_id: str, items: list):
    """
    Accepts either:
      1. ["email@example.com", "John Doe"]
      2. [{"text": "...", "start": ..., "end": ..., "label": "..."}]

    Always performs layout‑preserving blackout redaction.
    """

    if not items:
        raise HTTPException(status_code=400, detail="No redaction items provided")

    pdf_bytes = get_pdf_bytes(doc_id)
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    total_hits = 0

    # Normalize input into a list of strings to search for
    terms = []

    for item in items:
        if isinstance(item, str):
            # Manual text redaction
            terms.append(item)

        elif isinstance(item, dict):
            # Smart suggestion span
            text = item.get("text")
            if text:
                terms.append(text)

    if not terms:
        raise HTTPException(status_code=400, detail="No valid redaction terms found")

    # ---------------------------------------------------------
    # Apply blackout rectangles for each term
    # ---------------------------------------------------------
    for term in terms:
        for page in doc:
            matches = page.search_for(term)
            for rect in matches:
                page.add_redact_annot(rect, fill=(0, 0, 0))
                total_hits += 1

            if matches:
                page.apply_redactions()

    # ---------------------------------------------------------
    # Save updated PDF
    # ---------------------------------------------------------
    new_bytes = doc.tobytes()
    doc.close()

    update_pdf_bytes(doc_id, new_bytes)

    return {
        "status": "success",
        "total_terms": len(terms),
        "total_hits": total_hits
    }
