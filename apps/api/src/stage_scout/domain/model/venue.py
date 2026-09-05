"""후보 장소 모델. Naver Map 조회 결과가 도메인으로 들어오는 지점."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from stage_scout.domain.model.geo import Coordinate, Polygon


class GroundType(str, Enum):
    GRASS = "grass"
    ASPHALT = "asphalt"
    SOIL = "soil"
    DECK = "deck"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class AccessProfile:
    """접근성 지표. 지도 데이터에서 도출한다."""

    nearest_transit_distance_m: float
    parking_capacity: int | None
    vehicle_accessible: bool


@dataclass(frozen=True, slots=True)
class VenueCandidate:
    """공연 후보지 한 곳."""

    id: UUID
    name: str
    center: Coordinate
    boundary: Polygon | None
    ground_type: GroundType
    access: AccessProfile
    area_sqm: float | None
