import sys
from pathlib import Path

import PyQt5.QtWidgets as Widgets
from PyQt5 import uic
from .task_1 import Route, Routes

MAIN_WINDOW_PATH = Path('./ui/MainWindow.ui')
ERROR_WINDOW_PATH = Path('./ui/ErrorWindow.ui')
INPUT_WINDOW_PATH = Path('./ui/InputWindow.ui')
SAVE_WINDOW_PATH = Path('./ui/SaveWindow.ui')
SEARCH_WINDOW_PATH = Path('./ui/SearchWindow.ui')

ROUTES_COUNT = 2

routes = Routes()


class MainWindow(Widgets.QMainWindow):
    def __init__(self, *args) -> None:
        super().__init__()
        uic.loadUi(MAIN_WINDOW_PATH, self)

        self.initUI()

    def initUI(self) -> None:
        """ Инициализация окон и кнопок """
        self.InputWindow = InputWindow(self, [])
        self.ErrorWindow = ErrorWindow(self, [])
        self.SaveWindow = SaveWindow(self, [])
        self.SearchWindow = SearchWindow(self, [])
        self.setWindowTitle("Маршруты")

        self.SearchButton.clicked.connect(self.search)
        self.DumpButton.clicked.connect(self.dump)
        self.ExitButton.clicked.connect(self.close)

    def input(self) -> None:
        """ Вызов окна ввода маршрутов """
        if len(routes) == ROUTES_COUNT:
            self.ErrorWindow.display(
                "Список маршрутов уже задан, ввод невозможен")
            return
        self.InputWindow.show()

    def show(self) -> None:
        if len(routes) != ROUTES_COUNT:
            super().show()
            # self.InputWindow.show()
        else:
            self.RoutesBrowser.setText(str(routes))
            super().show()

    def dump(self) -> None:
        """ 'сохранить как', вывод в csv файл """
        if not routes:
            self.ErrorWindow.display(
                "Список маршрутов пуст, нечего выводить в файл")
            return
        self.SaveWindow.show()

    def search(self) -> None:
        if len(routes) == 0:
            self.ErrorWindow.display("Список маршрутов пуст, негде искать")
            return
        self.SearchWindow.show()

    def close(self) -> None:
        """ Закрыть все окна """
        self.ErrorWindow.close()
        self.InputWindow.close()
        self.SaveWindow.close()

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

    def clear(self) -> None:
        self.RNumInput.clear()
        self.RStartInput.clear()
        self.RDestInput.clear()

    def input(self) -> None:
        """ Считать из полей значения, преобразовать их в
        объект типа Route.

        :exception ValueError: если в качестве номера введено
        не число или если какая-то из строк оказалась пустой.
        """
        if not (len(self.RNumInput.text().strip()) > 0 and
                len(self.RStartInput.text().strip()) and
                len(self.RDestInput.text().strip()) > 0):
            self.clear()
            return

        try:
            num = int(self.RNumInput.text().strip())
        except ValueError:
            self.clear()
            return
        start = self.RStartInput.text().strip()
        dest = self.RDestInput.text().strip()

        routes.add(Route(num, start, dest))
        self.clear()

        if len(routes) == ROUTES_COUNT:
            self.close()

        self.RoutesRemain.setText(
            f"Осталось ввести: {ROUTES_COUNT - len(routes)}")

    def show(self) -> None:
        self.RoutesRemain.setText(f"Осталось ввести: {ROUTES_COUNT - len(routes)}")
        super().show()


class ErrorWindow(Widgets.QWidget):
    def __init__(self, *args) -> None:
        super().__init__()
        uic.loadUi(ERROR_WINDOW_PATH, self)
        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle("Ошибка")
        self.Box.clicked.connect(self.close)

    def display(self, message: str) -> None:
        error = "<center><b>Ошибка!</b></center><br>"
        self.ErrorBrowser.setText(f"{error}\n{message}")
        self.show()


class SaveWindow(Widgets.QWidget):
    def __init__(self, *args) -> None:
        super().__init__()
        uic.loadUi(SAVE_WINDOW_PATH, self)
        self.initUI()

    def initUI(self) -> None:
        self.ExitButton.clicked.connect(self.close)
        self.SaveButton.clicked.connect(self.save)

    def get_path(self) -> Path:
        name = self.FilenameInput.text()
        if len(name) < 2:
            raise ValueError("Имя файла слишком короткое или пустое")
        name = f"{name}{'.csv' * (not name.endswith('.csv'))}"
        return Path.cwd() / name

    def save(self) -> None:
        try:
            path = self.get_path()
        except ValueError as e:
            self.FilenameInput.setText(str(e))
        else:
            routes.dump(path)
            self.close()


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
            self.QueryInput.setText("<b>Введите запрос</b>")
            return

        query = self.QueryInput.text()
        self.QueryInput.clear()

        starts = routes.starts_in_point(query)
        ends = routes.ends_in_point(query)

        if not (starts or ends):
            self.ResultsBrowser.setText("Маршрутов не найдено")
        if starts:
            msg = f"Маршруты, начинающиеся в '{query}': "
            self.ResultsBrowser.setText(f"{msg}\n{starts}")
        if ends:
            last_text = self.ResultsBrowser.toPlainText()
            msg = f"Маршруты, заканчивающиеся в '{query}': "
            self.ResultsBrowser.setText(f"{last_text}\n{msg}\n{ends}")


def main() -> None:
    app = Widgets.QApplication(sys.argv)
    RoutesWindow = MainWindow()
    RoutesWindow.show()
    RoutesWindow.input()
    exit(app.exec_())
