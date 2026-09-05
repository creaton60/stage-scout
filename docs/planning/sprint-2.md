# Sprint 2 — Naver Map 연동 · 후보지 수집

| | |
|---|---|
| 주차 | W2 |
| 담당 요구사항 | FR-2 (지도 기반 후보지 수집) |
| 브랜치 | `sprint-2-map-data` |
| 선행 | S1 (포트 정의, 도메인 모델) |

## 목표

지도에서 **실제 후보지 데이터를 끌어와** 도메인 모델로 앉힌다.
S1 의 `MapDataPort` 뒤에 진짜 Naver Map 을 붙이고, 저장소를 인메모리에서 PostGIS 로 교체한다.
이 교체가 `config/container.py` 한 줄로 끝나는지가 헥사고날 채택의 첫 시험이다.

## 끝나면 보여줄 수 있는 것

지도에서 "서울숲" 을 검색하면 후보지가 면적·접근성과 함께 목록으로 나오고,
지도 위에 핀과 경계 폴리곤이 그려진다.

## 설계 사항

- [ ] **Naver Map API 매핑 설계** — 어떤 API 가 도메인의 어느 필드를 채우는지 표로 확정
- [ ] **좌표계 정책** — 저장은 WGS84, 면적·거리 계산은 UTM-K(EPSG:5179) 투영. ADR 로 기록
- [ ] **부지 경계 확보 전략 확정** — S1 SPIKE-1 결과에 따라 Naver / 공공데이터 / 수동 입력 조합 결정
- [ ] **캐시 정책** — 좌표 기준 캐시 키, TTL, 무효화 시점 (API 호출량·비용 리스크 대응)
- [ ] **PostGIS 스키마 설계** — 폴리곤 컬럼, 공간 인덱스, 마이그레이션 전략
- [ ] **외부 API 실패 정책** — 타임아웃·재시도·부분 실패 시 어떤 도메인 결과를 돌려줄지

## 개발 사항

- [ ] `NaverMapAdapter` 구현 (`MapDataPort`)
  - [ ] Geocoding / Reverse Geocoding (FR-2.2)
  - [ ] 장소 검색 — 공원·광장·운동장 카테고리 필터 (FR-2.1)
  - [ ] 접근성 수집 — 최근접 역·주차장 거리 (FR-2.4)
  - [ ] Static Map 이미지 조회 (S6 배경으로 재사용)
- [ ] 부지 경계·면적 확보 (FR-2.3) — 공공데이터 어댑터 또는 수동 입력 폴백
- [ ] 응답 → 도메인 타입 번역 계층 (**dict 가 어댑터 밖으로 새지 않게**)
- [ ] 좌표 기준 캐시
- [ ] `SearchVenuesService` 구현 (FR-2.1, FR-2.5)
- [ ] PostGIS 저장소 어댑터 — `VenueRepository`, `EventRepository`
- [ ] DB 마이그레이션 및 로컬 도커 구성
- [ ] 라우터 `POST /events/{id}/venues:search`, `GET /events/{id}/venues`
- [ ] `FakeMapAdapter` — 고정 응답으로 테스트·데모용 (`USE_REAL_MAP=false`)
- [ ] 웹: 지도 표시 + 후보지 핀 + 경계 폴리곤 (FR-2.5)

## 변경되는 리소스

| 리소스 | 변경 |
|---|---|
| `adapter/outbound/navermap/` | 신규 — API 클라이언트, 응답 번역, 캐시 |
| `adapter/outbound/persistence/` | **변경** — 인메모리 → PostGIS (인메모리는 테스트용으로 유지) |
| `application/usecase/search_venues.py` | 구현 채움 |
| `config/container.py` | `USE_REAL_MAP` 에 따른 어댑터 선택 배선 |
| `apps/web/` | 신규 — 지도 화면 |
| **인프라** | **PostgreSQL + PostGIS 인스턴스 신규** |
| **시크릿** | `NAVER_MAP_CLIENT_ID` / `NAVER_MAP_CLIENT_SECRET` 발급·주입 |
| `docs/architecture/adr/` | 좌표계 정책 ADR 추가 |

## 검증할 사항

- [ ] 실제 좌표로 지오코딩 왕복이 맞다 (주소 → 좌표 → 주소)
- [ ] 계약 테스트: 고정 응답으로 어댑터가 도메인 타입을 정확히 만든다 (**실제 API 호출 없이**)
- [ ] 외부 API 응답 dict 가 application 레이어에 도달하지 않는다 (의존 규칙 + 코드 리뷰)
- [ ] API 타임아웃·5xx·빈 결과 각각에서 유스케이스가 정의된 동작을 한다
- [ ] 캐시 적중 시 외부 호출이 발생하지 않는다 (호출 횟수 단언)
- [ ] 면적 계산이 UTM-K 투영 기준으로 맞다 (알려진 공원 면적과 대조)
- [ ] `USE_REAL_MAP=false` 로 전체 테스트가 네트워크 없이 돈다
- [ ] 저장소를 인메모리↔PostGIS 로 바꿔도 유스케이스 테스트가 그대로 통과한다

## 반영되는 기능

- **FR-2.1** 키워드·영역 후보지 검색
- **FR-2.2** 주소 ↔ 좌표 변환
- **FR-2.3** 부지 경계 폴리곤·면적
- **FR-2.4** 접근성 지표 수집
- **FR-2.5** 후보지-공연 연결 및 목록 관리

## 리스크

| 리스크 | 대응 |
|---|---|
| 경계 폴리곤을 어디서도 못 구함 | 수동 폴리곤 입력 UI 를 S2 범위에 포함 (축소 시 우선순위 1) |
| API 호출량 한도 초과 | 캐시 + `FakeMapAdapter` 로 개발 중 실호출 최소화 |
| PostGIS 도입이 1주를 넘김 | 인메모리 유지하고 S3 로 이월 — 포트가 있으므로 이월 비용이 작다 |
