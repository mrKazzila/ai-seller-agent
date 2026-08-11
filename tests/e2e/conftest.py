from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from ai_seller_agent.presentation.api.application import create_app


@pytest.fixture(scope="module")
def client() -> Iterator[TestClient]:
    with TestClient(create_app()) as test_client:
        yield test_client
