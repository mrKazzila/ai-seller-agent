from http import HTTPStatus

import pytest


def generate_invalid_match_request_data() -> list:
    requests = [
        {"message": "exact"},
        {},
        {"messages": "exact"},
        {"messages": [1]},
    ]
    return [
        pytest.param(
            request,
            HTTPStatus.UNPROCESSABLE_ENTITY,
            id=f"payload: {request}, status: 422",
        )
        for request in requests
    ]
