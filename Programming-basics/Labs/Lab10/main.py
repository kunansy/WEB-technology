#!/usr/bin/env python3
import logging
import os
import sys
from pathlib import Path
from typing import Union

import request


LEVEL = Union[int, str]

MSG_FMT = "[{asctime},{msecs:3.0f}] [{levelname}] " \
          "[{module}:{funcName}] {message}"
DATE_FMT = "%d.%m.%Y %H:%M:%S"

LOG_FOLDER = Path('logs')
os.makedirs(LOG_FOLDER, exist_ok=True)

formatter = logging.Formatter(
    fmt=MSG_FMT, datefmt=DATE_FMT, style='{'
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

try:
    data_folder = os.environ['DATA_FOLDER']
except KeyError:
    logger.error("You have to define environment variable 'DATA_FOLDER'")
    exit(-1)

DATA_FOLDER = Path(data_folder)
os.makedirs(DATA_FOLDER, exist_ok=True)


def set_handler_level(handler_class: type):
    def wrapped(level: LEVEL) -> None:
        try:
            level = level.upper()
        except AttributeError:
            pass

        for handler in logger.handlers:
            if isinstance(handler, handler_class):
                handler.setLevel(level)
                return
        print(f"There is no '{handler_class}' handler."
              f"This behavior is undefined, contact the developer",
              file=sys.stderr)

    return wrapped


set_stream_handler_level = set_handler_level(logging.StreamHandler)
set_file_handler_level = set_handler_level(logging.FileHandler)


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
