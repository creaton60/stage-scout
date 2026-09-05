"""S5: 무대·관객 배치안 생성.

흐름: 지형 분석 + 환경 조건 → 무대 후보 생성 → 시야선 평가 → 관객 구역 산출 → 상위 N안.
"""

from __future__ import annotations

from stage_scout.application.port.inbound.use_cases import GenerateLayoutCommand
from stage_scout.application.port.outbound.environment import SolarPort, WeatherPort
from stage_scout.application.port.outbound.repository import (
    EventRepository,
    LayoutRepository,
    TerrainRepository,
    VenueRepository,
)
from stage_scout.domain.model.layout import LayoutPlan


class GenerateLayoutService:
    def __init__(
        self,
        venues: VenueRepository,
        events: EventRepository,
        terrains: TerrainRepository,
        layouts: LayoutRepository,
        solar: SolarPort,
        weather: WeatherPort,
    ) -> None:
        self._venues = venues
        self._events = events
        self._terrains = terrains
        self._layouts = layouts
        self._solar = solar
        self._weather = weather

    def generate(self, command: GenerateLayoutCommand) -> list[LayoutPlan]:
        raise NotImplementedError("S5에서 구현")
