#!/usr/bin/env python3
import argparse
import logging
import os
from pathlib import Path
from typing import Union

import gui
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
        logger.error(f"There is no '{handler_class}' handler.")

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
    parser = argparse.ArgumentParser(
        description="Get HTML codes of the sites"
    )
    parser.add_argument(
        '-f', '--file',
        type=str,
        help="File where there are links and expected file names",
        dest='links'
    )
    parser.add_argument(
        '-l', '--link',
        type=str,
        nargs=2,
        help="Link to get its HTML code and file name from where put it",
        metavar="LINK",
        dest='links'
    )
    parser.add_argument(
        '-dest',
        type=str,
        help="Folder to where save HTML codes",
        required=False,
        default=os.getenv('DATA_FOLDER', 'data')
    )
    parser.add_argument(
        '--log-level',
        type=str,
        help="Set stream handler level",
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        default='debug',
        dest='level'
    )
    parser.add_argument(
        "--no-gui",
        help="Whether start app without GUI",
        action="store_true",
        default=False,
        dest="no_gui"
    )
    args = parser.parse_args()

    os.environ['DATA_FOLDER'] = args.dest
    os.makedirs(args.dest, exist_ok=True)

    set_stream_handler_level(args.level)

    if args.no_gui is False:
        gui.main()
        return

    if args.links is None:
        raise ValueError("Links not set")

    links = args.links
    from_link = False
    if isinstance(links, list):
        links = ' '.join(links)
        from_link = True
    else:
        links = Path(args.links)

    request.main(links, Path(args.dest), from_link)


if __name__ == '__main__':
    main()
