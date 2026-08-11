from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from tests.e2e.parameters.negative_messages import (
    generate_negative_message_data,
)
from tests.e2e.parameters.product_messages import (
    generate_ambiguous_product_data,
    generate_exact_product_data,
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


@pytest.mark.e2e
@pytest.mark.parametrize(
    ("message", "expected_sku"),
    generate_exact_product_data(),
)
def test_match_returns_exact_catalog_product(
    client: TestClient,
    message: str,
    expected_sku: str,
) -> None:
    response = client.post("/match", json={"messages": [message]})

    assert response.status_code == HTTPStatus.OK
    result = response.json()["results"][0]
    assert result["status"] == "matched"
    assert [candidate["sku"] for candidate in result["candidates"]] == [
        expected_sku,
    ]


@pytest.mark.e2e
@pytest.mark.parametrize(
    ("message", "expected_skus"),
    generate_ambiguous_product_data(),
)
def test_match_returns_relevant_ambiguous_candidates(
    client: TestClient,
    message: str,
    expected_skus: set[str] | None,
) -> None:
    response = client.post("/match", json={"messages": [message]})

    assert response.status_code == HTTPStatus.OK
    result = response.json()["results"][0]
    assert result["status"] == "ambiguous"
    assert 2 <= len(result["candidates"]) <= 3

    if expected_skus is not None:
        assert {
            candidate["sku"] for candidate in result["candidates"]
        } == expected_skus
