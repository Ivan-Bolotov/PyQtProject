import copy

from PIL import ImageFont

from src.resource_path import resource_path
from src.constants import *
from src.Components.componentWithFillingOfBlanks import ComponentWithFillingOfBlanks

from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QRadioButton, QWidget, QPushButton, QFileDialog
from PyQt6.QtGui import QPixmap, QImage


class MainScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.saved_im_with_rows = None  # изображение со строчками
        self.cross = None  # картинка креста
        self.saved_image = None  # начальное изображение с крестом
        self.component_with_filling = None  # компонент для ввода имён
        self.saved_im_with_label = None  # изображение с заголовком
        self.text = None  # заголовок на изображении
        self.im = None  # изображение с заголовком
        self.slider_value = None  # кол-во строк
        self.my_font = None  # шрифт изображения
        uic.loadUi(resource_path("src/Screens/MainScreen.ui"), self)
        self.initUI()

    def initUI(self):
        self.r_b_format_1.setChecked(True)
        self.r_b_type_1.setChecked(True)
        self.r_b_fill_1.setChecked(True)
        self.my_font = ImageFont.truetype(resource_path("resources/Fonts/Futura_PT.ttf"), 14)
        self.generate_base_image_with_cross()
        self.generate_image_with_cross_and_label()
        self.generate_image_with_cross_and_rows()
        self.slider_value = int(self.horizontalSlider.value())
        self.change_amount_of_rows("init")
        self.commitButton.clicked.connect(self.save_image)
        self.buttonGroupFormat.buttonClicked.connect(self.radio_button_format)
        self.buttonGroupType.buttonClicked.connect(self.radio_button_type)
        self.buttonGroupFilling.buttonClicked.connect(self.radio_button_filling)
        self.horizontalSlider.valueChanged.connect(self.slider_value_changed)

    @staticmethod
    def radio_button_format(btn: QRadioButton):
        print(btn.text())

    def radio_button_type(self, btn: QRadioButton):
        """Изменение заголовка записки."""
        self.im = copy.copy(self.saved_image)
        self.text = btn.text()[0] + btn.text().lower()[1:]
        if not self.text == "Универсальная":
            draw = ImageDraw.Draw(self.im)
            draw.text((52, 28), self.text, BLACK_RGB, font=self.my_font)
        self.saved_im_with_label = copy.copy(self.im)
        self.change_amount_of_rows("r_b_type_changed")

    def radio_button_filling(self, btn: QRadioButton):
        if self.component_with_filling is None:
            self.component_with_filling = ComponentWithFillingOfBlanks(self, self.slider_value)
            self.verticalLayout.addWidget(self.component_with_filling)
            self.component_with_filling.hide()

        if btn.text() == "Пустые":
            self.component_with_filling.hide()
        else:
            self.component_with_filling.show()

    def slider_value_changed(self):
        self.slider_value = int(self.horizontalSlider.value())
        self.change_amount_of_rows("slider_changed")
        if self.component_with_filling is not None:
            self.component_with_filling.change_amount_of_inputs(self.slider_value)

    def generate_base_image_with_cross(self):
        self.saved_image = Image.new("RGBA", (180, 300), WHITE_RGB)
        if self.cross is None:
            self.cross = self.generate_cross_image()
            self.cross = self.cross.resize((20, 30))

        x0, y0 = 80, 4
        self.saved_image.paste(self.cross, (x0, y0, x0 + self.cross.width, y0 + self.cross.height))

    def generate_image_with_cross_and_label(self):
        self.saved_im_with_label = copy.copy(self.saved_image)
        if self.text is None:
            btn = self.buttonGroupType.checkedButton()
            self.text = btn.text()[0] + btn.text().lower()[1:]

        draw = ImageDraw.Draw(self.saved_im_with_label)
        draw.text((52, 28), self.text, BLACK_RGB, font=self.my_font)

    def generate_image_with_cross_and_rows(self):
        self.saved_im_with_rows = copy.copy(self.saved_image)
        arr = self.saved_im_with_rows.load()
        sl_val = int(self.horizontalSlider.value())
        working_space = self.saved_im_with_rows.height - self.saved_im_with_rows.height * 5 // 20
        # 15/20 (75%) от полной высоты картинки
        for i in range(self.saved_im_with_rows.height * 4 // 20,
                       self.saved_im_with_rows.height * 19 // 20,
                       working_space // sl_val):
            for j in range(self.saved_im_with_rows.width // 10,
                           self.saved_im_with_rows.width - self.saved_im_with_rows.width // 10):
                arr[j, i] = BLACK_RGBA

    def render_names(self, component_with_filling: QWidget):
        """Отображение введённых имён."""
        sl_val = self.slider_value
        self.im = copy.copy(self.saved_im_with_label)
        arr = self.im.load()
        working_space = self.im.height - self.im.height * 5 // 20  # 15/20 (75%) от полной высоты картинки

        step = working_space // sl_val
        c = self.im.height * 4 // 20
        for i in range(sl_val):
            for j in range(self.im.width // 10, self.im.width - self.im.width // 10):
                arr[j, c] = BLACK_RGBA
            text = component_with_filling.list_of_inputs[i].text()
            draw = ImageDraw.Draw(self.im)
            draw.text((20, c - self.my_font.size - 2), text, BLACK_RGB, font=self.my_font)

            c += step
        self.show_pix_map()

    def change_amount_of_rows(self, from__):
        """Изменяет кол-во строк."""
        sl_val = self.slider_value
        match from__:
            case "init":
                self.im = copy.copy(self.saved_im_with_label)
                arr = self.im.load()
                working_space = self.im.height - self.im.height * 5 // 20  # 15/20 (75%) от полной высоты картинки

                step = working_space // sl_val
                c = self.im.height * 4 // 20
                for _ in range(sl_val):
                    for j in range(self.im.width // 10, self.im.width - self.im.width // 10):
                        arr[j, c] = BLACK_RGBA
                    c += step

            case "slider_changed":
                self.saved_im_with_rows = copy.copy(self.saved_image)
                arr = self.saved_im_with_rows.load()
                working_space = self.saved_im_with_rows.height - self.saved_im_with_rows.height * 5 // 20
                # 15/20 (75%) от полной высоты картинки

                step = working_space // sl_val
                c = self.saved_im_with_rows.height * 4 // 20
                for _ in range(sl_val):
                    for j in range(self.saved_im_with_rows.width // 10, self.saved_im_with_rows.width * 9 // 10):
                        arr[j, c] = BLACK_RGBA
                    c += step
                self.im = copy.copy(self.saved_im_with_label)
                arr = self.im.load()
                working_space = self.im.height - self.im.height * 5 // 20  # 15/20 (75%) от полной высоты картинки

                step = working_space // sl_val
                c = self.im.height * 4 // 20
                for _ in range(sl_val):
                    for j in range(self.im.width // 10, self.im.width - self.im.width // 10):
                        arr[j, c] = BLACK_RGBA
                    c += step

            case "r_b_type_changed":
                arr = self.im.load()
                working_space = self.im.height - self.im.height * 5 // 20  # 15/20 (75%) от полной высоты картинки

                step = working_space // sl_val
                c = self.im.height * 4 // 20
                for _ in range(sl_val):
                    for j in range(self.im.width // 10, self.im.width - self.im.width // 10):
                        arr[j, c] = BLACK_RGBA
                    c += step

        self.show_pix_map()

    def show_pix_map(self):
        """Отображение текущей записки"""
        image = QImage(ImageQt(self.im))
        pixmap = QPixmap.fromImage(image).scaled(200, 400)
        self.label.setPixmap(pixmap)

    def save_image(self, btn: QPushButton):
        path, t = QFileDialog.getSaveFileName(self, "Сохранить записку", "", "PNG File (*.png)")
        self.im.save(path, "PNG")

    @staticmethod
    def generate_cross_image() -> Image.Image:
        cross = Image.new("RGBA", (20, 40), WHITE_RGB)
        arr = cross.load()
        for i in range(cross.height):
            for j in range(cross.width):
                if 8 <= j <= 10 or 11 <= i <= 13:
                    arr[j, i] = BLACK_RGBA  # крест по центру изображения
                if 4 <= i <= 6 and 5 <= j <= 14:
                    arr[j, i] = BLACK_RGBA  # маленькая перекладина вверху изображения
                draw = ImageDraw.Draw(cross)
                draw.line((3, 20, 15, 30), fill=BLACK_RGB, width=3)  # нижняя перекладина
        return cross
