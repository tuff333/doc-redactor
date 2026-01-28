# ---------------------------------------------------------
# File: redact_multiple.py
# Route: POST /redact/multiple
# Uses span-based blackout redaction (layout-preserving)
# ---------------------------------------------------------

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

from ..services.multiple_redaction_service import redact_multiple

router = APIRouter()


class Span(BaseModel):
    text: str
    start: int
    end: int
    label: str | None = "SENSITIVE"


class MultipleRedactRequest(BaseModel):
    doc_id: str
    spans: List[Span]


@router.post("/redact/multiple")
async def redact_multiple_route(data: MultipleRedactRequest) -> Dict[str, Any]:
    """
    Apply redaction for selected spans.
    Spans come from the suggestions panel (ML + PII).
    """
    spans_payload = [s.dict() for s in data.spans]

    result = redact_multiple(data.doc_id, spans_payload)

    return {
        "doc_id": data.doc_id,
        "applied": result.get("total_hits", 0),
        "total_selected": len(spans_payload),
        "status": result.get("status", "success")
    }
