"""면적 → 수용 인원 환산.

밀도 기준은 안전 규정에 해당하므로 도메인 상수로 고정하고,
바꿀 일이 생기면 ADR 로 남긴다.
"""

from __future__ import annotations

STANDING_DENSITY_SQM_PER_PERSON = 0.5
SEATED_DENSITY_SQM_PER_PERSON = 1.2
AISLE_RATIO = 0.20  # 통로·비상동선으로 빼두는 면적 비율


def capacity_for(area_sqm: float, *, is_standing: bool) -> int:
    """통로 면적을 제외한 실 수용 인원."""
    if area_sqm <= 0:
        return 0
    density = STANDING_DENSITY_SQM_PER_PERSON if is_standing else SEATED_DENSITY_SQM_PER_PERSON
    usable = area_sqm * (1.0 - AISLE_RATIO)
    return int(usable / density)
