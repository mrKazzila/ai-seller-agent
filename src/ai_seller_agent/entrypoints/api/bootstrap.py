from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from starlette.types import Lifespan

from ai_seller_agent.application.use_cases.get_health_status import (
    GetHealthStatus,
)
from ai_seller_agent.application.use_cases.match_messages import MatchMessages
from ai_seller_agent.config.settings import Settings, get_settings
from ai_seller_agent.domain.matching.policy import MatchPolicy
from ai_seller_agent.infrastructure.catalog.exceptions import (
    CatalogLoadError,
    EmptyCatalogError,
)
from ai_seller_agent.infrastructure.catalog.in_memory import (
    InMemoryProductCatalog,
)
from ai_seller_agent.infrastructure.catalog.loader import CsvCatalogLoader
from ai_seller_agent.infrastructure.matching.features import FeatureExtractor
from ai_seller_agent.infrastructure.matching.matcher import ProductMatcher
from ai_seller_agent.infrastructure.matching.normalizer import TextNormalizer
from ai_seller_agent.infrastructure.matching.scorer import (
    ProductScorer,
    ScoringWeights,
)
from ai_seller_agent.infrastructure.matching.search import (
    TfidfProductSearch,
)
from ai_seller_agent.presentation.api.application import (
    create_app as create_http_app,
)

logger = structlog.get_logger(__name__)


def create_lifespan(settings: Settings) -> Lifespan[FastAPI]:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        try:
            loader = CsvCatalogLoader(settings.app.catalog_path)
            products = loader.load()
            catalog = InMemoryProductCatalog(products)
        except (CatalogLoadError, EmptyCatalogError):
            logger.exception("application_startup_failed")
            raise

        logger.info(
            "catalog_loaded",
            product_count=len(products),
        )

        normalizer = TextNormalizer()
        search = TfidfProductSearch(
            products=catalog.products,
            normalizer=normalizer,
        )

        feature_extractor = FeatureExtractor()
        scoring_weights = ScoringWeights(
            tfidf=settings.matching.tfidf_weight,
            fuzzy=settings.matching.fuzzy_weight,
            features=settings.matching.feature_weight,
        )

        scorer = ProductScorer(scoring_weights)

        policy = MatchPolicy(
            match_threshold=settings.matching.match_threshold,
            candidate_threshold=settings.matching.candidate_threshold,
            minimum_margin=settings.matching.minimum_margin,
            candidates_limit=settings.matching.candidates_limit,
        )

        matcher = ProductMatcher(
            catalog=catalog,
            search=search,
            normalizer=normalizer,
            feature_extractor=feature_extractor,
            scorer=scorer,
            policy=policy,
        )

        app.state.get_health_status = GetHealthStatus(catalog)
        app.state.match_messages = MatchMessages(matcher)

        logger.info(
            "application_ready",
            app_version=settings.app.version,
        )

        yield

    return lifespan


def create_application(
    settings: Settings | None = None,
) -> FastAPI:
    resolved_settings = settings or get_settings()

    return create_http_app(
        title=resolved_settings.app.name,
        version=resolved_settings.app.version,
        lifespan=create_lifespan(resolved_settings),
    )
