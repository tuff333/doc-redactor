import os

def make_redacted_filename(original_name: str) -> str:
    """
    Given 'abcdefghi.pdf' → return 'abcdefghi_redacted.pdf'.
    """
    base, ext = os.path.splitext(original_name)
    if not ext:
        ext = ".pdf"
    return f"{base}_redacted{ext}"