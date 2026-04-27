import logging

from fastapi import APIRouter, HTTPException

from . import model
from .schemas import FilterRequest, FilterResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/v1/privacy-filter", response_model=FilterResponse)
async def privacy_filter(request: FilterRequest) -> FilterResponse:
    if not request.inputs:
        return FilterResponse(results=[])
    try:
        results = await model.process_batch(request.inputs)
    except Exception:
        logger.exception("Inference failed")
        raise HTTPException(status_code=500, detail="Inference failed")
    return FilterResponse(results=results)


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
