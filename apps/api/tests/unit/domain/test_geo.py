import pytest

from stage_scout.domain.model.geo import Bearing, Coordinate

SEOUL_CITY_HALL = Coordinate(37.5663, 126.9779)
GWANGHWAMUN = Coordinate(37.5759, 126.9769)


def test_distance_between_known_points() -> None:
    # 시청 ~ 광화문은 약 1.0~1.2km
    distance = SEOUL_CITY_HALL.distance_to(GWANGHWAMUN)
    assert 900 < distance < 1300


def test_invalid_latitude_rejected() -> None:
    with pytest.raises(ValueError):
        Coordinate(91.0, 126.0)


def test_bearing_normalizes_and_measures_shortest_angle() -> None:
    assert Bearing(370.0).degrees == pytest.approx(10.0)
    assert Bearing(350.0).difference(Bearing(10.0)) == pytest.approx(20.0)
