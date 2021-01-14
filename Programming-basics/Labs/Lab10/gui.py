#!/usr/bin/env python3
import logging
import os
import sys
from pathlib import Path

import request

import PyQt5.QtWidgets as Widgets
from PyQt5 import uic, QtCore, QtGui

MAIN_WINDOW_PATH = ".{sep}ui{sep}main_window.ui".format(sep=os.sep)
MAIN_WINDOW_PATH = Path(MAIN_WINDOW_PATH)

logger = logging.getLogger('web-scraper')


class QtHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        record = self.format(record)
        if record:
            XStream.stdout().write(str(record))


class XStream(QtCore.QObject):
    _stdout = None
    _stderr = None
    messageWritten = QtCore.pyqtSignal(str)

    def flush(self):
        pass

    def fileno(self):
        return -1

    def write(self, msg):
        if not self.signalsBlocked():
            self.messageWritten.emit(str(msg))

    @staticmethod
    def stdout():
        if not XStream._stdout:
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout

        return XStream._stdout

    @staticmethod
    def stderr():
        if not XStream._stderr:
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr

        return XStream._stderr


def is_ok(txt: str) -> bool:
    return bool(txt.strip())


class MainWindow(Widgets.QMainWindow):
    def __init__(self, *args) -> None:
        super().__init__()
        uic.loadUi(MAIN_WINDOW_PATH, self)

        self.initUI()

        XStream.stdout().messageWritten.connect(self.LogsBrowser.append)
        XStream.stderr().messageWritten.connect(self.LogsBrowser.append)

    def initUI(self) -> None:
        self.GetButton.clicked.connect(self.request)

    def msg(self,
            txt: str) -> None:
        self.LogsBrowser.setText(txt)

    def request(self) -> None:
        self.LogsBrowser.clear()

        if (is_ok(self.FromFileInput.text()) and
                is_ok(self.FromLinkInput.text())):
            self.msg(
                "Choose only one way from where get links and filenames")

        elif is_ok(self.FromLinkInput.text()):
            try:
                request.main(
                    self.FromLinkInput.text(),
                    from_line=True
                )
            except ValueError as e:
                self.msg(str(e))

        elif is_ok(self.FromFileInput.text()):
            try:
                request.main(Path(self.FromFileInput.text()))
            except FileNotFoundError as e:
                self.msg(str(e))
        else:
            self.msg("Set the parameter")

        self.FromFileInput.clear()
        self.FromLinkInput.clear()


def main() -> None:
    handler = QtHandler()
    handler.setFormatter(logger.handlers[0].formatter)
    handler.setLevel(logging.DEBUG)

    logger.addHandler(handler)

    app = Widgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    exit(app.exec_())


if __name__ == '__main__':
    main()
