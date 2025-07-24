from abc import ABC, abstractmethod

class VerificationMethod(ABC):
    name: str  # unique identifier, e.g. "qr", "nfc"

    @abstractmethod
    def generate_credential(self, ticket_id: int) -> dict:
        """
        Returns whatever payload the client needs
        (e.g. {'qr_token': '…'}).
        """
        pass

    @abstractmethod
    def verify_credential(self, ticket_id: int, presented: dict) -> bool:
        """
        Accepts the client‑presented data and returns True if valid.
        """
        pass
