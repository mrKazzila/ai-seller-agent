from collections.abc import Sequence
from dataclasses import dataclass

from ai_seller_agent.application.ports.matching import ProductMatcher
from ai_seller_agent.domain.models import MatchResult


@dataclass(frozen=True, slots=True)
class MessageMatch:
    message: str
    result: MatchResult


class MatchMessages:
    def __init__(self, matcher: ProductMatcher) -> None:
        self._matcher = matcher

    def execute(
        self,
        messages: Sequence[str],
    ) -> tuple[MessageMatch, ...]:
        return tuple(
            MessageMatch(
                message=message,
                result=self._matcher.match(message),
            )
            for message in messages
        )
