from sqlalchemy.orm import Session
from apps.verifications.interface import VerificationMethod
from apps.verifications.crud import record_credential, mark_used
import uuid

class BlockchainNFTMethod(VerificationMethod):
    name = "blockchain"

    def generate_credential(self, db: Session, ticket_id: int) -> dict:
        # Simulate NFT minting to a wallet address
        wallet_address = f"0x{uuid.uuid4().hex[:40]}"
        token_id = str(uuid.uuid4())
        credential = {"wallet": wallet_address, "token_id": token_id}
        record_credential(db, ticket_id, self.name, credential)
        return credential

    def verify_credential(self, db: Session, ticket_id: int, presented: dict) -> bool:
        wallet = presented.get("wallet")
        token_id = presented.get("token_id")
        if not wallet or not token_id:
            return False
        return mark_used(db, ticket_id, self.name, {"wallet": wallet, "token_id": token_id})
