from ..state.memory import DOC_TEXT
from ..utils.llm_utils import ask_llm


def suggest_for_doc(doc_id: str):
    text = DOC_TEXT.get(doc_id, "")

    prompt = f"""
Extract 5 useful suggestions for improving or understanding this document.

Document:
{text}
"""

    suggestions = ask_llm(prompt)
    return {"suggestions": suggestions}