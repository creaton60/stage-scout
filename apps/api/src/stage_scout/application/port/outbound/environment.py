"""공연 일자 환경 조건 조회 포트."""

from __future__ import annotations

from datetime import date
from typing import Protocol

from stage_scout.domain.model.environment import SolarTrack, WeatherForecast
from stage_scout.domain.model.event import PerformanceSchedule
from stage_scout.domain.model.geo import Coordinate


class SolarPort(Protocol):
    """태양 궤적 계산. 외부 API 대신 천문 계산 라이브러리로 구현할 수 있다."""

    def track_for(self, point: Coordinate, schedule: PerformanceSchedule) -> SolarTrack:
        ...


class WeatherPort(Protocol):
    """기상 예보 조회. 예보 가능 범위를 넘어서면 None 을 돌려준다."""

    def forecast_for(self, point: Coordinate, target: date) -> WeatherForecast | None:
        ...
