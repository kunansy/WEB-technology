#!/usr/bin/env python3
import asyncio
import re
from pathlib import Path
from typing import Union

import aiofiles
import aiohttp
from colorama import Fore

PATH = Union[str, Path]
LINKS_PATH = 'l.txt'


async def get_link(path: PATH):
    async with aiofiles.open(path, 'r', encoding='utf-8') as f:
        async for link in f:
            yield link.split()


async def dump(content: str,
               filename: str) -> None:
    pass
    # async with aiofiles.open(f"data/{filename}", 'w', encoding='utf-8') as f:
    #     await f.write(content)


async def fetch(ses: aiohttp.ClientSession,
                url: str,
                filename: str) -> None:
    timeout = aiohttp.ClientTimeout(1)
    print(f"Requested to '{url}'")
    async with ses.get(url, timeout=timeout) as resp:
        print(f"Received from '{url}'")
        if resp.status is 200:
            text = await resp.text()
            await dump(text, f"{filename}.html")
            print(f"Dumped: '{url}'")
            return
        print(Fore.RED, f"{resp.status} error requesting to {resp.url}: {resp.reason}")
        print(Fore.RESET, end='')


async def bound_fetch(path: str) -> None:
    async with aiohttp.ClientSession() as ses:
        tasks = [
            asyncio.create_task(fetch(ses, url, filename))
            async for url, filename in get_link(path)
        ]
        while True:
            done, pending = await asyncio.wait(tasks)
            for future in done:
                try:
                    future.result()
                except Exception as e:
                    # print(e)
                    return


def main() -> None:
    asyncio.run(bound_fetch(LINKS_PATH))


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
