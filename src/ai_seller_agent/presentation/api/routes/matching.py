import structlog
from fastapi import APIRouter

from ai_seller_agent.domain.enums import MatchStatus
from ai_seller_agent.presentation.api.mappers.match import to_match_response
from ai_seller_agent.presentation.api.routes.types import MatchMessagesDep
from ai_seller_agent.presentation.api.schemas.match import (
    MatchRequest,
    MatchResponse,
)

router = APIRouter(prefix="/match", tags=["Matching"])
logger = structlog.get_logger(__name__)


@router.post("")
def match_product(
    payload: MatchRequest,
    match_messages_uc: MatchMessagesDep,
) -> MatchResponse:
    matches = match_messages_uc.execute(messages=payload.messages)

    results = [
        to_match_response(
            match.message,
            match.result,
        )
        for match in matches
    ]

    logger.info(
        "product_match_batch_completed",
        message_count=len(results),
        matched_count=sum(
            result.status is MatchStatus.MATCHED for result in results
        ),
        ambiguous_count=sum(
            result.status is MatchStatus.AMBIGUOUS for result in results
        ),
        not_found_count=sum(
            result.status is MatchStatus.NOT_FOUND for result in results
        ),
    )

    return MatchResponse(results=results)
