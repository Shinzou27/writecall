from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, crud 
from ..database import get_db

router = APIRouter()
@router.post("/api/transcription", response_model=schemas.Transcription)
def create_transcription(
    transcription: schemas.TranscriptionCreate, db: Session = Depends(get_db)
):
    print(transcription)
    created_transcription = crud.create_transcription(db=db, transcription=transcription)
    print(created_transcription)
    return created_transcription


@router.get("/api/transcription/{call_id}", response_model=list[schemas.Transcription])
def get_transcriptions(call_id: int, db: Session = Depends(get_db)):

    audio_chunks = crud.get_audio_chunks_by_call_id(db, call_id)
    if not audio_chunks:
        raise HTTPException(status_code=404, detail="Esta call não tem áudios associados.")


    transcriptions = crud.get_transcriptions_by_audio_chunks(db, audio_chunks)
    if not transcriptions:
        raise HTTPException(status_code=404, detail="Não foram encontradas transcrições nesta call.")

    return transcriptions
