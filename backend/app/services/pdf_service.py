import uuid
import fitz
from fastapi import UploadFile, HTTPException
from ..state.memory import DOC_PDF_BYTES, DOC_ORIGINAL_NAME
from ..utils.rag_utils import ingest_document


def generate_doc_id() -> str:
    return str(uuid.uuid4())


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text


async def load_pdf_into_memory(file: UploadFile):
    filename = file.filename or "document.pdf"

    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    pdf_bytes = await file.read()
    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="Empty file")

    doc_id = generate_doc_id()

    DOC_PDF_BYTES[doc_id] = pdf_bytes
    DOC_ORIGINAL_NAME[doc_id] = filename

    try:
        text = extract_text_from_pdf(pdf_bytes)
        ingest_document(doc_id, text)
    except Exception as e:
        print(f"[WARN] RAG ingestion failed for {doc_id}: {e}")

    return {"doc_id": doc_id, "file_type": "pdf"}


def get_pdf_bytes(doc_id: str) -> bytes:
    if doc_id not in DOC_PDF_BYTES:
        raise HTTPException(status_code=404, detail="Document not found")
    return DOC_PDF_BYTES[doc_id]


def update_pdf_bytes(doc_id: str, new_bytes: bytes):
    DOC_PDF_BYTES[doc_id] = new_bytes