from typing import Annotated

from fastapi import APIRouter, Depends

from ai_seller_agent.matching.matcher import ProductMatcher
from ai_seller_agent.presentation.api.dependencies import get_matcher
from ai_seller_agent.presentation.api.schemas import (
    MatchRequest,
    MatchResponse,
)

router = APIRouter(prefix="/matches", tags=["Matching"])


@router.post("", response_model=MatchResponse)
def match_product(
    payload: MatchRequest,
    matcher: Annotated[ProductMatcher, Depends(get_matcher)],
) -> MatchResponse:
    result = matcher.match(payload.message)

    return MatchResponse.from_domain(result)
