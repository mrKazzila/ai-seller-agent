from fastapi import Request

from ai_seller_agent.application.use_cases.get_health_status import (
    GetHealthStatus,
)
from ai_seller_agent.application.use_cases.match_messages import MatchMessages


def get_match_messages(request: Request) -> MatchMessages:
    return request.app.state.match_messages


def get_health_status(request: Request) -> GetHealthStatus:
    return request.app.state.get_health_status
