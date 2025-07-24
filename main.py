from fastapi import FastAPI
from core.config import settings
from core.dependencies import engine, Base
from apps.verifications.registry import register_method
from apps.qr.handler import QRMethod
from apps.verifications.router import router as verifications_router
# ... import users_router, tickets_router

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# Register verification methods
register_method(QRMethod())

# Include routers
app.include_router(verifications_router)
# app.include_router(users_router)
# app.include_router(tickets_router)
