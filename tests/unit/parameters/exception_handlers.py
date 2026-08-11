from collections.abc import Awaitable, Callable

import pytest
from starlette.requests import Request
from starlette.responses import JSONResponse

from ai_seller_agent.infrastructure.catalog.exceptions import (
    CatalogLoadError,
    EmptyCatalogError,
)
from ai_seller_agent.presentation.api.exception_handlers import (
    catalog_load_error_handler,
    empty_catalog_error_handler,
)

ExceptionHandler = Callable[[Request, Exception], Awaitable[JSONResponse]]


def generate_exception_handler_data() -> list:
    return [
        pytest.param(
            catalog_load_error_handler,
            CatalogLoadError("Unable to read catalog"),
            {
                "error": "catalog_load_error",
                "detail": "Unable to read catalog",
            },
            id="error: catalog_load_error, status: 500",
        ),
        pytest.param(
            empty_catalog_error_handler,
            EmptyCatalogError("Catalog must not be empty"),
            {
                "error": "empty_catalog_error",
                "detail": "Catalog must not be empty",
            },
            id="error: empty_catalog_error, status: 500",
        ),
    ]
