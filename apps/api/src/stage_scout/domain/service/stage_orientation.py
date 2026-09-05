"""무대 배치 후보 생성.

가용 영역·장애물·태양 궤적·바람 방향을 제약으로 받아
실행 가능한 (위치, 방향) 조합을 만들어낸다. 평가는 suitability 가 맡는다.

TODO(S5): 격자 샘플링 + 제약 필터 + 상위 N개 반환으로 구현.
"""

from __future__ import annotations

from stage_scout.domain.model.environment import SolarTrack, WeatherForecast
from stage_scout.domain.model.event import StageRequirement
from stage_scout.domain.model.layout import StagePlacement
from stage_scout.domain.model.survey import TerrainAnalysis

CANDIDATE_BEARING_STEP_DEG = 15.0


def generate_candidates(
    terrain: TerrainAnalysis,
    requirement: StageRequirement,
    solar: SolarTrack,
    weather: WeatherForecast,
    limit: int = 10,
) -> list[StagePlacement]:
    """제약을 만족하는 무대 배치 후보를 생성한다."""
    raise NotImplementedError("S5에서 구현")
