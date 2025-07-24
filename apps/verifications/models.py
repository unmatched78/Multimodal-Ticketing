from sqlalchemy import Column, Integer, String, DateTime, func
from db.base import Base

class CredentialRecord(Base):
    __tablename__ = "credential_records"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, nullable=False, index=True)
    method_name = Column(String, nullable=False, index=True)
    credential_id = Column(String, nullable=False, unique=True)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    used_at = Column(DateTime(timezone=True), nullable=True)
