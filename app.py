import os
from flask import Flask, request, redirect, render_template
from lib.database_connection import get_flask_database_connection
from lib.album_repository import *
from lib.artist_repository import *
from lib.album import *
from lib.artist import *

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==


"""Test-drive and implement a form page to add a new album.
You should then be able to use the form in your web browser to add a new album,
and see this new album in the albums list page."""
@app.route('/albums/new', methods=['GET'])
def get_album_new():
    return render_template('new.html')


"""Add a route GET /artists which returns an HTML page with the list 
of artists. This page should contain a link for each artist listed, 
linking to /artists/<id> where <id> needs to be the corresponding artist id."""
@app.route('/artists', methods=['GET'])
def get_all_artists_links():
    connection = get_flask_database_connection(app)
    repository = ArtistRepository(connection)
    all_artists = repository.all()
    return render_template('all_artists.html', all_artists=all_artists)

"""Add a route GET /artists/<id> which returns an HTML page showing 
details for a single artist."""
@app.route('/artists/<id>', methods=['GET'])
def show_artist_info(id):
    
    connection = get_flask_database_connection(app)
    repository = ArtistRepository(connection)
    artist_info = repository.find(id)
    return render_template('artist_info.html', artist_info=artist_info)

@app.route('/albums', methods=['POST'])
def create_album():
    connection = get_flask_database_connection(app)
    repository = AlbumRepository(connection)
    
    title = request.form['title']
    release_year = request.form['release_year']
    artist_id = request.form['artist_id']
    album = Album(None, title, release_year, artist_id)
    
    if not album.is_valid():
        error = album.generate_errors()
        return render_template('new.html', error=error)
    else:
        repository.create(album)
        return redirect(f"/albums/{album.id}")

@app.route('/albums', methods=['GET'])
def get_all_albums():
    connection = get_flask_database_connection(app)
    repository = AlbumRepository(connection)
    all_albums = repository.all()
    return render_template('albums.html', all_albums=all_albums)

@app.route('/albums/<id>', methods=['GET'])
def show_album_info(id):
    connection = get_flask_database_connection(app)
    repository = AlbumRepository(connection)
    album_info = repository.find(id)
    return render_template('album_info.html', album_info=album_info)

@app.route('/album', methods=['GET'])
def get_album():
    connection = get_flask_database_connection(app)
    repository = AlbumRepository(connection)
    
    artist_id = request.args['artist_id']
    album = repository.find(artist_id)
    return render_template('single_album.html', album=album)

# == Example Code Below ==

@app.route('/emoji', methods=['GET'])
def get_emoji():
    return render_template('emoji.html', emoji=':)')

from example_routes import apply_example_routes
apply_example_routes(app)

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
