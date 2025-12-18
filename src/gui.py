import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget

import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from main import analyze_everything_in_one


def load_all_results():
    """
    Собирает и агрегирует результаты анализа раскладок клавиатуры.

    Логика:
    - вызывает функцию `analyze_everything_in_one()` для получения исходных данных,
    - извлекает статистику нагрузки (`нагрузка`) и комбинаций (`комбинации`),
    - для каждой раскладки суммирует:
        - количество нажатий по пальцам (`finger_counts`),
        - использование левой и правой руки,
        - количество комбинаций с Shift и Alt,
    - формирует итоговый словарь с агрегированными результатами по каждой раскладке.

    Returns:
        dict: Словарь с результатами по раскладкам, где ключ — код раскладки, 
        а значение — словарь с полями:
            - 'name' (str): название раскладки,
            - 'fingers' (dict): суммарное распределение нажатий по пальцам,
            - 'left' (int): количество нажатий левой рукой,
            - 'right' (int): количество нажатий правой рукой,
            - 'both' (int): количество комбинаций с Shift/Alt,
            - 'combos' (dict): статистика комбинаций для данной раскладки.
    """
    data = analyze_everything_in_one()
    load_data = data["нагрузка"]
    combo_data = data["комбинации"]

    all_results = {}

    for layout_code, results in load_data.items():
        left = right = both = 0

        for r in results:
            left += r["left_hand_count"]
            right += r["right_hand_count"]
            both += r["shift_count"] + r["alt_count"]

        all_results[layout_code] = {
            "left": left,
            "right": right,
            "both": both,
            "combos": combo_data[layout_code]
        }

    return all_results



layout_order = [
    "ytsuken",
    "skoropis",
    "ant",
    "rusfon",
    "diktor",
    "vyzov",
    "zubachev"
]

layout_colors = {
    "skoropis": "green",
    "ant": "cyan",
    "rusfon": "pink",
    "diktor": "gold",
    "vyzov": "black",
    "zubachev": "purple",
    "ytsuken": "red"
}

layout_names_ru = {
    "skoropis": "Скоропись",
    "ant": "АНТ",
    "rusfon": "РусФон",
    "diktor": "Диктор",
    "vyzov": "Вызов",
    "zubachev": "Зубачёв",
    "ytsuken": "ЙЦУКЕН"
}


def create_pie_plots(all_results):
    """
    Строит круговые диаграммы для визуализации удобства комбинаций клавиш
    в разных раскладках.

    Логика:
    - создаёт сетку из 2 строк и 4 столбцов для размещения диаграмм,
    - для каждой раскладки из `layout_order` суммирует количество комбинаций:
        - "удобные",
        - "частично_удобные",
        - "неудобные",
    - строит круговую диаграмму с процентным распределением этих категорий,
    - задаёт заголовок диаграммы по имени раскладки,
    - последнюю пустую ось скрывает для симметрии.

    Args:
        all_results (dict): Словарь с агрегированными результатами анализа,
            где для каждой раскладки содержится статистика комбинаций.

    Returns:
        matplotlib.figure.Figure: Объект фигуры с круговыми диаграммами
        по всем раскладкам.
    """
    fig, axs = plt.subplots(2, 4, figsize=(17, 9))
    axs = axs.flatten()

    for i, layout in enumerate(layout_order):
        combos = all_results[layout]["combos"]

        good = partial = bad = 0
        for ngram_type, stats in combos.items():
            good += stats.get("удобные", 0)
            partial += stats.get("частично_удобные", 0)
            if ngram_type == "двухграммы":
                bad += stats.get("неудобные", 0)

        axs[i].pie(
            [good, partial, bad],
            labels=["Удобные", "Частично", "Неудобные"],
            autopct="%1.1f%%",
            startangle=90,
            labeldistance=1.15,
            pctdistance=0.65,
            colors=["lightpink", "lightblue", "lavender"],
            textprops={"fontsize": 9}
        )

        axs[i].set_title(layout_names_ru[layout], fontsize=11)

    axs[-1].axis("off")
    fig.suptitle("Процент удобства переходов (2–4-х символьные)", fontsize=15)
    plt.tight_layout()
    return fig


def create_ngram_bar(all_results):
    """
    Строит вертикальные столбчатые диаграммы для сравнения удобных n-грамм
    (двухграмм, трехграмм, четырехграмм) в разных раскладках.

    Логика:
    - создаёт фигуру и ось для построения графика,
    - для каждой раскладки из `layout_order` извлекает количество удобных n-грамм
      из словаря `combos`,
    - размещает столбцы с небольшим смещением по вертикали для каждой раскладки,
    - окрашивает столбцы в цвет из `layout_colors` и подписывает их названием раскладки,
    - добавляет числовые подписи к каждому столбцу,
    - задаёт метки оси Y ("2-граммы", "3-граммы", "4-граммы"),
    - формирует легенду и аккуратно выравнивает макет.

    Args:
        all_results (dict): Словарь с агрегированными результатами анализа,
            где для каждой раскладки содержится статистика комбинаций.

    Returns:
        matplotlib.figure.Figure: Объект фигуры с горизонтальными столбчатыми
        диаграммами по всем раскладкам.
    """
    fig, ax = plt.subplots(figsize=(14, 8))

    categories = [
        ("двухграммы", "удобные", "2-х символьные — удобные"),
        ("двухграммы", "частично_удобные", "2-х символьные — частично"),
        ("трехграммы", "удобные", "3-х символьные — удобные"),
        ("трехграммы", "частично_удобные", "3-х символьные — частично"),
        ("четырехграммы", "удобные", "4-х символьные — удобные"),
        ("четырехграммы", "частично_удобные", "4-х символьные — частично"),
    ]

    x = range(len(categories))
    bar_w = 0.1

    for i, layout in enumerate(layout_order):
        values = [all_results[layout]["combos"][ng][kind] for ng, kind, _ in categories]

        bars = ax.bar(
            [v + i * bar_w for v in x],
            values,
            width=bar_w,
            color=layout_colors[layout],
            label=layout_names_ru[layout]
        )

        for b in bars:
            ax.text(
                b.get_x() + b.get_width() / 2,
                b.get_height(),
                str(int(b.get_height())),
                ha="center",
                va="bottom",
                fontsize=8,
                rotation=90
            )

    ax.set_xticks([v + bar_w * 3 for v in x])
    ax.set_xticklabels([label for _, _, label in categories], rotation=25)

    ax.set_ylabel("Количество")
    ax.set_title("Удобные и частично удобные комбинации")
    ax.legend(ncol=3)

    ax.margins(y=0.15)
    plt.tight_layout()
    return fig

def create_bad_ngram_bar(all_results):
    fig, ax = plt.subplots(figsize=(14, 7))

    values = [
        all_results[layout]["combos"]["двухграммы"]["неудобные"]
        for layout in layout_order
    ]

    bars = ax.bar(
        range(len(layout_order)),
        values,
        color=[layout_colors[l] for l in layout_order]
    )

    for b in bars:
        ax.text(
            b.get_x() + b.get_width() / 2,
            b.get_height(),
            str(int(b.get_height())),
            ha="center",
            va="bottom",
            fontsize=10
        )

    ax.set_xticks(range(len(layout_order)))
    ax.set_xticklabels(
        [layout_names_ru[l] for l in layout_order],
        rotation=25
    )

    ax.set_ylabel("Количество")
    ax.set_title("Неудобные комбинации (2-х символьные)")

    ax.margins(y=0.2)
    plt.tight_layout()
    return fig


class MainWindow(QWidget):
    """
    Основное окно графического интерфейса приложения.

    Логика:
    - наследует от `QWidget` и служит контейнером для всех элементов интерфейса,
    - управляет размещением виджетов, обработкой событий и отображением результатов анализа,
    - связывает визуальные компоненты (графики, диаграммы, таблицы) с данными из функций анализа,
    - обеспечивает единый доступ к настройкам и элементам управления.
    """
    def __init__(self):
        """
        Инициализирует главное окно приложения для анализа раскладок клавиатуры.

        Логика:
        - вызывает конструктор базового класса `QWidget`,
        - задаёт заголовок окна,
        - загружает результаты анализа раскладок через `load_all_results()`,
        - создаёт вертикальный макет (`QVBoxLayout`) и вкладки (`QTabWidget`),
        - добавляет две вкладки:
            - "Удобство" с круговыми диаграммами (`create_pie_plots`),
            - "2–4 граммы" с горизонтальными столбчатыми диаграммами (`create_ngram_bar`),
        - размещает вкладки в основном макете и устанавливает его для окна.

        Returns:
            None: метод изменяет внутреннее состояние объекта и формирует интерфейс.
        """
        super().__init__()
        self.setWindowTitle("Анализ раскладок клавиатуры")

        self.results = load_all_results()

        layout = QVBoxLayout()
        tabs = QTabWidget()

        tabs.addTab(self.make_tab(create_pie_plots), "Удобство")
        tabs.addTab(self.make_tab(create_ngram_bar), "2–4-х символьные")
        tabs.addTab(self.make_tab(create_bad_ngram_bar), "Неудобные")

        layout.addWidget(tabs)
        self.setLayout(layout)


    def make_tab(self, plot_func):
        """
        Создаёт вкладку интерфейса с графиком, построенным по результатам анализа.

        Логика:
        - создаёт новый виджет (`QWidget`) для вкладки,
        - формирует вертикальный макет (`QVBoxLayout`),
        - вызывает переданную функцию построения графика (`plot_func`) с данными `self.results`,
        - оборачивает полученную фигуру в `FigureCanvas` для отображения в Qt,
        - добавляет холст в макет и устанавливает его для вкладки,
        - возвращает готовый виджет вкладки.

        Args:
            plot_func (callable): Функция построения графика, принимающая словарь результатов
                и возвращающая объект `matplotlib.figure.Figure`.

        Returns:
            QWidget: Виджет вкладки с встроенным графиком.
        """
        w = QWidget()
        v = QVBoxLayout()
        canvas = FigureCanvas(plot_func(self.results))
        v.addWidget(canvas)
        w.setLayout(v)
        return w


if __name__ == "__main__":
    """
    Точка входа в приложение.

    Логика:
    - создаёт экземпляр `QApplication` для управления циклом событий,
    - инициализирует главное окно (`MainWindow`),
    - задаёт размеры окна (1350×850),
    - отображает окно на экране,
    - запускает основной цикл обработки событий (`app.exec()`),
    - завершает программу при закрытии окна.

    Returns:
        None: выполняет запуск графического интерфейса.
    """
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(1400, 950)
    win.show()
    sys.exit(app.exec())
