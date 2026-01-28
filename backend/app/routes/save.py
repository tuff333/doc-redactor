from fastapi import APIRouter, Response
from ..services.pdf_service import get_pdf_bytes
from ..state.memory import DOC_ORIGINAL_NAME

router = APIRouter()

@router.get("/save/{doc_id}")
async def save_pdf(doc_id: str):
    pdf_bytes = get_pdf_bytes(doc_id)
    original = DOC_ORIGINAL_NAME.get(doc_id, "document.pdf")
    base = original.rsplit(".", 1)[0]
    filename = f"{base}_redacted.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )