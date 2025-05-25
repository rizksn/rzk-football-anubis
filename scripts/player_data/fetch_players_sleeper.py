import aiohttp
import asyncio
import json
from pathlib import Path

async def fetch_sleeper_players():
    url = "https://api.sleeper.app/v1/players/nfl"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            output_path = Path("anubis/data/raw/sleeper/sleeper_players_full.json")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with output_path.open("w") as f:
                json.dump(data, f, indent=2)
            print(f"Saved {len(data)} players to {output_path}")

if __name__ == "__main__":
    asyncio.run(fetch_sleeper_players())