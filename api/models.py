from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from datetime import datetime
class Call(Base):
    __tablename__ = "calls"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class AudioChunk(Base):
    __tablename__ = "audio_chunks"
    id = Column(Integer, primary_key=True, index=True)
    audio_file = Column(String, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    call_id = Column(Integer, ForeignKey("calls.id"))

    call = relationship("Call")

class Transcription(Base):
    __tablename__ = "transcriptions"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    audio_chunk_id = Column(Integer, ForeignKey("audio_chunks.id"))

    audio_chunk = relationship("AudioChunk")
