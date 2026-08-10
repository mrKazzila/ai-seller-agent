from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from tests.e2e.parameters.negative_messages import (
    generate_negative_message_data,
)


@pytest.mark.e2e
def test_health_reports_loaded_catalog(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "ok", "catalog_size": 466}


@pytest.mark.e2e
def test_match_uses_real_matcher(client: TestClient) -> None:
    payload = {"messages": ["   "]}

    response = client.post("/match", json=payload)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "results": [
            {
                "message": "   ",
                "status": "not_found",
                "candidates": [],
            },
        ],
    }


@pytest.mark.e2e
@pytest.mark.parametrize("message", generate_negative_message_data())
def test_match_returns_not_found_for_negative_message(
    client: TestClient,
    message: str,
) -> None:
    payload = {"messages": [message]}

    response = client.post("/match", json=payload)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "results": [
            {
                "message": message,
                "status": "not_found",
                "candidates": [],
            },
        ],
    }
