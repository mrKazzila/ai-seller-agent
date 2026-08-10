from pydantic import BaseModel, Field

from ai_seller_agent.domain.enums import MatchStatus


class MatchRequest(BaseModel):
    messages: list[str]


class CandidateResponse(BaseModel):
    sku: str
    confidence: float = Field(ge=0, le=1)


class MessageMatchResponse(BaseModel):
    message: str
    status: MatchStatus
    candidates: list[CandidateResponse] = Field(default_factory=list)


class MatchResponse(BaseModel):
    results: list[MessageMatchResponse]
