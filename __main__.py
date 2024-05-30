# -*- coding: utf-8 -*-

import sys
import time

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QMenu, QStackedWidget, QSplashScreen

from src.resource_path import resource_path
from src.Screens.MainScreen import MainScreen
from src.Screens.DBScreen import DBScreen


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Конструктор записок")  # название
        self.setWindowIcon(QIcon(resource_path("resources/Images/icon.png")))  # иконка
        self.resize(800, 600)
        self.stacked_widget = QStackedWidget()
        self.main_window_screen = MainScreen()
        self.db_screen = DBScreen()
        self.stacked_widget.addWidget(self.main_window_screen)
        self.stacked_widget.addWidget(self.db_screen)
        self.setCentralWidget(self.stacked_widget)
        self.stacked_widget.show()

        menu = QMenu("Главное меню", self)  # меню вверху приложения

        main_action = QAction("Главное окно", self)
        main_action.triggered.connect(self.set_main_screen)

        db_action = QAction("Данные о поминаемых", self)
        db_action.triggered.connect(self.set_db_screen)

        help_action = QAction("Помощь", self)
        help_action.triggered.connect(lambda: print("help"))

        menu.addAction(main_action)
        menu.addAction(db_action)
        menu.addSeparator()
        menu.addAction(help_action)
        menu_bar = self.menuBar()
        menu_bar.addMenu(menu)

    def set_main_screen(self):
        """Отображение главного экрана."""
        self.stacked_widget.setCurrentWidget(self.main_window_screen)

    def set_db_screen(self):
        """Отображение экрана с БД."""
        self.stacked_widget.setCurrentWidget(self.db_screen)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash_pix = QPixmap('./resources/Images/book.png').scaled(360, 260)
    splash = QSplashScreen(splash_pix, Qt.WindowType.WindowStaysOnTopHint)

    opaqueness = 0.0
    step = 0.1

    splash.setWindowOpacity(opaqueness)
    splash.show()
    while opaqueness < 1:
        splash.setWindowOpacity(opaqueness)
        time.sleep(step)
        opaqueness += step
    splash.close()
    ex = MainWindow()
    ex.show()
    app.exec()
