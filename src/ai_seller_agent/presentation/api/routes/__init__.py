from fastapi import FastAPI

from ai_seller_agent.presentation.api.routes.health import (
    router as health_router,
)
from ai_seller_agent.presentation.api.routes.matching import (
    router as matching_router,
)


def setup_routes(app: FastAPI) -> None:
    app.include_router(health_router)
    app.include_router(matching_router)
