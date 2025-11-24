'''
Модуль построения графиков 
Импортирует результаты анализа из модуля main.py
Строит столбчатую диаграмму и таблицу с распределением нагрузки в % 
Столбчатая диаграмма показывает показывает абсолютные штрафы по каждому пальцу
'''

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTabWidget
)
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Импортируем функции из main.py
from main import analyze_all_layouts_optimized, KeyboardAnalyzer, get_common_chars


# ------------------------------------------------------------
#  Автозагрузка и суммирование данных
# ------------------------------------------------------------

def load_all_results():
    texts = [
        ('voina_i_mir.txt', 'Война и мир'),
        ('sortchbukw.csv', 'Сортировка букв'),
        ('1grams.txt', 'Минимальные фразы')
    ]

    common_chars = get_common_chars()

    layouts = [
        ('skoropis', 'Скоропись'),
        ('ant', 'Ант'),
        ('rusfon', 'Фонетическая'),
        ('diktor', 'Диктор'),
        ('vyzov', 'Вызов'),
        ('zubachev', 'Зубачев'),
        ('ytsuken', 'Йцукен')
    ]

    # заранее читаем тексты
    loaded_texts = {}
    for filename, _ in texts:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                loaded_texts[filename] = f.read()
        except:
            loaded_texts[filename] = ""

    all_results = {}

    for code, name in layouts:
        analyzer = KeyboardAnalyzer(layout=code)
        total_fingers = None
        left_total = right_total = both_total = 0

        for filename, tname in texts:
            text = loaded_texts[filename]
            result = analyzer.analyze_text(text, tname, common_chars)

            if result:
                if total_fingers is None:
                    total_fingers = {k: 0 for k in result["finger_counts"]}

                for finger, cnt in result["finger_counts"].items():
                    total_fingers[finger] += cnt

                left_total += result["left_hand_letters_percentage" ]
                right_total += result["right_hand_letters_percentage"] 
                both_total += result["hand_switches_per_100_chars"]

        all_results[code] = {
            "name": name,
            "fingers": total_fingers,
            "left": left_total,
            "right": right_total,
            "both": both_total
        }

    return all_results


# ------------------------------------------------------------
#  Графики
# ------------------------------------------------------------

finger_order = [
    "left_pinky", "left_ring", "left_middle", "left_index",
    "right_index", "right_middle", "right_ring", "right_pinky",
    "left_thumb", "right_thumb"
]

# русские подписи
finger_labels_ru = {
    "left_pinky": "Левый мизинец",
    "left_ring": "Левый безымянный",
    "left_middle": "Левый средний",
    "left_index": "Левый указательный",
    "right_index": "Правый указательный",
    "right_middle": "Правый средний",
    "right_ring": "Правый безымянный",
    "right_pinky": "Правый мизинец",
    "left_thumb": "Левый большой",
    "right_thumb": "Правый большой"
}

# сортировка раскладок
layout_order = [
    "skoropis",
    "ant",
    "rusfon",
    "diktor",
    "vyzov",
    "zubachev",
    "ytsuken"
]

layout_colors = {
    'ytsuken': "red",
    'vyzov': "black",
    'diktor': "yellow",
    'rusfon': "pink",
    'ant': "cyan",
    'zubachev': "purple",
    'skoropis': "green"
}


# --------- Горизонтальный график ---------

def create_bar_plot(all_results):
    fig, ax = plt.subplots(figsize=(13, 9))

    #толщинf столбцов
    bar_height = 0.4

    num_layouts = len(layout_order)
    group_height = num_layouts * bar_height

    # расстояние между группами пальцев
    group_gap = 0.6

    # позиции Y для групп пальцев (без отступов)
    y_positions = [i * (group_height + group_gap) for i in range(len(finger_order))]

    # добавляем равный отступ сверху для симметрии
    y_positions = [y + group_gap for y in y_positions]

    # глобальный максимум значений
    global_max = 0
    for code in layout_order:
        values = [all_results[code]["fingers"][f] for f in finger_order]
        global_max = max(global_max, max(values) if values else 0)

    # рисуем столбцы
    for i, code in enumerate(layout_order):
        data = all_results[code]
        values = [data["fingers"][f] for f in finger_order]

        # вертикальные смещения внутри группы
        offsets = [y + i * bar_height for y in y_positions]

        bars = ax.barh(
            offsets,
            values,
            height=bar_height,
            label=data["name"],
            color=layout_colors.get(code, "gray")
        )

        # подписи по центру столбцов
        for bar in bars:
            w = bar.get_width()
            y_center = bar.get_y() + bar.get_height() / 2

            ax.text(
                w + global_max * 0.003,
                y_center,
                f"{int(w)}",
                va='center',
                ha='left',
                fontsize=5.5
            )

    # отступы по оси Y
    min_y = 0
    max_y = y_positions[-1] + group_height + group_gap
    ax.set_ylim(min_y, max_y)

    # подписи групп пальцев точно по центру
    tick_positions = [y + group_height / 2 for y in y_positions]
    ax.set_yticks(tick_positions)
    ax.set_yticklabels([finger_labels_ru[f] for f in finger_order])

    ax.set_xlabel("Нагрузка (нажатия)")
    ax.set_ylabel("Пальцы")
    ax.set_title("Сравнение нагрузок на пальцы (горизонтальный график)")
    ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1.0))

    plt.tight_layout()
    return fig
    
    
    # --------- Круговые диаграммы ---------

def create_pie_plot(all_results):
    fig, axs = plt.subplots(2, 4, figsize=(16, 8))
    axs = axs.flatten()

    for i, code in enumerate(layout_order):
        data = all_results[code]
        axs[i].pie(
            [data["left"], data["right"], data["both"]],
            labels=["Левая", "Правая", "Обе"],
            autopct="%1.1f%%",
            colors=["lightblue", "lightcoral", "mediumpurple"]
        )
        axs[i].set_title(all_results[code]["name"])

    axs[-1].axis('off')  # скрываем лишний график

    fig.suptitle("Соотношение нагрузок на руки")
    return fig


# ------------------------------------------------------------
#GUI
# ------------------------------------------------------------

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Анализатор раскладок клавиатуры")

        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.results = load_all_results()

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "Нагрузка по пальцам")
        self.tabs.addTab(self.tab2, "Нагрузка по рукам")

        self.bar_drawn = False
        self.pie_drawn = False

        self.tabs.currentChanged.connect(self.on_tab_change)

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def on_tab_change(self, index):
        if index == 0 and not self.bar_drawn:
            fig = create_bar_plot(self.results)
            canvas = FigureCanvas(fig)
            box = QVBoxLayout()
            box.addWidget(canvas)
            self.tab1.setLayout(box)
            self.bar_drawn = True

        elif index == 1 and not self.pie_drawn:
            fig = create_pie_plot(self.results)
            canvas = FigureCanvas(fig)
            box = QVBoxLayout()
            box.addWidget(canvas)
            self.tab2.setLayout(box)
            self.pie_drawn = True


# ------------------------------------------------------------
#main
# ------------------------------------------------------------

if __name__ == "__main__":
    """
    Точка входа в приложение.

    - Создаёт экземпляр QApplication.
    - Инициализирует главное окно `KeyboardComparisonGUI`.
    - Отображает окно и запускает главный цикл событий Qt.
    """
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(1300, 950)
    win.show()
    sys.exit(app.exec())
