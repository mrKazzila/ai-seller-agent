from ai_seller_agent.presentation.api.routes.health import (
    router as health_router,
)
from ai_seller_agent.presentation.api.routes.matching import (
    router as matching_router,
)

ROUTERS = (
    health_router,
    matching_router,
)
