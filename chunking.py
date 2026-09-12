import re

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks

def split_into_sentences(text: str) -> list[str]:
    # Potong di titik/tanda tanya/tanda seru yang diikuti spasi atau baris baru
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if s.strip()]

def split_into_paragraphs(text: str) -> list[str]:
    paragraphs = re.split(r"\n\s*\n", text.strip())
    return [p.strip() for p in paragraphs if p.strip()] 

def semantic_chunk(text: str, max_chunk_size: int = 800) -> list[str]:
    paragraphs = split_into_paragraphs(text)
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(paragraph) > max_chunk_size:
            # Paragraf ini sendiri kepanjangan, pecah jadi kalimat
            sentences = split_into_sentences(paragraph)
            for sentence in sentences:
                if len(current_chunk) + len(sentence) > max_chunk_size:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence
                else:
                    current_chunk += (" " + sentence) if current_chunk else sentence
        else:
            # Paragraf muat utuh, coba gabung ke chunk yang sedang dibangun
            if len(current_chunk) + len(paragraph) > max_chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph
            else:
                current_chunk += ("\n\n" + paragraph) if current_chunk else paragraph

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks