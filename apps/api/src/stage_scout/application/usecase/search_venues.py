"""S2: 지도 검색 → 후보지 등록.

MapDataPort 호출과 저장만 조율한다. 판단 로직은 도메인에 있다.
"""

from __future__ import annotations

from stage_scout.application.port.inbound.use_cases import SearchVenuesCommand
from stage_scout.application.port.outbound.map_data import MapDataPort
from stage_scout.application.port.outbound.repository import EventRepository, VenueRepository
from stage_scout.domain.model.venue import VenueCandidate


class SearchVenuesService:
    def __init__(
        self,
        map_data: MapDataPort,
        venues: VenueRepository,
        events: EventRepository,
    ) -> None:
        self._map_data = map_data
        self._venues = venues
        self._events = events

    def search(self, command: SearchVenuesCommand) -> list[VenueCandidate]:
        raise NotImplementedError("S2에서 구현")
