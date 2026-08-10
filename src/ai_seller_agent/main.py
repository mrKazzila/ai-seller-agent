from ai_seller_agent.application import create_app
from ai_seller_agent.config.logging import LoggingConfig
from ai_seller_agent.config.settings import get_settings
from ai_seller_agent.observability import setup_logging

setup_logging(LoggingConfig.from_settings(get_settings()))
app = create_app()


def main() -> None:
    import uvicorn

    uvicorn.run(
        "ai_seller_agent.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
