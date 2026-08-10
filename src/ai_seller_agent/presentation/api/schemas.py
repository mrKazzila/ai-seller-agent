from pydantic import BaseModel, Field

from ai_seller_agent.domain.enums import MatchStatus
from ai_seller_agent.domain.models import MatchResult


class MatchRequest(BaseModel):
    messages: list[str]


class CandidateResponse(BaseModel):
    sku: str
    confidence: float = Field(ge=0, le=1)


class MessageMatchResponse(BaseModel):
    message: str
    status: MatchStatus
    candidates: list[CandidateResponse] = Field(default_factory=list)

    @classmethod
    def from_domain(
        cls,
        message: str,
        result: MatchResult,
    ) -> "MessageMatchResponse":
        return cls(
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


class MatchResponse(BaseModel):
    results: list[MessageMatchResponse]
