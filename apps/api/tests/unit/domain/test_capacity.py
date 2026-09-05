from stage_scout.domain.service.capacity import capacity_for


def test_standing_capacity_excludes_aisle_area() -> None:
    # 100㎡ 중 20%는 통로 → 80㎡ / 0.5㎡ = 160명
    assert capacity_for(100.0, is_standing=True) == 160


def test_seated_capacity_is_lower_than_standing() -> None:
    assert capacity_for(100.0, is_standing=False) < capacity_for(100.0, is_standing=True)


def test_non_positive_area_yields_zero() -> None:
    assert capacity_for(0.0, is_standing=True) == 0
    assert capacity_for(-10.0, is_standing=False) == 0
