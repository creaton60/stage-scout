"""지리 좌표계 값 객체.

이 모듈은 외부 지도 서비스(Naver Map 등)에 의존하지 않는다.
좌표계는 WGS84(위경도)를 기준으로 하고, 면적/거리 계산이 필요한 경우
어댑터가 UTM-K(EPSG:5179) 등으로 투영해 전달한다.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

EARTH_RADIUS_M = 6_371_008.8


@dataclass(frozen=True, slots=True)
class Coordinate:
    """WGS84 위경도 한 점."""

    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if not -90.0 <= self.latitude <= 90.0:
            raise ValueError(f"latitude out of range: {self.latitude}")
        if not -180.0 <= self.longitude <= 180.0:
            raise ValueError(f"longitude out of range: {self.longitude}")

    def distance_to(self, other: Coordinate) -> float:
        """두 점 사이의 대권 거리(m). Haversine."""
        lat1, lat2 = math.radians(self.latitude), math.radians(other.latitude)
        dlat = lat2 - lat1
        dlon = math.radians(other.longitude - self.longitude)
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        return 2 * EARTH_RADIUS_M * math.asin(math.sqrt(a))


@dataclass(frozen=True, slots=True)
class Bearing:
    """진북 기준 방위각(0~360, 시계 방향). 무대 정면 방향·태양 방위 표현에 쓴다."""

    degrees: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "degrees", self.degrees % 360.0)

    def difference(self, other: Bearing) -> float:
        """두 방위 사이의 최소 사잇각(0~180)."""
        raw = abs(self.degrees - other.degrees) % 360.0
        return min(raw, 360.0 - raw)


@dataclass(frozen=True, slots=True)
class BoundingBox:
    """지도 검색 범위."""

    south_west: Coordinate
    north_east: Coordinate

    def contains(self, point: Coordinate) -> bool:
        return (
            self.south_west.latitude <= point.latitude <= self.north_east.latitude
            and self.south_west.longitude <= point.longitude <= self.north_east.longitude
        )


@dataclass(frozen=True, slots=True)
class Polygon:
    """단순 폴리곤. 부지 경계·가용 영역·관객 구역 경계에 공통으로 쓴다."""

    exterior: tuple[Coordinate, ...]

    def __post_init__(self) -> None:
        if len(self.exterior) < 3:
            raise ValueError("polygon needs at least 3 vertices")

    @property
    def centroid(self) -> Coordinate:
        lat = sum(c.latitude for c in self.exterior) / len(self.exterior)
        lon = sum(c.longitude for c in self.exterior) / len(self.exterior)
        return Coordinate(lat, lon)
