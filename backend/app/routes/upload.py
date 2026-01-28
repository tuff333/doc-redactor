# ---------------------------------------------------------
# File: upload.py
# Path: backend/app/routes/upload.py
# ---------------------------------------------------------

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import uuid

from ..storage.storage import save_original_pdf, log_action
from ..utils.pdf_utils import extract_text_from_pdf
from ..state.memory_helpers import (
    set_original_name,
    set_text,
    set_pdf_bytes,
    set_options
)

router = APIRouter()


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    save_original: bool = Form(False),
    save_audit: bool = Form(False)
):
    """
    Upload a PDF, extract text, optionally save original, and return doc_id.
    """

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # Generate unique document ID
    doc_id = str(uuid.uuid4())

    # Read PDF bytes
    pdf_bytes = await file.read()

    # Extract text
    try:
        extracted_text = extract_text_from_pdf(pdf_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {e}")

    # Store original filename
    set_original_name(doc_id, file.filename)

    # Store extracted text
    set_text(doc_id, extracted_text)

    # Store PDF bytes
    set_pdf_bytes(doc_id, pdf_bytes)

    # Store checkbox options
    set_options(doc_id, {
        "save_original": save_original,
        "save_audit": save_audit,
        "save_versions": True,      # default ON
        "save_redacted": True       # default ON
    })

    # Save original PDF (optional)
    if save_original:
        save_original_pdf(doc_id, file.filename, pdf_bytes)

    # Log audit (optional)
    if save_audit:
        log_action(doc_id, "upload", {"filename": file.filename})

    return JSONResponse({
        "doc_id": doc_id,
        "filename": file.filename,
        "text_length": len(extracted_text),
        "options": {
            "save_original": save_original,
            "save_audit": save_audit
        }
    })