from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from tests.integration.parameters.matching_api import (
    generate_invalid_match_request_data,
)


@pytest.mark.integration
def test_match_api_returns_batch_in_input_order(client: TestClient) -> None:
    payload = {"messages": ["exact", "broad", "missing", "   "]}

    response = client.post("/match", json=payload)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "results": [
            {
                "message": "exact",
                "status": "matched",
                "candidates": [
                    {"sku": "SKU-1", "confidence": 0.8765},
                ],
            },
            {
                "message": "broad",
                "status": "ambiguous",
                "candidates": [
                    {"sku": "SKU-2", "confidence": 0.72},
                    {"sku": "SKU-3", "confidence": 0.68},
                    {"sku": "SKU-4", "confidence": 0.61},
                ],
            },
            {
                "message": "missing",
                "status": "not_found",
                "candidates": [],
            },
            {
                "message": "   ",
                "status": "not_found",
                "candidates": [],
            },
        ],
    }

    for result in response.json()["results"]:
        assert set(result) == {"message", "status", "candidates"}
        for item in result["candidates"]:
            assert set(item) == {"sku", "confidence"}
            assert 0 <= item["confidence"] <= 1


@pytest.mark.integration
def test_match_api_accepts_empty_batch(client: TestClient) -> None:
    response = client.post("/match", json={"messages": []})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"results": []}


@pytest.mark.integration
@pytest.mark.parametrize(
    ("payload", "expected_status"),
    generate_invalid_match_request_data(),
)
def test_match_api_rejects_invalid_requests(
    client: TestClient,
    payload: object,
    expected_status: HTTPStatus,
) -> None:
    response = client.post("/match", json=payload)

    assert response.status_code == expected_status


@pytest.mark.integration
def test_old_matches_endpoint_is_not_available(client: TestClient) -> None:
    payload = {"messages": ["exact"]}

    response = client.post("/matches", json=payload)

    assert response.status_code == HTTPStatus.NOT_FOUND
