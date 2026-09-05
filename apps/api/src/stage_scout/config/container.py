"""Composition Root — 유일하게 '어떤 어댑터를 쓸지' 아는 곳.

여기 말고 어디에서도 구현체를 직접 import 하지 않는다.
어댑터 교체(인메모리 → PostGIS, 목 지도 → Naver)는 이 파일만 고치면 끝나야 한다.
"""

from __future__ import annotations

from dataclasses import dataclass

from stage_scout.adapter.outbound.persistence.in_memory import (
    InMemoryEventRepository,
    InMemoryLayoutRepository,
    InMemoryPhotoRepository,
    InMemoryTerrainRepository,
    InMemoryVenueRepository,
)
from stage_scout.application.usecase.register_event import RegisterEventService
from stage_scout.config.settings import Settings


@dataclass
class Container:
    """조립된 유스케이스 모음. HTTP 어댑터는 이걸 통해서만 기능에 접근한다."""

    register_event: RegisterEventService


def build_container(settings: Settings) -> Container:
    events = InMemoryEventRepository()
    _venues = InMemoryVenueRepository()
    _photos = InMemoryPhotoRepository()
    _terrains = InMemoryTerrainRepository()
    _layouts = InMemoryLayoutRepository()

    # S2 이후: settings.use_real_map 에 따라 NaverMapAdapter / FakeMapAdapter 선택
    return Container(register_event=RegisterEventService(events))
