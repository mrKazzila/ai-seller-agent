from decimal import Decimal

from pydantic import BaseModel, Field

from ai_seller_agent.domain.enums import MatchStatus
from ai_seller_agent.domain.models import MatchResult


class MatchRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2_000)


class ProductResponse(BaseModel):
    sku: str
    name: str
    unit: str
    price: Decimal


class CandidateResponse(BaseModel):
    product: ProductResponse
    score: float = Field(ge=0, le=1)


class MatchResponse(BaseModel):
    status: MatchStatus
    candidates: list[CandidateResponse]
    reason: str | None = None
    missing_attributes: list[str] = []

    @classmethod
    def from_domain(cls, result: MatchResult) -> "MatchResponse":
        return cls(
            status=result.status,
            candidates=[
                CandidateResponse(
                    product=ProductResponse(
                        sku=candidate.product.sku,
                        name=candidate.product.name,
                        unit=candidate.product.unit,
                        price=candidate.product.price,
                    ),
                    score=round(candidate.score, 4),
                )
                for candidate in result.candidates
            ],
            reason=result.reason,
            missing_attributes=list(result.missing_attributes),
        )
