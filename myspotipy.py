import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import keyring
import json
import re
import os
import myazlyrics as az
import time
import mylyricsgenius as lg

# get_password("KeyChainItem.Name", "keychainitem.Account")
id = keyring.get_password("SpotifyApiClientId", "client_id")
secret = keyring.get_password("SpotifyApiClientSecret", "client_secret")

client_credentials_manager = SpotifyClientCredentials(client_id=id, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


duoTunes = None
spUser = 'hasvj5rw9thy2r107qy794d8y'
playlists = sp.user_playlists(spUser)
while playlists:
    for i, playlist in enumerate(playlists['items']):
        # # print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        if 'Duo Tunes' in playlist['name']:
            duoTunes = playlist
            print(f'Found Duo Tunes!\n{duoTunes}')
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None

tracks = sp.user_playlist_tracks(user=spUser, playlist_id=duoTunes['id'])
# # print(tracks)

allLyrics = {}
for t in tracks['items']:
    songName = t["track"]["name"]
    artistName = t["track"]["album"]["artists"][0]["name"]
    # # lyrics = az.get_lyrics(artistName, songName)
    lyrics = lg.lyrics(songName, artistName)
    if not lyrics or len(lyrics.strip()) == 0:
        print(f'ERROR - Couldn\'t retrieve lyrics for {songName} by {artistName}')
        continue
    fileName = re.sub(r'[^a-zA-Z]', '', songName) + "_" + re.sub(r'[^a-zA-Z]', '', artistName) + ".onsong"
    outputDir = "TestOutputDir"
    path = os.path.join(outputDir, fileName)
    with open(path, "w+") as fp:
        fp.write(f'{songName}\n{artistName}\n\n{lyrics}')
    print(f'{songName} by {artistName} written to {path}')
    
    # only need to sleep when use az lyrics so don't get kicked out
    # # time.sleep(5)

ACCESS_TOKEN = ""
REDIRECT_URI = ""
