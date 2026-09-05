# 헥사고날 아키텍처 가이드

## 왜 헥사고날인가

이 시스템의 바깥쪽은 **전부 흔들린다**. 지도 API 는 Naver 에서 바뀔 수 있고, 사진 분석 모델은
6주 안에도 두세 번 갈아끼울 것이며, 기상 예보 출처도 미정이다. 반면 안쪽 규칙 — 역광이 나쁘다,
통로는 20% 확보한다, 시야각 60도를 넘으면 관람이 어렵다 — 은 잘 바뀌지 않는다.

**자주 바뀌는 것을 잘 안 바뀌는 것 바깥에 두는 것**이 이 구조의 전부다.

## 레이어와 의존 방향

```
                      ┌─────────────────────────────────┐
        HTTP 요청  ──▶ │  adapter/inbound/http           │
                      │  (FastAPI 라우터)                │
                      └────────────┬────────────────────┘
                                   │ 호출
                                   ▼
                      ┌─────────────────────────────────┐
                      │  application/port/inbound        │  ← 우리가 제공하는 기능 목록
                      │  application/usecase             │  ← 절차 조율만
                      └────────────┬────────────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
              ┌──────────┐  ┌─────────────────────────┐
              │ domain   │  │ application/port/outbound│  ← 우리가 필요로 하는 것
              │ (규칙)    │  │ (Protocol 선언만)        │
              └──────────┘  └────────────┬────────────┘
                                         │ 구현
                    ┌────────────────────┼────────────────────┐
                    ▼                    ▼                    ▼
            ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
            │ navermap     │    │ vision       │    │ persistence  │
            │ (지도 API)    │    │ (사진 분석)   │    │ (PostGIS)    │
            └──────────────┘    └──────────────┘    └──────────────┘
                                adapter/outbound
```

**화살표는 언제나 안쪽을 향한다.** 바깥이 안을 알고, 안은 바깥을 모른다.

## 세 줄 규칙

1. `domain` 은 아무것도 import 하지 않는다.
2. `application` 은 `domain` 만 import 한다. 어댑터는 `Protocol` 을 통해서만 만난다.
3. 구현체를 고르는 곳은 `config/container.py` 하나뿐이다.

이 규칙은 문서가 아니라 **테스트로 강제**된다 →
`apps/api/tests/unit/domain/test_dependency_rule.py`

## 인바운드 포트 vs 아웃바운드 포트

헷갈리기 쉬운 지점이라 방향으로 외운다.

| | 인바운드 포트 | 아웃바운드 포트 |
|---|---|---|
| 뜻 | "우리가 **해줄 수 있는** 일" | "우리가 **필요한** 것" |
| 누가 구현? | 우리 (`application/usecase/`) | 어댑터 (`adapter/outbound/`) |
| 누가 호출? | 어댑터 (HTTP 라우터) | 우리 (유스케이스) |
| 예 | `GenerateLayoutUseCase` | `MapDataPort`, `PhotoAnalysisPort` |

## 새 기능을 넣을 때 어디를 만지나

> "공연 일자에 해당 지역 축제가 겹치는지 확인하고 감점하고 싶다"

1. `domain/model/scoring.py` 에 `Criterion.EVENT_CONFLICT` 추가
2. `domain/service/suitability.py` 가중치에 추가 — **여기까지가 규칙**
3. `application/port/outbound/` 에 `LocalEventPort` Protocol 선언 — **필요한 것 선언**
4. `application/usecase/evaluate_venues.py` 에서 호출 순서 추가 — **절차**
5. `adapter/outbound/localevent/` 에 실제 API 클라이언트 구현 — **기술**
6. `config/container.py` 에서 배선

1~4 는 외부 API 없이 테스트할 수 있다. 그게 이 구조를 쓰는 이유다.

## 흔한 실수

| 실수 | 왜 문제인가 | 대신 |
|---|---|---|
| 유스케이스에서 `httpx` 직접 호출 | 테스트에 네트워크가 필요해진다 | 아웃바운드 포트 선언 후 어댑터에서 호출 |
| 어댑터가 API 응답 dict 를 그대로 반환 | 외부 스키마가 도메인에 새어든다 | 어댑터 안에서 도메인 타입으로 번역 |
| 도메인 dataclass 에 `@field_validator` (pydantic) | 도메인이 프레임워크에 묶인다 | 표준 dataclass + `__post_init__` |
| 라우터에서 점수 계산 | 규칙이 HTTP 에 묶여 재사용 불가 | 도메인 서비스로 이동 |
