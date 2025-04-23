import asyncio
import httpx

from logger import log_error
from models import Club, ClubEvent, ClubList


async def fetch(client, url, semaphore: asyncio.Semaphore = asyncio.Semaphore(5)):
    async with semaphore:
        try:
            resp = await client.get(url, timeout=60)

            if resp.status_code == 429:
                retry_after = int(resp.headers.get("Retry-After", "5"))
                print(f"Rate limited on {url}, retrying in {retry_after}s...")
                await asyncio.sleep(retry_after)
                return await fetch(client, url)

            if resp.status_code != 200:
                log_error(url, resp.status_code, resp.text)
                return url, {"error": f"Status code {resp.status_code}"}

            if "application/json" in resp.headers.get("Content-Type", ""):
                data = resp.json()

                events = []
                #for ev in data['upcoming_events']:
                
                for ev in data.get("upcoming_events", []):
                    event = ClubEvent(
                        id=ev.get("id"),
                        title=ev.get("title"),
                        start_date=ev.get("acf", {}).get("start_date"),
                        end_date=ev.get("acf", {}).get("end_date"),
                        desc=ev.get("acf", {}).get("html"),
                        url=ev.get("url")
                )
                    events.append(event)
                

                return Club(
                    club_id=data.get("post_name"),
                    name=data.get("post_title"),
                    url=data.get("url"),
                    events=events if events else None
                )
            else:
                log_error(url, resp.status_code, resp.text)
                return url, {"error": "Non-JSON response", "content": resp.text[:200]}

        except Exception as e:
            log_error(url, "Exception", str(e))
            return url, {"error": str(e)}
        
async def fetch_all_clubs(club_urls, semaphore: asyncio.Semaphore = asyncio.Semaphore(5)):
    async with httpx.AsyncClient() as client:
        tasks = [fetch(client, url, semaphore) for url in club_urls]
        results = await asyncio.gather(*tasks)
        return ClubList(clubs=[club for club in results if isinstance(club, Club)])