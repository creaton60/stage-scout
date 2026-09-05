"""환경 설정. 시크릿은 전부 환경변수에서 읽고 기본값을 두지 않는다."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    naver_map_client_id: str | None
    naver_map_client_secret: str | None
    database_url: str
    photo_bucket: str
    use_real_map: bool

    @staticmethod
    def from_env() -> Settings:
        return Settings(
            naver_map_client_id=os.getenv("NAVER_MAP_CLIENT_ID"),
            naver_map_client_secret=os.getenv("NAVER_MAP_CLIENT_SECRET"),
            database_url=os.getenv("DATABASE_URL", "postgresql://localhost/stage_scout"),
            photo_bucket=os.getenv("PHOTO_BUCKET", "stage-scout-photos"),
            use_real_map=os.getenv("USE_REAL_MAP", "false").lower() == "true",
        )
