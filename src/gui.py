'''
Модуль построения графиков 
Импортирует результаты анализа из модуля main.py
Строит два типа графиков(столбчатую и круговую диаграммы)
Столбчатая диаграмма показывает показывает абсолютные штрафы по каждому пальцу
Круговая диограмма показывает процентное распределение нагрузки по пальцам 
'''
import sys
import matplotlib
matplotlib.use("Qt5Agg")

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout,
    QPushButton, QLabel, QSizePolicy, QComboBox
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from main import KeyboardAnalyzer, get_common_chars


class KeyboardGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ раскладки клавиатуры")
        self.resize(1200, 800)

        self.filepaths = [
            "voina_i_mir.txt",
            "1grams.txt",
            "digramms.txt"
        ]

        self.common_chars = get_common_chars()
        self.current_layout = "standard"
        self.analyzer = KeyboardAnalyzer(layout=self.current_layout)
        self.results = self.analyzer.analyze_all_files(self.common_chars)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QGridLayout(central_widget)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        self.canvas = None

        self.layout.addWidget(QLabel("📁 Выбор текста и раскладки:"), 0, 0, 1, 4)

        self.layout.addWidget(QLabel("Раскладка:"), 1, 0)
        self.layout_selector = QComboBox()
        self.layout_selector.addItems(["standard", "challenge", "zubachev"])
        self.layout_selector.currentTextChanged.connect(self.reload_analysis)
        self.layout.addWidget(self.layout_selector, 1, 1)

        for i, path in enumerate(self.filepaths):
            btn_bar = QPushButton(f"Столбчатая: {path}")
            btn_pie = QPushButton(f"Круговая: {path}")
            btn_bar.clicked.connect(lambda _, idx=i: self.show_bar_chart(idx))
            btn_pie.clicked.connect(lambda _, idx=i: self.show_pie_chart(idx))
            self.layout.addWidget(btn_bar, i + 2, 0)
            self.layout.addWidget(btn_pie, i + 2, 1)

        self.layout.addWidget(QLabel("📊 Сравнение раскладок по текстам:"), len(self.filepaths) + 3, 0, 1, 4)

        for i, path in enumerate(self.filepaths):
            btn_compare_bar = QPushButton(f"Сравнение (столбцы): {path}")
            btn_compare_pie = QPushButton(f"Сравнение (круг): {path}")
            btn_compare_bar.clicked.connect(lambda _, idx=i: self.compare_layouts_for_file(idx, chart_type="bar"))
            btn_compare_pie.clicked.connect(lambda _, idx=i: self.compare_layouts_for_file(idx, chart_type="pie"))
            self.layout.addWidget(btn_compare_bar, len(self.filepaths) + 4 + i, 0)
            self.layout.addWidget(btn_compare_pie, len(self.filepaths) + 4 + i, 1)

        self.btn_back = QPushButton("🔙 Очистить график")
        self.btn_back.clicked.connect(self.clear_canvas)
        self.layout.addWidget(self.btn_back, len(self.filepaths) + 7, 0, 1, 2)

    def reload_analysis(self, layout_name):
        self.current_layout = layout_name
        self.analyzer = KeyboardAnalyzer(layout=layout_name)
        self.results = self.analyzer.analyze_all_files(self.common_chars)
        self.clear_canvas()

    def clear_canvas(self):
        if self.canvas:
            self.layout.removeWidget(self.canvas)
            self.canvas.setParent(None)
            self.canvas = None

    def show_bar_chart(self, index):
        result = self.results[index]
        penalties = result['finger_penalties']
        fingers = list(penalties.keys())
        values = list(penalties.values())

        fig = Figure(figsize=(16, 10))
        ax = fig.add_subplot(111)
        ax.bar(fingers, values, color="deepskyblue")
        ax.set_title(f"Нагрузка на пальцы — {self.filepaths[index]} ({self.current_layout})", fontsize=16)
        ax.set_ylabel("Суммарный штраф", fontsize=14)
        ax.set_xlabel("Пальцы", fontsize=14)
        ax.set_xticklabels(fingers, rotation=45, ha="right")
        ax.grid(True, linestyle='--', alpha=0.5)

        for i, v in enumerate(values):
            ax.text(i, v + 1, str(v), ha='center', fontsize=12)

        fig.tight_layout()
        self.clear_canvas()
        self.canvas = FigureCanvasQTAgg(fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.canvas, len(self.filepaths) + 8, 0, 1, 4)
        self.canvas.draw()

    def show_pie_chart(self, index):
        result = self.results[index]
        penalties = result['finger_penalties']
        fingers = list(penalties.keys())
        values = list(penalties.values())

        fig = Figure(figsize=(12, 12))
        ax = fig.add_subplot(111)
        explode = [0.03] * len(fingers)

        wedges, texts, autotexts = ax.pie(
            values,
            labels=fingers,
            explode=explode,
            autopct='%1.1f%%',
            startangle=90,
            colors=['#20B2AA', '#FF6347', '#FFD700', '#8A2BE2', '#FF69B4',
                    '#7FFFD4', '#DC143C', '#00CED1', '#DDA0DD'],
            textprops={'rotation_mode': 'anchor', 'va': 'center', 'fontsize': 10},
            labeldistance=1.1,
            pctdistance=0.75
        )

        for text in texts:
            text.set_rotation(90)
            text.set_fontsize(10)

        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_bbox(dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.6))

        ax.set_title(f"Распределение нагрузки — {self.filepaths[index]} ({self.current_layout})", fontsize=16)
        fig.tight_layout()

        self.clear_canvas()
        self.canvas = FigureCanvasQTAgg(fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.canvas, len(self.filepaths) + 8, 0, 1, 4)
        self.canvas.draw()

    def compare_layouts_for_file(self, index, chart_type="bar"):
        layout_codes = ['standard', 'challenge', 'zubachev']
        all_data = []

        for layout in layout_codes:
            analyzer = KeyboardAnalyzer(layout=layout)
            results = analyzer.analyze_all_files(self.common_chars)
            result = results[index]
            all_data.append((layout, result['total_penalty']))

        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        layouts = [x[0] for x in all_data]
        penalties = [x[1] for x in all_data]

        if chart_type == "bar":
            ax.bar(layouts, penalties, color=["#20B2AA", "#FF6347", "#FFD700"])
            for i, v in enumerate(penalties):
                ax.text(i, v + 1, str(v), ha='center', fontsize=12)
            ax.set_ylabel("Общий штраф", fontsize=14)
            ax.set_xlabel("Раскладка", fontsize=14)
            ax.grid(True, linestyle='--', alpha=0.5)

        elif chart_type == "pie":
            explode = [0.03] * len(layouts)
            wedges, texts, autotexts = ax.pie(
                penalties,
                labels=layouts,
                explode=explode,
                autopct='%1.1f%%',
                startangle=90,
                colors=["#20B2AA", "#FF6347", "#FFD700"],
                textprops={'rotation_mode': 'anchor', 'va': 'center', 'fontsize': 10},
                labeldistance=1.1,
                pctdistance=0.75
            )
            for text in texts:
                text.set_rotation(90)
                text.set_fontsize(10)
            for autotext in autotexts:
                autotext.set_fontsize(9)
                autotext.set_bbox(dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.6))

        ax.set_title(f"Сравнение раскладок — {self.filepaths[index]}", fontsize=16)
        fig.tight_layout()
        self.clear_canvas()
        self.canvas = FigureCanvasQTAgg(fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.canvas, len(self.filepaths) + 8, 0, 1, 4)
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KeyboardGUI()
    window.show()
    sys.exit(app.exec_())


