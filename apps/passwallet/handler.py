import time, hmac, hashlib
from sqlalchemy.orm import Session
from apps.verifications.interface import VerificationMethod
from apps.verifications.crud import record_credential, mark_used

SECRET_KEY = b"supersecret"  # later use env var or vault

class PassWalletMethod(VerificationMethod):
    name = "passwallet"

    def generate_credential(self, db: Session, ticket_id: int) -> dict:
        # Store only a base ID — token will rotate client-side
        credential = {"base_id": f"ticket-{ticket_id}"}
        record_credential(db, ticket_id, self.name, credential)
        return credential

    def generate_rotating_token(self, base_id: str, timestamp: int = None):
        if timestamp is None:
            timestamp = int(time.time() // 30)  # rotate every 30s
        msg = f"{base_id}:{timestamp}".encode()
        signature = hmac.new(SECRET_KEY, msg, hashlib.sha256).hexdigest()
        return {"token": signature, "timestamp": timestamp}

    def verify_credential(self, db: Session, ticket_id: int, presented: dict) -> bool:
        base_id = f"ticket-{ticket_id}"
        token = presented.get("token")
        ts = presented.get("timestamp")

        # Check current and previous windows (grace window)
        for offset in (0, -1):
            test_ts = ts + offset
            valid_token = self.generate_rotating_token(base_id, test_ts)["token"]
            if hmac.compare_digest(valid_token, token):
                return mark_used(db, ticket_id, self.name, {"used": True})
        return False
