import pytest

from ai_seller_agent.domain.enums import MatchStatus


def generate_matcher_result_data() -> list:
    return [
        pytest.param(
            [("SKU-1", 0.70)],
            MatchStatus.NOT_FOUND,
            [],
            id="scores: [0.70], status: not_found, candidates: []",
        ),
        pytest.param(
            [
                ("SKU-1", 0.70),
                ("SKU-2", 0.68),
                ("SKU-3", 0.66),
                ("SKU-4", 0.64),
            ],
            MatchStatus.AMBIGUOUS,
            ["SKU-1", "SKU-2", "SKU-3"],
            id=(
                "scores: [0.70, 0.68, 0.66, 0.64], "
                "status: ambiguous, candidates: 3"
            ),
        ),
        pytest.param(
            [("SKU-1", 0.90), ("SKU-2", 0.70)],
            MatchStatus.MATCHED,
            ["SKU-1"],
            id="scores: [0.90, 0.70], status: matched, candidates: 1",
        ),
    ]
