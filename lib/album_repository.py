from lib.album import Album
from lib.database_connection import DatabaseConnection

class AlbumRepository:
    def __init__(self, connection):
        self._connection = connection


    def all(self):
        rows = self._connection.execute('SELECT * from albums')
        albums = []
        for row in rows:
            item = (Album(row["id"], row["title"], row["release_year"], row["artist_id"]))
            albums.append(item)
        return albums


    def find(self, id):
        rows = self._connection.execute(
            'SELECT * from albums WHERE id = %s', [id])
        row = rows[0]
        return Album(row["id"], row["title"], row["release_year"], row["artist_id"])
    
# Test-drive a create method for your AlbumRepository class.
# Create a new album
    def create(self, album):
        rows = self._connection.execute(
            'INSERT INTO albums (title, release_year, artist_id) VALUES (%s, %s, %s) RETURNING id',
            [album.title, album.release_year, album.artist_id])
        row = rows[0]
        album.id = row["id"]
        return album


# Test-drive a delete method for your AlbumRepository class.
# Delete an album by its id
    def delete(self, id):
        self._connection.execute(
            'DELETE FROM albums WHERE id = %s', [id])
        return None