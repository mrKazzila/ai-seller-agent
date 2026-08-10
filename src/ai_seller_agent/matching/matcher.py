from ai_seller_agent.catalog.service import CatalogService
from ai_seller_agent.config.settings import MatchingSettings
from ai_seller_agent.domain.enums import MatchStatus
from ai_seller_agent.domain.models import (
    MatchResult,
    ProductCandidate,
)
from ai_seller_agent.matching.features import FeatureExtractor
from ai_seller_agent.matching.index import ProductSearchIndex
from ai_seller_agent.matching.normalizer import TextNormalizer
from ai_seller_agent.matching.rules import (
    has_strong_feature_conflict,
)
from ai_seller_agent.matching.scorer import ProductScorer


class ProductMatcher:
    def __init__(
        self,
        *,
        catalog: CatalogService,
        normalizer: TextNormalizer,
        feature_extractor: FeatureExtractor,
        scorer: ProductScorer,
        settings: MatchingSettings,
    ) -> None:
        self._catalog = catalog
        self._normalizer = normalizer
        self._feature_extractor = feature_extractor
        self._scorer = scorer
        self._settings = settings

        self._product_texts = tuple(
            normalizer.normalize(product.name) for product in catalog.products
        )
        self._product_features = tuple(
            feature_extractor.extract(text) for text in self._product_texts
        )
        self._index = ProductSearchIndex(self._product_texts)

    def match(self, message: str) -> MatchResult:
        query = self._normalizer.normalize(message)

        if not query:
            return MatchResult(
                status=MatchStatus.NON_PRODUCT,
                reason="Message is empty after normalization",
            )

        query_features = self._feature_extractor.extract(query)
        tfidf_scores = self._index.search(query)

        candidates: list[ProductCandidate] = []

        for index, product in enumerate(self._catalog.products):
            product_features = self._product_features[index]

            if has_strong_feature_conflict(
                query_features,
                product_features,
            ):
                continue

            score = self._scorer.calculate(
                query=query,
                product_text=self._product_texts[index],
                tfidf_score=float(tfidf_scores[index]),
                query_features=query_features,
                product_features=product_features,
            )

            if score.total < self._settings.candidate_threshold:
                continue

            candidates.append(
                ProductCandidate(
                    product=product,
                    score=score.total,
                ),
            )

        candidates.sort(
            key=lambda candidate: candidate.score,
            reverse=True,
        )

        return self._build_result(candidates)

    def _build_result(
        self,
        candidates: list[ProductCandidate],
    ) -> MatchResult:
        if not candidates:
            return MatchResult(status=MatchStatus.NOT_FOUND)

        top = candidates[0]
        selected = tuple(
            candidates[: self._settings.candidates_limit],
        )

        if top.score < self._settings.match_threshold:
            return MatchResult(
                status=MatchStatus.AMBIGUOUS,
                candidates=selected,
            )

        if len(candidates) > 1:
            margin = top.score - candidates[1].score

            if margin < self._settings.minimum_margin:
                return MatchResult(
                    status=MatchStatus.AMBIGUOUS,
                    candidates=selected,
                )

        return MatchResult(
            status=MatchStatus.MATCHED,
            candidates=(top,),
        )
