from fastapi import APIRouter, Response
from ..services.pdf_service import get_pdf_bytes

router = APIRouter()

@router.get("/view/{doc_id}")
async def view_pdf(doc_id: str):
    pdf_bytes = get_pdf_bytes(doc_id)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Cache-Control": "no-store"}
    )