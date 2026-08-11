from collections.abc import Sequence

from ai_seller_agent.application.ports.search import ProductSearchHit
from ai_seller_agent.domain.models import Product
from ai_seller_agent.infrastructure.matching.index import ProductSearchIndex
from ai_seller_agent.infrastructure.matching.normalizer import TextNormalizer


class TfidfProductSearch:
    def __init__(
        self,
        *,
        products: Sequence[Product],
        normalizer: TextNormalizer,
    ) -> None:
        self._products = tuple(products)

        documents = tuple(
            normalizer.normalize(product.name) for product in self._products
        )

        self._index = ProductSearchIndex(documents)

    def search(
        self,
        query: str,
    ) -> tuple[ProductSearchHit, ...]:
        scores = self._index.search(query)

        return tuple(
            ProductSearchHit(
                product=product,
                lexical_score=float(scores[index]),
            )
            for index, product in enumerate(self._products)
        )
