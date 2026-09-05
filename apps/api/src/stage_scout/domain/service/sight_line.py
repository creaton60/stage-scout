"""시야선 계산. 관객 지점에서 무대가 잘 보이는지 판정한다.

TODO(S5): 장애물 폴리곤과의 교차 판정, 무대 높이 대비 앞줄 가림 반영.
"""

from __future__ import annotations

from stage_scout.domain.model.geo import Coordinate
from stage_scout.domain.model.layout import SightLine, StagePlacement
from stage_scout.domain.model.survey import Obstacle

ACCEPTABLE_VIEW_ANGLE_DEG = 60.0
MAX_COMFORTABLE_DISTANCE_M = 80.0


def evaluate(
    point: Coordinate,
    stage: StagePlacement,
    obstacles: tuple[Obstacle, ...],
) -> SightLine:
    """한 지점의 시야 품질을 평가한다."""
    raise NotImplementedError("S5에서 구현")
