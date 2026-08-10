from http import HTTPStatus

import pytest


def generate_invalid_match_request_data() -> list:
    requests = [
        ({"message": "exact"}, "missing messages field"),
        ({}, "empty object"),
        ({"messages": "exact"}, "messages is string"),
        ({"messages": [1]}, "message is integer"),
        (None, "null body"),
        ([], "array body"),
        ({"messages": None}, "messages is null"),
        ({"messages": [None]}, "message is null"),
        ({"messages": [{}]}, "message is object"),
        ({"messages": [True]}, "message is boolean"),
    ]
    return [
        pytest.param(
            request,
            HTTPStatus.UNPROCESSABLE_ENTITY,
            id=f"payload: {description}, status: 422",
        )
        for request, description in requests
    ]
