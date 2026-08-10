import re
from dataclasses import dataclass, field

DIMENSION_PATTERN = re.compile(
    r"\b\d+(?:\.\d+)?(?:х\d+(?:\.\d+)?){1,2}\b",
)

THREAD_PATTERN = re.compile(r"\bм\d+\b")
BIT_PATTERN = re.compile(r"\b(?:ph|pz|t)\d+\b")
GRIT_PATTERN = re.compile(r"\bp\d+\b")
MODEL_PATTERN = re.compile(
    r"\b(?=[a-zа-я0-9-]*[a-zа-я])"
    r"(?=[a-zа-я0-9-]*\d)"
    r"[a-zа-я0-9]+(?:-[a-zа-я0-9]+)+\b",
)


@dataclass(frozen=True, slots=True)
class TextFeatures:
    dimensions: frozenset[str] = field(default_factory=frozenset)
    thread_sizes: frozenset[str] = field(default_factory=frozenset)
    bit_types: frozenset[str] = field(default_factory=frozenset)
    grit_values: frozenset[str] = field(default_factory=frozenset)
    model_codes: frozenset[str] = field(default_factory=frozenset)


class FeatureExtractor:
    def extract(self, text: str) -> TextFeatures:
        return TextFeatures(
            dimensions=frozenset(DIMENSION_PATTERN.findall(text)),
            thread_sizes=frozenset(THREAD_PATTERN.findall(text)),
            bit_types=frozenset(BIT_PATTERN.findall(text)),
            grit_values=frozenset(GRIT_PATTERN.findall(text)),
            model_codes=frozenset(MODEL_PATTERN.findall(text)),
        )
