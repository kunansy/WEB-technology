#!/usr/bin/env python3
import csv
import sys
from pathlib import Path
from typing import List, Any

import PyQt5.QtWidgets as Widgets
from PyQt5 import uic, QtCore

MAIN_WINDOW_PATH = Path('./ui/MainWindow.ui')
ERROR_WINDOW_PATH = Path('./ui/ErrorWindow.ui')
INPUT_WINDOW_PATH = Path('./ui/InputWindow.ui')
SAVE_WINDOW_PATH = Path('./ui/SaveWindow.ui')
SEARCH_WINDOW_PATH = Path('./ui/SearchWindow.ui')

ROUTES_COUNT = 8


def sltext(text: str) -> str:
    return text.lower().strip()


def stext(text: str) -> str:
    return text.strip()


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
        num = f"Маршрут №{self.num}"
        start = f"Из: '{self.start}'"
        dest = f"В: '{self.dest}'"

        return f"{num}\n{start}\n{dest}"


class Routes:
    """ Class for working with Routes – a list of Routes """
    # for csv writing
    DELIMITER = '\t'
    QUOTECHAR = '"'
    COLUMNS = ["Номер маршрута", "Начало маршрута", "Конец маршрута"]

    def __init__(self,
                 routes: List[Route] = None) -> None:
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
        point = sltext(point)
        starts = [
            route for route in self._routes
            if sltext(route.start) == point
        ]
        return Routes(starts)

    def ends_in_point(self, point: str) -> Any:
        """ Find Routes, which end in the point.
        Registers are equaled.

        :param point: str, point to find.
        :return: Routes, routes end in the point.
        """
        point = sltext(point)
        ends = [
            route for route in self._routes
            if sltext(route.dest) == point
        ]
        return Routes(ends)

    def dump(self, path: Path) -> None:
        """ Dump all Routes into a csv file.

        :param path: Path to csv file to dump the routes.
        :return: None.
        """
        with path.open('w', encoding='utf-8', newline='') as f:
            dm = self.DELIMITER
            qch = self.QUOTECHAR
            writer = csv.writer(
                f, delimiter=dm, quotechar=qch, quoting=csv.QUOTE_MINIMAL)

            writer.writerow(self.COLUMNS)
            for route in self._routes:
                writer.writerow([route.num, route.start, route.dest])

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
        if len(self) == 0:
            return ''

        corner = '-' * 25
        inside = '\n' + '-' * 20 + '\n'

        res = inside.join(str(route) for route in self._routes)
        return f"{corner}\n{res}\n{corner}"


routes = Routes()


class MainWindow(Widgets.QMainWindow):
    def __init__(self, *args) -> None:
        super().__init__()
        uic.loadUi(MAIN_WINDOW_PATH, self)

        self.initUI()

    def initUI(self) -> None:
        self.InputWindow = InputWindow(self, [])
        self.ErrorWindow = ErrorWindow(self, [])
        self.SaveWindow = SaveWindow(self, [])
        self.SearchWindow = SearchWindow(self, [])
        self.setWindowTitle("Маршруты")

        self.SearchButton.clicked.connect(self.search)
        self.DumpButton.clicked.connect(self.dump)
        self.ExitButton.clicked.connect(self.close)

        self.checkThreadTimer = QtCore.QTimer(self)
        self.checkThreadTimer.setInterval(500)
        self.checkThreadTimer.start()

        self.checkThreadTimer.timeout.connect(self.show)

    def show(self) -> None:
        self.RoutesBrowser.setText(str(routes))
        super().show()

        if len(routes) != ROUTES_COUNT:
            self.InputWindow.show()

    def dump(self) -> None:
        if len(routes) != ROUTES_COUNT:
            self.error("Ввод маршрутов ещё не закончен!")
            return
        self.SaveWindow.show()

    def search(self) -> None:
        if len(routes) != ROUTES_COUNT:
            self.error("Ввод маршрутов ещё не закончен!")
            return
        self.SearchWindow.show()

    def error(self, msg: str) -> None:
        self.ErrorWindow.close()
        self.ErrorWindow.display(msg)

    def close(self) -> None:
        self.ErrorWindow.close()
        self.InputWindow.close()
        self.SaveWindow.close()
        self.SearchWindow.close()

        super().close()


class InputWindow(Widgets.QWidget):
    def __init__(self, *args) -> None:
        super().__init__()
        uic.loadUi(INPUT_WINDOW_PATH, self)

        self.initUI()

    def initUI(self) -> None:
        self.EnterButton.clicked.connect(self.input)
        self.ClearButton.clicked.connect(self.clear)
        self.setWindowTitle("Ввод маршрутов")

    def stext(self, obj) -> str:
        return obj.text().strip()

    def clear(self) -> None:
        self.RNumInput.clear()
        self.RStartInput.clear()
        self.RDestInput.clear()

    def input(self) -> None:
        if not (len(self.stext(self.RNumInput)) > 0 and
                len(self.stext(self.RStartInput)) and
                len(self.stext(self.RDestInput)) > 0):
            self.clear()
            return

        num = self.stext(self.RNumInput)
        try:
            num = int(num)
        except ValueError:
            self.clear()
            return
        start = self.stext(self.RStartInput)
        dest = self.stext(self.RDestInput)

        routes.add(Route(num, start, dest))
        self.clear()

        if len(routes) == ROUTES_COUNT:
            self.close()

        self.RoutesRemain.setText(
            f"Осталось ввести: {ROUTES_COUNT - len(routes)}")

    def show(self) -> None:
        self.RoutesRemain.setText(
            f"Осталось ввести: {ROUTES_COUNT - len(routes)}")
        super().show()


class ErrorWindow(Widgets.QWidget):
    def __init__(self, *args) -> None:
        super().__init__()
        uic.loadUi(ERROR_WINDOW_PATH, self)

        self.initUI()

    def initUI(self) -> None:
        self.Box.clicked.connect(self.close)
        self.setWindowTitle("Ошибка")

    def display(self, message: str) -> None:
        error = "<center><b>Ошибка!</b></center><br>"
        self.ErrorBrowser.setText(f"{error}\n{message}")
        self.show()


class SaveWindow(Widgets.QWidget):
    DEFAULT_FILENAME = 'default.csv'

    def __init__(self, *args) -> None:
        super().__init__()
        uic.loadUi(SAVE_WINDOW_PATH, self)

        self.initUI()

    def initUI(self) -> None:
        self.ExitButton.clicked.connect(self.close)
        self.SaveButton.clicked.connect(self.save)
        self.setWindowTitle("Сохранить как")

    def path(self) -> Path:
        name = stext(self.FilenameInput.text())
        if len(name) == 0:
            raise ValueError("Имя файла слишком короткое или пустое")
        name = f"{name}{'.csv' * (not name.endswith('.csv'))}"
        return Path.cwd() / name

    def save(self) -> None:
        try:
            path = self.path()
        except ValueError:
            path = Path.cwd() / self.DEFAULT_FILENAME
        routes.dump(path)
        self.clear()
        self.close()

    def clear(self) -> None:
        self.FilenameInput.clear()

    def close(self) -> None:
        self.clear()
        super().close()


class SearchWindow(Widgets.QWidget):
    def __init__(self, *args) -> None:
        super().__init__()
        uic.loadUi(SEARCH_WINDOW_PATH, self)

        self.initUI()

    def initUI(self) -> None:
        self.SearchButton.clicked.connect(self.show_results)
        self.ExitButton.clicked.connect(self.close)
        self.setWindowTitle("Поиск маршрутов")

    def show_results(self) -> None:
        if len(self.QueryInput.text().strip()) == 0:
            self.ResultsBrowser.setText("<center><b>Введите запрос</b></center>")
            return

        query = self.QueryInput.text()
        self.clear()

        starts = routes.starts_in_point(query)
        ends = routes.ends_in_point(query)

        if not (starts or ends):
            self.ResultsBrowser.setText("Маршруты не найдены")
        if starts:
            msg = f"Маршруты, начинающиеся в '{query}': "
            self.ResultsBrowser.setText(f"{msg}\n{starts}")
        if ends:
            last_text = self.ResultsBrowser.toPlainText()
            msg = f"Маршруты, заканчивающиеся в '{query}': "
            self.ResultsBrowser.setText(f"{last_text}\n{msg}\n{ends}")

    def clear(self) -> None:
        self.ResultsBrowser.clear()
        self.QueryInput.clear()

    def close(self) -> None:
        self.clear()
        super().close()


def main() -> None:
    app = Widgets.QApplication(sys.argv)
    RoutesWindow = MainWindow()
    RoutesWindow.show()
    exit(app.exec_())


if __name__ == '__main__':
    main()
