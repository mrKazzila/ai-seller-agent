from ai_seller_agent.domain.matching.features import TextFeatures


def has_strong_feature_conflict(
    query: TextFeatures,
    product: TextFeatures,
) -> bool:
    return any(
        (
            _has_dimension_conflict(query.dimensions, product.dimensions),
            _has_measurement_conflict(query, product),
            _has_conflict(query.thread_sizes, product.thread_sizes),
            _has_conflict(query.bit_types, product.bit_types),
            _has_conflict(query.grit_values, product.grit_values),
            _has_conflict(query.model_codes, product.model_codes),
            _has_conflict(
                query.package_quantities,
                product.package_quantities,
            ),
            _has_conflict(query.voltages, product.voltages),
            _has_conflict(query.tooth_counts, product.tooth_counts),
            _has_conflict(query.numeric_values, product.numeric_values),
            _has_conflict(query.cable_markers, product.cable_markers),
        ),
    )


def dimension_matches(query_value: str, product_value: str) -> bool:
    query_parts = query_value.split("х")
    product_parts = product_value.split("х")

    return product_parts[: len(query_parts)] == query_parts


def measurement_matches_dimension(
    measurement: str,
    dimensions: frozenset[str],
) -> bool:
    value = measurement.removesuffix("мм")
    return any(value in dimension.split("х") for dimension in dimensions)


def _has_dimension_conflict(
    query_values: frozenset[str],
    product_values: frozenset[str],
) -> bool:
    if not query_values:
        return False

    return any(
        not any(
            dimension_matches(query_value, product_value)
            for product_value in product_values
        )
        for query_value in query_values
    )


def _has_measurement_conflict(
    query: TextFeatures,
    product: TextFeatures,
) -> bool:
    unsupported = query.measurements - product.measurements
    return any(
        not measurement_matches_dimension(value, product.dimensions)
        for value in unsupported
    )


def _has_conflict(
    query_values: frozenset[str],
    product_values: frozenset[str],
) -> bool:
    if not query_values:
        return False

    return not query_values.issubset(product_values)
