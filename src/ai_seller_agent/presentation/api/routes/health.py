from fastapi import APIRouter

from ai_seller_agent.presentation.api.routes.types import CatalogDep
from ai_seller_agent.presentation.api.schemas.health import HealthResponse

router = APIRouter(tags=["System"])


@router.get("/health")
def health(
    catalog: CatalogDep,
) -> HealthResponse:
    return HealthResponse(
        status="ok",
        catalog_size=len(catalog),
    )
