from fastapi import Request

from ai_seller_agent.catalog.service import CatalogService
from ai_seller_agent.matching.matcher import ProductMatcher


def get_matcher(request: Request) -> ProductMatcher:
    return request.app.state.matcher


def get_catalog(request: Request) -> CatalogService:
    return request.app.state.catalog
