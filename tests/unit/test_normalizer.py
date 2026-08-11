import pytest

from ai_seller_agent.infrastructure.matching.normalizer import TextNormalizer


@pytest.mark.unit
@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("сдс бур 6 на 110", "sds бур 6х110"),
        (
            "диск пильный 190 на 48 зубьев",
            "диск пильный 190 мм 48 зубьев",
        ),
        (
            "проф труба 20х20 стенка полтора",
            "труба профильная 20х20х1.5",
        ),
        ("наждачка р120 листами", "шкурка шлифовальная p120 листами"),
        ("гкл 9.5 сколько лист", "гипсокартон 9.5 лист"),
        (
            "шуруповерт как у макиты, только дешевле",
            "шуруповерт",
        ),
    ],
)
def test_normalize_product_language(source: str, expected: str) -> None:
    assert TextNormalizer().normalize(source) == expected
