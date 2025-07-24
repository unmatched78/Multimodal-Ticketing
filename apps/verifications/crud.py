from sqlalchemy.orm import Session
from .models import CredentialRecord

def record_credential(db: Session, ticket_id: int, method: str, credential_id: str):
    rec = CredentialRecord(
        ticket_id=ticket_id,
        method_name=method,
        credential_id=credential_id
    )
    db.add(rec)
    db.commit()

def mark_used(db: Session, credential_id: str) -> bool:
    rec = db.query(CredentialRecord)\
            .filter_by(credential_id=credential_id, used_at=None)\
            .first()
    if not rec:
        return False
    rec.used_at = func.now()
    db.commit()
    return True
