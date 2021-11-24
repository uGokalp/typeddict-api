from fastapi import APIRouter

from src.models import Success

router = APIRouter()


@router.get("/", response_model=Success)
async def ping() -> Success:
    return Success(data="")
