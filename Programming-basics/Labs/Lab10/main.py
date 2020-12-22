#!/usr/bin/env python3
import logging
import os
from pathlib import Path
from typing import Union

import request

LEVEL = Union[int, str]

MSG_FMT = "[{module}:{levelname}:{funcName}:{asctime}] {message}"
DATE_FMT = "%d.%m.%Y %H:%M:%S"

LOG_FOLDER = Path('logs')
DATA_FOLDER = Path(os.getenv('DATA_FOLDER'))

os.makedirs(LOG_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

formatter = logging.Formatter(
    fmt=MSG_FMT,
    datefmt=DATE_FMT,
    style='{'
)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

path = LOG_FOLDER / f"lab10.log"
file_handler = logging.FileHandler(
    path, delay=True, encoding='utf-8')
file_handler.setLevel(logging.CRITICAL)
file_handler.setFormatter(formatter)

logger = logging.getLogger("web-scraper")
logger.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


def set_handler_level(level: LEVEL,
                      handler_class: type) -> None:
    try:
        level = level.upper()
    except AttributeError:
        pass

    for handler_index in range(len(logger.handlers)):
        if logger.handlers[handler_index].__class__ == handler_class:
            logger.handlers[handler_index].setLevel(level)


def set_stream_handler_level(level: LEVEL) -> None:
    set_handler_level(level, logging.StreamHandler)


def set_file_handler_level(level: LEVEL) -> None:
    set_handler_level(level, logging.FileHandler)


def set_logger_level(level: LEVEL) -> None:
    try:
        level = level.upper()
    except AttributeError:
        pass
    logger.setLevel(level)


def main() -> None:
    request.main(Path('links10.txt'))


if __name__ == '__main__':
    main()
