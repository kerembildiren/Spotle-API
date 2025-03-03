import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from app.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

# Authenticate with Spotify API
client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def search_artist(artist_name):
    """
    Search for an artist on Spotify and return details.
    """
    results = sp.search(q=artist_name, type="artist", limit=1)

    if results["artists"]["items"]:
        artist = results["artists"]["items"][0]
        return {
            "name": artist["name"],
            "popularity": artist["popularity"],  # Score 0-100
            "followers": artist["followers"]["total"],
            "genres": artist["genres"],
            "image": artist["images"][0]["url"] if artist["images"] else None,
            "spotify_url": artist["external_urls"]["spotify"]
        }

    return None
