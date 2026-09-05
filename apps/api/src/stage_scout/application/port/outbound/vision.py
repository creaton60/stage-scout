"""현장 사진 분석 포트.

모델 교체(온프레미스 세그멘테이션 ↔ 외부 비전 API)를 어댑터 교체로 처리하기 위해
유스케이스는 이 포트만 안다.
"""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from stage_scout.domain.model.geo import Polygon
from stage_scout.domain.model.survey import Obstacle, PhotoPose, SitePhoto, TerrainAnalysis


class PhotoAnalysisPort(Protocol):
    def extract_pose(self, image: bytes) -> PhotoPose | None:
        """EXIF 에서 촬영 위치·방위·화각을 추출한다."""
        ...

    def detect_obstacles(self, image: bytes, pose: PhotoPose) -> list[Obstacle]:
        """사진에서 장애물을 검출하고 지도 좌표로 정합한다."""
        ...

    def estimate_usable_area(self, image: bytes, pose: PhotoPose) -> Polygon:
        """평탄하고 비어 있는 가용 영역을 추정한다."""
        ...

    def analyze(self, venue_id: UUID, photos: list[tuple[SitePhoto, bytes]]) -> TerrainAnalysis:
        """여러 장을 종합해 하나의 지형 분석 결과를 만든다."""
        ...
