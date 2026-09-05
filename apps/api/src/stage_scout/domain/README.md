# domain — 가장 안쪽 레이어

공연 장소 선정과 배치 설계의 **규칙 그 자체**. 육각형의 중심이다.

## 의존 규칙

- 이 디렉터리는 **아무것도 import 하지 않는다** (표준 라이브러리 제외).
- `application`, `adapter`, FastAPI, DB 드라이버, HTTP 클라이언트 → 전부 금지.
- 위반 여부는 `tests/unit/domain/test_dependency_rule.py` 가 자동 검사한다.

## 구성

- `model/` — 엔티티와 값 객체. 전부 `frozen=True` 불변 dataclass.
- `service/` — 한 객체에 담기 어려운 순수 계산 규칙.
