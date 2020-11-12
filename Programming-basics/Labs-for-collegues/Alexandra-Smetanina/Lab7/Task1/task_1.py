#!/usr/bin/env python3
import csv
import os
import sys

import PyQt5.QtWidgets as W
from PyQt5 import uic, QtCore


class Price:
    def __init__(self, a, b, c):
        self.name = a
        self.price = b
        self.shop = c

    def __str__(self):
        return f"Товар {self.name} {self.price}р\nПродаётся в {self.shop}"


class Shop:
    def __init__(self, a):
        self.items = a

    def to_file(self, a):
        headers = ['Товар', 'Цена', 'Магазин']
        with open(a, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)

            writer.writerow(headers)
            for item in self.items:
                writer.writerow([item.name, item.price, item.shop])

    def append(self, a):
        self.items.append(a)
        self.items.sort(key=lambda x: x.shop)

    def find(self, a):
        res = []
        a = a.strip()
        for i in self.items:
            if i.shop.strip() == a:
                res.append(i)
        return Shop(res)

    def __str__(self):
        if len(self.items) == 0:
            return ''

        return '\n\n'.join(str(item) for item in self.items)


shop = Shop([])


class MainWindow(W.QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('./windows/MainWindow.ui', self)

        self.InputWindow = InputWindow(self, [])
        self.ErrorWindow = ErrorWindow(self, [])
        self.SaveWindow = SaveWindow(self, [])
        self.SearchWindow = SearchWindow(self, [])
        self.setWindowTitle("Товары")

        self.SearchButton.clicked.connect(self.find)
        self.DumpButton.clicked.connect(self.to_file)
        self.ExitButton.clicked.connect(self.close)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.start()
        self.timer.timeout.connect(self.show)

    def show(self):
        a = Shop(shop.items[:4])
        b = Shop(shop.items[4:])

        self.ItemsBrowser1.setText(str(a))
        self.ItemsBrowser2.setText(str(b))
        super().show()

        if len(shop.items) != 8:
            self.InputWindow.show()

    def to_file(self):
        if len(shop.items) != 8:
            self.error("Ввод ещё не окончен!")
            return
        self.SaveWindow.show()

    def find(self):
        if len(shop.items) != 8:
            self.error("Ввод ещё не окончен!")
            return
        self.SearchWindow.show()

    def error(self, a):
        self.ErrorWindow.close()
        self.ErrorWindow.display(a)

    def close(self):
        self.ErrorWindow.close()
        self.InputWindow.close()
        self.SaveWindow.close()
        self.SearchWindow.close()

        super().close()


class InputWindow(W.QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('./windows/InputWindow.ui', self)

        self.EnterButton.clicked.connect(self.input)
        self.ClearButton.clicked.connect(self.clear)
        self.setWindowTitle("Ввод товаров")

    def clear(self):
        self.NameInput.clear()
        self.PriceInput.clear()
        self.ShopInput.clear()

    def input(self):
        if not (len(self.NameInput.text().strip()) > 0 and
                len(self.PriceInput.text().strip()) > 0 and
                len(self.ShopInput.text().strip()) > 0):
            self.clear()
            return

        p = self.PriceInput.text().strip()
        try:
            p = float(p)
        except ValueError:
            self.clear()
            return
        n = self.NameInput.text().strip()
        s = self.ShopInput.text().strip()

        shop.append(Price(n, p, s))
        self.clear()

        if len(shop.items) == 8:
            self.close()

        self.ItemsRemain.setText(f"Осталось ввести: {8 - len(shop.items)}")

    def show(self):
        self.ItemsRemain.setText(f"Осталось ввести: {8 - len(shop.items)}")
        super().show()


class ErrorWindow(W.QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('./windows/ErrorWindow.ui', self)

        self.OkButton.clicked.connect(self.close)
        self.setWindowTitle("Ошибка")

    def display(self, message):
        self.ErrorBrowser.setText(f"Ошибка!\n\n{message}")
        self.show()


class SaveWindow(W.QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('./windows/SaveWindow.ui', self)

        self.ExitButton.clicked.connect(self.close)
        self.SaveButton.clicked.connect(self.save)
        self.setWindowTitle("Сохранить как")

    def path(self):
        name = self.FilenameInput.text().strip()
        if len(name) == 0:
            raise ValueError("Имя файла не введено")
        if not name.endswith('.csv'):
            name += '.csv'
        return os.getcwd() + '/' + name

    def save(self):
        try:
            path = self.path()
        except ValueError:
            path = os.getcwd() + '/' + 'file.csv'
        shop.to_file(path)

        self.clear()
        self.close()

    def clear(self):
        self.FilenameInput.clear()

    def close(self):
        self.clear()
        super().close()


class SearchWindow(W.QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('./windows/SearchWindow.ui', self)

        self.SearchButton.clicked.connect(self.res)
        self.ExitButton.clicked.connect(self.close)
        self.setWindowTitle("Поиск по магазинам")

    def res(self):
        if len(self.QueryInput.text().strip()) == 0:
            self.ResultsBrowser.setText("<center><b>Введите запрос</b></center>")
            return

        query = self.QueryInput.text()
        self.clear()

        shops = shop.find(query)
        if not shops.items:
            self.ResultsBrowser.setText(f"Товары из '{query}' не найдены")
        else:
            text = f"Товары из '{query}': "
            self.ResultsBrowser.setText(f"{text}\n{shops}")

    def clear(self):
        self.ResultsBrowser.clear()
        self.QueryInput.clear()

    def close(self):
        self.clear()
        super().close()


app = W.QApplication(sys.argv)
main = MainWindow()
main.show()
exit(app.exec_())
