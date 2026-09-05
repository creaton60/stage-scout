# Sprint 1 — 기반 구축 · 도메인 모델링 · 리스크 스파이크

| | |
|---|---|
| 주차 | W1 |
| 담당 요구사항 | FR-1 (공연 등록) |
| 브랜치 | `sprint-1-foundation` |

## 목표

**뒤 5개 스프린트가 딛고 설 바닥을 만든다.** 그리고 이 프로젝트를 통째로 무너뜨릴 수 있는
기술 리스크 두 개를 1주차에 미리 건드려 본다 — 실패한다면 6주차가 아니라 지금 알아야 한다.

## 끝나면 보여줄 수 있는 것

공연을 등록하면 저장되고 다시 조회되는 **동작하는 API 한 줄기**.
인메모리 저장소를 쓰지만 HTTP → 유스케이스 → 도메인 → 포트 → 어댑터가 실제로 관통한다.

## 설계 사항

- [ ] **도메인 모델 확정** — 공연/장소/환경/답사/배치/평가 6개 묶음의 엔티티와 값 객체
- [ ] **포트 경계 확정** — 아웃바운드 포트 5종(`MapDataPort`, `SolarPort`, `WeatherPort`,
      `PhotoAnalysisPort`, 각종 `Repository`)의 시그니처를 못박는다.
      **S3·S5 가 이 시그니처에 의존하므로 여기서 흔들리면 뒤가 전부 흔들린다.**
- [ ] **용어사전 1차** — 코드·문서·대화에서 같은 단어를 같은 뜻으로 쓰기 위한 목록
- [ ] **ADR-0002/0003 확정** — 헥사고날 채택 근거, Python/FastAPI 선택 근거
- [ ] **ADR-0004 검증** — 사진-지도 정합 방식을 스파이크 결과로 확정 또는 대체

## 개발 사항

- [ ] 프로젝트 스캐폴딩 (`apps/api` 헥사고날 디렉터리, `pyproject.toml`)
- [ ] 도메인 모델 구현 — `geo`, `event`, `venue`, `environment`, `survey`, `layout`, `scoring`
- [ ] 도메인 서비스 `capacity.py` 구현 (면적 → 수용 인원, 통로 20% 공제)
- [ ] 인바운드/아웃바운드 포트 Protocol 선언
- [ ] `RegisterEventService` 구현 (FR-1.1~1.3)
- [ ] 인메모리 저장소 어댑터 5종
- [ ] Composition Root (`config/container.py`), 설정 로더 (`config/settings.py`)
- [ ] FastAPI 라우터 `POST /events`, `GET /events/{id}`
- [ ] **의존 규칙 테스트** — domain→외부 import 금지, application→adapter 금지
- [ ] CI: `pytest` + `ruff check` + `mypy --strict`

## 스파이크 (타임박스 각 1일)

- [ ] **SPIKE-1: Naver Map 부지 경계**
      Naver Map API 가 공원·광장의 경계 폴리곤을 주는지 확인.
      안 주면 공공데이터 연속지적도 대안을 검증하고 ADR 로 남긴다.
- [ ] **SPIKE-2: 사진-지도 정합 (ADR-0004)**
      실제 공원 사진 5장으로 EXIF 추출 → 호모그래피 투영을 시도.
      **판정 기준: 지상 기준점 오차 5m 이내면 S4 원안 유지, 초과면 S4 를 수동 편집 중심으로 축소.**

## 변경되는 리소스

| 리소스 | 변경 |
|---|---|
| `apps/api/src/stage_scout/domain/` | 신규 — 모델 7개, 서비스 5개 |
| `apps/api/src/stage_scout/application/` | 신규 — 포트 6개, 유스케이스 5개(1개 구현, 4개 뼈대) |
| `apps/api/src/stage_scout/adapter/outbound/persistence/` | 신규 — 인메모리 저장소 |
| `apps/api/src/stage_scout/adapter/inbound/http/` | 신규 — events 라우터 |
| `apps/api/src/stage_scout/config/` | 신규 — Composition Root, 설정 |
| `apps/api/tests/` | 신규 — 도메인 단위 테스트, 의존 규칙 테스트 |
| `docs/` | 신규 — 요구사항, 아키텍처, ADR 4건, 용어사전, 로드맵 |
| 외부 | GitHub 저장소·Project 생성. 인프라 없음 |

## 검증할 사항

- [ ] `POST /events` → `GET /events/{id}` 왕복이 실제로 동작한다
- [ ] 의존 규칙 테스트 3건 통과 (이게 깨지면 아키텍처가 무너진 것)
- [ ] `capacity_for(100㎡, 입석)` = 160명 — 통로 20% 공제가 반영됐는지
- [ ] 위경도 범위 밖 좌표가 `ValueError` 로 거부된다
- [ ] `Bearing(370°)` → 10° 정규화, 350°와 10°의 사잇각 = 20°
- [ ] `mypy --strict` 통과 (Python 선택의 대가를 여기서 치른다)
- [ ] 시크릿이 코드·커밋에 없다 (`.env.example` 만 커밋)
- [ ] SPIKE-2 결과가 ADR-0004 에 판정과 함께 기록됐다

## 반영되는 기능

- **FR-1.1** 공연명·일자·시각·예상 관객 수 등록
- **FR-1.2** 무대 형태·규격 등록
- **FR-1.3** 셋업·철수 시간 등록

## 다음 스프린트로 넘기는 것

- 실제 영속성(PostGIS)은 S2 — S1 은 인메모리로 흐름만 뚫는다
- 지도 어댑터 실구현은 S2 — S1 은 포트 선언까지

## 리스크

| 리스크 | 대응 |
|---|---|
| 포트 시그니처를 잘못 잡으면 S3·S5 에서 대공사 | 스파이크 결과를 반영한 뒤 확정 |
| 스파이크 2건이 1주를 잡아먹음 | 각 1일 타임박스. 초과 시 결론 없이도 중단하고 ADR 에 "미결"로 기록 |
