from fastapi import APIRouter
from pydantic import BaseModel
from ..services.box_redaction_service import redact_box

router = APIRouter()

class BoxRedactRequest(BaseModel):
    doc_id: str
    page: int
    x: float
    y: float
    w: float
    h: float

@router.post("/redact/box")
async def redact_box_route(data: BoxRedactRequest):
    return redact_box(data.doc_id, data.page, data.x, data.y, data.w, data.h)