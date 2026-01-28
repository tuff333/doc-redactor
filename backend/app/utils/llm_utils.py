import requests
import json

def ask_llm(prompt: str) -> str:
    """
    Correct streaming handler for Ollama /api/generate.
    Collects all chunks and returns the full response text.
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3:latest", "prompt": prompt},
            stream=True,
            timeout=60
        )

        full_answer = ""

        for line in response.iter_lines():
            if not line:
                continue

            data = json.loads(line.decode("utf-8"))

            if "response" in data:
                full_answer += data["response"]

            if data.get("done"):
                break

        return full_answer.strip()

    except Exception as e:
        return f"[LLM Error] {e}"
