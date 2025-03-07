import json
import os
import random
import time
from pprint import pprint

from fastapi import APIRouter, HTTPException

from app import config, spotify
from app.spotify import search_artist
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

from app.utils import DateOperations

FastAPICache.init(InMemoryBackend())

router = APIRouter()

# Load the Turkish singers JSON file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE_PATH = os.path.join(BASE_DIR, "../data/turkish_singers.json")


def get_artist_data_dict():
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_artist_data(singer):
    try:
        updated_time = get_artist_data_dict()[singer]["updated_date"]
        # check past 1 day
        if DateOperations.has_one_day_passed(updated_time):
            artist_data = search_artist(singer)
        else:
            artist_data = get_artist_data_dict()[singer]
    except KeyError:
        artist_data = search_artist(singer)

    return artist_data


@router.get("/genres")
async def get_all_genres():
    """Fetch all unique genres from Turkish singers and identify similar ones."""
    genre_set = set()

    for singer in get_artist_data_dict():

        artist_data = get_artist_data(singer)

        if artist_data and "genres" in artist_data:
            for genre in artist_data["genres"]:
                genre_set.add(genre)
        time.sleep(1)

    return {"unique_genres": sorted(genre_set)}


@router.get("/turkish_singers")
async def get_turkish_singers():
    """Fetch Turkish singers' data from Spotify and rank them based on popularity."""

    singers_data = []

    turkish_singers = get_artist_data_dict()
    for singer in turkish_singers.keys():
        while config.SEARCH_REQ:
            time.sleep(1)
        artist_data = get_artist_data(singer)
        if artist_data:
            popularity = artist_data.get("popularity", 0)

            if popularity >= 500000:  # ✅ Only add if followers are 500K+
                # ✅ Force debug print to check if function runs
                # print(f"🔥 DEBUG: {name} - Raw: {followers}, Formatted: {formatted_followers}")

                singers_data.append({
                    "name": artist_data.get("name", "N/A"),
                    "image": artist_data.get("image", "N/A"),
                    "popularity": artist_data.get("popularity", "N/A"),
                    "followers": artist_data.get("followers", "N/A"),  # ✅ Use formatted followers
                    "debut_year": artist_data.get("debut_year", "N/A"),
                    "group_size": artist_data.get("group_size", "N/A"),
                    "gender": artist_data.get("gender", "N/A"),
                    "genres": artist_data.get("genres", "N/A"),
                    "nationality": "Turkish"
                })
    return singers_data  # ✅ Remove unnecessary logging


def select_random_singer():
    turkish_singers = get_artist_data_dict()
    # random select dict key
    random_artist_name = random.choice(list(turkish_singers.keys()))
    artist_data = search_artist(random_artist_name)
    if artist_data["first_album"] is None:
        select_random_singer()
    else:
        config.SELECTED_SINGER_DATA = artist_data
    try:
        while not turkish_singers[random_artist_name]["updated"]:
            time.sleep(0.1)
    except:
        pass


def compare_singers(guess, correct):
    result = {}

    # ✅ Compare each attribute & mark matches in green
    result["name"] = guess["name"]
    result["image"] = guess["image"]
    result["debut_year"] = f"✅ {guess['debut_year']}" if guess["debut_year"] == correct["debut_year"] else str(
        guess["debut_year"])
    result["group_size"] = f"✅ {guess['group_size']}" if guess["group_size"] == correct["group_size"] else str(
        guess["group_size"])
    result["gender"] = f"✅ {guess['gender']}" if guess["gender"] == correct["gender"] else guess["gender"]
    result["genres"] = f"✅ {guess['genres']}" if guess["genres"] == correct["genres"] else guess["genres"]
    result["nationality"] = f"✅ {guess['nationality']}" if guess["nationality"] == correct["nationality"] else guess[
        "nationality"]
    result["followers"] = f"✅ {guess['followers']}" if guess["followers"] == correct["followers"] else guess[
        "followers"]

    # ✅ Show "⬆ Higher" or "⬇ Lower" for popularity
    guess_followers = guess.get("popularity", 0)
    correct_followers = correct.get("popularity", 0)

    if guess_followers > correct_followers:
        result["popularity"] = f"⬇ Lower ({guess['followers']})"
    elif guess_followers < correct_followers:
        result["popularity"] = f"⬆ Higher ({guess['followers']})"
    else:
        result["popularity"] = f"✅ {guess_followers}"

    return result


@router.get("/search")
async def search_singer(artist_name: str):
    """Search for an artist in Spotify and return their data, but only if they exist in the Turkish singers dataset."""
    config.SEARCH_REQ = True
    # 1. artist secildi mi kontrolu
    if len(config.SELECTED_SINGER_DATA) < 1 or not DateOperations.is_new_day():
        # 1. secilmemis ise rastgele sec
        print("SELECTED ARTIST NOT FOUND, SELECTING RANDOM SINGER")
        select_random_singer()

    # artist_name_lower = artist_name.lower()
    # valid_singers = {singer[artist_name].lower() for singer in turkish_singers}

    # if artist_name_lower not in valid_singers:
    #     raise HTTPException(status_code=404, detail="Singer not found in the Turkish singers list")

    artist_data = get_artist_data(artist_name)

    if not artist_data:
        raise HTTPException(status_code=404, detail="Singer not found in Spotify")

    # 3. secildiyse, secilen artist verileri ile karsılastır
    compared_data = compare_singers(artist_data, config.SELECTED_SINGER_DATA)

    # ✅ Force debug print to check if function runs
    # print(f"🔥 DEBUG: {artist_data['name']} - Raw: {raw_followers}, Formatted: {formatted_followers}")
    config.SEARCH_REQ = False
    return compared_data

