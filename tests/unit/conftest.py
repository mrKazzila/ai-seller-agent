import logging
from collections.abc import Callable, Iterator
from decimal import Decimal

import pytest

from ai_seller_agent.config.settings import MatchingSettings
from ai_seller_agent.domain.models import Product, ProductCandidate
from ai_seller_agent.infrastructure.matching.matcher import ProductMatcher
from ai_seller_agent.infrastructure.observability import reset_logging


@pytest.fixture
def product() -> Product:
    return Product(
        sku="SKU-1",
        name="Саморез по дереву 4.2х75",
        unit="шт",
        price=Decimal("1.00"),
    )


@pytest.fixture
def candidate_factory() -> Callable[[str, float], ProductCandidate]:
    def create_candidate(sku: str, score: float) -> ProductCandidate:
        return ProductCandidate(
            product=Product(
                sku=sku,
                name=sku,
                unit="шт",
                price=Decimal("1.00"),
            ),
            score=score,
        )

    return create_candidate


@pytest.fixture
def result_builder() -> ProductMatcher:
    matcher = object.__new__(ProductMatcher)
    matcher._settings = MatchingSettings()
    return matcher


@pytest.fixture
def restore_logging_state() -> Iterator[None]:
    root = logging.getLogger()
    original_handlers = root.handlers[:]
    original_level = root.level
    httpx_logger = logging.getLogger("httpx")
    original_httpx_level = httpx_logger.level

    yield

    reset_logging()
    root.handlers = original_handlers
    root.setLevel(original_level)
    httpx_logger.setLevel(original_httpx_level)
