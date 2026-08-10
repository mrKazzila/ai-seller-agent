from dataclasses import dataclass
from decimal import Decimal

from ai_seller_agent.domain.enums import MatchStatus


@dataclass(frozen=True, slots=True)
class Product:
    sku: str
    name: str
    unit: str
    price: Decimal


@dataclass(frozen=True, slots=True)
class ProductCandidate:
    product: Product
    score: float
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class MatchResult:
    status: MatchStatus
    candidates: tuple[ProductCandidate, ...] = ()
    reason: str | None = None
    missing_attributes: tuple[str, ...] = ()
