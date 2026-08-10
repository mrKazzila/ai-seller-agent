from typing import Annotated

import structlog
from fastapi import APIRouter, Depends

from ai_seller_agent.domain.enums import MatchStatus
from ai_seller_agent.matching.matcher import ProductMatcher
from ai_seller_agent.presentation.api.dependencies import get_matcher
from ai_seller_agent.presentation.api.schemas import (
    MatchRequest,
    MatchResponse,
    MessageMatchResponse,
)

router = APIRouter(prefix="/match", tags=["Matching"])
logger = structlog.get_logger(__name__)


@router.post("", response_model=MatchResponse)
def match_product(
    payload: MatchRequest,
    matcher: Annotated[ProductMatcher, Depends(get_matcher)],
) -> MatchResponse:
    results = [
        MessageMatchResponse.from_domain(message, matcher.match(message))
        for message in payload.messages
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
