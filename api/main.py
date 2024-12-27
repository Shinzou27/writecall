from fastapi import FastAPI
from api.database import engine, Base
from .routers import call, audio, transcription
app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"msg": "Olá!"}

app.include_router(call.router)
app.include_router(audio.router)
app.include_router(transcription.router)