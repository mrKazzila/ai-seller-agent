from collections.abc import Sequence
from typing import Protocol

from ai_seller_agent.domain.models import Product


class ProductCatalog(Protocol):
    @property
    def products(self) -> Sequence[Product]: ...

    def get_by_sku(self, sku: str) -> Product | None: ...

    def __len__(self) -> int: ...
