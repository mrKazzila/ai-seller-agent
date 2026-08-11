from ai_seller_agent.config.logging import LoggingConfig
from ai_seller_agent.config.settings import get_settings
from ai_seller_agent.entrypoints.api.bootstrap import create_application
from ai_seller_agent.entrypoints.api.server import run_app
from ai_seller_agent.infrastructure.observability import setup_logging


def main() -> None:
    """Run API application."""
    settings = get_settings()
    setup_logging(LoggingConfig.from_settings(settings.app))

    app = create_application(settings)

    run_app(
        app=app,
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.reload,
    )


if __name__ == "__main__":
    main()
