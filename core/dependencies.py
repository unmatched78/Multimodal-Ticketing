#shared FastAPI Depends (e.g. get_db, get_current_user)
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import SessionLocal
from core.security import decode_token
from apps.users import crud as users_crud

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token_data: dict = Depends(decode_token), db: Session = Depends(get_db)):
    user = users_crud.get_user_by_id(db, token_data.get("sub"))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user
