from src.Dialogs.dialogWithNames import DialogWithNames
from src.resource_path import resource_path

from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit


class ComponentWithFillingOfBlanks(QWidget):
    def __init__(self, parent: QWidget, amount_of_inputs: int):
        super().__init__(parent=parent)
        self.par = self.parent()  # родительский компонент
        self.list_of_inputs = None  # поля ввода данных
        uic.loadUi(resource_path("src/Components/componentWithFillingOfBlanks.ui"), self)
        self.amount_of_inputs = amount_of_inputs  # кол-во полей для ввода
        self.initUI()

    def initUI(self):
        self.radio_button_new_or_not(self.buttonGroupNewOrNot.checkedButton())
        self.buttonGroupNewOrNot.buttonClicked.connect(self.radio_button_new_or_not)

    def radio_button_new_or_not(self, btn: QPushButton):
        if self.list_of_inputs is None:
            self.list_of_inputs = []
            for i in range(self.amount_of_inputs):
                inp = QLineEdit()
                self.list_of_inputs.append(inp)
                self.verticalLayout.addWidget(inp)
        if btn.text() == "Новую записку":
            for i in self.list_of_inputs:
                i.show()
            dialog = DialogWithNames()
            dialog.exec()
            if dialog.res:
                c = 0
                for i in self.list_of_inputs:
                    if c >= len(dialog.data):
                        break
                    i.setText(dialog.data[c])
                    c += 1
            self.par.render_names(self)
        else:
            for i in self.list_of_inputs:
                i.hide()

    def change_amount_of_inputs(self, val: int):
        if val > self.amount_of_inputs:
            for _ in range(val - self.amount_of_inputs):
                inp = QLineEdit()
                self.list_of_inputs.append(inp)
                self.verticalLayout.addWidget(inp)
        else:
            self.list_of_inputs = self.list_of_inputs[:val]
            for i in range(val - 1, self.amount_of_inputs - 1):
                self.verticalLayout.itemAt(i).widget().deleteLater()
        self.amount_of_inputs = val
