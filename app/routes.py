import json
import os
from fastapi import APIRouter, HTTPException
from app.spotify import search_artist
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

FastAPICache.init(InMemoryBackend())

router = APIRouter()

# Load the Turkish singers JSON file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE_PATH = os.path.join(BASE_DIR, "../data/turkish_singers.json")

try:
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
        turkish_singers = json.load(f)
except FileNotFoundError:
    raise HTTPException(status_code=500, detail="Turkish singers JSON file not found!")


@router.get("/genres")
async def get_all_genres():
    """Fetch all unique genres from Turkish singers and identify similar ones."""
    genre_set = set()

    for singer in turkish_singers:
        artist_data = search_artist(singer["name"])
        if artist_data and "genres" in artist_data:
            for genre in artist_data["genres"]:
                genre_set.add(genre)

    return {"unique_genres": sorted(genre_set)}

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

@router.get("/turkish_singers")
@cache(expire=86400)  # ✅ Cache data for 24 hours (86400 seconds)
async def get_turkish_singers():
    """Fetch Turkish singers' data from Spotify and rank them based on popularity."""

    singers_data = []

    for singer in turkish_singers:
        name = singer["name"]

        # Fetch artist details from Spotify API
        artist_data = search_artist(name)

        if artist_data:
            followers = artist_data.get("followers", 0)
            if followers >= 500000:  # ✅ Only add if followers are 500K+
                monthly_listeners = artist_data.get("monthly_listeners", None)
                popularity_score = monthly_listeners if monthly_listeners else followers

                singers_data.append({
                    "name": artist_data["name"],
                    "image": artist_data.get("image", "N/A"),
                    "popularity": popularity_score,
                    "followers": followers,
                    "debut_year": singer.get("debut_year", "N/A"),
                    "group_size": singer.get("group_size", "N/A"),
                    "gender": artist_data.get("gender", "N/A"),
                    "genre": map_genre(artist_data.get("genres", [])),
                    "nationality": "Turkish"
                })

    ranked_singers = sorted(singers_data, key=lambda x: x["popularity"], reverse=True)
    return {"singers": ranked_singers}



@router.get("/search")
async def search_singer(artist_name: str):
    """Search for an artist in Spotify and return their data, but only if they exist in the Turkish singers dataset."""

    # Convert the input name to lowercase for matching
    artist_name_lower = artist_name.lower()

    # Check if the artist exists in turkish_singers.json
    valid_singers = {singer["name"].lower() for singer in turkish_singers}
    if artist_name_lower not in valid_singers:
        raise HTTPException(status_code=404, detail="Singer not found in the Turkish singers list")

    # Fetch artist details from Spotify API
    artist_data = search_artist(artist_name)

    if not artist_data:
        raise HTTPException(status_code=404, detail="Singer not found in Spotify")

    return {
        "name": artist_data["name"],
        "image": artist_data.get("image", "N/A"),
        "popularity": artist_data.get("monthly_listeners", artist_data.get("followers", "N/A")),
        "followers": artist_data.get("followers", "N/A"),
        "debut_year": "N/A",
        "group_size": "N/A",
        "gender": artist_data.get("gender", "N/A"),
        "genre": ", ".join(artist_data.get("genres", [])) if artist_data.get("genres") else "N/A",
        "nationality": "Turkish"
    }
