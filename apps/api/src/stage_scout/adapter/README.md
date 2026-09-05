# adapter — 바깥 세계와의 접점

기술이 바뀌면 **여기만** 바뀐다.

## 구성

```
inbound/http/          FastAPI 라우터        (인바운드 포트를 호출)
outbound/navermap/     Naver Map API         (MapDataPort 구현)
outbound/weather/      기상 예보 API          (WeatherPort 구현)
outbound/vision/       사진 분석 파이프라인    (PhotoAnalysisPort 구현)
outbound/persistence/  PostgreSQL + PostGIS  (각종 Repository 구현)
outbound/storage/      오브젝트 스토리지       (PhotoStoragePort 구현)
```

## 의존 규칙

- `domain` 과 `application.port` 를 import 한다.
- `application.usecase` 의 **구현체**는 import 하지 않는다 — 조립은 `config/container.py` 담당.
- 외부 응답(dict/JSON)은 어댑터 경계를 넘기 전에 도메인 타입으로 번역한다.
