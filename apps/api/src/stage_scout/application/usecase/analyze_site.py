"""S4: 현장 사진 업로드 및 지형 분석."""

from __future__ import annotations

from uuid import UUID

from stage_scout.application.port.inbound.use_cases import UploadSitePhotoCommand
from stage_scout.application.port.outbound.repository import PhotoRepository, TerrainRepository
from stage_scout.application.port.outbound.storage import PhotoStoragePort
from stage_scout.application.port.outbound.vision import PhotoAnalysisPort
from stage_scout.domain.model.survey import TerrainAnalysis


class AnalyzeSiteService:
    def __init__(
        self,
        storage: PhotoStoragePort,
        vision: PhotoAnalysisPort,
        photos: PhotoRepository,
        terrains: TerrainRepository,
    ) -> None:
        self._storage = storage
        self._vision = vision
        self._photos = photos
        self._terrains = terrains

    def upload(self, command: UploadSitePhotoCommand) -> UUID:
        raise NotImplementedError("S4에서 구현")

    def analyze(self, venue_id: UUID) -> TerrainAnalysis:
        raise NotImplementedError("S4에서 구현")
