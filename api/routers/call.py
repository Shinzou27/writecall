from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, crud 
from ..database import get_db
router = APIRouter()

@router.post("/api/call", response_model=schemas.Call)
def create_call(call: schemas.CallCreate, db: Session = Depends(get_db)):
    return crud.create_call(db=db, call=call)

@router.get("/api/call/{call_id}", response_model=schemas.Call)
def get_call(call_id: int, db: Session = Depends(get_db)):
    db_call = crud.get_call(db, call_id)
    if db_call is None:
        raise HTTPException(status_code=404, detail="Call não encontrada.")
    return db_call