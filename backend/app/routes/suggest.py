from fastapi import APIRouter
from pydantic import BaseModel
from ..services.suggest_service import suggest_for_doc

router = APIRouter()

class SuggestRequest(BaseModel):
    doc_id: str

@router.post("/suggest")
async def suggest_route(data: SuggestRequest):
    return suggest_for_doc(data.doc_id)