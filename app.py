import os
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from document_loader import load_document
from main import ingest_document

from pydantic import BaseModel
from main import get_answer

app = FastAPI(title="Mini RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ganti sesuai domain frontend kamu
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/ingest")
async def ingest_endpoint(file:UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1]
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
        
    try:
        text = load_document(tmp_path)
        ingest_document(text, source_name=file.filename)
    finally:
        os.remove(tmp_path)
        
    return {"message": f"'{file.filename}' berhasil diproses"}

@app.post("/query")
def query_endpoint(request: QueryRequest):
    result = get_answer(request.question)
    return result