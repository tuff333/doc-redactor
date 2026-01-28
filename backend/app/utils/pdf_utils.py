import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from typing import Tuple


# ---------------------------------------------------------
# Extract text from PDF
# ---------------------------------------------------------
def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text from PDF bytes.
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text


# ---------------------------------------------------------
# Text-based redaction (search + blackout)
# ---------------------------------------------------------
def redact_text_in_pdf(input_path: str, output_path: str, target_text: str) -> int:
    """
    Find all instances of target_text and draw black rectangles over them.
    Used by manual text redaction.
    """
    doc = fitz.open(input_path)
    occurrences = 0

    for page in doc:
        text_instances = page.search_for(target_text)
        for inst in text_instances:
            page.add_redact_annot(inst, fill=(0, 0, 0))
            occurrences += 1

        if text_instances:
            page.apply_redactions()

    doc.save(output_path)
    doc.close()
    return occurrences


# ---------------------------------------------------------
# Box-based redaction (drag area)
# ---------------------------------------------------------
def redact_box_in_pdf(
    input_path: str,
    output_path: str,
    page_number: int,
    nx1: float,
    ny1: float,
    nx2: float,
    ny2: float,
):
    """
    Redact a rectangular region on a given page using normalized coordinates.
    Used by click-and-drag area redaction.
    """
    doc = fitz.open(input_path)

    if page_number < 1 or page_number > len(doc):
        doc.close()
        raise ValueError("Invalid page number")

    page = doc[page_number - 1]
    page_rect = page.rect

    x1 = page_rect.x0 + nx1 * page_rect.width
    y1 = page_rect.y0 + ny1 * page_rect.height
    x2 = page_rect.x0 + nx2 * page_rect.width
    y2 = page_rect.y0 + ny2 * page_rect.height

    rect = fitz.Rect(x1, y1, x2, y2)

    page.add_redact_annot(rect, fill=(0, 0, 0))
    page.apply_redactions()

    doc.save(output_path)
    doc.close()


# ---------------------------------------------------------
# Image → PDF conversion
# ---------------------------------------------------------
def image_to_pdf(image_path: str, pdf_path: str):
    """
    Convert PNG/JPG to PDF so we can use the same redaction and viewer pipelines.
    """
    img = Image.open(image_path).convert("RGB")
    img.save(pdf_path, "PDF", resolution=100.0)


# ---------------------------------------------------------
# OCR for images
# ---------------------------------------------------------
def ocr_image(image_path: str) -> str:
    """
    Extract text from image using Tesseract OCR.
    """
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text