from fastapi import FastAPI
from starlette.types import Lifespan

from ai_seller_agent.presentation.api.routes import ROUTERS


def create_app(
    *,
    title: str,
    version: str,
    lifespan: Lifespan[FastAPI] | None = None,
) -> FastAPI:
    app = FastAPI(
        title=title,
        version=version,
        lifespan=lifespan,
    )

    for router in ROUTERS:
        app.include_router(router)

    return app
