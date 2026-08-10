from typing import Annotated

import structlog
from fastapi import APIRouter, Depends

from ai_seller_agent.matching.matcher import ProductMatcher
from ai_seller_agent.presentation.api.dependencies import get_matcher
from ai_seller_agent.presentation.api.schemas import (
    MatchRequest,
    MatchResponse,
)

router = APIRouter(prefix="/matches", tags=["Matching"])
logger = structlog.get_logger(__name__)


@router.post("", response_model=MatchResponse)
def match_product(
    payload: MatchRequest,
    matcher: Annotated[ProductMatcher, Depends(get_matcher)],
) -> MatchResponse:
    result = matcher.match(payload.message)
    logger.info(
        "product_match_completed",
        status=result.status.value,
        candidate_count=len(result.candidates),
        selected_sku=(
            result.candidates[0].product.sku if result.candidates else None
        ),
    )

    return MatchResponse.from_domain(result)
