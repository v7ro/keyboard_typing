'''
Модуль построения графиков 
Импортирует результаты анализа из модуля main.py
Строит столбчатую диаграмму и таблицу с распределением нагрузки в % 
Столбчатая диаграмма показывает показывает абсолютные штрафы по каждому пальцу
'''
import sys
import matplotlib
matplotlib.use("Qt5Agg")

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from main import KeyboardAnalyzer, get_common_chars

LAYOUTS = {
    'ytsuken': '#FF0000',     # красный
    'vyzov': '#000000',       # черный
    'diktor': '#FFD700',      # желтый
    'rusfon': '#FF69B4',      # розовый
    'ant': '#00BFFF',         # голубой
    'zubachev': '#800080',    # фиолетовый
    'skoropis': '#228B22'     # зеленый
}

LAYOUT_NAMES = {
    'ytsuken': 'Йцукен',
    'vyzov': 'Вызов',
    'diktor': 'Диктор',
    'rusfon': 'Фонетическая',
    'ant': 'Ант',
    'zubachev': 'Зубачев',
    'skoropis': 'Скоропись'
}

FINGERS = [
    'left_pinky', 'left_ring', 'left_middle', 'left_index',
    'right_index', 'right_middle', 'right_ring', 'right_pinky', 'right_thumb'
]
"""
Графический интерфейс для визуального сравнения раскладок клавиатуры.

Интерфейс отображает:
- диаграмму нагрузки на пальцы,
- круговую диаграмму распределения по рукам,
- сводную таблицу с общей статистикой.

Используется для анализа эргономики раскладок на основе текстов и метрик нагрузки.
"""
class KeyboardComparisonGUI(QMainWindow):
    """
    Инициализирует главное окно приложения и добавляет вкладки с визуализациями.

    - Устанавливает заголовок окна и размеры.
    - Создаёт QTabWidget с тремя вкладками:
    - «Нагрузка на пальцы» — отображает столбчатую диаграмму по пальцам.
    - «Нагрузка на руки» — отображает круговую диаграмму по рукам.
    - «Сводная нагрузка» — отображает таблицу со статистикой по раскладкам.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Сравнение раскладок — нагрузка на пальцы и руки")
        self.resize(1600, 900)

        tabs = QTabWidget()
        tabs.addTab(self.create_finger_chart_tab(), "Нагрузка на пальцы")
        tabs.addTab(self.create_hand_pie_tab(), "Нагрузка на руки")
        tabs.addTab(self.create_summary_tab(), "Сводная нагрузка")

        self.setCentralWidget(tabs)
    """
    Создаёт вкладку с горизонтальной диаграммой нагрузки на пальцы для всех раскладок.

    Метод:
    - Загружает общие символы для анализа (`get_common_chars()`).
    - Для каждой раскладки (`LAYOUTS`) анализирует три текста и суммирует количество нажатий по пальцам.
    - Строит горизонтальные столбцы для каждой раскладки, с цветовой дифференциацией.
    - Добавляет числовые подписи к каждому столбцу.
    - Настраивает оси, сетку, легенду и заголовок графика.

    return: QWidget с встроенным графиком matplotlib, готовым для отображения во вкладке GUI.
    """
    def create_finger_chart_tab(self):
        fig = Figure(figsize=(12, 8))
        fig.subplots_adjust(left=0.12, right=0.94, top=0.92, bottom=0.08)
        ax = fig.add_subplot(111)

        common_chars = get_common_chars()
        layout_totals = {}

        for layout_code in LAYOUTS:
            analyzer = KeyboardAnalyzer(layout=layout_code)
            results = analyzer.analyze_all_files(common_chars)

            total_counts = {finger: 0 for finger in FINGERS}
            for result in results:
                for finger in FINGERS:
                    total_counts[finger] += result['finger_counts'].get(finger, 0)

            layout_totals[layout_code] = [total_counts[f] for f in FINGERS]

        total_layouts = len(LAYOUTS)
        bar_height = 1 / (total_layouts + 1)

        for i, (layout_code, color) in enumerate(LAYOUTS.items()):
            y_offsets = [y + i * bar_height for y in range(len(FINGERS))]
            values = layout_totals[layout_code]

            bars = ax.barh(
                y_offsets,
                values,
                height=bar_height * 0.9,
                color=color,
                label=LAYOUT_NAMES.get(layout_code, layout_code)
            )

            for bar, value in zip(bars, values):
                ax.text(
                    bar.get_width() + max(5, value * 0.01),
                    bar.get_y() + bar.get_height() / 2,
                    f"{value:.0f}",
                    va='center',
                    ha='left',
                    fontsize=9,
                    color='black',
                    bbox=dict(facecolor='white', alpha=0.6, boxstyle='round,pad=0.2', edgecolor='none')
                )

        ax.set_yticks([y + bar_height * (total_layouts / 2) for y in range(len(FINGERS))])
        ax.set_yticklabels(FINGERS, fontsize=12)
        ax.set_xlabel("Количество нажатий", fontsize=14)
        ax.set_title("Сравнение нагрузок на пальцы во всех раскладках", fontsize=16)
        ax.grid(True, axis='x', linestyle='--', alpha=0.5)
        ax.legend(title="Раскладка", loc="lower right", fontsize=12, title_fontsize=13)

        canvas = FigureCanvasQTAgg(fig)
        layout = QVBoxLayout()
        layout.addWidget(canvas)

        container = QWidget()
        container.setLayout(layout)
        return container
    """
    Создаёт вкладку с круговыми диаграммами распределения нагрузки между руками для каждой раскладки.

    Метод:
    - Загружает общие символы (`get_common_chars()`).
    - Для каждой раскладки из `LAYOUTS` анализирует три текста и суммирует количество нажатий левой и правой рукой.
    - Строит круговую диаграмму (pie chart) с двумя секторами: «Левая» и «Правая».
    - Настраивает подписи, цвета, заголовки и визуальные параметры диаграмм.
    - Размещает диаграммы в сетке (по 3 на строку) внутри одного matplotlib-фигурного холста.

    return: QWidget с визуализацией, готовой для отображения во вкладке GUI.
    """
    def create_hand_pie_tab(self):
        fig = Figure(figsize=(16, 9))
        fig.subplots_adjust(hspace=0.4)
        layout_codes = list(LAYOUTS.keys())
        rows = (len(layout_codes) + 2) // 3

        for i, layout_code in enumerate(layout_codes):
            analyzer = KeyboardAnalyzer(layout=layout_code)
            results = analyzer.analyze_all_files(get_common_chars())

            left_total = sum(r['left_hand_count'] for r in results)
            right_total = sum(r['right_hand_count'] for r in results)

            ax = fig.add_subplot(rows, 3, i + 1)
            wedges, texts, autotexts = ax.pie(
                [left_total, right_total],
                labels=['Левая', 'Правая'],
                colors=['#00BFFF', '#FF0000'],
                startangle=90,
                autopct='%1.0f%%',
                wedgeprops=dict(width=0.4)
            )
            for autotext in autotexts:
                autotext.set_bbox(dict(facecolor='white', alpha=0.6, boxstyle='round,pad=0.2', edgecolor='none'))
            ax.set_title(LAYOUT_NAMES.get(layout_code, layout_code), fontsize=13)

        canvas = FigureCanvasQTAgg(fig)
        layout = QVBoxLayout()
        layout.addWidget(canvas)

        container = QWidget()
        container.setLayout(layout)
        return container
    """
    Создаёт вкладку со сводной визуализацией нагрузки по пальцам и раскладкам.

    Метод:
    - Загружает общий набор символов (`get_common_chars()`).
    - Для каждой раскладки из `LAYOUTS` анализирует три текста и суммирует:
      - общее количество нажатий по каждому пальцу,
      - общее количество нажатий по каждой раскладке.
    - Строит две круговые диаграммы:
      - слева: распределение нагрузки по пальцам (все раскладки и тексты),
      - справа: распределение нагрузки по раскладкам (все тексты).
    - Настраивает подписи, цвета, заголовки и визуальные параметры диаграмм.

    return: QWidget с двумя круговыми диаграммами, готовый для отображения во вкладке GUI.
    """
    def create_summary_tab(self):
        fig = Figure(figsize=(16, 9))
        fig.subplots_adjust(hspace=0.3, wspace=0.3)

        common_chars = get_common_chars()
        total_finger_counts = {finger: 0 for finger in FINGERS}
        layout_press_totals = {}

        for layout_code in LAYOUTS:
            analyzer = KeyboardAnalyzer(layout=layout_code)
            results = analyzer.analyze_all_files(common_chars)

            layout_total = 0
            for result in results:
                layout_total += sum(result['finger_counts'].values())
                for finger in FINGERS:
                    total_finger_counts[finger] += result['finger_counts'].get(finger, 0)

            layout_press_totals[layout_code] = layout_total

        # Круговая диаграмма по пальцам
        ax1 = fig.add_subplot(121)
        finger_labels = [f.replace('_', ' ').title() for f in FINGERS]
        finger_values = [total_finger_counts[f] for f in FINGERS]

        wedges1, texts1, autotexts1 = ax1.pie(
            finger_values,
            labels=finger_labels,
            autopct='%1.0f%%',
            startangle=90,
            wedgeprops=dict(width=0.4)
        )
        for autotext in autotexts1:
            autotext.set_bbox(dict(facecolor='white', alpha=0.6, boxstyle='round,pad=0.2', edgecolor='none'))
        ax1.set_title("Нагрузка по пальцам (все раскладки и тексты)", fontsize=13)

        # Круговая диаграмма по раскладкам
        ax2 = fig.add_subplot(122)
        layout_labels = [LAYOUT_NAMES.get(code, code) for code in LAYOUTS]
        layout_values = [layout_press_totals[code] for code in LAYOUTS]
        layout_colors = [LAYOUTS[code] for code in LAYOUTS]

        wedges2, texts2, autotexts2 = ax2.pie(
            layout_values,
            labels=layout_labels,
            colors=layout_colors,
            autopct='%1.0f%%',
            startangle=90,
            wedgeprops=dict(width=0.4)
        )
        for autotext in autotexts2:
            autotext.set_bbox(dict(facecolor='white', alpha=0.6, boxstyle='round,pad=0.2', edgecolor='none'))
        ax2.set_title("Нагрузка по раскладкам (все тексты)", fontsize=13)

        canvas = FigureCanvasQTAgg(fig)
        layout = QVBoxLayout()
        layout.addWidget(canvas)

        container = QWidget()
        container.setLayout(layout)
        return container
"""
Точка входа в приложение.

- Создаёт экземпляр QApplication.
- Инициализирует главное окно `KeyboardComparisonGUI`.
- Отображает окно и запускает главный цикл событий Qt.
"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KeyboardComparisonGUI()
    window.show()
    sys.exit(app.exec_())








