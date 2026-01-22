from fastapi import APIRouter
from pydantic import BaseModel
from ..services.tags_service import get_tags, add_tag, remove_tag

router = APIRouter()

class TagRequest(BaseModel):
    doc_id: str
    tag: str

@router.post("/tags/get")
async def tags_get(data: TagRequest):
    return get_tags(data.doc_id)

@router.post("/tags/add")
async def tags_add(data: TagRequest):
    return add_tag(data.doc_id, data.tag)

@router.post("/tags/remove")
async def tags_remove(data: TagRequest):
    return remove_tag(data.doc_id, data.tag)