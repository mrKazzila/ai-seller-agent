from typing import cast

import structlog
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from ai_seller_agent.infrastructure.catalog.exceptions import (
    CatalogLoadError,
    EmptyCatalogError,
)

logger = structlog.get_logger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(CatalogLoadError, catalog_load_error_handler)
    app.add_exception_handler(EmptyCatalogError, empty_catalog_error_handler)


async def catalog_load_error_handler(
    _request: Request,
    exc: Exception,
) -> JSONResponse:
    exc = cast(CatalogLoadError, exc)
    logger.error(
        "catalog_load_failed",
        exc_info=(type(exc), exc, exc.__traceback__),
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "catalog_load_error",
            "detail": str(exc),
        },
    )


async def empty_catalog_error_handler(
    _request: Request,
    exc: Exception,
) -> JSONResponse:
    exc = cast(EmptyCatalogError, exc)
    logger.error(
        "catalog_empty",
        exc_info=(type(exc), exc, exc.__traceback__),
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "empty_catalog_error",
            "detail": str(exc),
        },
    )
