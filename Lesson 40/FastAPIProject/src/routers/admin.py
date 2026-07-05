from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, responses
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from ..db.connector import get_session, check_database
from ..settings import settings
from ..services.seed import generate_test_data

router = APIRouter()

class SeedResponse(BaseModel):
    status: str
    message: str

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.get("/health/db")
async def readiness_check(session: Annotated[AsyncSession, Depends(get_session)]):
    if await check_database(session):
        return {"status": "ready", "database": "connected"}
    else:
        return responses.JSONResponse(
            status_code=503, #  Service Unavailable
            content={"status": "not ready", "database": "disconnected"}
        )

@router.post("/seed", response_model=SeedResponse)
async def seed_data(secret: str, session: Annotated[AsyncSession, Depends(get_session)]):
    # создание тестовых данных
    if secret != settings.SEED_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")

    await generate_test_data(session)
    return {"status": "ok", "message": "Test data seeded successfully"}
