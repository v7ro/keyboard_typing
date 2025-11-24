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
    """
    Загружает набор текстов и анализирует их для всех заданных раскладок клавиатуры,
    возвращая агрегированные результаты по нагрузке на пальцы и руки.

    Входные данные (точка входа):
        - texts (list[tuple]): список текстов для анализа:
            * ('voina_i_mir.txt', 'Война и мир')
            * ('sortchbukw.csv', 'Сортировка букв')
            * ('1grams.txt', 'Минимальные фразы')
        - common_chars (set): множество общих символов, получаемое через ``get_common_chars()``
        - layouts (list[tuple]): список раскладок для анализа:
            * ('skoropis', 'Скоропись')
            * ('ant', 'Ант')
            * ('rusfon', 'Фонетическая')
            * ('diktor', 'Диктор')
            * ('vyzov', 'Вызов')
            * ('zubachev', 'Зубачев')
            * ('ytsuken', 'Йцукен')

    Алгоритм:
        1. Загружает содержимое всех текстов в словарь ``loaded_texts``.
           Если файл отсутствует или не читается — сохраняет пустую строку.
        2. Для каждой раскладки создаёт объект ``KeyboardAnalyzer``.
        3. Анализирует все тексты методом ``analyze_text``.
        4. Агрегирует результаты:
            - суммарные счётчики по пальцам (``finger_counts``),
            - общее количество нажатий левой руки (``left_hand_count``),
            - общее количество нажатий правой руки (``right_hand_count``),
            - общее количество нажатий с модификаторами (``shift_count`` + ``alt_count``).

    Выходные данные (точка выхода):
        dict: словарь ``all_results``, где ключ — код раскладки, а значение — словарь:
            - ``name`` (str): название раскладки
            - ``fingers`` (dict): суммарные счётчики по пальцам
            - ``left`` (int): общее количество нажатий левой рукой
            - ``right`` (int): общее количество нажатий правой рукой
            - ``both`` (int): общее количество нажатий с модификаторами (Shift + Alt)
    """
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

                left_total += result["left_hand_count"]
                right_total += result["right_hand_count"]
                both_total += result["shift_count"] + result["alt_count"]

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
    """
    Строит горизонтальный столбчатый график сравнения нагрузок на пальцы
    для разных раскладок клавиатуры.

    Входные данные (точка входа):
        - all_results (dict): агрегированные результаты анализа, полученные из
          функции ``load_all_results()``. Для каждой раскладки словарь содержит:
            * ``name`` (str): название раскладки
            * ``fingers`` (dict): количество нажатий по каждому пальцу
            * ``left`` (int): общее количество нажатий левой рукой
            * ``right`` (int): общее количество нажатий правой рукой
            * ``both`` (int): количество нажатий с модификаторами (Shift + Alt)

    Алгоритм:
        1. Определяет параметры отображения: высоту столбцов, расстояние между
           группами пальцев, позиции по оси Y.
        2. Находит глобальный максимум значений для корректного масштабирования.
        3. Для каждой раскладки строит горизонтальные столбцы по нагрузке на пальцы.
        4. Добавляет числовые подписи внутри столбцов.
        5. Настраивает подписи осей, легенду и заголовок графика.

    Выходные данные (точка выхода):
        - matplotlib.figure.Figure: объект графика с визуализацией нагрузок.

    Особенности:
        - Использует список ``finger_order`` для порядка пальцев.
        - Использует словарь ``finger_labels_ru`` для русских подписей пальцев.
        - Цвета раскладок задаются через словарь ``layout_colors``.
    """
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
    """
    Строит набор круговых диаграмм (pie charts), показывающих соотношение нагрузок
    на левую руку, правую руку и обе руки (модификаторы) для каждой раскладки клавиатуры.

    Входные данные (точка входа):
        - all_results (dict): агрегированные результаты анализа, полученные из
          функции ``load_all_results()``. Для каждой раскладки словарь содержит:
            * ``name`` (str): название раскладки
            * ``left`` (int): общее количество нажатий левой рукой
            * ``right`` (int): общее количество нажатий правой рукой
            * ``both`` (int): количество нажатий с модификаторами (Shift + Alt)

    Алгоритм:
        1. Создаёт сетку подграфиков (2 строки × 4 столбца).
        2. Для каждой раскладки строит круговую диаграмму с тремя секторами:
            - "Левая" (lightblue),
            - "Правая" (lightcoral),
            - "Обе" (mediumpurple).
        3. Добавляет подписи процентов (``autopct="%1.1f%%"``).
        4. Устанавливает заголовок диаграммы по названию раскладки.
        5. Скрывает лишний пустой подграфик.
        6. Добавляет общий заголовок для всей фигуры.

    Выходные данные (точка выхода):
        - matplotlib.figure.Figure: объект фигуры с круговыми диаграммами.
    """
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

class MainWindow(QWidget):
    """
    Главное окно приложения «Анализатор раскладок клавиатуры».

    Назначение:
        - Отображает результаты анализа раскладок клавиатуры в виде графиков.
        - Содержит вкладки для сравнения нагрузок:
            * по пальцам (горизонтальный столбчатый график),
            * по рукам (круговые диаграммы).
    """
    def __init__(self):
        """
        Конструктор главного окна приложения «Анализатор раскладок клавиатуры».

        Назначение:
            - Инициализирует интерфейс главного окна.
            - Загружает результаты анализа раскладок.
            - Создаёт вкладки для отображения графиков:
                * «Нагрузка по пальцам» (горизонтальный столбчатый график),
                * «Нагрузка по рукам» (круговые диаграммы).

        Входные данные (точка входа):
            - None: конструктор вызывается при создании экземпляра класса.

        Алгоритм:
            1. Устанавливает заголовок окна.
            2. Создаёт основной вертикальный макет (QVBoxLayout).
            3. Создаёт виджет вкладок (QTabWidget).
            4. Загружает результаты анализа через ``load_all_results()``.
            5. Добавляет две вкладки:
                * self.tab1 — для графика нагрузок по пальцам,
                * self.tab2 — для графика нагрузок по рукам.
            6. Инициализирует флаги:
                * self.bar_drawn = False — график по пальцам ещё не построен,
                * self.pie_drawn = False — график по рукам ещё не построен.
            7. Подключает обработчик переключения вкладок (``on_tab_change``).
            8. Добавляет вкладки в основной макет и применяет его к окну.

        Выходные данные (точка выхода):
            - None: метод не возвращает значение, но подготавливает интерфейс окна.
        """
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
        """
        Обработчик переключения вкладок в главном окне приложения.

        Назначение:
            - Отслеживает смену активной вкладки в ``QTabWidget``.
            - При первом открытии вкладки строит соответствующий график и добавляет его
              в макет вкладки.

        Входные данные (точка входа):
            - index (int): индекс выбранной вкладки.
                * 0 — вкладка «Нагрузка по пальцам»
                * 1 — вкладка «Нагрузка по рукам»

        Алгоритм:
            1. Если выбрана вкладка «Нагрузка по пальцам» (index == 0) и график ещё не построен:
                - вызывает ``create_bar_plot(self.results)`` для построения столбчатого графика,
                - создаёт ``FigureCanvas`` для отображения графика,
                - добавляет график в макет вкладки ``self.tab1``,
                - устанавливает флаг ``self.bar_drawn = True``.
            2. Если выбрана вкладка «Нагрузка по рукам» (index == 1) и график ещё не построен:
                - вызывает ``create_pie_plot(self.results)`` для построения круговых диаграмм,
                - создаёт ``FigureCanvas`` для отображения графика,
                - добавляет график в макет вкладки ``self.tab2``,
                - устанавливает флаг ``self.pie_drawn = True``.

        Выходные данные (точка выхода):
            - None: метод не возвращает значение, но обновляет интерфейс вкладок.
        """
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

if __name__ == "__main__":
    """
    Точка входа в приложение «Анализатор раскладок клавиатуры».

    Назначение:
        - Запускает графический интерфейс пользователя (GUI) на основе PyQt5.
        - Инициализирует главное окно приложения и отображает результаты анализа
          раскладок клавиатуры в виде графиков.

    Алгоритм:
        1. Создаёт экземпляр ``QApplication`` для управления событиями Qt.
        2. Инициализирует главное окно ``MainWindow``.
        3. Устанавливает размеры окна (1300 × 950 пикселей).
        4. Отображает окно на экране.
        5. Запускает главный цикл обработки событий Qt через ``app.exec()``.

    Выходные данные (точка выхода):
        - None: блок не возвращает значения.
        - Завершает работу приложения при закрытии окна с помощью ``sys.exit()``.
    """
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(1300, 950)
    win.show()
    sys.exit(app.exec())
