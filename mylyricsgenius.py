import lyricsgenius
import re

APP_NAME = "LyricGrabber"
API_WEBSITE_URL = "https://github.com/BenTurcotte/PlaylistToOnSong"

__genius = lyricsgenius.Genius(CLIENT_ACCESS_TOKEN)

def prep_search_str(s : str) -> str:
    return re.sub(r'(^the)|(band$)|[^a-zA-Z0-9\s&]|(live.in.*$)', '', s.lower()).strip()

def lyrics(song : str, artist : str) -> str:
    song = __genius.search_song(prep_search_str(song), prep_search_str(artist))
    if song:
        return song.lyrics
    return None

# # # print(prep_search_str("Right Next Door (Because of Me)"))
# # # print(prep_search_str("The Robert Cray Band"))
# # print(lyrics("Right next Door (Because of Me)", "the robert cray Band"))
