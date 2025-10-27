'''
Модуль построения графиков 
Импортирует результаты анализа из модуля main.py
Строит столбчатую диаграмму и таблицу с распределением нагрузки в % 
Столбчатая диаграмма показывает показывает абсолютные штрафы по каждому пальцу
'''
# Импорт системного модуля для работы с аргументами командной строки
import sys

# Импорт библиотеки matplotlib и установка backend для интеграции с PyQt5
import matplotlib
matplotlib.use("Qt5Agg")  # Используем Qt5Agg для отображения графиков в окне PyQt

# Импорт необходимых виджетов из PyQt5
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QLabel, QSizePolicy, QComboBox, QStackedWidget
)

# Импорт константы выравнивания
from PyQt5.QtCore import Qt

# Импорт объектов для построения графиков
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

# Импорт собственного анализатора и функции получения символов
from main import KeyboardAnalyzer, get_common_chars

# Глобальный словарь цветов для каждой раскладки
LAYOUT_COLORS = {
    'standard': '#00BFFF',   # голубой
    'challenge': '#000000',  # чёрный
    'zubachev': '#FF0000'    # красный
}

# Основной класс GUI приложения
class KeyboardGUI(QMainWindow):
    def __init__(self):
        super().__init__()  # Инициализация родительского класса
        self.setWindowTitle("Анализ раскладки клавиатуры")  # Заголовок окна
        self.resize(1200, 800)  # Размер окна

        # Список текстов для анализа
        self.filepaths = [
            "voina_i_mir.txt",
            "1grams.txt",
            "digramms.txt"
        ]

        # Получаем список часто используемых символов
        self.common_chars = get_common_chars()

        # Устанавливаем текущую раскладку по умолчанию
        self.current_layout = "standard"

        # Создаём экземпляр анализатора с выбранной раскладкой
        self.analyzer = KeyboardAnalyzer(layout=self.current_layout)

        # Анализируем все файлы
        self.results = self.analyzer.analyze_all_files(self.common_chars)

        # Создаём стек страниц для переключения между экранами
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Страница выбора и страница графика
        self.page_selection = QWidget()
        self.page_chart = QWidget()

        # Добавляем страницы в стек
        self.stack.addWidget(self.page_selection)
        self.stack.addWidget(self.page_chart)

        # Инициализируем интерфейс страницы выбора
        self.init_selection_page()

        # Инициализируем интерфейс страницы графика
        self.init_chart_page()

    # Метод инициализации страницы выбора
    def init_selection_page(self):
        layout = QGridLayout(self.page_selection)  # Сетка для размещения элементов
        layout.setContentsMargins(10, 10, 10, 10)  # Отступы
        layout.setSpacing(10)  # Расстояние между элементами

        layout.addWidget(QLabel("Выбор текста и раскладки:"), 0, 0, 1, 4)  # Заголовок

        layout.addWidget(QLabel("Раскладка:"), 1, 0)  # Метка для выпадающего списка
        self.layout_selector = QComboBox()  # Выпадающий список раскладок
        self.layout_selector.addItems(list(LAYOUT_COLORS.keys()))  # Добавляем раскладки
        self.layout_selector.currentTextChanged.connect(self.reload_analysis)  # Обновление анализа при смене
        layout.addWidget(self.layout_selector, 1, 1)  # Добавляем в сетку

        # Кнопки для отображения графиков по каждому тексту
        for i, path in enumerate(self.filepaths):
            btn_bar = QPushButton(f"График нагрузки: {path}")  # Кнопка для графика
            btn_bar.clicked.connect(lambda _, idx=i: self.show_bar_chart(idx))  # Обработчик клика
            layout.addWidget(btn_bar, i + 2, 0, 1, 2)  # Добавляем кнопку в сетку

        layout.addWidget(QLabel("Сравнение раскладок по текстам:"), len(self.filepaths) + 3, 0, 1, 4)  # Заголовок

        # Кнопки для сравнения раскладок по каждому тексту
        for i, path in enumerate(self.filepaths):
            btn_compare = QPushButton(f"Сравнение раскладок: {path}")  # Кнопка сравнения
            btn_compare.clicked.connect(lambda _, idx=i: self.compare_layouts_for_file(idx))  # Обработчик
            layout.addWidget(btn_compare, len(self.filepaths) + 4 + i, 0, 1, 2)  # Добавляем в сетку

    # Метод инициализации страницы графика
    def init_chart_page(self):
        self.chart_layout = QVBoxLayout(self.page_chart)  # Вертикальный layout
        self.chart_layout.setContentsMargins(10, 10, 10, 10)  # Отступы
        self.chart_layout.setSpacing(10)  # Интервалы

        self.btn_back_to_selection = QPushButton("Вернуться к выбору")  # Кнопка возврата
        self.btn_back_to_selection.clicked.connect(self.back_to_selection)  # Обработчик
        self.chart_layout.addWidget(self.btn_back_to_selection, alignment=Qt.AlignCenter)  # Добавляем кнопку

        self.canvas = None  # Полотно для графика

    # Метод обновления анализа при смене раскладки
    def reload_analysis(self, layout_name):
        self.current_layout = layout_name  # Обновляем текущую раскладку
        self.analyzer = KeyboardAnalyzer(layout=layout_name)  # Новый анализатор
        self.results = self.analyzer.analyze_all_files(self.common_chars)  # Перезапускаем анализ

    # Метод очистки текущего графика
    def clear_canvas(self):
        if self.canvas:
            self.chart_layout.removeWidget(self.canvas)  # Удаляем из layout
            self.canvas.setParent(None)  # Отключаем от родителя
            self.canvas = None  # Обнуляем

    # Метод возврата к странице выбора
    def back_to_selection(self):
        self.clear_canvas()  # Очищаем график
        self.stack.setCurrentWidget(self.page_selection)  # Переключаем страницу

    # Метод отображения графика нагрузки на пальцы
    def show_bar_chart(self, index):
        result = self.results[index]  # Получаем результат анализа
        penalties = result['finger_penalties']  # Штрафы по пальцам
        total = sum(penalties.values())  # Общий штраф

        # Сортировка по процентной нагрузке
        sorted_items = sorted(
            [(finger, value, value / total * 100) for finger, value in penalties.items()],
            key=lambda x: x[2],
            reverse=True
        )

        fingers = [item[0] for item in sorted_items]  # Список пальцев
        values = [item[1] for item in sorted_items]  # Список штрафов


        fig = Figure(figsize=(16, 10))  # Создаём фигуру
        ax_bar = fig.add_axes([0.05, 0.2, 0.70, 0.60])  # Область графика
        ax_table = fig.add_axes([0.80, 0.2, 0.15, 0.6])  # Область таблицы

        color = LAYOUT_COLORS.get(self.current_layout, "#00BFFF")  # Цвет текущей раскладки
        bars = ax_bar.bar(fingers, values, color=color)  # Столбчатый график

        ax_bar.set_title(f"Нагрузка на пальцы — {self.filepaths[index]} ({self.current_layout})", fontsize=16)
        ax_bar.set_ylabel("Суммарный штраф", fontsize=14)
        ax_bar.set_xlabel("Пальцы", fontsize=14)
        ax_bar.set_xticklabels(fingers, rotation=45, ha="right")
        ax_bar.grid(True, linestyle='--', alpha=0.5)

        for bar, value in zip(bars, values):  # Подписи над столбцами
            ax_bar.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 1,
                f"{value:.0f}",
                ha='center',
                fontsize=12,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.6)
            )

        ax_bar.bar([0], [0], color=color, label=self.current_layout)  # Пустой элемент для легенды
        ax_bar.legend(title="Раскладка", loc="upper right", fontsize=12, title_fontsize=13)  # Легенда

        ax_table.axis("off")  # Отключаем оси у таблицы

        # Формируем данные для таблицы: палец и его процентная нагрузка
        table_data = [[f"  {f}  ", f"  {p:.1f} %  "] for f, _, p in sorted_items]

        # Создаём таблицу с подписями
        table = ax_table.table(
            cellText=table_data,  # Содержимое ячеек
            colLabels=["Палец", "Нагрузкa"],  # Заголовки столбцов
            cellLoc="left",  # Выравнивание текста в ячейках
            loc="center"  # Положение таблицы
        )
        table.auto_set_font_size(False)  # Отключаем авторазмер шрифта
        table.set_fontsize(11)  # Устанавливаем размер шрифта
        table.scale(1.4, 1.5)  # Масштабируем таблицу

        fig.tight_layout()  # Автоматически подгоняем размеры элементов

        self.clear_canvas()  # Удаляем старый график, если был
        self.canvas = FigureCanvasQTAgg(fig)  # Создаём холст для matplotlib
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Растягиваем по размеру
        self.chart_layout.addWidget(self.canvas)  # Добавляем холст в layout
        self.canvas.draw()  # Отрисовываем график
        self.stack.setCurrentWidget(self.page_chart)  # Переключаемся на страницу графика

    def compare_layouts_for_file(self, index):
        layout_codes = list(LAYOUT_COLORS.keys())

        all_data = []
        for layout in layout_codes:
            analyzer = KeyboardAnalyzer(layout=layout)
            results = analyzer.analyze_all_files(self.common_chars)
            result = results[index]
            all_data.append((layout, result['total_penalty']))

        total = sum([x[1] for x in all_data])
        sorted_data = sorted(all_data, key=lambda x: x[1], reverse=True)

        layouts = [x[0] for x in sorted_data]
        penalties = [x[1] for x in sorted_data]
        percentages = [v / total * 100 for v in penalties]
        colors = [LAYOUT_COLORS[layout] for layout in layouts]

        fig = Figure(figsize=(12, 8))
        ax_bar = fig.add_axes([0.05, 0.2, 0.70, 0.6])
        ax_table = fig.add_axes([0.80, 0.2, 0.15, 0.6])

        bars = ax_bar.bar(layouts, penalties, color=colors)
        ax_bar.set_title(f"Сравнение раскладок — {self.filepaths[index]}", fontsize=16)
        ax_bar.set_ylabel("Общий штраф", fontsize=14)
        ax_bar.set_xlabel("Раскладка", fontsize=14)
        ax_bar.grid(True, linestyle='--', alpha=0.5)

        for bar, value in zip(bars, penalties):
            ax_bar.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 1,
                f"{value:.0f}",
                ha='center',
                fontsize=12,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.6)
            )

        # Легенда по всем раскладкам
        for layout in layout_codes:
            ax_bar.bar([0], [0], color=LAYOUT_COLORS[layout], label=layout)
        ax_bar.legend(title="Раскладки", loc="upper right", fontsize=12, title_fontsize=13)

        ax_table.axis("off")
        table_data = [[f"  {layout}  ", f"  {percent:.1f} %  "] for layout, percent in zip(layouts, percentages)]
        table = ax_table.table(
            cellText=table_data,
            colLabels=["Раскладка", "Нагрузка"],
            cellLoc="left",
            loc="center"
        )
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1.4, 1.5)

        fig.tight_layout()
        self.clear_canvas()
        self.canvas = FigureCanvasQTAgg(fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.chart_layout.addWidget(self.canvas)
        self.canvas.draw()
        self.stack.setCurrentWidget(self.page_chart)


# Точка входа в приложение
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Создаём экземпляр приложения
    window = KeyboardGUI()  # Создаём главное окно
    window.show()  # Показываем окно пользователю
    sys.exit(app.exec_())  # Запускаем главный цикл приложения





