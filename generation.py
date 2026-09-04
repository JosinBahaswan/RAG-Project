import requests
from config import BASE_URL, HEADERS, CHAT_MODEL


def generate_answer(query: str, context_chunks: list[str]) -> str:
    context_text = "\n\n---\n\n".join(context_chunks)

    system_prompt = (
        "Kamu adalah asisten yang menjawab pertanyaan HANYA berdasarkan "
        "context yang diberikan di bawah. Jika jawabannya tidak ada di "
        "context, katakan kamu tidak tahu — jangan mengarang. "
        "Jawab langsung dan ringkas, cukup 1-2 kalimat, tanpa bullet point "
        "kecuali user secara eksplisit minta rincian."
    )
    user_prompt = f"Context:\n{context_text}\n\nPertanyaan: {query}"

    response = requests.post(
        url=f"{BASE_URL}/chat/completions",
        headers=HEADERS,
        json={
            "model": CHAT_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        },
    )
    response.raise_for_status()
    data = response.json()

    return data["choices"][0]["message"]["content"]