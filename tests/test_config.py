import sys
import os

# Add the root project directory to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI


from app.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

def test_config():
    assert SPOTIFY_CLIENT_ID is not None, "SPOTIFY_CLIENT_ID is missing!"
    assert SPOTIFY_CLIENT_SECRET is not None, "SPOTIFY_CLIENT_SECRET is missing!"
    assert SPOTIFY_REDIRECT_URI is not None, "SPOTIFY_REDIRECT_URI is missing!"
    print("✅ Environment variables loaded successfully!")

test_config()
