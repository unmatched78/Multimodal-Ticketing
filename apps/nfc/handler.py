import uuid
from sqlalchemy.orm import Session
from apps.verifications.interface import VerificationMethod
from apps.verifications.crud import record_credential, mark_used

class NFCMethod(VerificationMethod):
    name = "nfc"

    def generate_credential(self, db: Session, ticket_id: int) -> dict:
        # Simulate generating a unique NFC tag ID
        tag_id = str(uuid.uuid4())
        record_credential(db, ticket_id, self.name, tag_id)
        return {"nfc_tag_id": tag_id}

    def verify_credential(self, db: Session, ticket_id: int, presented: dict) -> bool:
        tag_id = presented.get("nfc_tag_id")
        if not tag_id:
            return False
        return mark_used(db, ticket_id, self.name, tag_id)
