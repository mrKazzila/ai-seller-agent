from collections.abc import Callable
from decimal import Decimal

import pytest

from ai_seller_agent.domain.enums import MatchStatus
from ai_seller_agent.domain.matching.policy import MatchPolicy
from ai_seller_agent.domain.models import Product, ProductCandidate
from ai_seller_agent.infrastructure.catalog.in_memory import (
    InMemoryProductCatalog,
)
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
from tests.unit.parameters.matcher_results import (
    generate_matcher_result_data,
)


@pytest.mark.unit
@pytest.mark.parametrize(
    ("candidate_data", "expected_status", "expected_skus"),
    generate_matcher_result_data(),
)
def test_match_policy_decision(
    candidate_data: list[tuple[str, float]],
    expected_status: MatchStatus,
    expected_skus: list[str],
    candidate_factory: Callable[[str, float], ProductCandidate],
    match_policy: MatchPolicy,
) -> None:
    candidates = [
        candidate_factory(sku, score)
        for sku, score in candidate_data
    ]

    result = match_policy.decide(candidates)

    assert result.status is expected_status
    assert [item.product.sku for item in result.candidates] == expected_skus

@pytest.mark.unit
def test_blank_message_is_not_found(
    product: Product,
    match_policy: MatchPolicy,
    scoring_weights: ScoringWeights,
) -> None:
    products = (product,)
    normalizer = TextNormalizer()

    search = TfidfProductSearch(
        products=products,
        normalizer=normalizer,
    )

    matcher = ProductMatcher(
        catalog=InMemoryProductCatalog(products),
        search=search,
        normalizer=normalizer,
        feature_extractor=FeatureExtractor(),
        scorer=ProductScorer(scoring_weights),
        policy=match_policy,
    )
    result = matcher.match("   ")

    assert result.status is MatchStatus.NOT_FOUND
    assert result.candidates == ()


@pytest.mark.unit
def test_measurement_conflict_excludes_wrong_size(
    match_policy: MatchPolicy,
    scoring_weights: ScoringWeights,
) -> None:
    products = (
        Product(
            sku="DSK-0022",
            name="Диск лепестковый торцевой 115 мм P60",
            unit="шт",
            price=Decimal("174.45"),
        ),
        Product(
            sku="DSK-0026",
            name="Диск лепестковый торцевой 125 мм P60",
            unit="шт",
            price=Decimal("195.37"),
        ),
    )

    normalizer = TextNormalizer()

    search = TfidfProductSearch(
        products=products,
        normalizer=normalizer,
    )

    matcher = ProductMatcher(
        catalog=InMemoryProductCatalog(products),
        search=search,
        normalizer=normalizer,
        feature_extractor=FeatureExtractor(),
        scorer=ProductScorer(scoring_weights),
        policy=match_policy,
    )

    result = matcher.match("Диск лепестковый торцевой 115 мм P60")

    assert result.status is MatchStatus.MATCHED
    assert [item.product.sku for item in result.candidates] == ["DSK-0022"]
