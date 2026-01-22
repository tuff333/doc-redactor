from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.multiple_redaction_service import redact_multiple

router = APIRouter()

class RedactTextRequest(BaseModel):
    doc_id: str
    target_text: str

@router.post("/redact/text")
async def redact_text_route(data: RedactTextRequest):
    if not data.target_text.strip():
        raise HTTPException(status_code=400, detail="target_text is empty")

    # Use the same engine as multiple redaction
    result = redact_multiple(data.doc_id, [data.target_text])

    return {
        "doc_id": data.doc_id,
        "target_text": data.target_text,
        "status": result.get("status", "success"),
        "total_hits": result.get("total_hits", 0)
    }
