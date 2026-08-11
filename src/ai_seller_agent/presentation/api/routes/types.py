from typing import Annotated

from fastapi import Depends

from ai_seller_agent.application.use_cases.get_health_status import (
    GetHealthStatus,
)
from ai_seller_agent.application.use_cases.match_messages import MatchMessages
from ai_seller_agent.presentation.api.dependencies import (
    get_health_status,
    get_match_messages,
)

HealthStatusDep = Annotated[
    GetHealthStatus,
    Depends(get_health_status),
]

MatchMessagesDep = Annotated[
    MatchMessages,
    Depends(get_match_messages),
]
