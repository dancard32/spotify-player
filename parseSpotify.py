import spotipy                          # Spotipy's python module
from spotipy.oauth2 import SpotifyOAuth # Allows authentication of Spotify
from API_Key import API_KEY             # Allows constants across scripts
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""" Globally loaded constants """
DEVICE_ID, CLIENT_ID, CLIENT_SECRET = API_KEY()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                redirect_uri="http://localhost:8080",
                scope="user-read-playback-state,user-modify-playback-state"))

# Start playing a song
sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:1jNNHFZmRGXZFHlil5uhei'])