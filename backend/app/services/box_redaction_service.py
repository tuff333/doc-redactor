# ---------------------------------------------------------
# File: box_redaction_service.py
# Layout‑preserving box redaction
# ---------------------------------------------------------

import fitz
from fastapi import HTTPException
from .pdf_service import get_pdf_bytes, update_pdf_bytes


def redact_box(doc_id: str, page_number: int, x: float, y: float, w: float, h: float):
    """
    x, y, w, h are normalized (0–1)
    """

    pdf_bytes = get_pdf_bytes(doc_id)
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    if page_number < 0 or page_number >= len(doc):
        raise HTTPException(status_code=400, detail="Invalid page number")

    page = doc[page_number]

    # Convert normalized coords to absolute PDF coords
    page_width = page.rect.width
    page_height = page.rect.height

    abs_x = x * page_width
    abs_y = y * page_height
    abs_w = w * page_width
    abs_h = h * page_height

    rect = fitz.Rect(abs_x, abs_y, abs_x + abs_w, abs_y + abs_h)

    page.add_redact_annot(rect, fill=(0, 0, 0))
    page.apply_redactions()

    new_bytes = doc.tobytes()
    doc.close()

    update_pdf_bytes(doc_id, new_bytes)

    return {
        "status": "success",
        "page": page_number,
        "rect": [abs_x, abs_y, abs_w, abs_h]
    }
