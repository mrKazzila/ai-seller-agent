from dataclasses import dataclass

from rapidfuzz import fuzz

from ai_seller_agent.domain.matching.features import TextFeatures


@dataclass(frozen=True, slots=True)
class ScoringWeights:
    tfidf: float
    fuzzy: float
    features: float


@dataclass(frozen=True, slots=True)
class ScoreDetails:
    total: float
    tfidf: float
    fuzzy: float
    features: float


class ProductScorer:
    def __init__(self, weights: ScoringWeights) -> None:
        self._weights = weights

    def calculate(
        self,
        *,
        query: str,
        product_text: str,
        tfidf_score: float,
        query_features: TextFeatures,
        product_features: TextFeatures,
    ) -> ScoreDetails:
        fuzzy_score = fuzz.WRatio(query, product_text) / 100
        feature_score = self._calculate_feature_score(
            query_features,
            product_features,
        )

        total = (
            self._weights.tfidf * tfidf_score
            + self._weights.fuzzy * fuzzy_score
            + self._weights.features * feature_score
        )

        return ScoreDetails(
            total=total,
            tfidf=tfidf_score,
            fuzzy=fuzzy_score,
            features=feature_score,
        )

    @staticmethod
    def _calculate_feature_score(
        query: TextFeatures,
        product: TextFeatures,
    ) -> float:
        expected = (
            query.dimensions
            | query.measurements
            | query.thread_sizes
            | query.bit_types
            | query.grit_values
            | query.model_codes
        )

        if not expected:
            return 0.0

        actual = (
            product.dimensions
            | product.measurements
            | product.thread_sizes
            | product.bit_types
            | product.grit_values
            | product.model_codes
        )

        return len(expected & actual) / len(expected)
