# stage-scout

Naver Map 데이터와 현장 사진을 근거로 **공연 장소를 고르고 무대·관객 배치도를 만드는** 시스템.

## 먼저 읽을 것

| 알고 싶은 것 | 문서 |
|---|---|
| 무엇을 만드는가 | [docs/requirements.md](docs/requirements.md) |
| 왜 이 구조인가 | [docs/architecture/hexagonal.md](docs/architecture/hexagonal.md) |
| 용어의 정확한 뜻 | [docs/domain/glossary.md](docs/domain/glossary.md) |
| 언제 무엇을 하는가 | [docs/planning/roadmap.md](docs/planning/roadmap.md) |
| 왜 그렇게 정했나 | [docs/architecture/adr/](docs/architecture/adr/) |

## 아키텍처 — 이것만은 지킨다

헥사고날(포트-어댑터). **의존은 언제나 안쪽을 향한다.**

```
apps/api/src/stage_scout/
├── domain/          ← 아무것도 import 하지 않음. 순수 규칙
│   ├── model/         엔티티·값 객체 (전부 frozen dataclass)
│   └── service/       한 객체에 안 담기는 계산 규칙
├── application/     ← domain 만 import
│   ├── port/inbound/  "우리가 해줄 수 있는 일" (유스케이스 인터페이스)
│   ├── port/outbound/ "우리가 필요한 것" (Protocol 선언만)
│   └── usecase/       절차 조율. 계산은 domain, I/O 는 adapter 에 위임
├── adapter/         ← 바깥 기술. 교체 대상
│   ├── inbound/http/         FastAPI 라우터
│   └── outbound/navermap|weather|vision|persistence|storage/
└── config/          ← 유일한 조립 지점 (container.py)
```

### 세 줄 규칙

1. `domain` 은 표준 라이브러리 외에 아무것도 import 하지 않는다.
2. `application` 은 `adapter` 를 절대 import 하지 않는다. 외부는 `Protocol` 로만 만난다.
3. 구현체를 고르는 곳은 `config/container.py` 하나다.

규칙은 테스트로 강제된다 → `apps/api/tests/unit/domain/test_dependency_rule.py`.
**이 테스트가 깨지면 예외를 추가하지 말고 코드를 옳은 레이어로 옮긴다.**

## 코드를 어디에 둘지 헷갈릴 때

| 이 코드는… | 여기로 |
|---|---|
| 외부 API 없이 계산되고, 바뀌면 제품 규칙이 바뀐다 | `domain/service/` |
| 여러 포트를 순서대로 부르는 절차다 | `application/usecase/` |
| HTTP·DB·외부 SDK 를 직접 만진다 | `adapter/` |
| "무엇이 필요한지" 선언만 한다 | `application/port/outbound/` |

판단이 안 서면: **목(mock) 없이 테스트 가능한가?** 가능하면 도메인, 아니면 어댑터다.

## 작업 규칙

- 도메인 모델은 표준 `dataclass(frozen=True)`. pydantic 은 어댑터 경계에서만 쓴다.
- 어댑터는 외부 응답(dict/JSON)을 **경계를 넘기 전에** 도메인 타입으로 번역한다.
- 미구현 지점은 `raise NotImplementedError("SN에서 구현")` 로 스프린트를 명시해 둔다.
- 점수를 내는 코드는 **근거 문장(`reason`)을 반드시 함께** 만든다 (NFR-4).
- "최적"이라고 쓰지 않는다. 가중치에 따른 상대값이므로 "적합도 상위"로 쓴다.
- 되돌리기 어려운 결정은 ADR 을 추가한다. 기존 ADR 은 수정하지 않고 새 번호로 대체한다.
- 새 도메인 용어는 용어사전에 먼저 넣고 코드에 반영한다.

## 시크릿

API 키는 환경변수로만 주입한다. 코드·커밋 금지.

```
NAVER_MAP_CLIENT_ID, NAVER_MAP_CLIENT_SECRET, DATABASE_URL, PHOTO_BUCKET, USE_REAL_MAP
```

## 명령어

```bash
cd apps/api
pip install -e ".[dev]"

pytest                    # 전체 테스트
pytest tests/unit/domain  # 도메인 규칙 + 의존 규칙 검사
ruff check src tests
mypy --strict src
```

## 스프린트 진행 상황

각 스프린트는 브랜치 하나 + PR 하나로 진행한다. 현재 상태는
[docs/planning/roadmap.md](docs/planning/roadmap.md) 의 표와 열린 PR 목록을 함께 본다.
