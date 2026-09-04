import requests
from config import BASE_URL, HEADERS, EMBED_MODEL


def embed_texts(texts: list[str]) -> list[list[float]]:
    response = requests.post(
        url=f"{BASE_URL}/embeddings",
        headers=HEADERS,
        json={
            "model": EMBED_MODEL,
            "input": texts,
        },
    )
    response.raise_for_status()
    data = response.json()

    # data['data'] adalah list, urut sesuai urutan 'texts' yang dikirim
    return [item["embedding"] for item in data["data"]]