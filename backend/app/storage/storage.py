import os
import json
import shutil
import calendar
from pathlib import Path
from datetime import datetime

# -----------------------------------------
# Base storage directory
# -----------------------------------------
BASE_DIR = Path("storage")
BASE_DIR.mkdir(exist_ok=True)

# -----------------------------------------
# Document storage
# -----------------------------------------
DOC_FOLDER = BASE_DIR / "documents"
DOC_FOLDER.mkdir(exist_ok=True)

# Root folder for all per-document storage
# (Fixes: STORAGE_ROOT was not defined)
STORAGE_ROOT = DOC_FOLDER

# -----------------------------------------
# Audit logs
# -----------------------------------------
AUDIT_FOLDER = BASE_DIR / "audit_logs"
AUDIT_FOLDER.mkdir(parents=True, exist_ok=True)

# -----------------------------------------
# Archives
# -----------------------------------------
ARCHIVE_ROOT = BASE_DIR / "archives"
ARCHIVE_ROOT.mkdir(exist_ok=True)

MONTH_ARCHIVE = ARCHIVE_ROOT / "months"
YEAR_ARCHIVE = ARCHIVE_ROOT / "years"

MONTH_ARCHIVE.mkdir(exist_ok=True)
YEAR_ARCHIVE.mkdir(exist_ok=True)

# -----------------------------------------
# Helpers
# -----------------------------------------
def ensure_doc_folder(doc_id: str):
    folder = STORAGE_ROOT / doc_id
    folder.mkdir(parents=True, exist_ok=True)
    return folder

def timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


# -----------------------------------------
# ORIGINAL PDF
# -----------------------------------------
def save_original_pdf(doc_id: str, filename: str, pdf_bytes: bytes) -> str:
    """
    Save the original uploaded PDF.
    """
    folder = ensure_doc_folder(doc_id)
    path = folder / f"original_{filename}"

    with open(path, "wb") as f:
        f.write(pdf_bytes)

    return str(path)


def load_original_pdf(doc_id: str, filename: str) -> bytes:
    folder = ensure_doc_folder(doc_id)
    path = folder / f"original_{filename}"
    return path.read_bytes()


# -----------------------------------------
# REDACTED PDF (final output)
# -----------------------------------------
def save_final_redacted(doc_id: str, original_filename: str, pdf_bytes: bytes) -> str:
    """
    Save the final redacted PDF as originalName_redacted.pdf
    """
    folder = ensure_doc_folder(doc_id)

    base, ext = os.path.splitext(original_filename)
    redacted_name = f"{base}_redacted{ext}"

    path = folder / redacted_name

    with open(path, "wb") as f:
        f.write(pdf_bytes)

    return str(path)


# -----------------------------------------
# VERSION HISTORY (v001.pdf, v002.pdf, ...)
# -----------------------------------------
def save_version(doc_id: str, pdf_bytes: bytes) -> str:
    """
    Save a versioned PDF: v001.pdf, v002.pdf, ...
    """
    folder = ensure_doc_folder(doc_id)

    existing = sorted(folder.glob("v*.pdf"))
    if existing:
        last = existing[-1].stem  # "v003"
        last_num = int(last[1:])
        next_num = last_num + 1
    else:
        next_num = 1

    version_name = f"v{next_num:03d}.pdf"
    path = folder / version_name

    tmp_path = folder / (version_name + ".tmp")
    with open(tmp_path, "wb") as f:
        f.write(pdf_bytes)
    os.replace(tmp_path, path)

    return str(path)


# -----------------------------------------
# original PDF only save_pdf_version(doc_id, pdf_bytes) list_archives() history
# -----------------------------------------
def load_pdf_bytes(doc_id: str) -> bytes:
    """
    Load the original PDF bytes for a document.
    Hybrid Mode (Option B):
    - Always load original_<filename>
    - Ignore version files for loading
    """
    folder = ensure_doc_folder(doc_id)

    # Find original PDF
    for file in folder.iterdir():
        if file.name.startswith("original_") and file.suffix.lower() == ".pdf":
            return file.read_bytes()

    raise FileNotFoundError(f"No original PDF found for doc_id={doc_id}")


def save_pdf_version(doc_id: str, pdf_bytes: bytes) -> str:
    """
    Wrapper for save_version() so services can call a consistent name.
    """
    return save_version(doc_id, pdf_bytes)


def list_archives():
    """
    Return a list of all monthly and yearly archive ZIP files.
    """
    archives = []

    # Monthly archives
    for file in MONTH_ARCHIVE.iterdir():
        if file.is_file() and file.suffix == ".zip":
            archives.append(file.name)

    # Yearly archives
    for file in YEAR_ARCHIVE.iterdir():
        if file.is_file() and file.suffix == ".zip":
            archives.append(file.name)

    return archives

def get_audit_log(doc_id: str):
    """
    Return audit log entries for a document, if stored on disk.
    Adjust this to your actual audit storage format.
    """
    # Example: logs stored as JSONL per doc_id
    log_file = AUDIT_FOLDER / f"{doc_id}.jsonl"
    if not log_file.exists():
        return []

    entries = []
    for line in log_file.read_text().splitlines():
        try:
            import json
            entries.append(json.loads(line))
        except Exception:
            continue
    return entries

# -----------------------------------------
# AUDIT LOGS
# -----------------------------------------
def log_action(doc_id: str, action: str, details: dict):
    """
    Append an audit log entry.
    """
    folder = ensure_doc_folder(doc_id)
    log_path = folder / "audit.json"

    entry = {
        "timestamp": timestamp(),
        "action": action,
        "details": details
    }

    if log_path.exists():
        logs = json.loads(log_path.read_text())
    else:
        logs = []

    logs.append(entry)
    log_path.write_text(json.dumps(logs, indent=2))


def load_audit_log(doc_id: str):
    folder = ensure_doc_folder(doc_id)
    log_path = folder / "audit.json"

    if not log_path.exists():
        return []

    return json.loads(log_path.read_text())


# ---------------------------------------------------
# Create a monthly archive ZIP
# ---------------------------------------------------
def archive_month(year: int, month: int):
    """
    Create a ZIP file containing all documents from the given month.
    After creating the ZIP, delete the original monthly data.
    """
    month_name = calendar.month_name[month]
    zip_name = f"{month_name}{year}.zip"
    zip_path = MONTH_ARCHIVE / zip_name

    # Temporary folder to collect files
    temp_folder = ARCHIVE_ROOT / f"temp_month_{year}_{month}"
    temp_folder.mkdir(exist_ok=True)

    # Copy all doc folders that match the month/year
    for doc_folder in STORAGE_ROOT.iterdir():
        if not doc_folder.is_dir() or doc_folder.name == "archives":
            continue

        # Check audit log for timestamps
        audit_path = doc_folder / "audit.json"
        if not audit_path.exists():
            continue

        logs = json.loads(audit_path.read_text())
        if not logs:
            continue

        # Check if any action happened in this month
        for entry in logs:
            ts = datetime.strptime(entry["timestamp"], "%Y-%m-%d_%H-%M-%S")
            if ts.year == year and ts.month == month:
                shutil.copytree(doc_folder, temp_folder / doc_folder.name)
                break

    # Create ZIP
    shutil.make_archive(str(zip_path.with_suffix("")), "zip", temp_folder)

    # Cleanup temp folder
    shutil.rmtree(temp_folder)

    # Cleanup original data
    cleanup_after_archive(year=year, month=month)

    return str(zip_path)


# ---------------------------------------------------
# Create a yearly archive ZIP
# ---------------------------------------------------
def archive_year(year: int):
    """
    Create a ZIP file containing all documents from the given year.
    After creating the ZIP, delete the original yearly data.
    """
    zip_name = f"{year}.zip"
    zip_path = YEAR_ARCHIVE / zip_name

    temp_folder = ARCHIVE_ROOT / f"temp_year_{year}"
    temp_folder.mkdir(exist_ok=True)

    for doc_folder in STORAGE_ROOT.iterdir():
        if not doc_folder.is_dir() or doc_folder.name == "archives":
            continue

        audit_path = doc_folder / "audit.json"
        if not audit_path.exists():
            continue

        logs = json.loads(audit_path.read_text())
        if not logs:
            continue

        for entry in logs:
            ts = datetime.strptime(entry["timestamp"], "%Y-%m-%d_%H-%M-%S")
            if ts.year == year:
                shutil.copytree(doc_folder, temp_folder / doc_folder.name)
                break

    shutil.make_archive(str(zip_path.with_suffix("")), "zip", temp_folder)
    shutil.rmtree(temp_folder)

    cleanup_after_archive(year=year)

    return str(zip_path)


# ---------------------------------------------------
# Cleanup after archive
# ---------------------------------------------------
def cleanup_after_archive(year: int, month: int = None):
    """
    Delete all doc folders that belong to the given month/year.
    """
    for doc_folder in STORAGE_ROOT.iterdir():
        if not doc_folder.is_dir() or doc_folder.name == "archives":
            continue

        audit_path = doc_folder / "audit.json"
        if not audit_path.exists():
            continue

        logs = json.loads(audit_path.read_text())
        if not logs:
            continue

        for entry in logs:
            ts = datetime.strptime(entry["timestamp"], "%Y-%m-%d_%H-%M-%S")

            if month is not None:
                # Monthly cleanup
                if ts.year == year and ts.month == month:
                    shutil.rmtree(doc_folder)
                    break
            else:
                # Yearly cleanup
                if ts.year == year:
                    shutil.rmtree(doc_folder)
                    break