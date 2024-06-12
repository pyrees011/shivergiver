from pydantic import BaseModel, Field
from typing import Optional, List

class TrackModel(BaseModel):
    name: str = Field(..., description="The title of the track")
    Artist_name: int = Field(..., description="The duration of the track in seconds")
    Album_name: Optional[int] = Field(None, description="The associated album ID")

    class Config:
        schema_extra = {
            "example": {
                "name": "Track One",
                "Artist_name": "Artist One",
                "Album_name": "Album One"
            }
        }

class AlbumModel(BaseModel):
    name: str = Field(..., description="The name of the album")
    Release_Date: str = Field(..., description="The artist of the album")
    Total_tracks: int = Field(..., description="The total number of tracks in the album")

    class Config:
        schema_extra = {
            "example": {
                "name": "Album One",
                "Release_Date": "2021-01-01",
                "Total_tracks": 10
            }
        }
