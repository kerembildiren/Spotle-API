import requests
from bs4 import BeautifulSoup


def get_wikipedia_info(artist_name):
    """Scrape Wikipedia for debut year, group size, and gender."""
    search_url = f"https://en.wikipedia.org/wiki/{artist_name.replace(' ', '_')}_singer"
    response = requests.get(search_url)

    if response.status_code != 200:
        print(f"❌ Wikipedia page not found for {artist_name}")
        return {"debut_year": "N/A", "group_size": "N/A", "gender": "N/A"}

    soup = BeautifulSoup(response.text, 'html.parser')

    # ✅ Extract gender
    gender = "N/A"
    for row in soup.find_all("tr"):
        if "Gender" in row.text:
            gender = row.find("td").text.strip()
            break

    # ✅ Extract debut year
    debut_year = "N/A"
    for row in soup.find_all("tr"):
        if "Years active" in row.text:
            year_text = row.find("td").text.strip()
            debut_year = ''.join(filter(str.isdigit, year_text.split("-")[0]))  # Get first year
            break

    # ✅ Assume group size is 1 unless otherwise stated
    group_size = "1"
    if "band" in soup.text.lower():
        group_size = "N/A"

    return {"debut_year": debut_year, "group_size": group_size, "gender": gender}


# ✅ Test the scraper
print(get_wikipedia_info("Tarkan_(singer)"))
