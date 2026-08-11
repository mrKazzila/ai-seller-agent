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


@pytest.mark.unit
def test_extract_product_discriminators() -> None:
    features = FeatureExtractor().extract(
        "кабель ввгнг ls 3х1.5 12 в уп 200 шт 48 зубьев",
    )

    assert features.dimensions == frozenset({"3х1.5"})
    assert features.package_quantities == frozenset({"200"})
    assert features.voltages == frozenset({"12"})
    assert features.tooth_counts == frozenset({"48"})
    assert features.numeric_values == frozenset(
        {"1.5", "3", "12", "48", "200"},
    )
    assert features.cable_markers == frozenset({"ls"})
