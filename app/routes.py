from fastapi import APIRouter, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.backends.inmemory import InMemoryBackend
from app.spotify import search_artist

# Create a router for API endpoints
router = APIRouter()

@router.get("/search")
@cache(expire=600)  # Cache search results for 10 minutes
def get_artist(artist_name: str):
    """
    API endpoint to search for a Turkish singer.
    Example: /search?artist_name=Tarkan
    """
    artist = search_artist(artist_name)
    if artist:
        return artist
    return {"error": "Artist not found"}


# List of popular Turkish singers
turkish_singers = [
    "Tarkan", "Sezen Aksu", "Ajda Pekkan", "Hadise",
    "Kenan Doğulu", "Murat Boz", "Aleyna Tilki",
    "Edis", "Gülşen", "Bengü", "Mustafa Sandal"
]

@router.get("/turkish_singers")
@cache(expire=3600)  # Cache results for 1 hour
def get_turkish_singers():
    """
    API endpoint to get a list of top Turkish singers.
    Example: /turkish_singers
    """
    singers_data = []
    for singer in turkish_singers:
        artist = search_artist(singer)  # Fetch data from Spotify API
        if artist:
            singers_data.append(artist)

    return singers_data
