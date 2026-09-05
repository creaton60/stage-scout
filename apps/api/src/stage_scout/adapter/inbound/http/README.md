# HTTP 어댑터 (인바운드)

FastAPI 라우터. 하는 일은 셋뿐이다.

1. HTTP 요청 → 인바운드 포트의 Command DTO 변환
2. 유스케이스 호출
3. 도메인 결과 → 응답 스키마 변환

**금지**: 여기에 도메인 규칙(점수 계산, 배치 판단)을 넣지 않는다.
라우터가 두꺼워지기 시작하면 유스케이스로 옮길 신호다.

| 라우터 | 엔드포인트 | 스프린트 |
|---|---|---|
| `events.py` | `POST /events` | S1 |
| `venues.py` | `POST /events/{id}/venues:search`, `GET /events/{id}/venues` | S2 |
| `evaluation.py` | `GET /events/{id}/venues:ranked` | S3 |
| `photos.py` | `POST /venues/{id}/photos`, `POST /venues/{id}:analyze` | S4 |
| `layouts.py` | `POST /layouts:generate`, `GET /layouts/{id}` | S5 |
| `exports.py` | `GET /layouts/{id}/export.pdf` | S6 |
