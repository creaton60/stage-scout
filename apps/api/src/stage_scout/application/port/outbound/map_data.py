"""지도 데이터 조회 포트. Naver Map 은 이 포트의 한 구현일 뿐이다."""

from __future__ import annotations

from typing import Protocol

from stage_scout.domain.model.geo import BoundingBox, Coordinate, Polygon
from stage_scout.domain.model.venue import AccessProfile, VenueCandidate


class MapDataPort(Protocol):
    """지도 서비스에서 후보지와 그 주변 정보를 가져온다."""

    def search_places(self, keyword: str, area: BoundingBox) -> list[VenueCandidate]:
        """키워드/영역으로 공연 가능 후보지를 검색한다."""
        ...

    def geocode(self, address: str) -> Coordinate | None:
        """주소 → 좌표."""
        ...

    def reverse_geocode(self, point: Coordinate) -> str | None:
        """좌표 → 주소."""
        ...

    def fetch_boundary(self, point: Coordinate) -> Polygon | None:
        """해당 지점이 속한 부지 경계 폴리곤."""
        ...

    def fetch_access_profile(self, point: Coordinate) -> AccessProfile:
        """대중교통·주차·차량 진입 등 접근성 지표."""
        ...

    def fetch_static_map(self, point: Coordinate, zoom: int) -> bytes:
        """배치도 배경으로 쓸 정적 지도 이미지."""
        ...
