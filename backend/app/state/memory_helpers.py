# ---------------------------------------------------------
# File: memory_helpers.py
# Path: backend/app/state/memory_helpers.py
# ---------------------------------------------------------
# Helper functions for safely accessing and updating
# in-memory document state.
# ---------------------------------------------------------

from .memory import (
    DOC_ORIGINAL_NAME,
    DOC_TEXT,
    DOC_PDF_BYTES,
    DOC_OPTIONS,
    DOC_VERSIONS,
    DOC_TAGS,
    CHAT_HISTORY,
    TAGS
)


# ---------------------------------------------------------
# GETTERS
# ---------------------------------------------------------

def get_original_name(doc_id: str) -> str:
    """
    Get the original filename for a document.
    # doc_id -> original filename (e.g., "invoice.pdf")
    """
    return DOC_ORIGINAL_NAME.get(doc_id)


def get_text(doc_id: str) -> str:
    """
    Get extracted text for a document.
    # doc_id -> extracted text
    """
    return DOC_TEXT.get(doc_id, "")


def get_pdf_bytes(doc_id: str) -> bytes:
    """
    Get the current working PDF bytes.
    # doc_id -> PDF bytes
    """
    return DOC_PDF_BYTES.get(doc_id)


def get_options(doc_id: str) -> dict:
    """
    Get user-selected checkbox options.
    # doc_id -> {"save_original": bool, ...}
    """
    return DOC_OPTIONS.get(doc_id, {})


def get_versions(doc_id: str) -> list:
    """
    Get version history list.
    # doc_id -> ["v001.pdf", "v002.pdf"]
    """
    return DOC_VERSIONS.get(doc_id, [])


# ---------------------------------------------------------
# SETTERS
# ---------------------------------------------------------

def set_original_name(doc_id: str, filename: str):
    """
    Set original filename.
    """
    DOC_ORIGINAL_NAME[doc_id] = filename


def set_text(doc_id: str, text: str):
    """
    Set extracted text.
    """
    DOC_TEXT[doc_id] = text


def set_pdf_bytes(doc_id: str, pdf_bytes: bytes):
    """
    Set current working PDF bytes.
    """
    DOC_PDF_BYTES[doc_id] = pdf_bytes


def set_options(doc_id: str, options: dict):
    """
    Set user-selected checkbox options.
    """
    DOC_OPTIONS[doc_id] = options


def add_version(doc_id: str, version_filename: str):
    """
    Add a version file to version history.
    """
    if doc_id not in DOC_VERSIONS:
        DOC_VERSIONS[doc_id] = []
    DOC_VERSIONS[doc_id].append(version_filename)


# ---------------------------------------------------------
# TAGGING + CHAT HELPERS
# ---------------------------------------------------------

def add_chat_message(doc_id: str, role: str, content: str):
    """
    Add a message to chat history.
    # doc_id -> [(role, content)]
    """
    if doc_id not in CHAT_HISTORY:
        CHAT_HISTORY[doc_id] = []
    CHAT_HISTORY[doc_id].append((role, content))


def add_tag(doc_id: str, tag_type: str, tag_value: str):
    """
    Add a tag to auto/manual tag lists.
    # doc_id -> {"auto": [...], "manual": [...]}
    """
    if doc_id not in TAGS:
        TAGS[doc_id] = {"auto": [], "manual": []}
    TAGS[doc_id][tag_type].append(tag_value)