import os
from datetime import datetime

from dotenv import load_dotenv

# Get the absolute path to the root folder
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Load .env from the root directory
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)

# Get credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Debugging: Print values to verify
print("SPOTIFY_CLIENT_ID:", SPOTIFY_CLIENT_ID)
print("SPOTIFY_CLIENT_SECRET:", SPOTIFY_CLIENT_SECRET)
print("SPOTIFY_REDIRECT_URI:", SPOTIFY_REDIRECT_URI)

# Ensure credentials exist
if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
    raise ValueError("Missing Spotify API credentials! Check your .env file.")

LAST_DATE = datetime.now().date()
SELECTED_SINGER_DATA = {}



