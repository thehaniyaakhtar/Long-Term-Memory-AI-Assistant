
from io import BytesIO

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

from app.database.database import SessionLocal
from app.memory.memory_service import create_memory
from app.vector_store.qdrant import store_memory_vector


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_file_text(filename, file_bytes):
    filename_lower = filename.lower()

    if filename_lower.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="replace")

    if filename_lower.endswith(".pdf"):
        reader = PdfReader(BytesIO(file_bytes))

        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    raise ValueError("Only TXT and PDF files are supported.")


def split_into_chunks(text, chunk_size=800, overlap=100):
    text = text.strip()

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def save_file_memories(user_id, filename, file_text):
    chunks = split_into_chunks(file_text)

    if not chunks:
        return []

    db = SessionLocal()
    saved = []

    try:
        for index, chunk in enumerate(chunks, start=1):
            memory_text = (
                f"Source file: {filename}. "
                f"Chunk {index}. Content: {chunk}"
            )

            embedding = embedding_model.encode(
                memory_text
            ).tolist()

            memory = create_memory(
                db=db,
                user_id=user_id,
                memory_text=memory_text,
                memory_type="file_memory",
                importance_score=5
            )

            try:
                store_memory_vector(
                    memory_id=memory.id,
                    embedding=embedding
                )
            except Exception:
                db.delete(memory)
                db.commit()
                raise

            saved.append({
                "id": memory.id,
                "memory_text": memory.memory_text,
                "memory_type": memory.memory_type
            })

        return saved

    finally:
        db.close()
