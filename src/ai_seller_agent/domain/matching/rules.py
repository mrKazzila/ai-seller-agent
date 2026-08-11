from ai_seller_agent.domain.matching.features import TextFeatures


def has_strong_feature_conflict(
    query: TextFeatures,
    product: TextFeatures,
) -> bool:
    return any(
        (
            _has_conflict(query.dimensions, product.dimensions),
            _has_conflict(query.measurements, product.measurements),
            _has_conflict(query.thread_sizes, product.thread_sizes),
            _has_conflict(query.bit_types, product.bit_types),
            _has_conflict(query.grit_values, product.grit_values),
            _has_conflict(query.model_codes, product.model_codes),
        ),
    )


def _has_conflict(
    query_values: frozenset[str],
    product_values: frozenset[str],
) -> bool:
    if not query_values:
        return False

    return not query_values.issubset(product_values)
