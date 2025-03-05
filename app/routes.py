import json
import os
from fastapi import APIRouter, HTTPException
from app.spotify import search_artist

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


@router.get("/turkish_singers")
async def get_turkish_singers():
    """Fetch Turkish singers' data from Spotify and rank them based on popularity."""

    singers_data = []

    for singer in turkish_singers:
        name = singer["name"]

        # Fetch artist details from Spotify API
        artist_data = search_artist(name)

        if artist_data:
            # Determine popularity ranking based on Monthly Listeners or Followers
            monthly_listeners = artist_data.get("monthly_listeners", None)
            followers = artist_data.get("followers", None)

            popularity_score = monthly_listeners if monthly_listeners else followers

            singers_data.append({
                "name": artist_data["name"],
                "image": artist_data.get("image", "N/A"),
                "popularity": popularity_score,
                "debut_year": singer["debut_year"],
                "group_size": singer["group_size"],
                "gender": artist_data.get("gender", "N/A"),
                "genre": ", ".join(artist_data.get("genres", [])) if artist_data.get("genres") else "N/A",
                "nationality": "Turkish"  # We assume all are Turkish
            })

    # Rank singers by popularity (highest first)
    ranked_singers = sorted(singers_data, key=lambda x: x["popularity"], reverse=True)

    return {"singers": ranked_singers}


@router.get("/search")
async def search_singer(artist_name: str):
    """Search for an artist in Spotify and return their data."""
    artist_data = search_artist(artist_name)

    if not artist_data:
        raise HTTPException(status_code=404, detail="Singer not found")

    return {
        "name": artist_data["name"],
        "image": artist_data.get("image", "N/A"),
        "popularity": artist_data.get("monthly_listeners", artist_data.get("followers", "N/A")),
        "debut_year": "N/A",  # To be filled later
        "group_size": "N/A",  # To be filled later
        "gender": artist_data.get("gender", "N/A"),
        "genre": ", ".join(artist_data.get("genres", [])) if artist_data.get("genres") else "N/A",
        "nationality": "Turkish"  # Assume all are Turkish
    }
