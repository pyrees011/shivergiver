from pydantic import BaseModel, Field
from typing import Optional, List

class TrackModel(BaseModel):
    title: str = Field(..., description="The title of the track")
    length: int = Field(..., description="The duration of the track in seconds")
    album_id: Optional[int] = Field(None, description="The associated album ID")

    class Config:
        schema_extra = {
            "example": {
                "title": "Track One",
                "length": 300,
                "album_id": 1
            }
        }

class AlbumModel(BaseModel):
    name: str = Field(..., description="The name of the album")
    artist: str = Field(..., description="The artist of the album")
    tracks: List[TrackModel] = []

    class Config:
        schema_extra = {
            "example": {
                "name": "Album One",
                "artist": "Artist A",
                "tracks": [
                    {"title": "Track One", "length": 300},
                    {"title": "Track Two", "length": 200}
                ]
            }
        }
