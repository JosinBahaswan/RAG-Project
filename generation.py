import requests
from config import BASE_URL, HEADERS, CHAT_MODELS


def generate_answer(query: str, context_chunks: list[str]) -> str:
    context_text = "\n\n---\n\n".join(context_chunks)

    system_prompt = (
        "Kamu adalah asisten yang menjawab pertanyaan HANYA berdasarkan "
        "context yang diberikan di bawah. Jika jawabannya tidak ada di "
        "context, katakan kamu tidak tahu — jangan mengarang."
    )
    user_prompt = f"Context:\n{context_text}\n\nPertanyaan: {query}"

    last_error = None
    for model in CHAT_MODELS:
        try:
            response = requests.post(
                url=f"{BASE_URL}/chat/completions",
                headers=HEADERS,
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.exceptions.HTTPError as e:
            print(f"Model '{model}' gagal ({e.response.status_code}), coba model berikutnya...")
            last_error = e
            continue

    raise RuntimeError("Semua model di CHAT_MODELS gagal dipanggil.") from last_error