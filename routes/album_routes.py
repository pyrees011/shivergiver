from fastapi import APIRouter, HTTPException, status, Depends
from models.music_models import AlbumModel, TrackModel
from typing import List

router = APIRouter(
    prefix="/albums",
    tags=["albums"],
    responses={404: {"description": "Not found"}},
)

# Mock database for demonstration
db = []

@router.get("/", response_model=List[AlbumModel])
async def read_albums():
    return db

@router.post("/", response_model=AlbumModel, status_code=status.HTTP_201_CREATED)
async def create_album(album: AlbumModel):
    db.append(album)
    return album

@router.get("/{album_id}", response_model=AlbumModel)
async def read_album(album_id: int):
    album = next((a for a in db if a.id == album_id), None)
    if album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return album

@router.put("/{album_id}", response_model=AlbumModel)
async def update_album(album_id: int, album_update: AlbumModel):
    index = next((i for i, a in enumerate(db) if a.id == album_id), -1)
    if index == -1:
        raise HTTPException(status_code=404, detail="Album not found")
    db[index] = album_update
    return album_update

@router.delete("/{album_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_album(album_id: int):
    index = next((i for i, a in enumerate(db) if a.id == album_id), -1)
    if index == -1:
        raise HTTPException(status_code=404, detail="Album not found")
    db.pop(index)
    return {"message": "Album deleted successfully"}
