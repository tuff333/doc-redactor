from ..state.memory import CHAT_HISTORY, DOC_TEXT
from ..utils.rag_utils import query_rag
from ..utils.llm_utils import ask_llm


def chat_with_doc(doc_id: str, user_message: str):
    if doc_id not in CHAT_HISTORY:
        CHAT_HISTORY[doc_id] = []

    # Retrieve context from RAG
    context = query_rag(doc_id, user_message)

    # Build prompt
    prompt = f"""
You are assisting with a document. Use the context below to answer.

Context:
{context}

User:
{user_message}
"""

    # Ask LLM
    answer = ask_llm(prompt)
    print("DEBUG ANSWER FROM LLM:", repr(answer))


    # Save history
    CHAT_HISTORY[doc_id].append({"user": user_message, "assistant": answer})

    return {"answer": answer, "history": CHAT_HISTORY[doc_id]}