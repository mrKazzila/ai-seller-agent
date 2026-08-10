from pydantic import BaseModel, Field

__all__ = ("MatchingSettings",)


class MatchingSettings(BaseModel):
    match_threshold: float = 0.82
    candidate_threshold: float = 0.50
    minimum_margin: float = 0.10
    candidates_limit: int = Field(default=3, ge=2, le=3)

    tfidf_weight: float = 0.60
    fuzzy_weight: float = 0.25
    feature_weight: float = 0.15
