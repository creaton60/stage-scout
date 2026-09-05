"""무대·관객 배치도. 이 시스템의 최종 산출물."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from stage_scout.domain.model.geo import Bearing, Coordinate, Polygon


@dataclass(frozen=True, slots=True)
class StagePlacement:
    """무대를 어디에 어느 방향으로 놓을지."""

    center: Coordinate
    facing: Bearing  # 무대가 관객을 바라보는 방향
    width_m: float
    depth_m: float


@dataclass(frozen=True, slots=True)
class SeatingZone:
    """관객 구역 하나. 무대로부터의 거리대별로 나눈다."""

    name: str
    area: Polygon
    capacity: int
    is_standing: bool


@dataclass(frozen=True, slots=True)
class SightLine:
    """특정 관객 지점에서 무대가 보이는 정도."""

    from_point: Coordinate
    horizontal_angle_deg: float  # 무대 정면 기준 이탈 각
    distance_m: float
    blocked_by: str | None


@dataclass(frozen=True, slots=True)
class LayoutPlan:
    """무대 + 관객 구역 + 동선을 합친 배치안 하나."""

    id: UUID
    venue_id: UUID
    event_id: UUID
    stage: StagePlacement
    zones: tuple[SeatingZone, ...]
    aisles: tuple[Polygon, ...]
    total_capacity: int
