"""역광 판정.

관객이 무대를 볼 때 태양을 정면으로 마주보면 관람이 불가능하다.
무대가 바라보는 방향(facing)의 반대편이 관객 시선 방향이므로,
관객 시선과 태양 방위가 가까울수록 나쁘다.

TODO(S3): 태양 고도에 따른 가중(고도 15도 이하에서 눈부심 급증) 반영.
"""

from __future__ import annotations

from stage_scout.domain.model.environment import SolarTrack
from stage_scout.domain.model.geo import Bearing

GLARE_ANGLE_THRESHOLD_DEG = 45.0
LOW_SUN_ALTITUDE_DEG = 15.0


def audience_view_bearing(stage_facing: Bearing) -> Bearing:
    """무대가 바라보는 방향의 역방향 = 관객이 무대를 보는 방향."""
    return Bearing(stage_facing.degrees + 180.0)


def glare_ratio(stage_facing: Bearing, track: SolarTrack) -> float:
    """공연 시간대 중 역광에 노출되는 비율(0.0~1.0). 낮을수록 좋다."""
    raise NotImplementedError("S3에서 구현")
