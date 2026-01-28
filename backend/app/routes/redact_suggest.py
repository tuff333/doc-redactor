# backend/app/routes/redact_suggest.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from ..services.redaction_suggestion_service import suggest_redactions
from ..state.memory_helpers import get_text
from ..services.pdf_service import get_pdf_bytes
import fitz

router = APIRouter()


class SuggestRequest(BaseModel):
    doc_id: str


@router.post("/redact/suggest")
async def suggest_route(data: SuggestRequest):
    text = get_text(data.doc_id)
    if not text:
        raise HTTPException(status_code=404, detail="Document not found or no text extracted")

    result = suggest_redactions(data.doc_id)

    if "error" in result:
        return result

    suggestions = result.get("suggestions", [])

    # Load PDF to compute page + coordinates for each suggestion
    pdf_bytes = get_pdf_bytes(data.doc_id)
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    formatted = []

    for s in suggestions:
        s_text = s.get("text", "")
        s_start = s.get("start")
        s_end = s.get("end")
        s_label = s.get("label", "SENSITIVE")

        page_num = None
        norm_x = norm_y = norm_w = norm_h = None

        if s_text:
            # Find first occurrence of this text in the PDF
            for i, page in enumerate(doc):
                rects = page.search_for(s_text)
                if rects:
                    r = rects[0]
                    page_rect = page.rect

                    # Normalize to 0–1
                    norm_x = (r.x0 - page_rect.x0) / page_rect.width
                    norm_y = (r.y0 - page_rect.y0) / page_rect.height
                    norm_w = r.width / page_rect.width
                    norm_h = r.height / page_rect.height

                    page_num = i + 1  # 1-based
                    break

        formatted.append({
            "text": s_text,
            "start": s_start,
            "end": s_end,
            "label": s_label,
            "page": page_num,
            "x": norm_x,
            "y": norm_y,
            "w": norm_w,
            "h": norm_h,
        })

    doc.close()

    return JSONResponse({
        "doc_id": data.doc_id,
        "suggestions": formatted,
        "total": len(formatted),
        "status": "success"
    })
