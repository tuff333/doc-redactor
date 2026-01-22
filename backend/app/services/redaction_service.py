# ---------------------------------------------------------
# File: redaction_service.py
# Safe layout-preserving text redaction
# ---------------------------------------------------------

import fitz  # PyMuPDF
from ..state.memory import DOC_TEXT, DOC_OPTIONS, DOC_VERSIONS
from ..services.pdf_service import get_pdf_bytes, update_pdf_bytes
from ..storage.storage import save_version, log_action


def apply_text_redaction(doc_id: str, start: int, end: int):
    """
    Redact text by blacking out the matching text on the PDF.
    This version preserves layout, background, fonts, and structure.
    """

    # ---------------------------------------------------------
    # 1. Validate text exists
    # ---------------------------------------------------------
    if doc_id not in DOC_TEXT:
        raise ValueError("Document text not found")

    text = DOC_TEXT[doc_id]

    if start < 0 or end > len(text) or start >= end:
        raise ValueError("Invalid redaction span")

    # Extract the exact substring to search for in the PDF
    target_text = text[start:end]

    # ---------------------------------------------------------
    # 2. Update in-memory text (replace with █)
    # ---------------------------------------------------------
    redacted_segment = "█" * (end - start)
    new_text = text[:start] + redacted_segment + text[end:]
    DOC_TEXT[doc_id] = new_text

    # ---------------------------------------------------------
    # 3. Apply blackout redaction directly on the PDF
    # ---------------------------------------------------------
    original_pdf_bytes = get_pdf_bytes(doc_id)
    doc = fitz.open(stream=original_pdf_bytes, filetype="pdf")

    total_hits = 0

    for page in doc:
        matches = page.search_for(target_text)
        for inst in matches:
            page.add_redact_annot(inst, fill=(0, 0, 0))
            total_hits += 1

        if matches:
            page.apply_redactions()

    new_pdf_bytes = doc.tobytes()
    doc.close()

    # Update in-memory PDF
    update_pdf_bytes(doc_id, new_pdf_bytes)

    # ---------------------------------------------------------
    # 4. Optional: save version to disk
    # ---------------------------------------------------------
    options = DOC_OPTIONS.get(doc_id, {})
    version_path = None

    if options.get("save_versions", True):
        version_path = save_version(doc_id, new_pdf_bytes)
        DOC_VERSIONS.setdefault(doc_id, []).append(version_path)

    # ---------------------------------------------------------
    # 5. Optional: audit log
    # ---------------------------------------------------------
    if options.get("save_audit", False):
        log_action(doc_id, "text_redaction", {
            "start": start,
            "end": end,
            "hits": total_hits,
            "version_path": version_path
        })

    # ---------------------------------------------------------
    # 6. Return response
    # ---------------------------------------------------------
    return {
        "doc_id": doc_id,
        "start": start,
        "end": end,
        "hits": total_hits,
        "version_path": version_path,
        "status": "success"
    }
