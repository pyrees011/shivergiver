from neo4j import GraphDatabase

class Neo4jDatabase:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_artist(self, artist):
        with self.driver.session() as session:
            session.write_transaction(self._create_artist_node, artist)

    def add_album(self, album):
        with self.driver.session() as session:
            session.write_transaction(self._create_album_node, album)

    def add_track(self, track):
        with self.driver.session() as session:
            session.write_transaction(self._create_track_node, track)

    def add_genre(self, genre):
        with self.driver.session() as session:
            session.write_transaction(self._create_genre_node, genre)

    def create_relationships(self, track):
        with self.driver.session() as session:
            session.write_transaction(self._create_relationships, track)

    def create_genre_relationships(self, artist):
        with self.driver.session() as session:
            session.write_transaction(self._create_genre_relationships, artist)

    @staticmethod
    def _create_artist_node(tx, artist):
        tx.run("MERGE (a:Artist {name: $name, genres: $genres, popularity: $popularity})",
               name=artist['Name'], genres=artist['Genres'], popularity=artist['Popularity'])

    @staticmethod
    def _create_album_node(tx, album):
        tx.run("MERGE (a:Album {name: $name, release_date: $release_date, total_tracks: $total_tracks})",
               name=album['Name'], release_date=album['Release Date'], total_tracks=album['Total Tracks'])

    @staticmethod
    def _create_track_node(tx, track):
        tx.run("MERGE (t:Track {name: $name, artist_name: $artist_name, album_name: $album_name})",
               name=track['Name'], artist_name=track['Artist Name'], album_name=track['Album Name'])

    @staticmethod
    def _create_genre_node(tx, genre):
        tx.run("MERGE (g:Genre {name: $name})", name=genre)

    @staticmethod
    def _create_genre_relationships(tx, artist):
        for genre in artist['Genres']:
            tx.run("""
                MATCH (a:Artist {name: $artist_name})
                MATCH (g:Genre {name: $genre_name})
                MERGE (a)-[:HAS_GENRE]->(g)
                """, artist_name=artist['Name'], genre_name=genre)

    @staticmethod
    def _create_relationships(tx, track):
        tx.run("""
            MATCH (a:Artist {name: $artist_name})
            MATCH (al:Album {name: $album_name})
            MATCH (t:Track {name: $track_name})
            MERGE (a)-[:CREATED]->(al)
            MERGE (al)-[:CONTAINS]->(t)
            """, artist_name=track['Artist Name'], album_name=track['Album Name'], track_name=track['Name'])



