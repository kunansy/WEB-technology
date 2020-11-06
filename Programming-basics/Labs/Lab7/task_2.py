#!/usr/bin/env python3
import os
import sys
from typing import List, Set


def clear() -> None:
    # в разных системах экран очищается по-разному
    if 'linux' in sys.platform:
        os.system('clear')
    elif sys.platform == 'win32':
        os.system('cls')


class Point:
    def __init__(self,
                 word: str,
                 pages: List[int] or Set[int]) -> None:
        self._word = word
        self._pages = set(pages)

    @property
    def word(self) -> str:
        return self._word

    @property
    def pages(self) -> Set[int]:
        return self._pages

    def __contains__(self, page: int) -> bool:
        return page in self.pages

    def __str__(self) -> str:
        pages = ', '.join(str(page) for page in sorted(self.pages))
        return f"Слово: {self.word}\nНаходится: {pages}"


class Pointer:
    def __init__(self, points: List[Point] = None) -> None:
        self._points = points or []

    @property
    def points(self) -> List[Point]:
        return self._points

    def search(self, word: str) -> Point or None:
        word = word.lower().strip()
        for point in self.points:
            if word == point.word.lower().strip():
                return point

    def add(self, item: Point) -> None:
        self._points += [item]

    def __getitem__(self, word: str) -> Point:
        word = word.lower().strip()
        for point in self.points:
            if point.word.lower().strip() == word:
                return point

    def __str__(self) -> str:
        corner = '-' * 20
        inside = '\n' + '-' * 15 + '\n'

        points = inside.join(str(route) for route in self.points)
        return f"{corner}\n{points}\n{corner}"


def input_point() -> Pointer:
    pointer = Pointer()
    count = int(input("Введите количество записей: "))

    for _ in range(count):
        word = input("Слово: ")
        pages = input("Введите страницы через запятую: ")
        pages = [int(page) for page in pages.split(',')]

        point = Point(word, pages)
        pointer.add(point)
    return pointer


def menu() -> None:
    print("1. Распечатать указатель")
    print("2. Найти слово")
    print("3. Выйти")


def main() -> None:
    try:
        pointer = input_point()
    except ValueError:
        print("Неверный ввод, уничтожение...", file=sys.stderr)
        exit(-1)

    while True:
        clear()
        menu()
        choice = input()
        clear()

        if choice == '1':
            print(pointer)
        elif choice == '2':
            word_to_find = input("Ведите слово: ")
            point = pointer.search(word_to_find)
            if point is not None:
                print(point)
            else:
                print("Слово не найдено в указателе")
        elif choice == '3':
            break
        else:
            print("Неверный ввод", file=sys.stderr)
        input("----Нажмите Enter, чтобы продолжить----")


if __name__ == '__main__':
    main()
