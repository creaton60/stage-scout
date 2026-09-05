"""적합도 점수. 장소 랭킹과 배치안 비교에 공통으로 쓴다."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Criterion(str, Enum):
    """평가 축. 가중치는 도메인 서비스가 정책으로 들고 있다."""

    SOLAR_GLARE = "solar_glare"  # 관객 역광 여부
    WEATHER_RISK = "weather_risk"
    ACCESSIBILITY = "accessibility"
    CAPACITY_FIT = "capacity_fit"
    TERRAIN_FLATNESS = "terrain_flatness"
    OBSTACLE_PENALTY = "obstacle_penalty"
    SIGHT_LINE_QUALITY = "sight_line_quality"


@dataclass(frozen=True, slots=True)
class CriterionScore:
    criterion: Criterion
    raw_value: float
    normalized: float  # 0.0 ~ 1.0
    weight: float
    reason: str  # 사용자에게 보여줄 근거 문장

    @property
    def weighted(self) -> float:
        return self.normalized * self.weight


@dataclass(frozen=True, slots=True)
class SuitabilityScore:
    """가중 합산 결과. 근거(breakdown)를 항상 함께 들고 다닌다."""

    breakdown: tuple[CriterionScore, ...]

    @property
    def total(self) -> float:
        total_weight = sum(s.weight for s in self.breakdown)
        if total_weight == 0:
            return 0.0
        return sum(s.weighted for s in self.breakdown) / total_weight
