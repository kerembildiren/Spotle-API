import json
import os
import time
from pprint import pprint

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from app.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

# Authenticate with Spotify API
client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE_PATH = os.path.join(BASE_DIR, "../data/turkish_singers.json")
turkish_singers = {}

def get_artist_data_dict():
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_artist_data(artist_data):
    global turkish_singers
    turkish_singers = get_artist_data_dict()
    _name = artist_data["name"]
    turkish_singers[_name] = artist_data
    with open(JSON_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(turkish_singers, f, ensure_ascii=False, indent=4)
    print(f"ARTIST DATA SAVED: {_name}")
    print(artist_data)

GENRE_MAPPING = {
    "turkish pop": "Pop",
    "t-pop": "Pop",
    "turkish hip hop": "Rap",
    "slap house": "Electronic",
    "rap": "Rap",
    "oyun havasi": "Folk",
    "khaleeji": "Arabic",
    "karadeniz folk": "Folk",
    "hardstyle": "Metal",
    "hardcore": "Metal",
    "g-house": "Electronic",
    "frenchcore": "Metal",
    "drill": "Rap",
    "children's music": "",
    "arabic rap": "Arabic",
    "arabesk": "Arabesque",
    "anatolian rock": "Rock",
}
def map_genre(genres):
    """Map similar Spotify genres to a single standardized category."""
    for genre in genres:
        for key in GENRE_MAPPING:
            if key in genre.lower():
                return GENRE_MAPPING[key]
    return "Other"  # Default if no match

def format_followers_count(followers):
    """Convert raw followers count into K/M format (e.g., 587K, 1.2M, 5M)."""

    if not isinstance(followers, (int, float)):  # Ensure it's a number
        print(f"⚠️ Followers data is not a valid number: {followers}")
        return followers  # Return as-is if it's not a number

    # print(f"📌 Formatting followers count: {followers}")  # ✅ Debugging print

    if followers >= 1_000_000:
        formatted = f"{followers / 1_000_000:.1f}M"  # Convert to Millions
    elif followers >= 1_000:
        formatted = f"{followers // 1_000}K"  # Convert to Thousands
    else:
        formatted = str(followers)  # If below 1K, keep it as-is

    # print(f"✅ Formatted followers: {formatted}")  # ✅ Debugging print
    return formatted


def search_artist(artist_name):
    """
    Search for an artist on Spotify and return details.
    """
    results = sp.search(q=artist_name, type="artist", limit=1)

    if results["artists"]["items"]:
        artist = results["artists"]["items"][0]
        _id = get_artist_id(artist)
        albums = sp.artist_albums(_id, None, ["album","single","appears_on", "compilation"], "TR", 50, 0)
        artist_data = {
            "id": _id,
            "name": get_artist_name(artist),
            "gender": "N/A",
            "nationality": "N/A",
            "popularity": artist["followers"]["total"],  # Score 0-100
            "followers": format_followers_count(int(artist["followers"]["total"])),
            "genres": map_genre(artist.get("genres", [])),
            "image": artist["images"][0]["url"] if artist["images"] else None,
            "first_album": get_first_album(albums),
            "debut_year": get_first_album_year(albums),
            "spotify_url": artist["external_urls"]["spotify"],
            "group_size": "N/A",
            "updated": True,
            "updated_date": time.time()
        }

        save_artist_data(artist_data)

        return artist_data

    return None


def get_artist_id(artist_data: dict):
    return artist_data["external_urls"]["spotify"].split("/")[-1]


def get_artist_name(artist_data: dict):
    return artist_data["name"]


def get_first_album(albums_data: dict):
    album_list = albums_data[list(albums_data.keys())[-1]]
    if len(album_list):
        return album_list[-1]["name"]
    else:
        return None


def get_first_album_year(albums_data: dict):
    album_list = albums_data[list(albums_data.keys())[-1]]
    if len(album_list):
        return album_list[-1]["release_date"]
    else:
        return None
