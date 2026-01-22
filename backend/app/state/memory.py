# ---------------------------------------------------------
# File: memory.py
# Path: backend/app/state/memory.py
# ---------------------------------------------------------
# This module stores all in-memory state for each document.
# Everything is keyed by doc_id (UUID).
# ---------------------------------------------------------

from typing import Dict, List, Tuple


# ---------------------------------------------------------
# CORE DOCUMENT STATE
# ---------------------------------------------------------

# doc_id -> original filename (e.g., "invoice.pdf")
DOC_ORIGINAL_NAME: Dict[str, str] = {}

# doc_id -> extracted text from the PDF (used for ML + PII + span redaction)
DOC_TEXT: Dict[str, str] = {}

# doc_id -> current working PDF bytes (updated after each redaction)
DOC_PDF_BYTES: Dict[str, bytes] = {}


# ---------------------------------------------------------
# USER OPTIONS (checkboxes)
# ---------------------------------------------------------

# doc_id -> {
#     "save_original": bool,
#     "save_audit": bool,
#     "save_versions": bool,
#     "save_redacted": bool
# }
DOC_OPTIONS: Dict[str, dict] = {}


# ---------------------------------------------------------
# VERSION HISTORY (optional)
# ---------------------------------------------------------

# doc_id -> list of version filenames (e.g., ["v001.pdf", "v002.pdf"])
DOC_VERSIONS: Dict[str, List[str]] = {}


# ---------------------------------------------------------
# TAGGING + CHAT (legacy features)
# ---------------------------------------------------------

# doc_id -> list of tags (legacy)
DOC_TAGS: Dict[str, List[str]] = {}

# doc_id -> chat history (list of (role, content))
CHAT_HISTORY: Dict[str, List[Tuple[str, str]]] = {}

# doc_id -> {"auto": [...], "manual": [...]}
TAGS: Dict[str, Dict[str, List[str]]] = {}