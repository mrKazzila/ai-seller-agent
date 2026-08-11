import pytest

from ai_seller_agent.infrastructure.matching.features import FeatureExtractor


@pytest.mark.unit
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("диск 115 мм p60", frozenset({"115мм"})),
        ("диск 115мм p60", frozenset({"115мм"})),
        ("диск 115 mm p60", frozenset({"115мм"})),
        ("лента 12 мм х 10 м", frozenset({"12мм", "10м"})),
    ],
)
def test_extract_measurements(
    text: str,
    expected: frozenset[str],
) -> None:
    features = FeatureExtractor().extract(text)

    assert features.measurements == expected
