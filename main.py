from chunking import chunk_text
from embeddings import embed_texts
from vector_store import add_chunks, search_chunks, is_already_ingested
from generation import generate_answer
from document_loader import load_documents_from_folder

def ingest_document(text: str, source_name: str):
    if is_already_ingested(source_name):
        print(f"Lewati '{source_name}', sudah pernah di-ingest sebelumnya.")
        return
    
    chunks = chunk_text(text)
    embeddings = embed_texts(chunks)
    add_chunks(chunks, embeddings, source_name)
    print(f"Ingested {len(chunks)} chunk dari '{source_name}'")

def ingest_folder(folder_path: str):
    documents = load_documents_from_folder(folder_path)

    if not documents:
        print(f"Tidak ada dokumen yang didukung di folder '{folder_path}'")
        return

    for source_name, text in documents:
        ingest_document(text, source_name)
        
def rag_query(query: str):
    query_embedding = embed_texts([query])[0]
    chunks, metadatas = search_chunks(query_embedding, n_results=4)

    answer = generate_answer(query, chunks)

    print("\nJawaban:\n", answer)
    print("\nSumber yang dipakai:")
    for meta in metadatas:
        print(f"  - {meta['source']} (chunk #{meta['chunk_index']})")

if __name__ == "__main__":
    ingest_folder("./dokumen")

    print("\nDokumen siap. Ketik pertanyaan kamu (ketik 'exit' untuk keluar).\n")

    while True:
        query = input("Pertanyaan: ").strip()

        if query.lower() in ("exit", "quit"):
            print("Selesai.")
            break

        if not query:
            continue

        rag_query(query)