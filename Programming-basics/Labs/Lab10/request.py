#!/usr/bin/env python3
import asyncio
import logging
import os
import re
import time
from pathlib import Path
from typing import AsyncIterator, Tuple, AsyncGenerator

import aiofiles
import aiohttp

logger = logging.getLogger('web-scraper')
IS_LINE_CORRECT = re.compile(r'http(s)?://.+ .+', re.IGNORECASE)


async def from_link(line: str) -> AsyncIterator[Tuple[str, str]]:
    yield line.split()


async def from_file(path: Path) -> AsyncIterator[Tuple[str, str]]:
    """
    Asynchronous generator to get link to the site
    and path to where dump its HTML code.

    :param path: Path to the file.
    :return: yield tuple of str.
    """
    async with aiofiles.open(path, 'r', encoding='utf-8') as f:
        async for link in f:
            if IS_LINE_CORRECT.search(link):
                yield link.split()
            else:
                logger.error(
                    f"Line must be like 'http(s)://link filename', "
                    f"but {link} found")


async def dump(content: str,
               filename: str,
               **kwargs) -> None:
    """
    Dump page's HTML to to the file.
    All files will be dumped to 'data/' folder.

    :param content: str, HTML code to dump.
    :param filename: str, filename to where dump the content.
    :keyword worker_id: str, way to identify the worker.
    :keyword data_folder: Path to folder to where save the files.

    :return: None.
    """
    worker_id = kwargs.pop('worker_id', '')
    worker_id = f"{worker_id}: " * bool(worker_id)

    path = kwargs.pop('data_folder', Path('.')) / filename
    async with aiofiles.open(path, 'w', encoding='utf-8') as f:
        await f.write(content)

    logger.debug(f"{worker_id}{path} dumped")


async def fetch(ses: aiohttp.ClientSession,
                url: str,
                **kwargs) -> str:
    """
    Get HTML code of the page.

    :param ses: aiohttp.ClientSession.
    :param url: str, url from where get HTML code.
    :keyword worker_id: str, way to identify the worker.

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
                 *,
                 worker_id: str,
                 data_folder: Path) -> None:
    """
    Worker fetching HTML code of the site and dumping it to file.

    :param ses: aiohttp.ClientSession.
    :param queue: asyncio.Queue with args.
    :param worker_id: str, way to identify the worker.
    :param data_folder: Path to folder to where save the files.

    :return: None.
    """
    while True:
        url, filename = queue.get_nowait()

        text = await fetch(ses, url, worker_id=worker_id)
        await dump(
            text, filename, worker_id=worker_id, data_folder=data_folder)

        queue.task_done()


async def bound_fetch(data_folder: Path,
                      links: AsyncGenerator) -> None:
    """
    Run coro, get HTML codes and dump
    them to files using 5 workers for it.

    There is timeout = 5s.

    :param data_folder: Path to folder to
     where save the .html files.
    :param links: async generator from where
     get the links and file names.

    :return: None.
    """
    timeout = aiohttp.ClientTimeout(5)
    queue = asyncio.Queue()

    async with aiohttp.ClientSession(timeout=timeout) as ses:
        async for url, filename in links:
            queue.put_nowait((url, filename))

        tasks = []
        for worker_id in range(5):
            worker_id = f"Worker-{worker_id + 1}"
            task = asyncio.create_task(
                worker(ses, queue,
                       worker_id=worker_id, data_folder=data_folder)
            )
            tasks += [task]

        await queue.join()

        for task in tasks:
            task.cancel()


def main(links: str or Path,
         data_folder: Path or str = os.getenv('DATA_FOLDER', 'data'),
         from_line: bool = False) -> None:
    data_folder = Path(data_folder)

    logger.info("Requesting started")
    start = time.time()
    if from_line:
        if IS_LINE_CORRECT.search(links) is None:
            msg = f"Line must be like 'http(s)://link filename', " \
                  f"but {links} found"
            logger.error(msg)
            raise ValueError(msg)

        # noinspection PyTypeChecker
        asyncio.run(bound_fetch(data_folder, from_link(links)))
    else:
        if not links.exists():
            msg = f"File with links '{links}' not found"
            logger.error(msg)
            raise FileNotFoundError(msg)

        # noinspection PyTypeChecker
        asyncio.run(bound_fetch(data_folder, from_file(links)))

    logger.info(f"Working time: {time.time() - start:.2f}")
