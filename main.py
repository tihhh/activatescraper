import json
import asyncio
import time
from pathlib import Path
import datetime

from scraper import fetch_all_clubs

BASE_URL = "https://www.activateuts.com.au/wp-json/adrenalin/page?path="
CLUBS_FILE = "files/club_paths.json"
REQUEST_LIMIT = 5 
LATEST_FILE = "data/latest.json"

semaphore = asyncio.Semaphore(REQUEST_LIMIT)

def load_club_endpoints(json_path=CLUBS_FILE):
    raw = json.loads(Path(json_path).read_text(encoding="utf-8"))
    return [f"{BASE_URL}{slug}" for slug in raw.values()]

async def main():
    start = time.time()

    club_urls = load_club_endpoints()
    results = await fetch_all_clubs(club_urls, semaphore=semaphore)

    latest_file = Path(LATEST_FILE)
    if latest_file.exists():
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"data/club_data_{timestamp}.json"
        latest_file.rename(backup_file)

    
    with open(latest_file, "w", encoding="utf-8") as f:
        json.dump(results.model_dump(), f, indent=2, ensure_ascii=False)

    duration = time.time() - start
    print(f"Fetched {len(club_urls)} clubs in {duration:.2f} seconds.")

if __name__ == "__main__":
    asyncio.run(main())