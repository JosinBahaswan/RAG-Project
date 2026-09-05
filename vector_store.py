import chromadb

# PersistentClient artinya data tersimpan di disk (folder "chroma_db"),
# bukan cuma di memori — jadi tidak hilang saat script selesai jalan.
chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(name="dokumen_saya")


def add_chunks(chunks: list[str], embeddings: list[list[float]], source_name: str):
    ids = [f"{source_name}-{i}" for i in range(len(chunks))]
    metadatas = [{"source": source_name, "chunk_index": i} for i in range(len(chunks))]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )

def search_chunks(query_embedding: list[float], n_results: int = 4):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    return documents, metadatas

def is_already_ingested(source_name: str) -> bool:
    existing = collection.get(where={"source": source_name}, limit=1)
    return len(existing["ids"]) > 0