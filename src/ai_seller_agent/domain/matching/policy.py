from collections.abc import Sequence
from dataclasses import dataclass

from ai_seller_agent.domain.enums import MatchStatus
from ai_seller_agent.domain.models import MatchResult, ProductCandidate


@dataclass(frozen=True, slots=True)
class MatchPolicy:
    match_threshold: float
    candidate_threshold: float
    minimum_margin: float
    candidates_limit: int

    def decide(
        self,
        candidates: Sequence[ProductCandidate],
    ) -> MatchResult:
        ordered = tuple(
            sorted(
                candidates,
                key=lambda candidate: candidate.score,
                reverse=True,
            ),
        )

        if not ordered:
            return MatchResult(status=MatchStatus.NOT_FOUND)

        top = ordered[0]
        selected = ordered[: self.candidates_limit]

        if top.score < self.match_threshold:
            if len(selected) < 2:
                return MatchResult(status=MatchStatus.NOT_FOUND)

            return MatchResult(
                status=MatchStatus.AMBIGUOUS,
                candidates=selected,
            )

        if len(ordered) > 1:
            margin = top.score - ordered[1].score

            if margin < self.minimum_margin:
                return MatchResult(
                    status=MatchStatus.AMBIGUOUS,
                    candidates=selected,
                )

        return MatchResult(
            status=MatchStatus.MATCHED,
            candidates=(top,),
        )
