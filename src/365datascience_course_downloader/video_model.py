from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class PosterSource(BaseModel):
    class Config:
        allow_population_by_field_name = True

    src: str


class ThumbnailSource(PosterSource):
    pass


class Source(BaseModel):
    class Config:
        allow_population_by_field_name = True

    codecs: Optional[str] = None
    ext_x_version: Optional[str] = None
    src: str
    type: Optional[str] = None
    profiles: Optional[str] = None
    avg_bitrate: Optional[int] = None
    codec: Optional[str] = None
    container: Optional[str] = None
    duration: Optional[int] = None
    height: Optional[int] = None
    size: Optional[int] = None
    width: Optional[int] = None


class TextTrack(BaseModel):
    class Config:
        allow_population_by_field_name = True

    id: Any
    account_id: str
    src: str
    srclang: Any
    label: str
    kind: str
    mime_type: str
    asset_id: Any
    sources: Any
    default: bool
    width: Optional[int] = None
    height: Optional[int] = None
    bandwidth: Optional[int] = None


class VideoModel(BaseModel):
    class Config:
        allow_population_by_field_name = True

    poster: str
    thumbnail: str
    poster_sources: List[PosterSource]
    thumbnail_sources: List[ThumbnailSource]
    description: Any
    tags: List
    cue_points: List
    custom_fields: Dict[str, Any]
    account_id: str
    sources: List[Source]
    name: str
    reference_id: Any
    long_description: Any
    duration: int
    economics: str
    text_tracks: List[TextTrack]
    published_at: str
    created_at: str
    updated_at: str
    offline_enabled: bool
    link: Any
    id: str
    ad_keys: Any