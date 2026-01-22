# ---------------------------------------------------------
# File: download.py
# Path: backend/app/routes/download.py
# ---------------------------------------------------------
# This route supports downloading:
# - original PDFs (e.g., original_invoice.pdf)
# - redacted PDFs (e.g., original_invoice_redacted.pdf)
# - version history PDFs (e.g., original_invoice_redacted_v001.pdf)
# - monthly archives (e.g., January2026.zip)
# - yearly archives (e.g., 2026.zip)
# ---------------------------------------------------------

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()

# ---------------------------------------------------------
# Storage paths
# ---------------------------------------------------------

# Root storage directory
# storage/
STORAGE_ROOT = Path("storage")

# Monthly archives
# storage/archives/months/January2026.zip
ARCHIVE_MONTHS = STORAGE_ROOT / "archives" / "months"

# Yearly archives
# storage/archives/years/2026.zip
ARCHIVE_YEARS = STORAGE_ROOT / "archives" / "years"


@router.get("/download/{filename}")
async def download_file(filename: str):
    """
    Download any file stored in the system:
    - original PDFs
    - redacted PDFs
    - version history PDFs
    - monthly archives
    - yearly archives
    """

    # ---------------------------------------------------------
    # 1. Search inside each document folder
    #    storage/<doc_id>/<filename>
    # ---------------------------------------------------------
    for doc_folder in STORAGE_ROOT.iterdir():
        if doc_folder.is_dir() and doc_folder.name != "archives":
            candidate = doc_folder / filename
            if candidate.exists():
                return FileResponse(candidate, filename=filename)

    # ---------------------------------------------------------
    # 2. Search monthly archives
    #    storage/archives/months/<filename>
    # ---------------------------------------------------------
    candidate = ARCHIVE_MONTHS / filename
    if candidate.exists():
        return FileResponse(candidate, filename=filename)

    # ---------------------------------------------------------
    # 3. Search yearly archives
    #    storage/archives/years/<filename>
    # ---------------------------------------------------------
    candidate = ARCHIVE_YEARS / filename
    if candidate.exists():
        return FileResponse(candidate, filename=filename)

    # ---------------------------------------------------------
    # 4. Not found
    # ---------------------------------------------------------
    raise HTTPException(status_code=404, detail="File not found")