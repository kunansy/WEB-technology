#!/usr/bin/env python3
import csv
import sys
from pathlib import Path
from typing import List, Any


def clear() -> None:
    # в разных системах экран очищается по-разному
    if 'linux' in sys.platform:
        os.system('clear')
    elif sys.platform == 'win32':
        os.system('cls')


DUMP_PATH = Path('routes.txt')


class Route:
    def __init__(self,
                 num: int,
                 start: str,
                 dest: str) -> None:
        self._num = num
        self._start = start
        self._dest = dest

    @property
    def num(self) -> int:
        return self._num

    @property
    def start(self) -> str:
        return self._start

    @property
    def dest(self) -> str:
        return self._dest

    def __str__(self) -> str:
        num = f"Маршрут: {self.num}"
        start = f"Из: '{self.start}'"
        dest = f"В: '{self.dest}'"
        return f"{num}\n{start}\n{dest}"


class Routes:
    # for csv writing
    DELIMITER = '\t'
    QUOTECHAR = '"'
    COLUMNS = ["Номер маршрута", "Начало маршрута", "Конец маршрута"]

    def __init__(self, routes: List[Route] = None) -> None:
        self._routes = routes or []

    def starts_in_point(self, point: str) -> Any:
        point = point.lower().strip()
        starts = [
            route for route in self._routes
            if route.start.lower().strip() == point
        ]
        return Routes(starts)

    def ends_in_point(self, point: str) -> Any:
        point = point.lower().strip()
        ends = [
            route for route in self._routes
            if route.dest.lower().strip() == point
        ]
        return Routes(ends)

    def dump(self, path: Path) -> None:
        rows = [
            [route.num, route.start, route.dest]
            for route in self
        ]
        with path.open('w', encoding='utf-8', newline='') as f:
            dm = self.DELIMITER
            qch = self.QUOTECHAR
            writer = csv.writer(
                f, delimiter=dm, quotechar=qch, quoting=csv.QUOTE_MINIMAL)
            writer.writerows([self.COLUMNS] + rows)

    def add(self, route: Route) -> None:
        self._routes += [route]
        self._routes.sort(key=lambda route: route.num)

    def __iter__(self) -> iter:
        return iter(self._routes)

    def __bool__(self) -> bool:
        return bool(self._routes)

    def __iadd__(self, route: Route) -> Any:
        self.add(route)
        return self

    def __str__(self) -> str:
        corner = '-' * 20
        inside = '\n' + '-' * 15 + '\n'

        res = inside.join(str(route) for route in self._routes)
        return f"{corner}\n{res}\n{corner}"


def input_routes() -> Routes:
    routes = Routes()
    for _ in range(8):
        try:
            num = int(input("Введите номер маршрута: "))
        except ValueError:
            print("Ожидалось число", file=sys.stderr)
            raise
        start = input("Введите начальный пункт маршрута: ")
        dest = input("Введите конечный пункт маршрута: ")

        route = Route(num, start, dest)
        routes += route

        print()
    return routes


def menu() -> None:
    print("1. Распечатать маршруты")
    print("2. Искать маршрут")
    print("3. Вывести маршруты в файл")
    print("4. Выйти")


def main() -> None:
    try:
        routes = input_routes()
    except ValueError:
        print("Неверный ввод, уничтожение...", file=sys.stderr)
        exit(-1)

    while True:
        clear()
        menu()
        choice = input()
        clear()

        if choice == '1':
            print(routes)
        elif choice == '2':
            point = input("Введите пункт: ")
            starts = routes.starts_in_point(point)
            ends = routes.ends_in_point(point)

            if not (starts or ends):
                print("Маршрутов не найдено")
            if starts:
                print("Маршруты, начинающиеся в введённом пункте: ")
                print(starts)
            if ends:
                print("Маршруты, заканчивающиеся в введённом пункте: ")
                print(ends)
        elif choice == '3':
            path = Path(input("Введите имя файла: "))
            path = Path.cwd() / path
            routes.dump(path)
        elif choice == '4':
            break
        else:
            print("Неверный ввод", file=sys.stderr)
        input("----Нажмите Enter, чтобы продолжить----")


if __name__ == "__main__":
    main()
