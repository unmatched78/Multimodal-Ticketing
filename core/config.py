#Pydantic BaseSettings (env & defaults)
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "multimodal_ticketing"
    DATABASE_URL: str             # e.g. "postgresql://user:pass@localhost/db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Toggle which verification modes are enabled
    ENABLE_QR: bool = True
    ENABLE_NFC: bool = True
    ENABLE_PASS: bool = True
    ENABLE_BLOCKCHAIN: bool = False
    ENABLE_BIOMETRIC: bool = False
    ENABLE_GEOFENCE: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
