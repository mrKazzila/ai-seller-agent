from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from ai_seller_agent.domain.models import Product


@dataclass(frozen=True, slots=True)
class ProductSearchHit:
    product: Product
    lexical_score: float


class ProductSearch(Protocol):
    def search(
        self,
        query: str,
    ) -> Sequence[ProductSearchHit]: ...
