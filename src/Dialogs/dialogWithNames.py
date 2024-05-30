import sqlite3

from src.resource_path import resource_path

from PyQt6.QtGui import QIcon
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QCheckBox, QPushButton


class DialogWithNames(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.data = []  # итоговые данные
        self.res = False  # сброс или добавление данных (результат работы диалогового окна)
        self.list_of_rows = []  # поля ввода данных
        uic.loadUi(resource_path("src/Dialogs/dialogWithNames.ui"), self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Выберите имена")
        self.setWindowIcon(QIcon(resource_path("resources/Images/icon.png")))
        self.submitButton.clicked.connect(self.commit)
        with sqlite3.connect(resource_path("src/main.db")) as conn:
            cursor = conn.cursor()
            res = cursor.execute("SELECT name, lastname, surname FROM people;").fetchall()

            for i, v in enumerate(res):
                res[i] = list(v)
                for idx, val in enumerate(res[i]):
                    if val is None or val.strip() == "":
                        res[i][idx] = "-----"
                ch = QCheckBox("    ".join(res[i]))
                ch.setStyleSheet("margin: 4px;")
                self.list_of_rows.append(ch)
                self.verticalLayoutWithRows.addWidget(ch)

    def commit(self, btn: QPushButton):
        arr = []
        for i in self.list_of_rows:
            if i.isChecked():
                arr.append(i.text().split()[0])
        self.res = True
        self.data = arr
        self.hide()
