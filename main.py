from chunking import chunk_text
from embeddings import embed_texts
from vector_store import add_chunks, search_chunks
from generation import generate_answer


def ingest_document(text: str, source_name: str):
    chunks = chunk_text(text)
    embeddings = embed_texts(chunks)
    add_chunks(chunks, embeddings, source_name)
    print(f"Ingested {len(chunks)} chunk dari '{source_name}'")


def rag_query(query: str):
    query_embedding = embed_texts([query])[0]
    chunks, metadatas = search_chunks(query_embedding, n_results=4)

    answer = generate_answer(query, chunks)

    print("\nJawaban:\n", answer)
    print("\nSumber yang dipakai:")
    for meta in metadatas:
        print(f"  - {meta['source']} (chunk #{meta['chunk_index']})")


if __name__ == "__main__":
    contoh_dokumen = """
    ChromaDB adalah vector database open-source yang dirancang untuk
    menyimpan dan mencari embedding secara efisien. ChromaDB mendukung
    penyimpanan in-memory maupun persistent di disk.

    OpenRouter adalah layanan yang menyediakan satu API terpadu untuk
    mengakses berbagai model AI dari banyak provider, termasuk model
    embedding dan model chat/completion.
    """
    ingest_document(contoh_dokumen, source_name="pengantar.txt")

    rag_query("Apa itu ChromaDB dan apa gunanya?")