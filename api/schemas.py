from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CallBase(BaseModel):
    name: str

class CallCreate(CallBase):
    pass

class Call(CallBase):
    id: int

    class Config:
        orm_mode = True

class AudioChunkBase(BaseModel):
    audio_file: str
    created_at: datetime
    updated_at: datetime

class AudioChunkCreate(AudioChunkBase):
    pass

class AudioChunk(AudioChunkBase):
    id: int
    call_id: int

    class Config:
        orm_mode = True

class TranscriptionBase(BaseModel):
    text: str
    created_at: datetime
    updated_at: datetime

class TranscriptionCreate(TranscriptionBase):
    audio_chunk_id: int 
    text: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Transcription(TranscriptionBase):
    id: int
    audio_chunk_id: int

    class Config:
        orm_mode = True