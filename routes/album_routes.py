from fastapi import APIRouter, HTTPException, status, Depends
from models.music_models import AlbumModel, TrackModel
from typing import List
from bson import ObjectId

from auth.auth_bearer import JWTBearer
from config.mongo_config import db

from utils.redis_helper import check_redis_cache, get_album, store_album, delete_album
from schema.schemas import individual_schema, many_schema

router = APIRouter(
    prefix="/albums",
    tags=["albums"],
    responses={404: {"description": "Not found"}},
)

album_collection = db.albums

@router.get("/", dependencies=[Depends(JWTBearer())], response_model=List[AlbumModel])
async def get_albums():
    albums = album_collection.find()
    return many_schema(albums)

@router.post("/", dependencies=[Depends(JWTBearer())], response_model=AlbumModel)
async def create_album(album: AlbumModel):
    album_data = album.dict()
    result = album_collection.insert_one(album_data)

    album_id = str(result.inserted_id)
    store_album(album_id, album_data)
    return album

@router.get("/{album_id}", dependencies=[Depends(JWTBearer())], response_model=AlbumModel)
async def get_album(album_id: str):
    if check_redis_cache(album_id, "album"):
        return get_album(album_id)
    album = album_collection.find_one({"_id": ObjectId(album_id)})
    if album:
        store_album(album_id, album)
        return individual_schema(album)
    raise HTTPException(status_code=404, detail="Album not found")

@router.put("/{album_id}", dependencies=[Depends(JWTBearer())], response_model=AlbumModel)
async def update_album(album_id: str, album: AlbumModel):
    updated_album = album_collection.find_one_and_update(
        {"_id": ObjectId(album_id)}, {"$set": album.dict()}, return_document=True
    )
    if updated_album:
        store_album(album_id, updated_album)
        return individual_schema(updated_album)
    raise HTTPException(status_code=404, detail="Album not found")

@router.delete("/{album_id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT)
async def delete_album(album_id: str):
    album = album_collection.find_one({"_id": ObjectId(album_id)})
    if album:
        delete_album(album_id)
        album_collection.delete_one({"_id": ObjectId(album_id)})
        return
    raise HTTPException(status_code=404, detail="Album not found")
