from fastapi import APIRouter
from pydantic import BaseModel
from ..services.chat_service import chat_with_doc

router = APIRouter()

class ChatRequest(BaseModel):
    doc_id: str
    message: str

@router.post("/chat")
async def chat_route(data: ChatRequest):
    return chat_with_doc(data.doc_id, data.message)