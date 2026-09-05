"""인바운드 포트 = 이 시스템이 바깥에 제공하는 기능 목록.

HTTP 어댑터도 CLI 도 배치 잡도 이 Protocol 만 호출한다.
커맨드/결과 DTO 는 도메인 객체를 그대로 노출하지 않기 위해 여기서 정의한다.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time
from typing import Protocol
from uuid import UUID

from stage_scout.domain.model.event import PerformanceEvent, StageType
from stage_scout.domain.model.geo import BoundingBox
from stage_scout.domain.model.layout import LayoutPlan
from stage_scout.domain.model.scoring import SuitabilityScore
from stage_scout.domain.model.survey import TerrainAnalysis
from stage_scout.domain.model.venue import VenueCandidate


# --- Commands -------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RegisterEventCommand:
    title: str
    performance_date: date
    start_time: time
    end_time: time
    expected_audience: int
    stage_type: StageType
    stage_width_m: float
    stage_depth_m: float


@dataclass(frozen=True, slots=True)
class SearchVenuesCommand:
    event_id: UUID
    keyword: str
    area: BoundingBox


@dataclass(frozen=True, slots=True)
class UploadSitePhotoCommand:
    venue_id: UUID
    filename: str
    content: bytes
    content_type: str


@dataclass(frozen=True, slots=True)
class GenerateLayoutCommand:
    event_id: UUID
    venue_id: UUID
    alternatives: int = 3


@dataclass(frozen=True, slots=True)
class ScoredVenue:
    venue: VenueCandidate
    score: SuitabilityScore


# --- Inbound ports --------------------------------------------------------


class RegisterEventUseCase(Protocol):
    def register(self, command: RegisterEventCommand) -> PerformanceEvent: ...


class SearchVenuesUseCase(Protocol):
    """S2: 지도에서 후보지를 찾아 이벤트에 붙인다."""

    def search(self, command: SearchVenuesCommand) -> list[VenueCandidate]: ...


class EvaluateVenuesUseCase(Protocol):
    """S3: 공연 일자 기준으로 후보지를 평가·정렬한다."""

    def evaluate(self, event_id: UUID) -> list[ScoredVenue]: ...


class AnalyzeSiteUseCase(Protocol):
    """S4: 현장 사진을 올리고 지형 분석 결과를 얻는다."""

    def upload(self, command: UploadSitePhotoCommand) -> UUID: ...
    def analyze(self, venue_id: UUID) -> TerrainAnalysis: ...


class GenerateLayoutUseCase(Protocol):
    """S5: 무대·관객 배치안을 생성한다."""

    def generate(self, command: GenerateLayoutCommand) -> list[LayoutPlan]: ...


class ExportLayoutUseCase(Protocol):
    """S6: 배치안을 도면으로 내보낸다."""

    def export_pdf(self, plan_id: UUID) -> bytes: ...
