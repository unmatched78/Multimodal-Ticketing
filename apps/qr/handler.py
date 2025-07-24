import time, jwt
from core.config import settings
from apps.verifications.interface import VerificationMethod
from apps.verifications.crud import record_credential, mark_used

class QRMethod(VerificationMethod):
    name = "qr"

    def generate_credential(self, ticket_id: int) -> dict:
        payload = {"tid": ticket_id, "exp": time.time() + 300}
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        # persist so we can mark it used later
        record_credential(db=... , ticket_id=ticket_id, method=self.name, credential_id=token)
        return {"qr_token": token}

    def verify_credential(self, ticket_id: int, presented: dict) -> bool:
        token = presented.get("qr_token")
        try:
            data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            if data.get("tid") != ticket_id:
                return False
        except jwt.PyJWTError:
            return False
        # mark used exactly once
        return mark_used(db=..., credential_id=token)
