import re

from ai_seller_agent.domain.matching.features import TextFeatures

DIMENSION_PATTERN = re.compile(
    r"\b\d+(?:\.\d+)?(?:х\d+(?:\.\d+)?){1,2}\b",
)
MEASUREMENT_PATTERN = re.compile(
    r"\b(?P<value>\d+(?:\.\d+)?)\s*"
    r"(?P<unit>мм|mm|см|cm|м|m)\b",
)

THREAD_PATTERN = re.compile(r"\bм\d+\b")
BIT_PATTERN = re.compile(r"\b(?:ph|pz|t)\d+\b")
GRIT_PATTERN = re.compile(r"\bp\d+\b")
MODEL_PATTERN = re.compile(
    r"\b(?=[a-zа-я0-9-]*[a-zа-я])"
    r"(?=[a-zа-я0-9-]*\d)"
    r"[a-zа-я0-9]+(?:-[a-zа-я0-9]+)+\b",
)

class FeatureExtractor:
    def extract(self, text: str) -> TextFeatures:
        return TextFeatures(
            dimensions=frozenset(DIMENSION_PATTERN.findall(text)),
            measurements=self._extract_measurements(text),
            thread_sizes=frozenset(THREAD_PATTERN.findall(text)),
            bit_types=frozenset(BIT_PATTERN.findall(text)),
            grit_values=frozenset(GRIT_PATTERN.findall(text)),
            model_codes=frozenset(MODEL_PATTERN.findall(text)),
        )

    @staticmethod
    def _extract_measurements(text: str) -> frozenset[str]:
        unit_aliases = {
            "mm": "мм",
            "cm": "см",
            "m": "м",
        }

        return frozenset(
            f"{match.group('value')}"
            f"{unit_aliases.get(match.group('unit'), match.group('unit'))}"
            for match in MEASUREMENT_PATTERN.finditer(text)
        )
