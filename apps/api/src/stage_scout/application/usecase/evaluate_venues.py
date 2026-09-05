"""S3: 공연 일자 기준 후보지 평가.

환경 데이터(태양·기상·접근성)를 모아 CriterionScore 로 바꾼 뒤
도메인 서비스에 합산을 위임한다.
"""

from __future__ import annotations

from uuid import UUID

from stage_scout.application.port.inbound.use_cases import ScoredVenue
from stage_scout.application.port.outbound.environment import SolarPort, WeatherPort
from stage_scout.application.port.outbound.repository import EventRepository, VenueRepository


class EvaluateVenuesService:
    def __init__(
        self,
        venues: VenueRepository,
        events: EventRepository,
        solar: SolarPort,
        weather: WeatherPort,
    ) -> None:
        self._venues = venues
        self._events = events
        self._solar = solar
        self._weather = weather

    def evaluate(self, event_id: UUID) -> list[ScoredVenue]:
        raise NotImplementedError("S3에서 구현")
