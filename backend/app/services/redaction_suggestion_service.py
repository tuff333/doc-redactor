import spacy
from ..state.memory import DOC_TEXT
from .pii_service import detect_pii

MODEL_PATH = "backend/app/redaction_model/model-best"

try:
    nlp = spacy.load(MODEL_PATH)
    print(f"[INFO] Loaded redaction model from {MODEL_PATH}")
except Exception as e:
    print(f"[ERROR] Could not load redaction model: {e}")
    nlp = None


def suggest_redactions(doc_id: str):
    """
    Returns ML + PII hybrid suggestions in unified span format:
    {
        "text": "...",
        "start": int,
        "end": int,
        "label": "EMAIL" | "PHONE" | "SENSITIVE" | ...
    }
    """

    if nlp is None:
        return {"error": "Redaction model not loaded"}

    text = DOC_TEXT.get(doc_id)
    if not text:
        return {"error": "Document text not found"}

    suggestions = []

    # -----------------------------------------
    # 1. ML MODEL (spaCy NER)
    # -----------------------------------------
    try:
        doc = nlp(text)
        for ent in doc.ents:
            suggestions.append({
                "text": ent.text,
                "start": ent.start_char,
                "end": ent.end_char,
                "label": ent.label_ or "SENSITIVE"
            })
    except Exception as e:
        print(f"[WARN] ML model failed: {e}")

    # -----------------------------------------
    # 2. REGEX PII PATTERNS
    # -----------------------------------------
    try:
        pii_suggestions = detect_pii(text)
        suggestions.extend(pii_suggestions)
    except Exception as e:
        print(f"[WARN] PII detection failed: {e}")

    # -----------------------------------------
    # 3. Deduplicate overlapping spans
    # -----------------------------------------
    unique = {}
    for s in suggestions:
        key = (s["start"], s["end"])
        unique[key] = s

    suggestions = list(unique.values())

    # -----------------------------------------
    # 4. Sort by start offset
    # -----------------------------------------
    suggestions.sort(key=lambda x: x["start"])

    return {
        "doc_id": doc_id,
        "suggestions": suggestions,
        "total": len(suggestions)
    }