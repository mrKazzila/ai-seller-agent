from dataclasses import dataclass

from ai_seller_agent.application.ports.catalog import ProductCatalog


@dataclass(frozen=True, slots=True)
class HealthStatus:
    status: str
    catalog_size: int


class GetHealthStatus:
    def __init__(self, catalog: ProductCatalog) -> None:
        self._catalog = catalog

    def execute(self) -> HealthStatus:
        return HealthStatus(
            status="ok",
            catalog_size=len(self._catalog),
        )
