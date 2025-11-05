'''
Модуль построения графиков 
Импортирует результаты анализа из модуля main.py
Строит столбчатую диаграмму и таблицу с распределением нагрузки в % 
Столбчатая диаграмма показывает показывает абсолютные штрафы по каждому пальцу
'''
import sys
import matplotlib
matplotlib.use("Qt5Agg")

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from main import KeyboardAnalyzer, get_common_chars

# Цвета раскладок
LAYOUTS = {
    'ytsuken': '#FF0000',
    'vyzov': '#000000',
    'diktor': '#FFD700',
    'rusfon': '#FF69B4',
    'ant': '#00BFFF',
    'zubachev': '#800080',
    'skoropis': '#228B22'
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

class FingerComparisonChart(QMainWindow):
    def __init__(self, all_results):
        super().__init__()
        self.setWindowTitle("Нагрузка на пальцы по раскладкам")
        self.resize(1600, 900)

        fig = Figure(figsize=(18, 10))
        fig.subplots_adjust(left=0.25, right=0.95, top=0.95, bottom=0.1)
        ax = fig.add_subplot(111)

        fingers = [
            'left_pinky', 'left_ring', 'left_middle', 'left_index',
            'right_index', 'right_middle', 'right_ring', 'right_pinky', 'right_thumb'
        ]

        bar_height = 0.7 / len(LAYOUTS)
        y_positions = range(len(fingers))

        for i, (layout_code, color) in enumerate(LAYOUTS.items()):
            offset = (i - len(LAYOUTS) / 2) * bar_height
            values = [sum(all_results[layout_code][j]['finger_counts'][f] for j in range(3)) for f in fingers]

            bars = ax.barh(
                [y + offset for y in y_positions],
                values,
                height=bar_height,
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
                    fontsize=10,
                    color='black',
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.6)
                )

        ax.set_yticks(y_positions)
        ax.set_yticklabels(fingers, fontsize=12)
        ax.set_xlabel("Количество нажатий", fontsize=14)
        ax.set_title("Нагрузка на пальцы по раскладкам (3 текста, общие символы)", fontsize=16)
        ax.grid(True, axis='x', linestyle='--', alpha=0.5)
        ax.legend(title="Раскладка", loc="lower right", fontsize=12, title_fontsize=13)

        canvas = FigureCanvasQTAgg(fig)
        layout = QVBoxLayout()
        layout.addWidget(canvas)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

class HandLoadPieChartsWindow(QMainWindow):
    def __init__(self, all_results):
        super().__init__()
        self.setWindowTitle("Нагрузка на руки по раскладкам")
        self.resize(1600, 700)

        fig = Figure(figsize=(16, 7))
        fig.subplots_adjust(left=0.05, right=0.95, wspace=0.4, hspace=0.4)
        layout = QVBoxLayout()
        canvas = FigureCanvasQTAgg(fig)
        layout.addWidget(canvas)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        for i, layout_code in enumerate(LAYOUTS):
            ax = fig.add_subplot(2, 4, i + 1)
            results = all_results[layout_code]

            left_total = sum(r['left_hand_count'] for r in results)
            right_total = sum(r['right_hand_count'] for r in results)
            total = left_total + right_total

            if total == 0:
                continue

            ax.pie(
                [left_total, right_total],
                labels=['Левая', 'Правая'],
                colors=['#00BFFF', '#FF0000'],
                startangle=90,
                wedgeprops=dict(width=0.4),
                autopct='%1.0f%%'
            )
            ax.set_title(LAYOUT_NAMES.get(layout_code, layout_code), fontsize=12)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    common_chars = get_common_chars()
    all_results = {}

    for layout_code in LAYOUTS:
        analyzer = KeyboardAnalyzer(layout=layout_code)
        results = analyzer.analyze_all_files(common_chars)
        all_results[layout_code] = results

    bar_window = FingerComparisonChart(all_results)
    bar_window.show()

    pie_window = HandLoadPieChartsWindow(all_results)
    pie_window.show()

    sys.exit(app.exec_())






