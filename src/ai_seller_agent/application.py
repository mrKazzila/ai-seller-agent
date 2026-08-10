from contextlib import asynccontextmanager

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


def create_app() -> FastAPI:
    settings = get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        loader = CsvCatalogLoader(settings.catalog_path)
        catalog = loader.load()

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

        yield

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
    )

    setup_routes(app)
    setup_exception_handlers(app)

    return app
