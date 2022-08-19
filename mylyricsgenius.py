import lyricsgenius
import re

APP_NAME = "LyricGrabber"
API_WEBSITE_URL = "https://github.com/bturcott14/PlaylistToOnSong"
CLIENT_ID = "Hyie_kOLnGedncbqb-HwEuBUZSyyIfCFf4-XBKf6iNrJ08E38fdxp9PS9e7yQ6cU"
CLIENT_SECRET = "VvqADFh4mv93hn2BW8pS2C8VrTU6RJBJI2lYxqpJvr4wXB3S17izpkk4v2XVMrH4UOc87RpYujdEGhUrOeUUJg"
CLIENT_ACCESS_TOKEN = "yAsYZZO5FfE4asKPLPtcaAFDCE6YOcKOA0EZR4OV7OawABHLZP2JBRqESeh5efMh"

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