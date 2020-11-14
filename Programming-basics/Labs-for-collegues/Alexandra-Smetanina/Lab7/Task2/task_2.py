import sys

import PyQt5.QtWidgets as W
from PyQt5 import uic, QtCore
from datetime import datetime as dt


class Train:
    def __init__(self, a, b, c):
        self.number = a
        self.dest = b
        self.time = c

    def __str__(self):
        time = self.time.strftime("%H:%M")
        return f"Поезд {self.number}\nОтправляется в {time}\nИдёт до {self.dest}"


class Trains:
    def __init__(self, a):
        self.trains = a

    def search_by_num(self, num):
        for train in self.trains:
            if train.number == num:
                return train

    def search_by_dest(self, dest):
        res = []
        dest = dest.strip()
        for train in self.trains:
            if train.dest.strip() == dest:
                res.append(train)
        if res:
            return Trains(res)

    def append(self, train):
        if train not in self:
            self.trains.append(train)

    def __contains__(self, a):
        return any(i == a for i in self.trains)

    def __str__(self):
        if len(self.trains) == 0:
            return ''

        return '\n\n'.join(str(t) for t in self.trains)


trains = Trains([])


class MainWindow(W.QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('./windows/MainWindow.ui', self)

        self.InputWindow = InputWindow(self, [])
        self.ErrorWindow = ErrorWindow(self, [])
        self.SearchWindow = SearchWindow(self, [])
        self.setWindowTitle("Поезда")

        self.SearchButton.clicked.connect(self.find)
        self.AddButton.clicked.connect(self.input)
        self.ExitButton.clicked.connect(self.close)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(500)
        self.timer.start()
        self.timer.timeout.connect(self.show)

    def show(self):
        self.TrainsBrowser.setText(str(trains))
        super().show()

    def input(self):
        self.InputWindow.close()
        self.InputWindow.show()

    def find(self):
        self.SearchWindow.close()

        if len(trains.trains) == 0:
            self.error("Список поездов пуст")
        else:
            self.SearchWindow.show()

    def error(self, t):
        self.ErrorWindow.close()
        self.ErrorWindow.display(t)

    def close(self):
        self.ErrorWindow.close()
        self.InputWindow.close()
        self.SearchWindow.close()

        super().close()


class InputWindow(W.QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('./windows/InputWindow.ui', self)

        self.EnterButton.clicked.connect(self.input)
        self.ClearButton.clicked.connect(self.clear)
        self.setWindowTitle("Ввод поездов")

    def clear(self):
        self.DestInput.clear()
        self.NumberInput.clear()
        self.TimeInput.clear()

    def input(self):
        if len(self.NumberInput.text().strip()) == 0 or \
                len(self.TimeInput.text().strip()) == 0 or \
                len(self.DestInput.text().strip()) == 0:
            self.clear()
            return
        num = self.NumberInput.text()
        try:
            num = int(num)
        except ValueError:
            self.clear()
            return

        time = self.TimeInput.text().strip()
        try:
            time = dt.strptime(time, "%H:%M")
        except ValueError:
            self.clear()
            return

        dest = self.DestInput.text().strip()

        trains.append(Train(num, dest, time))
        self.clear()


class ErrorWindow(W.QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('./windows/ErrorWindow.ui', self)

        self.OkButton.clicked.connect(self.close)
        self.setWindowTitle("Ошибка")

    def display(self, t):
        self.ErrorBrowser.setText(f"Ошибка!\n\n{t}")
        self.show()


class SearchWindow(W.QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('./windows/SearchWindow.ui', self)

        self.SearchByNumButton.clicked.connect(self.search_by_num)
        self.SearchByDestButton.clicked.connect(self.search_by_dest)
        self.ExitButton.clicked.connect(self.close)
        self.setWindowTitle("Поиск")

    def search_by_num(self):
        if len(self.QueryInput.text().strip()) == 0:
            self.ResultsBrowser.setText("Введите запрос")
            return

        query = self.QueryInput.text().strip()
        self.clear()

        try:
            query = int(query)
        except ValueError:
            self.ResultsBrowser.setText("Введите число")
            return

        res = trains.search_by_num(query)

        if res is None:
            self.ResultsBrowser.setText("Поезд не найден")
        else:
            self.ResultsBrowser.setText(f"{res}")

    def search_by_dest(self):
        if len(self.QueryInput.text().strip()) == 0:
            self.ResultsBrowser.setText("Введите запрос")
            return

        query = self.QueryInput.text().strip()
        self.clear()

        res = trains.search_by_dest(query)
        if res is None:
            self.ResultsBrowser.setText(f"Поезда в {query} не идут")
        else:
            self.ResultsBrowser.setText(f"До {query} следуют: \n{res}")

    def clear(self):
        self.ResultsBrowser.clear()
        self.QueryInput.clear()

    def close(self):
        self.clear()
        super().close()


a = W.QApplication(sys.argv)
main = MainWindow()
main.show()
main.input()
exit(a.exec_())
