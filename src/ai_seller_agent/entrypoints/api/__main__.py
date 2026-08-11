from ai_seller_agent.config.logging import LoggingConfig
from ai_seller_agent.config.settings import get_settings
from ai_seller_agent.infrastructure.observability import setup_logging
from ai_seller_agent.presentation.api.application import create_app, run_app


def main() -> None:
    """Run API application."""
    settings = get_settings()
    setup_logging(LoggingConfig.from_settings(settings.app))

    app = create_app()

    run_app(
        app=app,
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.reload,
    )


if __name__ == "__main__":
    main()
