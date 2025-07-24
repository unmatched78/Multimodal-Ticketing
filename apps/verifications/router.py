from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from apps.tickets.crud import get_ticket
from apps.verifications import registry  # dynamic registry of method handlers

router = APIRouter(prefix="/tickets/{ticket_id}/verify/methods")

@router.get("/{method}/qr")
def generate_qr(ticket_id: int, method: str, db: Session = Depends(get_db)):
    ticket = get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(404, detail="Ticket not found")
    
    handler = registry.get(method)
    if not handler:
        raise HTTPException(404, detail="Verification method not supported")

    if hasattr(handler, "generate_signed_qr"):
        return handler.generate_signed_qr(ticket_id)
    
    return handler.generate_credential(db, ticket_id)

@router.post("/{method}/verify")
def verify(ticket_id: int, method: str, presented: dict, db: Session = Depends(get_db)):
    ticket = get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(404, detail="Ticket not found")

    handler = registry.get(method)
    if not handler:
        raise HTTPException(404, detail="Verification method not supported")

    success = handler.verify_credential(db, ticket_id, presented)
    if not success:
        raise HTTPException(403, detail="Invalid or used credential")

    return {"status": "success", "ticket_id": ticket_id}
