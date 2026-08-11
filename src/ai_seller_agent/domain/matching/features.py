from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class TextFeatures:
    dimensions: frozenset[str] = field(default_factory=frozenset)
    measurements: frozenset[str] = field(default_factory=frozenset)
    thread_sizes: frozenset[str] = field(default_factory=frozenset)
    bit_types: frozenset[str] = field(default_factory=frozenset)
    grit_values: frozenset[str] = field(default_factory=frozenset)
    model_codes: frozenset[str] = field(default_factory=frozenset)
    package_quantities: frozenset[str] = field(default_factory=frozenset)
    voltages: frozenset[str] = field(default_factory=frozenset)
    tooth_counts: frozenset[str] = field(default_factory=frozenset)
    numeric_values: frozenset[str] = field(default_factory=frozenset)
    cable_markers: frozenset[str] = field(default_factory=frozenset)
