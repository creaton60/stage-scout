# ADR-0003. 백엔드를 Python + FastAPI 로 한다

- 상태: 채택
- 일자: 2026-09-05

## 맥락

이 제품의 핵심 난도는 **기하 계산과 영상 처리**에 있다.

- 사진 → 지도 좌표 정합 (호모그래피)
- 세그멘테이션으로 지면·장애물 분리
- 폴리곤 연산, 좌표계 투영
- 태양 궤적 계산

## 결정

| 영역 | 선택 | 이유 |
|---|---|---|
| 백엔드 | Python 3.12 + FastAPI | shapely / pyproj / OpenCV / astral 이 전부 여기 있다 |
| 기하 | shapely, pyproj | 폴리곤 연산과 UTM-K(EPSG:5179) 투영 |
| 태양 | astral | 외부 API 없이 일출·일몰·고도·방위 계산 |
| 저장 | PostgreSQL + PostGIS | 폴리곤을 DB 에서 그대로 다룬다 |
| 프런트 | React + TypeScript + Vite | 지도 위 폴리곤 편집 UI |

JVM(Kotlin/Spring)은 헥사고날 구현이 더 관용적이지만, 비전·기하 라이브러리를
위해 Python 프로세스를 따로 띄우면 **제품의 핵심 가치가 프로세스 경계 너머로 간다.**
경계를 넘나드는 비용이 언어 취향보다 크다고 판단했다.

## 결과

- 정적 타입 보장이 JVM 보다 약하다 → `mypy --strict` 를 CI 필수로 건다.
- 도메인 모델은 pydantic 이 아닌 **표준 dataclass** 로 쓴다 (ADR-0002 의존 규칙).
  pydantic 은 어댑터 경계(HTTP 스키마)에서만 쓴다.

## 대안

- **Kotlin + Spring Boot** — 헥사고날에 관용적이나 비전 파이프라인이 분리된다.
- **Node/TypeScript 단일 스택** — 프런트와 언어를 통일하지만 기하·비전 생태계가 얕다.
