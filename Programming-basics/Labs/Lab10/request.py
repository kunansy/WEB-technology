#!/usr/bin/env python3
import asyncio
import logging
import os
import time
from pathlib import Path
from typing import AsyncIterator, Tuple

import aiofiles
import aiohttp

DATA_FOLDER = Path(os.getenv('DATA_FOLDER'))
logger = logging.getLogger('web-scraper')


async def get_link(path: Path) -> AsyncIterator[Tuple[str, str]]:
    """
    Asynchronous generator to get link to the site
    and path to where dump its HTML code.

    :param path: Path to the  file.
    :return: yield tuple of str.
    """
    async with aiofiles.open(path, 'r', encoding='utf-8') as f:
        async for link in f:
            yield link.split()


async def dump(content: str,
               filename: str) -> None:
    """
    Dump page's HTML to to the file.
    All files will be dumped to 'data/' folder.

    :param content: str, HTML code to dump.
    :param filename: str, filename to where dump the content.
    :return: None.
    """
    path = DATA_FOLDER / filename
    async with aiofiles.open(path, 'w', encoding='utf-8') as f:
        await f.write(content)

    logger.debug(f"{path} dumped")


async def fetch(ses: aiohttp.ClientSession,
                url: str) -> str or None:
    """
    :param ses: aiohttp.ClientSession.
    :param url: str, url from where get HTML code.
    :return: str, page's HTML code.
    """
    start = time.time()
    logger.debug(f"Requested to '{url}'")
    try:
        resp = await ses.get(url)
    except Exception as e:
        logger.error(f"Error requesting to {url}: {e}")
        return

    if resp.status == 200:
        logger.debug(f"Received from: '{url}', time={round(time.time() - start, 2)}")
        text = await resp.text()
        resp.close()
        return text
    else:
        logger.error(
            f"{resp.status} requesting to {resp.url}: {resp.reason}")
        resp.close()


async def worker(ses: aiohttp.ClientSession,
                 queue: asyncio.Queue) -> None:
    while True:
        url, filename = queue.get_nowait()

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


def main(link_path: Path) -> None:
    start = time.time()
    asyncio.run(bound_fetch(link_path))
    logger.info(f"Working time: {time.time() - start:.2f}")

