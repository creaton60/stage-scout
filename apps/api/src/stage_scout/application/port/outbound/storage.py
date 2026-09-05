"""원본 사진 바이너리 저장 포트."""

from __future__ import annotations

from typing import Protocol


class PhotoStoragePort(Protocol):
    def put(self, key: str, content: bytes, content_type: str) -> None: ...
    def get(self, key: str) -> bytes: ...
    def presigned_url(self, key: str, ttl_seconds: int) -> str: ...
