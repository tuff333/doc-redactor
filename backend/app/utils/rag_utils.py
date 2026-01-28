from ..state.memory import DOC_TEXT


def ingest_document(doc_id: str, text: str):
    """
    Store text in memory for simple RAG.
    """
    DOC_TEXT[doc_id] = text


def query_rag(doc_id: str, query: str) -> str:
    """
    Simple RAG: return the full document text.
    Later you can replace this with embeddings + vector search.
    """
    return DOC_TEXT.get(doc_id, "")