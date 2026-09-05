"""공연 요구사항 모델. '무엇을 언제 얼마나' 여는지를 표현한다."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time
from enum import Enum
from uuid import UUID


class StageType(str, Enum):
    PROSCENIUM = "proscenium"  # 정면 관람형
    THRUST = "thrust"  # 돌출형(3면 관람)
    ARENA = "arena"  # 사방 관람


@dataclass(frozen=True, slots=True)
class StageRequirement:
    """무대 자체가 요구하는 물리 조건."""

    stage_type: StageType
    width_m: float
    depth_m: float
    height_m: float
    needs_power: bool
    needs_vehicle_access: bool


@dataclass(frozen=True, slots=True)
class PerformanceSchedule:
    """공연 일자와 시간대. 태양 궤적·기상 평가의 입력."""

    performance_date: date
    start_time: time
    end_time: time
    setup_hours: float
    teardown_hours: float


@dataclass(frozen=True, slots=True)
class PerformanceEvent:
    """장소 선정의 기준이 되는 공연 한 건."""

    id: UUID
    title: str
    schedule: PerformanceSchedule
    expected_audience: int
    stage_requirement: StageRequirement
