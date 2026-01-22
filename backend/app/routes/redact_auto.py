# ---------------------------------------------------------
# File: redact_auto.py
# Route: POST /redact/auto
# Uses suggestions + span-based blackout redaction
# ---------------------------------------------------------

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

from ..services.redaction_suggestion_service import suggest_redactions
from ..services.multiple_redaction_service import redact_multiple

router = APIRouter()


class AutoRedactRequest(BaseModel):
    doc_id: str


@router.post("/redact/auto")
async def auto_redact_route(data: AutoRedactRequest) -> Dict[str, Any]:
    """
    Auto‑redact all suggested spans (ML + PII).
    Uses the same span-based blackout redaction as /redact/multiple.
    """
    result = suggest_redactions(data.doc_id)

    if "error" in result:
        return result

    spans = result.get("suggestions", []) or []

    if not spans:
        return {
            "doc_id": data.doc_id,
            "applied": 0,
            "total_suggestions": 0,
            "status": "no_suggestions"
        }

    redact_result = redact_multiple(data.doc_id, spans)

    return {
        "doc_id": data.doc_id,
        "applied": redact_result.get("total_hits", 0),
        "total_suggestions": len(spans),
        "status": redact_result.get("status", "success")
    }
