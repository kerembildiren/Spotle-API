from pprint import pprint

from app.spotify import search_artist

def test_spotify():
    artist = search_artist("Tarkan")  # Test with a popular Turkish singer

    if artist:
        print("✅ Artist Found:")
        pprint(artist, indent=4)
    else:
        print("❌ Artist Not Found")

test_spotify()
