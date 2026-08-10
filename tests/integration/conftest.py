from collections.abc import Iterator, Mapping
from decimal import Decimal

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from ai_seller_agent.application import create_app
from ai_seller_agent.domain.enums import MatchStatus
from ai_seller_agent.domain.models import (
    MatchResult,
    Product,
    ProductCandidate,
)
from ai_seller_agent.presentation.api.dependencies import get_matcher


class StubMatcher:
    def __init__(self, results: Mapping[str, MatchResult]) -> None:
        self._results = results

    def match(self, message: str) -> MatchResult:
        return self._results.get(
            message,
            MatchResult(status=MatchStatus.NOT_FOUND),
        )


def candidate(sku: str, score: float) -> ProductCandidate:
    return ProductCandidate(
        product=Product(
            sku=sku,
            name=f"Product {sku}",
            unit="шт",
            price=Decimal("100.00"),
        ),
        score=score,
    )


@pytest.fixture
def integration_app() -> Iterator[FastAPI]:
    app = create_app()
    matcher = StubMatcher(
        {
            "exact": MatchResult(
                status=MatchStatus.MATCHED,
                candidates=(candidate("SKU-1", 0.87654),),
            ),
            "broad": MatchResult(
                status=MatchStatus.AMBIGUOUS,
                candidates=(
                    candidate("SKU-2", 0.72),
                    candidate("SKU-3", 0.68),
                    candidate("SKU-4", 0.61),
                ),
            ),
        },
    )
    app.dependency_overrides[get_matcher] = lambda: matcher

    yield app

    app.dependency_overrides.clear()


@pytest.fixture
def client(integration_app: FastAPI) -> Iterator[TestClient]:
    test_client = TestClient(integration_app)

    yield test_client

    test_client.close()
