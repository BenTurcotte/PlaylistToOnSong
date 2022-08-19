from bs4 import BeautifulSoup
import requests
import json
import re

from typing import TypeVar, Iterable, Tuple

JSONstr = str
listr = Iterable[str]


base = "https://www.azlyrics.com/"

def prep_artist_name(name):
    name = name.strip().lower()
    if not name or len(name) == 0:
        return None

    # remove "the" from start of artist name
    name = re.sub(r'^the\w+', '', name)

    # remove "band" from the end of artist name
    name = re.sub(r'\w+band$', '', name)

    return prep_name_for_url(name)

def prep_song_name(name):
    name = name.strip().lower()
    if not name or len(name) == 0:
        return None

    # remove all text after "-"
    if " - " in name:
        name = name[:name.index(" - ")]
    
    # remove (remaster...)

    return prep_name_for_url(name)
    

def prep_name_for_url(name):
    name = name.strip().lower()
    if not name or len(name) == 0:
        return None

    # remove any brackets
    #   If don't work, also remove text they contain from song name
    # try replace "&"" with "and"
    #   if doesn't work, remove "and"
    # remove all punctuation marks
    return re.sub(r'[^a-zA-Z0-9]', '', name).lower()

def get_artists_by_letter(letter : str) -> JSONstr:
    if letter.isalpha() and len(letter) is 1:
        letter = letter.lower()
        url = base+letter+".html"
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")
        data = []

        for div in soup.find_all("div", {"class": "container main-page"}):
            links = div.findAll('a')
            for a in links:
                data.append(a.text.strip())
        return json.dumps(data)
    else:
        raise Exception("Unexpected Input")


def get_songs_by_artist(artist : str) -> JSONstr:
    artist = prep_name_for_url(artist)
    first_char = artist[0]
    url = base+first_char+"/"+artist+".html"
    req = requests.get(url)

    artist = {
        'artist': artist,
        'albums': {}
        }

    soup = BeautifulSoup(req.content, 'html.parser')

    all_albums = soup.find('div', id='listAlbum')
    first_album = all_albums.find('div', class_='album')
    album_name = first_album.b.text
    songs = []

    for tag in first_album.find_next_siblings(['a', 'div']):
        if tag.name == 'div':
            artist['albums'][album_name] = songs
            songs = []
            if tag.b is None:
                pass
            elif tag.b:
                album_name = tag.b.text

        else:
            if tag.text is "":
                pass
            elif tag.text:
                songs.append(tag.text)

    artist['albums'][album_name] = songs

    return (json.dumps(artist))


def get_lyrics(artist : str, song : str) -> str:
    artist = prep_name_for_url(artist)
    song = prep_name_for_url(song)
    url = base+"lyrics/"+artist+"/"+song+".html"
    print(f'... Searching {url}')
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    lyrics = soup.find_all("div", attrs={"class": None, "id": None})
    if not lyrics:
        return None
    elif lyrics:
        if len(lyrics) > 0:
            return lyrics[0].getText()
        else:
            return "no lyrics found."
        lyrics = [x.getText() for x in lyrics]
        return lyrics