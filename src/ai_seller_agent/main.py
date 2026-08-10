from ai_seller_agent.application import create_app

app = create_app()


def main() -> None:
    import uvicorn

    uvicorn.run(
        "ai_seller_agent.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
