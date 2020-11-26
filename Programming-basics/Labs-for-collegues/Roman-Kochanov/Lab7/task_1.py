import csv
import datetime
import os
import re
import sys

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication


class Note:
    def __init__(self, name, phone, birthday):
        self.name = name
        self.phone = phone
        self.birthday = birthday

    def __str__(self):
        birthday = self.birthday.strftime("%d.%m.%Y")
        return f'Имя: {self.name}\nТелефон: {self.phone}\nДата рождения: {birthday}'


class Notes:
    def __init__(self, notes):
        self.notes = notes

    def add(self, note):
        self.notes.append(note)
        self.notes.sort(key=lambda x: x.birthday)

    def search(self, phone):
        for note in self.notes:
            if note.phone == phone:
                return note

    def dump(self, path):
        with open(path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Имя, фамилия", "Телефон", "Дата рождения"])

            for item in self.notes:
                writer.writerow([item.name, item.phone, item.birthday.strftime("%d.%m.%Y")])

    def __str__(self):
        return '\n\n'.join(str(note) for note in self.notes)


notes = Notes([])


class MainWindow(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('./ui/MainWindow.ui', self)
        self.InputWindow = InputWindow(self, [])
        self.ErrorWindow = ErrorWindow(self, [])
        self.SaveWindow = SaveWindow(self, [])
        self.SearchWindow = SearchWindow(self, [])
        self.setWindowTitle("Note")
        self.AddButton.clicked.connect(self.input)
        self.SearchButton.clicked.connect(self.search)
        self.DumpButton.clicked.connect(self.dump)
        self.ExitButton.clicked.connect(self.close)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.timer.start()
        self.timer.timeout.connect(self.show)

    def input(self):
        self.InputWindow.show()

    def show(self):
        self.DataBrowser.setText(str(notes))
        super().show()

    def dump(self):
        if len(notes.notes) == 0:
            self.error("Список пуст")
            return
        self.SaveWindow.show()

    def search(self):
        if len(notes.notes) == 0:
            self.error("Список пуст")
            return
        self.SearchWindow.show()

    def error(self, text):
        self.ErrorWindow.close()
        self.ErrorWindow.display(text)

    def close(self):
        self.ErrorWindow.close()
        self.InputWindow.close()
        self.SaveWindow.close()
        self.SearchWindow.close()
        super().close()


class InputWindow(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('./ui/InputWindow.ui', self)
        self.EnterButton.clicked.connect(self.input)
        self.CloseButton.clicked.connect(self.close)
        self.setWindowTitle("Ввод Note")

    def clear(self):
        self.BirthInput.clear()
        self.FIOInput.clear()
        self.PhoneInput.clear()

    def input(self):
        if not (len(self.BirthInput.text().strip()) > 0 and
                len(self.FIOInput.text().strip()) > 0 and
                len(self.PhoneInput.text().strip())):
            self.clear()
            return

        fio = self.FIOInput.text().strip()
        phone = self.PhoneInput.text().strip()
        try:
            phone = int(phone)
        except ValueError:
            self.clear()
            return
        pattern = re.compile(r'(\d{2})\D*(\d{2})\D*(\d{4})')
        birth = pattern.search(self.BirthInput.text())

        dd, mm, yy = birth.group(1), birth.group(2), birth.group(3)
        try:
            birthday = datetime.datetime(int(yy), int(mm), int(dd))
        except ValueError:
            self.clear()
            return

        notes.add(Note(fio, phone, birthday))
        self.clear()


class ErrorWindow(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('./ui/ErrorWindow.ui', self)

        self.ExitButton.clicked.connect(self.close)
        self.setWindowTitle("Ошибка")

    def display(self, message):
        self.ErrorBrowser.setText("Ошибка!\n" + message)
        self.show()


class SaveWindow(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('./ui/SaveWindow.ui', self)
        self.ExitButton.clicked.connect(self.close)
        self.SaveButton.clicked.connect(self.save)
        self.setWindowTitle("Сохранить")

    def path(self):
        name = self.FilenameInput.text().strip()
        if len(name) == 0:
            raise ValueError
        if not name.endswith('.csv'):
            name = name + '.csv'
        return f"{os.getcwd()}/{name}"

    def save(self):
        try:
            path = self.path()
        except ValueError:
            path = f"{os.getcwd()}/notes.csv"
        notes.dump(path)
        self.clear()
        self.close()

    def clear(self):
        self.FilenameInput.clear()

    def close(self):
        self.clear()
        super().close()


class SearchWindow(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('./ui/SearchWindow.ui', self)

        self.SearchButton.clicked.connect(self.show_results)
        self.ExitButton.clicked.connect(self.close)
        self.setWindowTitle("Поиск")

    def show_results(self):
        if len(self.QueryInput.text().strip()) == 0:
            self.ResultsBrowser.setText("Введите запрос")
            return

        try:
            query = int(self.QueryInput.text())
        except ValueError:
            self.clear()
            return
        finally:
            self.clear()

        people = notes.search(query)

        if people:
            msg = f"Номер телефона '{query}' у: "
            self.ResultsBrowser.setText(f"{msg}\n{people}")
        else:
            self.ResultsBrowser.setText("Люди не найдены")

    def clear(self):
        self.ResultsBrowser.clear()
        self.QueryInput.clear()

    def close(self):
        self.clear()
        super().close()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
window.input()
exit(app.exec_())
