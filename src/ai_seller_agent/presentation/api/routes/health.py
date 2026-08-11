from fastapi import APIRouter

from ai_seller_agent.presentation.api.routes.types import HealthStatusDep
from ai_seller_agent.presentation.api.schemas.health import HealthResponse

router = APIRouter(tags=["System"])


@router.get("/health")
def health(
    get_health_status: HealthStatusDep,
) -> HealthResponse:
    result = get_health_status.execute()

    return HealthResponse(
        status=result.status,
        catalog_size=result.catalog_size,
    )
