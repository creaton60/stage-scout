"""현장 사진과 그 분석 결과. 지도만으로는 알 수 없는 실제 지형을 담는다."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID

from stage_scout.domain.model.geo import Bearing, Coordinate, Polygon


class ObstacleKind(str, Enum):
    TREE = "tree"
    POLE = "pole"
    BUILDING = "building"
    SLOPE = "slope"
    WATER = "water"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class PhotoPose:
    """사진을 찍은 위치와 방향. EXIF GPS/방위에서 추출한다."""

    shot_at: datetime
    position: Coordinate
    heading: Bearing
    horizontal_fov_deg: float


@dataclass(frozen=True, slots=True)
class SitePhoto:
    """현장 답사 사진 한 장."""

    id: UUID
    venue_id: UUID
    storage_key: str
    pose: PhotoPose | None  # EXIF가 없으면 사용자가 수동 지정


@dataclass(frozen=True, slots=True)
class Obstacle:
    """배치 시 피해야 할 장애물. 사진 좌표를 지도 좌표로 정합한 결과."""

    kind: ObstacleKind
    footprint: Polygon
    height_m: float | None


@dataclass(frozen=True, slots=True)
class TerrainAnalysis:
    """사진 분석 산출물. 이후 배치 최적화의 제약 조건이 된다."""

    venue_id: UUID
    source_photo_ids: tuple[UUID, ...]
    usable_area: Polygon
    obstacles: tuple[Obstacle, ...]
    mean_slope_deg: float
    confidence: float  # 0.0 ~ 1.0
