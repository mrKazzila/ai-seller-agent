from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class TextFeatures:
    dimensions: frozenset[str] = field(default_factory=frozenset)
    measurements: frozenset[str] = field(default_factory=frozenset)
    thread_sizes: frozenset[str] = field(default_factory=frozenset)
    bit_types: frozenset[str] = field(default_factory=frozenset)
    grit_values: frozenset[str] = field(default_factory=frozenset)
    model_codes: frozenset[str] = field(default_factory=frozenset)
