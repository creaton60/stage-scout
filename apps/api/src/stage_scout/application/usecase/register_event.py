"""S1: 공연 등록. 가장 단순한 유스케이스이자 배선(wiring) 검증용 슬라이스."""

from __future__ import annotations

from uuid import uuid4

from stage_scout.application.port.inbound.use_cases import RegisterEventCommand
from stage_scout.application.port.outbound.repository import EventRepository
from stage_scout.domain.model.event import (
    PerformanceEvent,
    PerformanceSchedule,
    StageRequirement,
)


class RegisterEventService:
    def __init__(self, events: EventRepository) -> None:
        self._events = events

    def register(self, command: RegisterEventCommand) -> PerformanceEvent:
        event = PerformanceEvent(
            id=uuid4(),
            title=command.title,
            schedule=PerformanceSchedule(
                performance_date=command.performance_date,
                start_time=command.start_time,
                end_time=command.end_time,
                setup_hours=4.0,
                teardown_hours=2.0,
            ),
            expected_audience=command.expected_audience,
            stage_requirement=StageRequirement(
                stage_type=command.stage_type,
                width_m=command.stage_width_m,
                depth_m=command.stage_depth_m,
                height_m=1.2,
                needs_power=True,
                needs_vehicle_access=True,
            ),
        )
        self._events.save(event)
        return event
