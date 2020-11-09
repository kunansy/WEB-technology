#!/usr/bin/env python3
import sys
from pathlib import Path
from typing import List, Set

import PyQt5.QtWidgets as Widgets
from PyQt5 import uic, QtCore

MAIN_WINDOW_PATH = Path('./ui/MainWindow.ui')
ERROR_WINDOW_PATH = Path('./ui/ErrorWindow.ui')
INPUT_WINDOW_PATH = Path('./ui/InputWindow.ui')
SEARCH_WINDOW_PATH = Path('./ui/SearchWindow.ui')


def sltext(text: str) -> str:
    return text.lower().strip()


class Point:
    def __init__(self,
                 word: str = '',
                 pages: List[int] = None) -> None:
        self._word = word.strip()
        self._pages = set(pages) or set()

    @property
    def word(self) -> str:
        return self._word

    @property
    def pages(self) -> List[int]:
        return list(sorted(self._pages))

    def update(self,
               pages: List[int] or Set[int]) -> None:
        self._pages.union(pages)

    def __contains__(self,
                     page: int) -> bool:
        return page in self.pages

    def __str__(self) -> str:
        num = f"Слово '{self.word}'"
        pages = ', '.join(str(page) for page in self.pages)
        pages = f"На страницах: {pages}"

        return f"{num}\n{pages}"


class Pointer:
    def __init__(self,
                 points: List[Point] = None) -> None:
        self._points = points or []

    @property
    def points(self) -> List[Point]:
        return self._points

    def search(self,
               word: str) -> Point or None:
        word = sltext(word)
        for point in self.points:
            if word == sltext(point.word):
                return point

    def add(self,
            point: Point) -> None:
        if point.word not in self:
            self._points += [point]
            return

        for i in range(len(self)):
            if self._points[i].word == point.word:
                self._points[i].update(point.pages)

    def __contains__(self,
                     word: str) -> bool:
        return any(word.strip() == point.word for point in self)

    def __getitem__(self,
                    word: str) -> Point or None:
        word = word.strip()
        if word not in self:
            return
        for point in self:
            if word == point.word:
                return point

    def __iter__(self) -> iter:
        return iter(self.points)

    def __str__(self) -> str:
        if len(self) == 0:
            return ''

        corner = '-' * 25
        inside = '\n' + '-' * 20 + '\n'

        points = inside.join(str(point) for point in self.points)
        return f"{corner}\n{points}\n{corner}"

    def __len__(self) -> int:
        return len(self.points)


pointer = Pointer()


class MainWindow(Widgets.QMainWindow):
    def __init__(self, *args) -> None:
        super().__init__()
        uic.loadUi(MAIN_WINDOW_PATH, self)

        self.initUI()

    def initUI(self) -> None:
        self.InputWindow = InputWindow(self, [])
        self.ErrorWindow = ErrorWindow(self, [])
        self.SearchWindow = SearchWindow(self, [])
        self.setWindowTitle("Предметный указатель")

        self.SearchButton.clicked.connect(self.search)
        self.AddButton.clicked.connect(self.add)
        self.ExitButton.clicked.connect(self.close)

        self.checkThreadTimer = QtCore.QTimer(self)
        self.checkThreadTimer.setInterval(500)
        self.checkThreadTimer.start()

        self.checkThreadTimer.timeout.connect(self.show)

    def show(self) -> None:
        self.PointsBrowser.setText(str(pointer))
        super().show()

    def add(self) -> None:
        self.InputWindow.close()
        self.InputWindow.show()

    def search(self) -> None:
        self.SearchWindow.close()

        if len(pointer) == 0:
            self.error("Предметный указатель пуст, негде искать")
        else:
            self.SearchWindow.show()

    def error(self, msg: str) -> None:
        self.ErrorWindow.close()
        self.ErrorWindow.display(msg)

    def close(self) -> None:
        self.ErrorWindow.close()
        self.InputWindow.close()
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
        self.setWindowTitle("Ввод компонентов указателя")

    def stext(self, obj) -> str:
        return obj.text().strip()

    def clear(self) -> None:
        self.WordInput.clear()
        self.PagesInput.clear()

    def input(self) -> None:
        if len(self.stext(self.WordInput)) == 0 or \
                len(self.stext(self.PagesInput)) == 0:
            self.clear()
            return
        word = self.stext(self.WordInput)
        pages = self.stext(self.PagesInput)
        if ',' in pages:
            pages = pages.split(',')
        else:
            pages = pages.split()

        try:
            pages = [int(page) for page in pages]
        except ValueError:
            pass
        else:
            pointer.add(Point(word, pages))
        finally:
            self.clear()


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


class SearchWindow(Widgets.QWidget):
    def __init__(self, *args) -> None:
        super().__init__()
        uic.loadUi(SEARCH_WINDOW_PATH, self)

        self.initUI()

    def initUI(self) -> None:
        self.SearchButton.clicked.connect(self.show_results)
        self.ExitButton.clicked.connect(self.close)
        self.setWindowTitle("Поиск слова")

    def show_results(self) -> None:
        if len(self.QueryInput.text().strip()) == 0:
            self.ResultsBrowser.setText("<center><b>Введите запрос</b></center>")
            return

        query = self.QueryInput.text().strip()
        self.clear()

        point = pointer.search(query)

        if point is None:
            self.ResultsBrowser.setText("Слова не найдены")
        else:
            msg = f"Слово '{query}' встречается на: "
            pages = ', '.join(str(page) for page in point.pages)
            self.ResultsBrowser.setText(f"{msg}\n{pages} страницах")

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
