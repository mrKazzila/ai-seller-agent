from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient


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
