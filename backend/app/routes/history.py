from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..state.memory import DOC_VERSIONS
from ..storage.storage import get_audit_log, load_pdf_bytes, save_pdf_version
from ..storage.storage import ensure_doc_folder  # if not already imported
from pathlib import Path

router = APIRouter()

class HistoryRequest(BaseModel):
    doc_id: str

class RevertRequest(BaseModel):
    doc_id: str
    version_path: str  # full path or relative path to version file

class UndoRequest(BaseModel):
    doc_id: str

@router.post("/history/undo_last")
async def undo_last_redaction(data: UndoRequest):
    """
    Naive undo: revert to the previous version, if it exists.
    """
    versions = DOC_VERSIONS.get(data.doc_id, [])
    if len(versions) < 2:
        raise HTTPException(status_code=400, detail="No previous version to revert to")

    # Last version is current, second last is previous
    previous_version = Path(versions[-2])
    if not previous_version.exists():
        raise HTTPException(status_code=404, detail="Previous version file not found")

    pdf_bytes = previous_version.read_bytes()
    save_pdf_version(data.doc_id, pdf_bytes)

    return {
        "doc_id": data.doc_id,
        "reverted_to": str(previous_version),
        "status": "success",
    }

@router.post("/history/versions")
async def list_versions(data: HistoryRequest):
    versions = DOC_VERSIONS.get(data.doc_id, [])
    return {
        "doc_id": data.doc_id,
        "versions": versions,
        "count": len(versions),
    }

@router.post("/history/audit")
async def list_audit(data: HistoryRequest):
    log = get_audit_log(data.doc_id)
    return {
        "doc_id": data.doc_id,
        "entries": log,
        "count": len(log),
    }

@router.post("/history/revert")
async def revert_to_version(data: RevertRequest):
    """
    Revert a document to a specific saved version.
    """
    version_file = Path(data.version_path)
    if not version_file.exists():
        raise HTTPException(status_code=404, detail="Version file not found")

    pdf_bytes = version_file.read_bytes()

    # Save as a new version (so revert itself is tracked)
    save_pdf_version(data.doc_id, pdf_bytes)

    return {
        "doc_id": data.doc_id,
        "reverted_to": str(version_file),
        "status": "success",
    }