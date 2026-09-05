"""인메모리 저장소. S1 수직 슬라이스와 테스트에서 쓰고, S2에서 PostGIS 어댑터로 교체한다.

포트를 지키는 한 유스케이스는 어느 쪽이 붙었는지 알 필요가 없다 —
이 어댑터의 존재 자체가 헥사고날 경계가 살아 있다는 증거다.
"""

from __future__ import annotations

from uuid import UUID

from stage_scout.domain.model.event import PerformanceEvent
from stage_scout.domain.model.layout import LayoutPlan
from stage_scout.domain.model.survey import SitePhoto, TerrainAnalysis
from stage_scout.domain.model.venue import VenueCandidate


class InMemoryEventRepository:
    def __init__(self) -> None:
        self._items: dict[UUID, PerformanceEvent] = {}

    def save(self, event: PerformanceEvent) -> None:
        self._items[event.id] = event

    def find_by_id(self, event_id: UUID) -> PerformanceEvent | None:
        return self._items.get(event_id)


class InMemoryVenueRepository:
    def __init__(self) -> None:
        self._items: dict[UUID, VenueCandidate] = {}
        self._by_event: dict[UUID, list[UUID]] = {}

    def save(self, venue: VenueCandidate) -> None:
        self._items[venue.id] = venue

    def find_by_id(self, venue_id: UUID) -> VenueCandidate | None:
        return self._items.get(venue_id)

    def find_all_for_event(self, event_id: UUID) -> list[VenueCandidate]:
        return [self._items[v] for v in self._by_event.get(event_id, []) if v in self._items]

    def link_to_event(self, event_id: UUID, venue_id: UUID) -> None:
        self._by_event.setdefault(event_id, []).append(venue_id)


class InMemoryPhotoRepository:
    def __init__(self) -> None:
        self._items: dict[UUID, SitePhoto] = {}

    def save(self, photo: SitePhoto) -> None:
        self._items[photo.id] = photo

    def find_by_venue(self, venue_id: UUID) -> list[SitePhoto]:
        return [p for p in self._items.values() if p.venue_id == venue_id]


class InMemoryTerrainRepository:
    def __init__(self) -> None:
        self._items: dict[UUID, TerrainAnalysis] = {}

    def save(self, analysis: TerrainAnalysis) -> None:
        self._items[analysis.venue_id] = analysis

    def find_by_venue(self, venue_id: UUID) -> TerrainAnalysis | None:
        return self._items.get(venue_id)


class InMemoryLayoutRepository:
    def __init__(self) -> None:
        self._items: dict[UUID, LayoutPlan] = {}

    def save(self, plan: LayoutPlan) -> None:
        self._items[plan.id] = plan

    def find_by_id(self, plan_id: UUID) -> LayoutPlan | None:
        return self._items.get(plan_id)

    def find_by_event(self, event_id: UUID) -> list[LayoutPlan]:
        return [p for p in self._items.values() if p.event_id == event_id]
