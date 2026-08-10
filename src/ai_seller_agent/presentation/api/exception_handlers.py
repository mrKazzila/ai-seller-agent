from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class ApplicationError(Exception):
    """Base application error."""


class CatalogError(ApplicationError):
    """Catalog-related error."""


class MatchingError(ApplicationError):
    """Matching-related error."""


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(CatalogError)
    async def handle_catalog_error(
        _request: Request,
        exc: CatalogError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "catalog_error",
                "detail": str(exc),
            },
        )

    @app.exception_handler(MatchingError)
    async def handle_matching_error(
        _request: Request,
        exc: MatchingError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "matching_error",
                "detail": str(exc),
            },
        )

    @app.exception_handler(ApplicationError)
    async def handle_application_error(
        _request: Request,
        exc: ApplicationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "application_error",
                "detail": str(exc),
            },
        )
