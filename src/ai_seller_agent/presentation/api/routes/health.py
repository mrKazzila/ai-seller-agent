from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ai_seller_agent.catalog.service import CatalogService
from ai_seller_agent.presentation.api.dependencies import get_catalog

router = APIRouter(tags=["System"])


class HealthResponse(BaseModel):
    status: str
    catalog_size: int


@router.get("/health", response_model=HealthResponse)
def health(
    catalog: Annotated[CatalogService, Depends(get_catalog)],
) -> HealthResponse:
    return HealthResponse(
        status="ok",
        catalog_size=len(catalog),
    )
