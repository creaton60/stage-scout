"""공연 일자에 종속되는 환경 조건. 장소 적합도 평가의 핵심 입력."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from stage_scout.domain.model.geo import Bearing


@dataclass(frozen=True, slots=True)
class SolarPosition:
    """특정 시각의 태양 위치."""

    at: datetime
    altitude_deg: float  # 지평선 기준 고도. 음수면 일몰 이후
    azimuth: Bearing

    @property
    def is_daylight(self) -> bool:
        return self.altitude_deg > 0


@dataclass(frozen=True, slots=True)
class SolarTrack:
    """공연 시간대 전체의 태양 궤적. 역광·눈부심 판정에 쓴다."""

    positions: tuple[SolarPosition, ...]
    sunrise: datetime | None
    sunset: datetime | None


@dataclass(frozen=True, slots=True)
class WeatherForecast:
    """공연 일자 기상 예보."""

    forecast_date: datetime
    precipitation_probability: float  # 0.0 ~ 1.0
    precipitation_mm: float
    temperature_c: float
    wind_speed_ms: float
    wind_direction: Bearing
