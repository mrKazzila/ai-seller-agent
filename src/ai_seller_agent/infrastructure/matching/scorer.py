from dataclasses import dataclass

from rapidfuzz import fuzz

from ai_seller_agent.domain.matching.features import TextFeatures
from ai_seller_agent.domain.matching.rules import (
    dimension_matches,
    measurement_matches_dimension,
)


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
        coverage_score = self._calculate_query_coverage(
            query,
            product_text,
        )
        feature_score = self._calculate_feature_score(
            query_features,
            product_features,
        )
        effective_lexical_score = max(tfidf_score, coverage_score)

        total = (
            self._weights.tfidf * effective_lexical_score
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
    def _calculate_query_coverage(query: str, product: str) -> float:
        query_tokens = query.split()
        product_tokens = product.split()

        if not query_tokens:
            return 0.0

        covered = sum(
            max(
                (
                    _token_match_score(query_token, product_token)
                    for product_token in product_tokens
                ),
                default=0.0,
            )
            for query_token in query_tokens
        )
        return covered / len(query_tokens)

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
            | query.package_quantities
            | query.voltages
            | query.tooth_counts
            | query.numeric_values
            | query.cable_markers
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
            | product.package_quantities
            | product.voltages
            | product.tooth_counts
            | product.numeric_values
            | product.cable_markers
        )
        matches = len(expected & actual)

        for query_dimension in query.dimensions:
            if any(
                dimension_matches(query_dimension, product_dimension)
                for product_dimension in product.dimensions
            ):
                matches += 1

        for query_measurement in query.measurements - product.measurements:
            if measurement_matches_dimension(
                query_measurement,
                product.dimensions,
            ):
                matches += 1

        matches -= len(query.dimensions & product.dimensions)
        return matches / len(expected)


def _token_match_score(query_token: str, product_token: str) -> float:
    if query_token == product_token:
        return 1.0

    if query_token.replace(".", "", 1).isdigit():
        return float(query_token in product_token.split("х"))

    shortest = min(len(query_token), len(product_token))
    if shortest >= 4 and (
        query_token.startswith(product_token)
        or product_token.startswith(query_token)
    ):
        return 0.8

    return 0.0
