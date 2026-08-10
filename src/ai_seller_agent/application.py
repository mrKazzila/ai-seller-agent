from collections.abc import Awaitable, Callable
from contextlib import asynccontextmanager
from time import perf_counter
from uuid import uuid4

import structlog
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from structlog.contextvars import bind_contextvars, clear_contextvars

from ai_seller_agent.catalog.loader import CsvCatalogLoader
from ai_seller_agent.catalog.service import CatalogService
from ai_seller_agent.config.settings import get_settings
from ai_seller_agent.matching.features import FeatureExtractor
from ai_seller_agent.matching.matcher import ProductMatcher
from ai_seller_agent.matching.normalizer import TextNormalizer
from ai_seller_agent.matching.scorer import ProductScorer
from ai_seller_agent.presentation.api.exception_handlers import (
    setup_exception_handlers,
)
from ai_seller_agent.presentation.api.routes import setup_routes

logger = structlog.get_logger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        loader = CsvCatalogLoader(settings.catalog_path)
        catalog = loader.load()
        logger.info("catalog_loaded", product_count=len(catalog))

        catalog_service = CatalogService(catalog)
        normalizer = TextNormalizer()
        feature_extractor = FeatureExtractor()
        scorer = ProductScorer(settings.matching)

        matcher = ProductMatcher(
            catalog=catalog_service,
            normalizer=normalizer,
            feature_extractor=feature_extractor,
            scorer=scorer,
            settings=settings.matching,
        )

        app.state.catalog = catalog_service
        app.state.matcher = matcher
        logger.info(
            "application_ready",
            app_version=settings.app_version,
        )

        yield

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
    )

    @app.middleware("http")
    async def request_logging_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = request.headers.get("x-request-id") or str(uuid4())
        clear_contextvars()
        bind_contextvars(request_id=request_id)
        started = perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            logger.exception(
                "request_failed",
                method=request.method,
                route=str(request.url.path),
                duration_ms=round((perf_counter() - started) * 1000, 2),
            )
            raise
        response.headers["x-request-id"] = request_id
        logger.info(
            "request_completed",
            method=request.method,
            route=str(request.url.path),
            status_code=response.status_code,
            duration_ms=round((perf_counter() - started) * 1000, 2),
        )
        return response

    setup_routes(app)
    setup_exception_handlers(app)

    return app
