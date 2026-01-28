# ---------------------------------------------------------
# File: archive_routes.py
# Path: backend/app/routes/archive_routes.py
# ---------------------------------------------------------
# Routes for generating and listing monthly/yearly archives.
# ---------------------------------------------------------

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse

from ..storage.storage import (
    archive_month,
    archive_year,
    list_archives
)

router = APIRouter()


# ---------------------------------------------------------
# Create Monthly Archive
# ---------------------------------------------------------
@router.post("/archive/month")
async def create_month_archive(year: int, month: int):
    """
    Create a ZIP archive for a specific month.
    Example: January 2026 -> archive_month(2026, 1)
    """

    try:
        zip_path = archive_month(year, month)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create monthly archive: {e}")

    return FileResponse(zip_path, filename=zip_path.name)


# ---------------------------------------------------------
# Create Yearly Archive
# ---------------------------------------------------------
@router.post("/archive/year")
async def create_year_archive(year: int):
    """
    Create a ZIP archive for a specific year.
    Example: 2026 -> archive_year(2026)
    """

    try:
        zip_path = archive_year(year)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create yearly archive: {e}")

    return FileResponse(zip_path, filename=zip_path.name)


# ---------------------------------------------------------
# List All Archives
# ---------------------------------------------------------
@router.get("/archives/list")
async def list_all_archives():
    """
    Return a list of all monthly and yearly archive ZIP files.
    """

    try:
        archives = list_archives()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list archives: {e}")

    return JSONResponse({
        "archives": archives,
        "total": len(archives),
        "status": "success"
    })