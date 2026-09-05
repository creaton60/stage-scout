"""후보지 적합도 합산 규칙.

가중치는 도메인 정책이므로 여기에 둔다. 값 자체(일조·기상·접근성)는
어댑터가 수집해 CriterionScore 로 만들어 넘긴다.
"""

from __future__ import annotations

from stage_scout.domain.model.scoring import Criterion, CriterionScore, SuitabilityScore

DEFAULT_WEIGHTS: dict[Criterion, float] = {
    Criterion.SOLAR_GLARE: 0.20,
    Criterion.WEATHER_RISK: 0.25,
    Criterion.ACCESSIBILITY: 0.20,
    Criterion.CAPACITY_FIT: 0.25,
    Criterion.TERRAIN_FLATNESS: 0.10,
}


def combine(scores: list[CriterionScore]) -> SuitabilityScore:
    """평가 축별 점수를 하나의 적합도로 합산한다."""
    return SuitabilityScore(breakdown=tuple(scores))


def rank(candidates: dict[str, SuitabilityScore]) -> list[tuple[str, SuitabilityScore]]:
    """적합도 내림차순 정렬. 동점이면 이름순으로 안정 정렬한다."""
    return sorted(candidates.items(), key=lambda kv: (-kv[1].total, kv[0]))
