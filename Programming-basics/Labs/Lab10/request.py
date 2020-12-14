#!/usr/bin/env python3
import asyncio
import logging
import re
import time
from pathlib import Path
from typing import Tuple

import aiofiles
import aiohttp
import aiojobs

LINKS_PATH = 'links100.txt'
DATA_FOLDER = Path('data')

logger = logging.getLogger('web-scraper')


async def get_link(path: str) -> Tuple[str, str]:
    """ Generator to get link to the site
    and path to where dump its HTML code.

    :param path: Path to the link file.
    :return: yield tuple of str.
    """
    async with aiofiles.open(path, 'r', encoding='utf-8') as f:
        async for link in f:
            yield link.split()


async def dump(content: str,
               filename: str) -> None:
    """ Dump page's HTML to to the file.
    All files will be dumped to 'data/' folder.

    :param content: str, HTML code to dump.
    :param filename: str, filename to where dump the content.
    :return: None.
    """
    path = DATA_FOLDER / filename
    async with aiofiles.open(path, 'w', encoding='utf-8') as f:
        await f.write(content)


async def fetch(ses: aiohttp.ClientSession,
                url: str,
                filename: str) -> None:
    """ Get page's HTML code and dump it to the file.

    :param ses: aiohttp.ClientSession.
    :param url: str, url from where get HTML code.
    :param filename: str, name of the file to where dump the code.
    :return: None.
    """
    logger.debug(f"Requested to '{url}'")
    try:
        resp = await ses.get(url)
    except Exception as e:
        logger.error(f"Sth went wrong requesting to {url}: {e}")
        return

    try:
        resp.raise_for_status()
    except Exception:
        logger.error(f"{resp.status} requesting to {resp.url}: {resp.reason}")
    else:
        logger.debug(f"Received from '{url}'")
        html = await resp.text()
        # await dump(html, f"{filename}.html")
        logger.debug(f"Dumped: '{url}'")
    finally:
        resp.close()


async def bound_fetch(path: str) -> None:
    """ Run coro, get HTML codes and dump them to files.
    There is timeout = 5s.

    :param path: str, path to the file with URLs and filenames.
    :return: None.
    """
    timeout = aiohttp.ClientTimeout(5)
    async with aiohttp.ClientSession(timeout=timeout) as ses:
        scheduler = await aiojobs.create_scheduler()
        async for url, filename in get_link(path):
            try:
                await scheduler.spawn(fetch(ses, url, filename))
            except Exception:
                print("oops, timeout")

        while len(scheduler) is not 0:
            await asyncio.sleep(.5)
        await scheduler.close()


def main() -> None:
    # TODO: check the file exists
    # TODO: get logger from main file
    start = time.time()
    asyncio.run(bound_fetch(LINKS_PATH))
    logger.info(f"Working time: {time.time() - start:.2f}")


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

