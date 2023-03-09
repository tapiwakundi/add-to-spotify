import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime
import requests
from bs4 import BeautifulSoup

# Replace with your Spotify client ID and client secret
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_ID'
# Authenticate with Spotify using OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, scope='playlist-modify-public', redirect_uri='http://localhost:8888/callback'))

# Replace with the URL of the playlist you want to copy
url = 'https://music.apple.com/ca/playlist/untitled-playlist/pl.u-gxblgEJF5VP5l0e'

# Replace with the name and description of the playlist you want to create defaults to current date-time
playlist_name = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
playlist_description = 'Playlist created by Tapiwa\'s python script'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

def getSongs():
    songs = []

    for item in soup.find_all("div", {"class": "songs-list-row"}):
        title = ''
        artist = ''

        if hasattr(item.select_one('div[class="songs-list-row__song-name-wrapper svelte-4druit"]'), 'text'):
            title = item.select_one('div[data-testid="track-title"]').text.strip()
        if hasattr(item.select_one('a[class="click-action"]'), "text"):
            artist = item.select_one('a[class="click-action"]').text.strip()

        songs.append({'title': title, 'artist': artist})

    return songs



songs = getSongs()

# Get the user's Spotify username
user = sp.me()['id']

# Create a new playlist with the name defined above
playlist = sp.user_playlist_create(user, playlist_name, public=True, description=playlist_description)

# Loop through the array of song names and try to add each song to the playlist
for song in songs:
    query = f"{song['title']} {song['artist']}"
    results = sp.search(query, type='track', limit=1)['tracks']['items']
    success_count = 0
    failure_count = 0
    if results:
        track = results[0]['uri']
        sp.playlist_add_items(playlist['uri'], [track])
        print(f"Added '{song['title']}' by '{song['artist']}' to the playlist '{playlist_name}'.")
        count = count + 1
    else:
        print(f"Failed to add '{song['title']}' by '{song['artist']}' to the playlist '{playlist_name}'.")
        failure_count = failure_count + 1

print(f"Successfully added {count} songs to the playlist '{playlist_name}'.")

if failure_count > 0:
     print(f"Failed to add {failure_count} songs to the playlist '{playlist_name}'.")

