from typing import Protocol

from ai_seller_agent.domain.models import MatchResult


class ProductMatcher(Protocol):
    def match(self, message: str) -> MatchResult: ...
