from sqlalchemy.orm import Session
from . import models, schemas

def add_to_db(db, model):
    db.add(model)
    db.commit()
    db.refresh(model)
    return model
def create_call(db: Session, call: schemas.CallCreate):
    db_call = models.Call(name=call.name)
    return add_to_db(db, db_call)

def get_call(db: Session, call_id: int):
    return db.query(models.Call).filter(models.Call.id == call_id).first()

def create_audio_chunk(db: Session, call_id: int, file_path: str):
    db_audio_chunk = models.AudioChunk(call_id=call_id, audio_file=file_path)
    return add_to_db(db, db_audio_chunk)

def get_audio_chunks_by_call_id(db: Session, call_id: int):
    return db.query(models.AudioChunk).filter(models.AudioChunk.call_id == call_id).all()

def create_transcription(db: Session, transcription: schemas.TranscriptionCreate):
    db_transcription = models.Transcription(
        text=transcription.text,
        audio_chunk_id=transcription.audio_chunk_id
    )
    return add_to_db(db, db_transcription)

def get_transcriptions_by_audio_chunks(db: Session, audio_chunks: list[models.AudioChunk]):
    audio_chunk_ids = [audio_chunk.id for audio_chunk in audio_chunks]
    return db.query(models.Transcription).filter(models.Transcription.audio_chunk_id.in_(audio_chunk_ids)).all()