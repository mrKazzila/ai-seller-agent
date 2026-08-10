from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    loader = CsvCatalogLoader(settings.app.catalog_path)
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
        app_version=settings.app.version,
    )

    yield


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app.name,
        version=settings.app.version,
        lifespan=lifespan,
    )

    setup_routes(app)
    setup_exception_handlers(app)

    return app
