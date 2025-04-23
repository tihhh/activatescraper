import json
import asyncio
from asyncio import tasks
import time
from pathlib import Path

from scraper import fetch_all_clubs

BASE_URL = "https://www.activateuts.com.au/wp-json/adrenalin/page?path="
CLUBS_FILE = "files/club_paths.json"
REQUEST_LIMIT = 5 

semaphore = asyncio.Semaphore(REQUEST_LIMIT)

def load_club_endpoints(json_path=CLUBS_FILE):
    raw = json.loads(Path(json_path).read_text(encoding="utf-8"))
    return [f"{BASE_URL}{slug}" for slug in raw.values()]

async def main():
    start = time.time()

    club_urls = load_club_endpoints()
    results = await fetch_all_clubs(club_urls, semaphore=semaphore)

    with open("data/club_data.json", "w", encoding="utf-8") as f:
        json.dump(results.model_dump(), f, indent=2, ensure_ascii=False)

    duration = time.time() - start
    print(f"Fetched {len(club_urls)} clubs in {duration:.2f} seconds.")

if __name__ == "__main__":
    asyncio.run(main())