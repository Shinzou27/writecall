from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
import os
from .. import models, schemas, crud 
from ..database import get_db

router = APIRouter()

AUDIO_UPLOAD_FOLDER = "api/media/audio"

os.makedirs(AUDIO_UPLOAD_FOLDER, exist_ok=True)

@router.post("/api/audio/", response_model=schemas.AudioChunk)
async def create_audio_chunk(
    call_id: int = Form(...), 
    audio_file: UploadFile = File(...), 
    db: Session = Depends(get_db),
):

    file_path = os.path.join(AUDIO_UPLOAD_FOLDER, audio_file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(audio_file.file, f)


    audio_chunk = crud.create_audio_chunk(db=db, call_id=call_id, file_path=file_path)

    return audio_chunk


@router.get("/api/audio/list/{call_id}", response_model=list[schemas.AudioChunk])
def get_audio_chunks(call_id: int, db: Session = Depends(get_db)):
    audio_chunks = crud.get_audio_chunks_by_call_id(db, call_id)
    if not audio_chunks:
        raise HTTPException(status_code=404, detail="Esta call não tem áudios associados.")
    return audio_chunks
