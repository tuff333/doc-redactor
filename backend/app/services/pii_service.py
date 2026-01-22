import re

# -----------------------------------------
# PII PATTERNS (Regex)
# -----------------------------------------
PII_PATTERNS = {
    # Email
    "EMAIL": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

    # Phone numbers (international-ish)
    "PHONE": r"\+?\d[\d\-\s]{7,}\d",

    # Credit card numbers (13–16 digits)
    "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b",

    # US SSN
    "SSN": r"\b\d{3}-\d{2}-\d{4}\b",

    # Dates (01/02/2024, 1-2-24, etc.)
    "DATE": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",

    # Addresses (simple heuristic)
    "ADDRESS": r"\b\d+\s+[A-Za-z0-9'\.\-]+\s+(Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b",

    # Driver license / ID
    "LICENSE": r"\b(?:DL|Driver.?s License|License No\.?)[:\s]*[A-Za-z0-9\-]{5,}\b",

    # Passport numbers
    "PASSPORT": r"\b[A-Z]{1,2}\d{6,9}\b",

    # Canadian Health Card (OHIP)
    "HEALTH_CARD": r"\b\d{4}\s?\d{3}\s?\d{3}\b",

    # Canadian Postal Code
    "POSTAL_CODE": r"\b[A-Za-z]\d[A-Za-z]\s?\d[A-Za-z]\d\b",
}

# -----------------------------------------
# Detect PII in text
# -----------------------------------------
def detect_pii(text: str):
    suggestions = []

    for label, pattern in PII_PATTERNS.items():
        try:
            for match in re.finditer(pattern, text):
                suggestions.append({
                    "text": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                    "label": label
                })
        except Exception as e:
            print(f"[WARN] Regex failed for {label}: {e}")

    return suggestions