from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from ai_seller_agent.entrypoints.api.bootstrap import create_application


@pytest.fixture(scope="module")
def client() -> Iterator[TestClient]:
    with TestClient(create_application()) as test_client:
        yield test_client
