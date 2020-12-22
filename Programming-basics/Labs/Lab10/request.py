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
        return await resp.text()
    finally:
        resp.close()

async def worker(ses: aiohttp.ClientSession,
                 queue: asyncio.Queue) -> None:
    while True:
        url, filename = await queue.get()

        text = await fetch(ses, url)
        if text:
            await dump(text, filename)

        queue.task_done()


async def bound_fetch(path: Path) -> None:
    """
    Run coro, get HTML codes and dump
    them to files using 5 workers for it.

    There is timeout = 5s.

    :param path: str, path to the file with URLs and filenames.
    :return: None.
    """
    timeout = aiohttp.ClientTimeout(5)
    queue = asyncio.Queue()

    async with aiohttp.ClientSession(timeout=timeout) as ses:
        async for url, filename in get_link(path):
            queue.put_nowait((url, filename))

        tasks = []
        for _ in range(5):
            task = asyncio.create_task(worker(ses, queue))
            tasks += [task]

        await queue.join()

        for task in tasks:
            task.cancel()

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

