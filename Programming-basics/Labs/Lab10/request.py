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

    :param path: Path to the file.
    :return: yield tuple of str.
    """
    async with aiofiles.open(path, 'r', encoding='utf-8') as f:
        async for link in f:
            yield link.split()


async def dump(content: str,
               filename: str,
               **kwargs) -> None:
    """
    Dump page's HTML to to the file.
    All files will be dumped to 'data/' folder.

    :param content: str, HTML code to dump.
    :param filename: str, filename to where dump the content.
    :return: None.
    """
    worker_id = kwargs.pop('worker_id', '')
    worker_id = f"{worker_id}: " * bool(worker_id)

    path = DATA_FOLDER / filename
    async with aiofiles.open(path, 'w', encoding='utf-8') as f:
        await f.write(content)

    logger.debug(f"{worker_id}{path} dumped")


async def fetch(ses: aiohttp.ClientSession,
                url: str,
                **kwargs) -> str:
    """
    :param ses: aiohttp.ClientSession.
    :param url: str, url from where get HTML code.
    :return: str, page's HTML code or error text.
    """
    worker_id = kwargs.pop('worker_id', '')
    worker_id = f"{worker_id}: " * bool(worker_id)

    start = time.time()
    logger.debug(f"{worker_id}Requested to '{url}'")
    try:
        resp = await ses.get(url)
    except Exception as e:
        msg = f"{worker_id}Error requesting to {url}: {e}"
        logger.error(msg)
        return msg

    if resp.status == 200:
        executing_time = round(time.time() - start, 2)
        logger.debug(f"{worker_id}Received from: '{url}', {executing_time=}")

        text = await resp.text()
        resp.close()

        return text

    msg = f"{worker_id}{resp.status} requesting to {resp.url}: {resp.reason}"
    logger.error(msg)

    resp.close()
    return msg


async def worker(ses: aiohttp.ClientSession,
                 queue: asyncio.Queue,
                 worker_id: str) -> None:
    while True:
        url, filename = queue.get_nowait()

        text = await fetch(ses, url, worker_id=worker_id)
        # await dump(text, filename, worker_id=worker_id)

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
        for worker_id in range(5):
            worker_id = f"Worker-{worker_id + 1}"
            task = asyncio.create_task(
                worker(ses, queue, worker_id=worker_id))
            tasks += [task]

        await queue.join()

        for task in tasks:
            task.cancel()


def main(link_path: Path) -> None:
    start = time.time()
    asyncio.run(bound_fetch(link_path))
    logger.info(f"Working time: {time.time() - start:.2f}")
