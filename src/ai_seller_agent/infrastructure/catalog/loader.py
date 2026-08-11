import csv
from decimal import Decimal
from pathlib import Path

from ai_seller_agent.domain.models import Product
from ai_seller_agent.infrastructure.catalog.exceptions import CatalogLoadError


class CsvCatalogLoader:
    def __init__(self, path: Path) -> None:
        self._path = path

    def load(self) -> tuple[Product, ...]:
        try:
            with self._path.open(
                mode="r",
                encoding="utf-8-sig",
                newline="",
            ) as file:
                reader = csv.DictReader(file)

                return tuple(
                    self._parse_row(row, line_number)
                    for line_number, row in enumerate(reader, start=2)
                )
        except OSError as exc:
            raise CatalogLoadError(
                f"Unable to read catalog: {self._path}",
            ) from exc

    @staticmethod
    def _parse_row(
        row: dict[str, str],
        line_number: int,
    ) -> Product:
        try:
            return Product(
                sku=row["sku"].strip(),
                name=row["name"].strip(),
                unit=row["unit"].strip(),
                price=Decimal(row["price"].strip()),
            )
        except (KeyError, ValueError) as exc:
            raise CatalogLoadError(
                f"Invalid catalog row at line {line_number}",
            ) from exc
