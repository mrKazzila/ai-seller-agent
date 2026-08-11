import asyncio
import json
from http import HTTPStatus

import pytest
from fastapi import FastAPI
from starlette.requests import Request

from ai_seller_agent.infrastructure.catalog.exceptions import (
    CatalogLoadError,
    EmptyCatalogError,
)
from ai_seller_agent.presentation.api.exception_handlers import (
    catalog_load_error_handler,
    empty_catalog_error_handler,
    setup_exception_handlers,
)
from tests.unit.parameters.exception_handlers import (
    ExceptionHandler,
    generate_exception_handler_data,
)


@pytest.mark.unit
def test_setup_exception_handlers_registers_catalog_errors() -> None:
    app = FastAPI()

    setup_exception_handlers(app)

    assert (
        app.exception_handlers[CatalogLoadError] is catalog_load_error_handler
    )
    assert (
        app.exception_handlers[EmptyCatalogError]
        is empty_catalog_error_handler
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    ("handler", "error", "expected_response"),
    generate_exception_handler_data(),
)
def test_exception_handler_returns_internal_server_error(
    handler: ExceptionHandler,
    error: Exception,
    expected_response: dict[str, str],
) -> None:
    request = Request({"type": "http"})

    response = asyncio.run(handler(request, error))

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert json.loads(response.body) == expected_response
