#!/usr/bin/env python3
import asyncio
import re
import sys
import time
from typing import Tuple

import aiofiles
import aiohttp
import aiojobs

LINKS_PATH = 'links10.txt'


async def get_link(path: str) -> Tuple[str, str]:
    async with aiofiles.open(path, 'r', encoding='utf-8') as f:
        async for link in f:
            yield link.split()


async def dump(content: str,
               filename: str) -> None:
    async with aiofiles.open(f"data/{filename}", 'w', encoding='utf-8') as f:
        await f.write(content)


async def fetch(ses: aiohttp.ClientSession,
                url: str,
                filename: str) -> None:
    print(f"Requested to '{url}'")
    try:
        resp = await ses.get(url)
    except Exception as e:
        print(f"Sth went wrong requesting to {url}: {e}",
              file=sys.stderr)
        return
    try:
        resp.raise_for_status()
    except Exception:
        print(f"{resp.status} requesting to {resp.url}: {resp.reason}",
              file=sys.stderr)
        return

    print(f"Received from '{url}'")
    html = await resp.text()
    # await dump(html, f"{filename}.html")
    print(f"Dumped: '{url}'")


async def bound_fetch(path: str) -> None:
    timeout = aiohttp.ClientTimeout(5)
    async with aiohttp.ClientSession(timeout=timeout) as ses:
        scheduler = await aiojobs.create_scheduler()
        async for url, filename in get_link(path):
            await scheduler.spawn(fetch(ses, url, filename))

        await asyncio.sleep(.5)
        await scheduler.close()


def main() -> None:
    # TODO: check the file exists
    # TODO: get logger from main file
    start = time.time()
    asyncio.run(bound_fetch(LINKS_PATH))
    print(f"Working time: {time.time() - start:.2f}")


def add_pt_and_filename():
    with open('links.txt', encoding='utf-8') as f:
        for link in f:
            domain_name = re.search(r'(https?://)?(www\.)?(.*)\..*', link)
            domain_name = domain_name.group(3)
            pt = "https://"
            link = pt * (not link.startswith(pt)) + link

            yield link.strip(), domain_name


if __name__ == "__main__":
    main()
