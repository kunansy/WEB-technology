#!/usr/bin/env python3
import os
from pathlib import Path
from typing import List

SCRIPT_PATH = None
TABLE_PATH = None


def get_chapters(path: Path) -> List[str]:
    """ Get headers from a file and convert them to
    string format: "1. [name](link)".

    :param path: Path to the file.
    :return: list of strings this format.
    """
    chapters = []
    with path.open(encoding="utf-8") as f:
        for line in f.readlines():
            if line.startswith('#'):
                clean_line = line.replace('#', '').strip()
                link = '#' * line.count('#') + clean_line.replace(' ', '-')
                table_line = f"1. [{clean_line}]({link})"
                chapters += [table_line]
    return chapters


def dump_chapters(chapters: List[str],
                  path: Path) -> None:
    """ Dump chapters to the file.

    :param chapters: list of strings to dump.
    :param path: Path to file to where chapters will be dumped.
    :return: None.
    """
    with path.open('w', encoding='utf-8') as f:
        for line in chapters:
            f.write(f"{line}\n")


def tree(startpath: str = '.',
         baseindent: int = 2,
         skip: List[str] = None) -> None:
    skip = skip or []

    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * baseindent * level

        for skip_dir in skip:
            try:
                dirs.remove(skip_dir)
            except ValueError:
                pass

        basename = root.split('/')[-1]
        print(f'{indent}{basename}/')

        subindent = ' ' * baseindent * (level + 1)
        for f in sorted(files):
            print(f'{subindent}{f}')


def main() -> None:
    show_tree = input("Do you want to see a tree (yes or not)? ")
    if show_tree == 'yes':
        tree(skip=['.git', 'venv', '.idea', '__pycache__'])

    script_path = Path.cwd() /  (SCRIPT_PATH or input("Volume path: "))
    table_path = Path.cwd() / (TABLE_PATH or input("Table path: "))

    if table_path is None or not table_path.name:
        name = f"{script_path.stem}_table{script_path.suffix}"
        table_path = script_path.with_name(name)
    chapters = get_chapters(script_path)
    dump_chapters(chapters, table_path)


if __name__ == "__main__":
     main()
