from collections.abc import Callable

import pytest

from ai_seller_agent.catalog.service import CatalogService
from ai_seller_agent.config.settings import MatchingSettings
from ai_seller_agent.domain.enums import MatchStatus
from ai_seller_agent.domain.models import Product, ProductCandidate
from ai_seller_agent.matching.features import FeatureExtractor
from ai_seller_agent.matching.matcher import ProductMatcher
from ai_seller_agent.matching.normalizer import TextNormalizer
from ai_seller_agent.matching.scorer import ProductScorer
from tests.unit.parameters.matcher_results import (
    generate_matcher_result_data,
)


@pytest.mark.unit
@pytest.mark.parametrize(
    ("candidate_data", "expected_status", "expected_skus"),
    generate_matcher_result_data(),
)
def test_build_result(
    candidate_data: list[tuple[str, float]],
    expected_status: MatchStatus,
    expected_skus: list[str],
    candidate_factory: Callable[[str, float], ProductCandidate],
    result_builder: ProductMatcher,
) -> None:
    candidates = [
        candidate_factory(sku, score) for sku, score in candidate_data
    ]

    result = result_builder._build_result(candidates)

    assert result.status is expected_status
    assert [item.product.sku for item in result.candidates] == expected_skus


@pytest.mark.unit
def test_blank_message_is_not_found(product: Product) -> None:
    settings = MatchingSettings()
    matcher = ProductMatcher(
        catalog=CatalogService((product,)),
        normalizer=TextNormalizer(),
        feature_extractor=FeatureExtractor(),
        scorer=ProductScorer(settings),
        settings=settings,
    )

    result = matcher.match("   ")

    assert result.status is MatchStatus.NOT_FOUND
    assert result.candidates == ()
