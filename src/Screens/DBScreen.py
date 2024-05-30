from src.resource_path import resource_path

from PyQt6 import uic
from PyQt6.QtCore import Qt, QObject
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import QMainWindow, QDialog, QPushButton, QLineEdit


class DBScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = None
        self.db = None
        uic.loadUi(resource_path("src/Screens/DBScreen.ui"), self)
        self.initUI()

    def initUI(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")  # тип БД
        self.db.setDatabaseName(resource_path("src/main.db"))  # имя БД
        self.db.open()  # подключение к БД

        self.model = QSqlTableModel(self, self.db)  # модель БД
        self.model.setTable("people")
        self.model.select()  # выборка данных из таблицы `people`
        arr = ["id", "Имя", "Фамилия", "Отчество", "День рождения", "Мать",
               "Отец", "Живой", "Дата смерти", "Статус", "Новоприставленный"]  # названия колонок

        for i, v in enumerate(arr):
            self.model.setHeaderData(i, Qt.Orientation.Horizontal, QObject.tr(v))

        self.tableView.setModel(self.model)  # отображение модели данных
        self.tableView.hideColumn(0)
        self.tableView.hideColumn(self.model.columnCount() - 1)  # удаление ненужные колонки
        self.pushButtonInsert.clicked.connect(self.add_row)
        self.pushButtonDelete.clicked.connect(self.del_row)

    def add_row(self):
        """Создание новой записи в таблице `people`."""
        row_count = self.model.rowCount()
        self.model.insertRow(row_count)
        self.model.setData(self.model.index(row_count, self.model.fieldIndex("name")), "")
        self.model.setData(self.model.index(row_count, self.model.fieldIndex("alive")), 1)
        self.model.submitAll()
        self.model.select()

    def del_row(self):
        """Удаление записи в таблице `people`."""
        def b_pressed(b: QPushButton):
            try:
                self.model.deleteRowFromTable(int(inpt.text()) - 1)
                self.model.submitAll()
                self.model.select()
                dialog.close()
            except Exception as e:
                print(e)

        dialog = QDialog(self)
        btn = QPushButton('OK', dialog)
        inpt = QLineEdit(dialog)
        btn.move(90, 130)
        inpt.move(60, 100)
        btn.clicked.connect(b_pressed)
        dialog.setWindowTitle("Введите номер строки")
        dialog.exec()
