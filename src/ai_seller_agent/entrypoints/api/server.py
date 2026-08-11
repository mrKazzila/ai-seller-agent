import uvicorn
from fastapi import FastAPI


def run_app(
    *,
    app: FastAPI,
    host: str,
    port: int,
    reload: bool = False,
) -> None:
    uvicorn.run(
        app=app,
        host=host,
        port=port,
        reload=reload,
        loop="uvloop",
        access_log=True,
        log_config=None,
    )
