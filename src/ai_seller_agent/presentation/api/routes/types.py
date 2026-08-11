from typing import Annotated

from fastapi import Depends

from ai_seller_agent.infrastructure.catalog.service import CatalogService
from ai_seller_agent.infrastructure.matching.matcher import ProductMatcher
from ai_seller_agent.presentation.api.dependencies import (
    get_catalog,
    get_matcher,
)

CatalogDep = Annotated[CatalogService, Depends(get_catalog)]
MatcherDep = Annotated[ProductMatcher, Depends(get_matcher)]
