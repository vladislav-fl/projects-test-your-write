"""

    TODO:
        1. Добавить вывод скорости за секунду
        2. Изменить и улучшить алгоритм нахождения скорости печатания за минуту

"""



# PyQt6 imports
from PyQt6.QtCore import QSize, Qt, QTimer, QTime
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QTextEdit, QLineEdit, QVBoxLayout, QWidget

# Folder imports:
from constants import Text, Interface

# Another imports
import sys
import os
import datetime
import random

class Objects:
    pass


class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=None)

        self.setWindowTitle('Test Your Write')
        self.setFixedSize(QSize(1000, 500))
        # self.setMaximumSize()
        # self.setMinimumSize()

        self.test_object = QLabel('test')

        # Сделать вместо словаря отдельный класс
        self.objects: dict = {
            'LAYOUT': QVBoxLayout(),
            'CONTAINER': QWidget(),

            'LABEL0': QLabel('Здесь будет создан новый текст'),
            'LABEL1': QLabel('Прошло времени: 0 сек.'),
            'LABEL2': QLabel('Напечатано: 0 символов'),
            'LABEL3': QLabel('Осталось: ? символов'),
            'LABEL4': QLabel('Текущая скорость: ? символов в минуту'),
            'PUSHBUTTON0': QPushButton('Button0'),
            'PUSHBUTTON1': QPushButton('Сгенерировать новый текст'),
            'TEXTEDIT0': QTextEdit()
        }
        # Различные настройки элементов:
        self.objects['TEXTEDIT0'].setReadOnly(True)

        # Добавление всех элементов в лэйаут:
        self.objects['LAYOUT'].addWidget(self.objects['LABEL0'])
        self.objects['LAYOUT'].addWidget(self.objects['TEXTEDIT0'])
        self.objects['LAYOUT'].addWidget(self.objects['LABEL1'])
        self.objects['LAYOUT'].addWidget(self.objects['LABEL2'])
        self.objects['LAYOUT'].addWidget(self.objects['LABEL3'])
        self.objects['LAYOUT'].addWidget(self.objects['LABEL4'])
        self.objects['LAYOUT'].addWidget(self.objects['PUSHBUTTON0'])
        self.objects['LAYOUT'].addWidget(self.objects['PUSHBUTTON1'])

        # Добавление лэйаута в контейнер:
        self.objects['CONTAINER'].setLayout(self.objects['LAYOUT'])
        
        # Центрирование контейнера:
        self.setCentralWidget(self.objects['CONTAINER'])
        
        # Связывание объектов и функций:
        self.objects['PUSHBUTTON0'].clicked.connect(self.clicked_b0)
        self.objects['PUSHBUTTON1'].clicked.connect(self.clicked_b1)
        self.objects['TEXTEDIT0'].textChanged.connect(self.write_te0)

        # Отображение всех объектов на экране:
        self.objects['LABEL0'].show()
        self.objects['LABEL1'].show()
        self.objects['LABEL2'].show()
        self.objects['LABEL3'].show()
        self.objects['LABEL4'].show()
        self.objects['PUSHBUTTON0'].show()
        self.objects['PUSHBUTTON1'].show()
        self.objects['TEXTEDIT0'].show()

        # Создание таймера:
        self.timer_info = QTimer(self)
        self.timer_info.setInterval(1000)
        self.timer_info.timeout.connect(self.timer_timeout)

    def timer_timeout(self, ):
        # Работа с таймером и некоторыми данными:

        # !!! Добавить массив всех прошлых значений скорость и работать с ним, а не только с одной предыдущей скоростью:
        Interface.timer += 1
        try:
            if Interface.timer == 1:
                Interface.print_speed = Interface.symbols_per_second * 60
            else:
                _all_last_print_speeds = 0
                _all_last_print_speeds_count = 0
                for element in Interface.last_print_speeds:
                    _all_last_print_speeds += element
                    _all_last_print_speeds_count += 1
                Interface.print_speed = int((Interface.symbols_per_second * 60 + _all_last_print_speeds) / (_all_last_print_speeds_count + 1))
                del _all_last_print_speeds
                del _all_last_print_speeds_count
        except ZeroDivisionError as error:
            # Ожидаем первого ввода, иначе счетчик обнуляется:
            # ДОБАВИТЬ ОЖИДАНИЕ ПЕРВОГО ВВОДА
            Interface.timer = 0
            with open('logs.txt', 'a') as file:
                file.write(f'[ERROR]:[{str(datetime.datetime.now())[:-7]}] - timer | {error}\n')
        if Interface.symbols_per_second == 0:
            Interface.last_print_speeds.append(0)
        else:
            Interface.last_print_speeds.append(Interface.print_speed)
        Interface.symbols_per_second = 0

        # Обновление объектов QLabel:
        self.objects['LABEL1'].setText(f'Прошло времени: {Interface.timer} сек.')
        self.objects['LABEL4'].setText(f'Текущая скорость: {Interface.print_speed} символов в минуту')

    def clicked_b0(self, ):
        # os.system('echo b0 clicked')
        with open('logs.txt', 'a') as file:
            file.write(f'[INFO]:[{str(datetime.datetime.now())[:-7]}] - b0 | \n')

    def clicked_b1(self, ):
        # Генерация нового текста:
        with open('logs.txt', 'a') as file:
            file.write(f'[INFO]:[{str(datetime.datetime.now())[:-7]}] - b1 | generating new text...\n')
        
        _random_text_id: int = random.randint(0, len(Text.text) - 1)

        # Запуск таймера и обновление данных:
        self.objects['LABEL1'].setText(f'Прошло времени: 0 сек.')
        Interface.timer = 0
        Interface.symbols_done = 0
        Interface.symbols_left = len(Text.text[_random_text_id])
        Interface.print_speed = 0
        Interface.last_print_speeds = []
        Interface.symbols_per_second = 0
        self.timer_info.start()

        # Обновление данных в объектах QLabel:
        self.objects['LABEL0'].setText(Text.text[_random_text_id])
        self.objects['LABEL0'].setWordWrap(True)
        self.objects['LABEL2'].setText(f'Напечатано: 0 символов')
        self.objects['LABEL3'].setText(f'Осталось: {Interface.symbols_left} символов')
        # self.objects['LABEL0'].setStyleSheet('font-size: 15px;')

        # Обновление данных в классе Text:
        Text.current_text_id = _random_text_id
        Text.current_symbol = 0

        # Обновление данных в объекте QTextEdit:
        self.objects['TEXTEDIT0'].setReadOnly(False)
        self.objects['TEXTEDIT0'].setText('')

        del _random_text_id

    def write_te0(self, ):
        # Возможно вместо всей строки после удачного ввода удалять прошлый символ:
        try:
            _: list = Text.check_symbol(self.objects['TEXTEDIT0'].toPlainText()[-1])
            self.objects['LABEL0'].setText(_[1])
            if _[0]:
                Interface.symbols_done += 1
                Interface.symbols_left -= 1
                Interface.symbols_per_second += 1

                self.objects['LABEL2'].setText(f'Напечатано: {Interface.symbols_done} символов')
                self.objects['LABEL3'].setText(f'Осталось: {Interface.symbols_left} символов')

                # self.objects['LABEL0'].setStyleSheet('background-color: #45c44d;')
                with open('logs.txt', 'a') as file:
                    file.write(f'[INFO]:[{str(datetime.datetime.now())[:-7]}] - te0 | successful typing\n')
                self.objects['TEXTEDIT0'].setText('')
            else:
                # self.objects['LABEL0'].setStyleSheet('background-color: #801818;')
                with open('logs.txt', 'a') as file:
                    file.write(f'[INFO]:[{str(datetime.datetime.now())[:-7]}] - te0 | unsuccessful typing\n')
        except IndexError as error:
            with open('logs.txt', 'a') as file:
                    file.write(f'[ERROR]:[{str(datetime.datetime.now())[:-7]}] - te0 | {error}\n')



def start():
    app = QApplication(sys.argv)
    # app.setFont(QFont("Times", 12, QFont.Bold))

    window = MainWindow()
    window.show()

    app.exec()

if __name__ == '__main__':
    start()

