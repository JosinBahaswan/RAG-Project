import re

def split_into_sentences(text: str) -> list[str]:
    # Potong di titik/tanda tanya/tanda seru yang diikuti spasi atau baris baru
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if s.strip()]

def split_into_paragraphs(text: str) -> list[str]:
    paragraphs = re.split(r"\n\s*\n", text.strip())
    return [p.strip() for p in paragraphs if p.strip()] 

def get_trailing_sentences(text: str, overlap: int) -> str:
    sentences = split_into_sentences(text)
    trailing = []
    total_len = 0

    for sentence in reversed(sentences):
        if total_len + len(sentence) > overlap:
            break
        trailing.insert(0, sentence)
        total_len += len(sentence)

    return " ".join(trailing)

def semantic_chunk(text: str, max_chunk_size: int = 800, overlap: int = 100) -> list[str]:
    paragraphs = split_into_paragraphs(text)
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(paragraph) > max_chunk_size:
            sentences = split_into_sentences(paragraph)
            for sentence in sentences:
                if len(current_chunk) + len(sentence) > max_chunk_size:
                    if current_chunk:
                        overlap_text = get_trailing_sentences(current_chunk, overlap)
                        chunks.append(current_chunk.strip())
                        current_chunk = (overlap_text + " " + sentence) if overlap_text else sentence
                    else:
                        current_chunk = sentence
                else:
                    current_chunk += (" " + sentence) if current_chunk else sentence
        else:
            if len(current_chunk) + len(paragraph) > max_chunk_size:
                if current_chunk:
                    overlap_text = get_trailing_sentences(current_chunk, overlap)
                    chunks.append(current_chunk.strip())
                    current_chunk = (overlap_text + "\n\n" + paragraph) if overlap_text else paragraph
                else:
                    current_chunk = paragraph
            else:
                current_chunk += ("\n\n" + paragraph) if current_chunk else paragraph

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks