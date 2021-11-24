from fastapi import APIRouter

from src.codegen import collect_types, create_typeddict, reduce_types
from src.models import DictCode, Success

router = APIRouter()


@router.post("", response_model=Success)
async def generate(body: DictCode) -> Success:
    collected = collect_types(body.data)
    types = reduce_types(collected)
    code = create_typeddict(types)
    return Success(data=code)
