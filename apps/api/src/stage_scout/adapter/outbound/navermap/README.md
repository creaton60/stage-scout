# Naver Map 어댑터 (`MapDataPort` 구현)

Naver Cloud Platform Maps API 를 도메인 모델로 번역하는 유일한 지점.
**여기서 나가는 값은 반드시 `stage_scout.domain.model` 타입이어야 한다** — API 응답 dict 가
application 레이어로 새어 나가면 헥사고날 경계가 깨진다.

## 사용 API (S2)

| 용도 | API | 비고 |
|---|---|---|
| 주소 → 좌표 | Geocoding | |
| 좌표 → 주소 | Reverse Geocoding | |
| 장소 검색 | Search / Local | 공원·광장·운동장 카테고리 필터 |
| 배경 지도 | Static Map | 배치도 렌더링 배경(S6) |
| 접근성 | Directions 5 | 최근접 역·주차장까지 거리 |

## 주의

- API 키는 `NAVER_MAP_CLIENT_ID` / `NAVER_MAP_CLIENT_SECRET` 환경변수로만 주입한다. 코드·커밋 금지.
- 호출량 제한이 있으므로 좌표 기준 캐시를 둔다(S2 과제).
- 부지 경계 폴리곤은 Naver 가 직접 주지 않는다 → 공공데이터(연속지적도) 병행. ADR-0004 참고.
