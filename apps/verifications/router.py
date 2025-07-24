from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_current_user
from apps.verifications.registry import get_method, list_methods

router = APIRouter(prefix="/tickets/{ticket_id}/verify", tags=["verifications"])

@router.get("/methods")
def available_methods():
    return {"methods": list_methods()}

@router.post("/methods/{method}/generate")
def generate(ticket_id: int, method: str, db: Session = Depends(get_db),
             user = Depends(get_current_user)):
    verifier = get_method(method)
    if not verifier:
        raise HTTPException(404, "Method not supported")
    return verifier.generate_credential(ticket_id)

@router.post("/methods/{method}/verify")
def verify(ticket_id: int, method: str, payload: dict,
           db: Session = Depends(get_db)):
    verifier = get_method(method)
    if not verifier:
        raise HTTPException(404, "Method not supported")
    ok = verifier.verify_credential(ticket_id, payload)
    if not ok:
        raise HTTPException(400, "Invalid or replayed credential")
    return {"status": "ok"}
