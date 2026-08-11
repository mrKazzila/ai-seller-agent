from ai_seller_agent.domain.models import Product
from ai_seller_agent.infrastructure.catalog.exceptions import EmptyCatalogError


class CatalogService:
    def __init__(self, products: tuple[Product, ...]) -> None:
        if not products:
            raise EmptyCatalogError("Catalog must not be empty")

        self._products = products
        self._products_by_sku = {product.sku: product for product in products}

    @property
    def products(self) -> tuple[Product, ...]:
        return self._products

    def get_by_sku(self, sku: str) -> Product | None:
        return self._products_by_sku.get(sku)

    def __len__(self) -> int:
        return len(self._products)
