from ai_seller_agent.domain.models import MatchResult
from ai_seller_agent.presentation.api.schemas import (
    CandidateResponse,
    MessageMatchResponse,
)


def map_message_match_response(
    message: str,
    result: MatchResult,
) -> MessageMatchResponse:
    return MessageMatchResponse(
        message=message,
        status=result.status,
        candidates=[
            CandidateResponse(
                sku=candidate.product.sku,
                confidence=round(candidate.score, 4),
            )
            for candidate in result.candidates
        ],
    )
