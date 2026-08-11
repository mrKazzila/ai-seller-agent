from ai_seller_agent.application.ports.catalog import ProductCatalog
from ai_seller_agent.application.ports.search import ProductSearch
from ai_seller_agent.domain.enums import MatchStatus
from ai_seller_agent.domain.matching.policy import MatchPolicy
from ai_seller_agent.domain.matching.rules import (
    has_strong_feature_conflict,
)
from ai_seller_agent.domain.models import (
    MatchResult,
    ProductCandidate,
)
from ai_seller_agent.infrastructure.matching.features import FeatureExtractor
from ai_seller_agent.infrastructure.matching.normalizer import TextNormalizer
from ai_seller_agent.infrastructure.matching.scorer import ProductScorer


class ProductMatcher:
    def __init__(
        self,
        *,
        catalog: ProductCatalog,
        search: ProductSearch,
        normalizer: TextNormalizer,
        feature_extractor: FeatureExtractor,
        scorer: ProductScorer,
        policy: MatchPolicy,
    ) -> None:
        self._catalog = catalog
        self._search = search
        self._normalizer = normalizer
        self._feature_extractor = feature_extractor
        self._scorer = scorer
        self._policy = policy

        self._product_texts = {
            product.sku: normalizer.normalize(product.name)
            for product in catalog.products
        }

        self._product_features = {
            product.sku: feature_extractor.extract(
                self._product_texts[product.sku],
            )
            for product in catalog.products
        }

    def match(self, message: str) -> MatchResult:
        query = self._normalizer.normalize(message)

        if not query:
            return MatchResult(
                status=MatchStatus.NOT_FOUND,
                reason="Message is empty after normalization",
            )

        query_features = self._feature_extractor.extract(query)

        candidates: list[ProductCandidate] = []

        for hit in self._search.search(query):
            product = hit.product
            product_text = self._product_texts[product.sku]
            product_features = self._product_features[product.sku]

            if has_strong_feature_conflict(
                query_features,
                product_features,
            ):
                continue

            score = self._scorer.calculate(
                query=query,
                product_text=product_text,
                tfidf_score=hit.lexical_score,
                query_features=query_features,
                product_features=product_features,
            )

            if score.total < self._policy.candidate_threshold:
                continue

            candidates.append(
                ProductCandidate(
                    product=product,
                    score=score.total,
                ),
            )

        return self._policy.decide(candidates)
