from ai_seller_agent.application import create_app
from ai_seller_agent.config.logging import LoggingConfig
from ai_seller_agent.config.settings import get_settings
from ai_seller_agent.observability import setup_logging

settings = get_settings()
setup_logging(LoggingConfig.from_settings(settings.app))
app = create_app()


def main() -> None:
    import uvicorn

    uvicorn.run(
        "ai_seller_agent.main:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.reload,
        log_config=None,
    )
