from playwright.sync_api import Page, expect
from lib.album_repository import *
from lib.artist_repository import *

# Tests for your routes go here

def test_get_artist(page, test_web_address, db_connection):
    db_connection.seed('seeds/music_library.sql')
    page.goto(f"http://{test_web_address}/album?artist_id=1")
    album_tag = page.locator("p")
    expect(album_tag).to_have_text("Title: Doolittle Released: 1989")


def test_visit_show_album_page(page, test_web_address, db_connection):
    db_connection.seed('seeds/music_library.sql')
    page.goto(f"http://{test_web_address}/albums")
    page.click("text='Doolittle'")
    
    title_element = page.locator(".t-title")
    expect(title_element).to_have_text("Album: Doolittle")
    
    release_year_element = page.locator(".t-release_year")
    expect(release_year_element).to_have_text("Release Year: 1989")


"""Test Get /artists returns web page with links (research how to test)"""
def test_artists_returns_page_with_artist_links(page, test_web_address, db_connection):
    db_connection.seed('seeds/music_library.sql')
    page.goto(f"http://{test_web_address}/artists")
    h1_tag= page.locator("h1")
    expect(h1_tag).to_have_text('Artists')
    p_tags= page.locator("p")
    expect(p_tags).to_have_text([
        'Pixies',
        'ABBA',
        'Taylor Swift',
        'Nina Simone'
    ])

"""Test Get /artists/<id> Returns correct page when link clicked"""
def test_visit_show_artist_page(page, test_web_address, db_connection):
    db_connection.seed('seeds/music_library.sql')
    page.goto(f"http://{test_web_address}/artists")
    page.click("text='Pixies'")
    h1_tag = page.locator("h1")
    p_tag = page.locator("p")
    expect(h1_tag).to_have_text("Artist: Pixies")
    expect(p_tag).to_have_text("Genre: Rock")


def test_create_new_album(page, test_web_address, db_connection):
    page.set_default_timeout(1000)
    db_connection.seed('seeds/music_library.sql')
    page.goto(f"http://{test_web_address}/albums")
    
    page.click("text='Add new album'")
    
    page.fill("input[name=title]", "Test Album")
    page.fill("input[name=release_year]", "2023")
    page.fill("input[name=artist_id]", "3")
    
    page.click("text='Add Album'")
    title_element = page.locator(".t-title")
    expect(title_element).to_have_text("Album: Test Album")
    
    release_year_element = page.locator(".t-release_year")
    expect(release_year_element).to_have_text("Release Year: 2023")


# If we submit a form without a title, release year or artist ID
# Then the form shows errors
def test_attempt_create_album_without_errors(page, test_web_address, db_connection):
    page.set_default_timeout(1000)
    db_connection.seed('seeds/music_library.sql')
    page.goto(f"http://{test_web_address}/albums")
    
    page.click("text='Add new album'")
    
    page.fill("input[name=title]", "Test Album")
    page.fill("input[name=release_year]", "2023")
    page.click("text='Add Album'")
    
    error_tag = page.locator(".t-error")
    expect(error_tag).to_have_text("Your form contained errors: Artist ID can't be blank")