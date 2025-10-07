'''
Модуль построения графиков 
Импортирует результаты анализа из модуля main.py
Строит два типа графиков(столбчатую и круговую диаграммы)
Столбчатая диаграмма показывает показывает абсолютные штрафы по каждому пальцу
Круговая диограмма показывает процентное распределение нагрузки по пальцам 
'''
import sys  # модуль sys нужен для корректного завершения приложения (sys.exit)
import matplotlib
matplotlib.use("Qt5Agg")  # указываем Matplotlib использовать бэкенд Qt5Agg вместо TkAgg

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
# импортируем классы из PyQt5:
# QApplication — главный объект приложения
# QMainWindow — главное окно
# QPushButton — кнопка
# QVBoxLayout — вертикальный менеджер компоновки
# QWidget — базовый контейнер для виджетов

from matplotlib.figure import Figure  # класс Figure для создания графиков
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
# FigureCanvasQTAgg — холст, который позволяет встроить график Matplotlib в окно Qt

from main import KeyboardAnalyzer  # импортируем твой класс анализатора из main.py


class MatplotlibWindow(QMainWindow):  # создаём класс окна, наследуем от QMainWindow
    def __init__(self):
        super().__init__()  # инициализируем родительский класс
        self.setWindowTitle("Анализ раскладки клавиатуры")  # задаём заголовок окна

        # создаём центральный виджет и layout для размещения элементов
        central_widget = QWidget()
        self.setCentralWidget(central_widget)  # делаем его центральным в окне
        self.layout = QVBoxLayout(central_widget)  # вертикальный layout для кнопок и графиков

        # создаём кнопки
        self.btn_bar = QPushButton("Показать столбчатую диаграмму")  # кнопка для bar chart
        self.btn_pie = QPushButton("Показать круговую диаграмму")    # кнопка для pie chart
        self.layout.addWidget(self.btn_bar)  # добавляем кнопку в layout
        self.layout.addWidget(self.btn_pie)  # добавляем вторую кнопку в layout

        # холст для графика (изначально пустой)
        self.canvas = None

        # подключаем обработчики кнопок
        self.btn_bar.clicked.connect(self.show_bar_chart)  # при нажатии вызвать show_bar_chart
        self.btn_pie.clicked.connect(self.show_pie_chart)  # при нажатии вызвать show_pie_chart

    def clear_canvas(self):
        """Удаляет старый график перед отрисовкой нового"""
        if self.canvas:  # если холст уже есть
            self.layout.removeWidget(self.canvas)  # убираем его из layout
            self.canvas.setParent(None)  # отвязываем от родителя
            self.canvas = None  # обнуляем ссылку

    def show_bar_chart(self):
        """Строит столбчатую диаграмму"""
        analyzer = KeyboardAnalyzer()  # создаём объект анализатора
        results = analyzer.analyze()   # получаем результаты анализа
        penalties = results['finger_penalties']  # словарь штрафов по пальцам
        fingers = list(penalties.keys())   # список названий пальцев
        values = list(penalties.values())  # список значений штрафов

        fig = Figure(figsize=(8, 5))  # создаём фигуру Matplotlib
        ax = fig.add_subplot(111)     # добавляем ось
        ax.bar(fingers, values, color="skyblue")  # строим столбчатую диаграмму
        ax.set_title("Нагрузка на пальцы (столбчатая диаграмма)")  # заголовок
        ax.set_ylabel("Суммарный штраф")  # подпись оси Y
        ax.set_xlabel("Пальцы")           # подпись оси X
        ax.set_xticklabels(fingers, rotation=45, ha="right")  # поворот подписей

        self.clear_canvas()  # очищаем старый график
        self.canvas = FigureCanvasQTAgg(fig)  # создаём новый холст
        self.layout.addWidget(self.canvas)    # добавляем его в layout
        self.canvas.draw()  # отрисовываем график

    def show_pie_chart(self):
        """Строит круговую диаграмму"""
        analyzer = KeyboardAnalyzer()  # создаём объект анализатора
        results = analyzer.analyze()   # получаем результаты анализа
        penalties = results['finger_penalties']  # словарь штрафов
        fingers = list(penalties.keys())   # список пальцев
        values = list(penalties.values())  # список штрафов

        fig = Figure(figsize=(6, 6))  # создаём фигуру
        ax = fig.add_subplot(111)     # добавляем ось
        ax.pie(values, labels=fingers, autopct='%1.1f%%', startangle=90)  # круговая диаграмма
        ax.set_title("Распределение нагрузки по пальцам (круговая диаграмма)")  # заголовок

        self.clear_canvas()  # очищаем старый график
        self.canvas = FigureCanvasQTAgg(fig)  # создаём новый холст
        self.layout.addWidget(self.canvas)    # добавляем его в layout
        self.canvas.draw()  # отрисовываем график


if __name__ == "__main__":  # точка входа в программу
    app = QApplication(sys.argv)  # создаём объект приложения Qt
    window = MatplotlibWindow()   # создаём главное окно
    window.show()                 # показываем окно
    sys.exit(app.exec_())         # запускаем главный цикл приложения

