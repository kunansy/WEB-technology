#!/usr/bin/env python3
import csv
import sys
from pathlib import Path
from typing import List, Any


class Route:
    """ Class for working with a Route """
    def __init__(self,
                 num: int,
                 start: str,
                 dest: str) -> None:
        """ Init a route.

        :param num: int, route number.
        :param start: str, start point of the route.
        :param dest: str, destination point of the route.
        :return: None.
        """
        self._num = num
        self._start = start
        self._dest = dest

    @property
    def num(self) -> int:
        """ Get number of the route.

        :return: int, number of the route.
        """
        return self._num

    @property
    def start(self) -> str:
        """ Get start point of the route.

        :return: str, start point of the route.
        """
        return self._start

    @property
    def dest(self) -> str:
        """ Get destination point of the route.

        :return: str, destination point of the route.
        """
        return self._dest

    def __str__(self) -> str:
        """ Convert the route to str like:
            Маршрут: 'route number'
            Из: `start point`
            В: `destination point`

        :return: str this format.
        """
        num = f"Маршрут: {self.num}"
        start = f"Из: '{self.start}'"
        dest = f"В: '{self.dest}'"

        return f"{num}\n{start}\n{dest}"


class Routes:
    """ Class for working with Routes – a list of Routes """
    # for csv writing
    DELIMITER = '\t'
    QUOTECHAR = '"'
    COLUMNS = ["Номер маршрута", "Начало маршрута", "Конец маршрута"]

    def __init__(self, routes: List[Route] = None) -> None:
        """ Init a Routes obj.

        :param routes: list of Route, Route points to work with
        (empty list by default).
        :return: None.
        """
        self._routes = routes or []

    def starts_in_point(self, point: str) -> Any:
        """ Find Routes, which start in the point.
        Registers are equaled.

        :param point: str, point to find.
        :return: Routes, routes start in the point.
        """
        point = point.lower().strip()
        starts = [
            route for route in self._routes
            if route.start.lower().strip() == point
        ]
        return Routes(starts)

    def ends_in_point(self, point: str) -> Any:
        """ Find Routes, which end in the point.
        Registers are equaled.

        :param point: str, point to find.
        :return: Routes, routes end in the point.
        """
        point = point.lower().strip()
        ends = [
            route for route in self._routes
            if route.dest.lower().strip() == point
        ]
        return Routes(ends)

    def dump(self, path: Path) -> None:
        """ Dump all Routes into a csv file.

        :param path: Path to csv file to dump the routes.
        :return: None.
        """
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
        """ Add a route to the list,
        sort the list by route numbers.

        :param route: Route to add.
        :return: None.
        """
        self._routes += [route]
        self._routes.sort(key=lambda route: route.num)

    def __iter__(self) -> iter:
        """ Standard list method.

        :return: iter to the list.
        """
        return iter(self._routes)

    def __bool__(self) -> bool:
        """ Standard list method.

        :return: whether the list is not empty.
        """
        return bool(self._routes)

    def __len__(self) -> int:
        """ Get len of the list.

        :return: int, len of the list.
        """
        return len(self._routes)

    def __iadd__(self, route: Route) -> Any:
        """ Add a route obj to the list.

        :param route: Route obj to add.
        :return: self.
        """
        self.add(route)
        return self

    def __str__(self) -> str:
        """ Convert all routes to a str, divide them.

        :return: str with converted routes.
        """
        corner = '-' * 20
        inside = '\n' + '-' * 15 + '\n'

        res = inside.join(str(route) for route in self._routes)
        return f"{corner}\n{res}\n{corner}"


if __name__ == "__main__":
    main()
