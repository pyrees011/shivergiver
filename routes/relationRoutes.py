from fastapi import APIRouter, Body, Depends

router = APIRouter()
from config.neo4j_config import Neo4jDatabase
from utils.neo_dummy_data import artist_data, album_data, track_data
from decouple import config

uri = config('NEO4J_URI')
user = config('NEO4J_USER')
password = config('NEO4J_PASSWORD')

db = Neo4jDatabase(uri, user, password)


@router.get("/neo4j", tags=["neo4j"])
async def get_neo4j_data():
    for artist in artist_data:
        db.add_artist(artist)

    for album in album_data:
        db.add_album(album)

    for track in track_data:
        db.add_track(track)
        db.create_relationships(track)

    db.close()
    return {"message": "Neo4j data added successfully"}

@router.get("/neo4j/genre", tags=["neo4j"])
async def get_neo4j_genre_data():
    for artist in artist_data:
        for genre in artist['Genres']:
            db.add_genre(genre)
        db.create_genre_relationships(artist)

    db.close()
    return {"message": "Neo4j genre data added successfully"}