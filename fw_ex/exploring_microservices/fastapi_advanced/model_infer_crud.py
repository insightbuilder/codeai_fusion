from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from cryptography.fernet import Fernet
import onnxruntime as ort
import os
import shutil
from transformers import BertTokenizer
import numpy as np

# Load the BERT tokenizer for input processing
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

app = FastAPI()

DB_URL = "sqlite:///./model_loader.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class UserRequest(Base):
    __tablename__ = "user_requests"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    process_text = Column(String)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()


class RequestCreate(BaseModel):
    filename: str


onnx_model_path = "bert_model.onnx"

if not os.path.exists(onnx_model_path):
    raise FileNotFoundError("Model missing")

ort_session = ort.InferenceSession(onnx_model_path)


def run_inference(input_text: str) -> str:
    # Tokenize the input text
    inputs = tokenizer(
        input_text, return_tensors="np"
    )  # Use NumPy format for ONNX runtime

    # Extract input_ids and attention_mask for the ONNX model
    onnx_inputs = {
        "input_ids": inputs["input_ids"].astype(
            np.int64
        ),  # Ensure input is in int64 format
        "attention_mask": inputs["attention_mask"].astype(np.int64),
    }
    outputs = ort_session.run(None, onnx_inputs)
    outputs = outputs[0][0]
    processed_text_str = " ".join(map(str, outputs))
    return processed_text_str


@app.post("/upload/", response_model=dict)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "text/plain":
        raise HTTPException(status_code=400, detail="Only.txt files")

    file_location = f"./uploaded_files/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(file_location, "r") as f:
        content = f.read()

    proc_text = run_inference(content)

    db_req = UserRequest(filename=file.filename, process_text=proc_text)
    db.add(db_req)
    db.commit()
    db.refresh(db_req)

    return {"filename": proc_text}


@app.get("/download/{filename}", response_class=FileResponse)
async def download_file(filename: str):
    file_path = f"/processed_files/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="file not found")
    return file_path


@app.get("/requests/", response_model=list)
async def get_requests(db: Session = Depends(get_db)):
    return db.query(UserRequest).all()


@app.get("/requests/{req_id}", response_model=dict)
async def get_request(req_id: int, db: Session = Depends(get_db)):
    req = db.query(UserRequest).filter(UserRequest.id == req_id).first()
    if req is None:
        raise HTTPException(status_code=404, detail="req id not found")
    return {"id": req.id, "file": req.filename}


@app.delete("/requests/{req_id}", response_model=dict)
async def del_request(req_id: int, db: Session = Depends(get_db)):
    req = db.query(UserRequest).filter(UserRequest.id == req_id).first()
    if req is None:
        raise HTTPException(status_code=404, detail="req id not found")
    db.delete(req)
    db.commit()
    return {"detail": "request deleted"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
