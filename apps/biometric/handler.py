import face_recognition
import base64
import numpy as np
from sqlalchemy.orm import Session
from apps.verifications.interface import VerificationMethod
from apps.verifications.crud import record_credential, mark_used

class BiometricMethod(VerificationMethod):
    name = "biometric"

    def generate_credential(self, db: Session, ticket_id: int, face_image_b64: str) -> dict:
        image_data = base64.b64decode(face_image_b64)
        image = face_recognition.load_image_file(io.BytesIO(image_data))
        encodings = face_recognition.face_encodings(image)
        if not encodings:
            raise ValueError("No face detected")
        face_vector = encodings[0].tolist()
        credential = {"face_vector": face_vector}
        record_credential(db, ticket_id, self.name, credential)
        return credential

    def verify_credential(self, db: Session, ticket_id: int, presented: dict) -> bool:
        live_b64 = presented.get("live_image_b64")
        image_data = base64.b64decode(live_b64)
        image = face_recognition.load_image_file(io.BytesIO(image_data))
        encodings = face_recognition.face_encodings(image)
        if not encodings:
            return False
        live_vector = encodings[0]

        stored = self.get_stored_credential(db, ticket_id)
        reference_vector = np.array(stored["face_vector"])

        # Compare face encodings
        distance = np.linalg.norm(live_vector - reference_vector)
        match = distance < 0.6  # threshold
        if match:
            return mark_used(db, ticket_id, self.name, {"used": True, "distance": distance})
        return False
