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
        fingers = {}
        left = right = both = 0

        for r in results:
            for f, cnt in r["finger_counts"].items():
                fingers[f] = fingers.get(f, 0) + cnt
            left += r["left_hand_count"]
            right += r["right_hand_count"]
            both += r["shift_count"] + r["alt_count"]

        all_results[layout_code] = {
            "name": results[0]["layout"],
            "fingers": fingers,
            "left": left,
            "right": right,
            "both": both,
            "combos": combo_data[layout_code]
        }

    return all_results


layout_order = [
    "skoropis", "ant", "rusfon",
    "diktor", "vyzov", "zubachev", "ytsuken"
]

layout_colors = {
    'skoropis': "green",
    'ant': "cyan",
    'rusfon': "pink",
    'diktor': "gold",
    'vyzov': "black",
    'zubachev': "purple",
    'ytsuken': "red"
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
    fig, axs = plt.subplots(2, 4, figsize=(16, 8))
    axs = axs.flatten()

    for i, layout in enumerate(layout_order):
        c = all_results[layout]["combos"]
        good = sum(c[n]["удобные"] for n in c)
        partial = sum(c[n]["частично_удобные"] for n in c)
        bad = sum(c[n]["неудобные"] for n in c)

        axs[i].pie(
            [good, partial, bad],
            labels=["Удобные", "Частично", "Неудобные"],
            autopct="%1.1f%%",
            colors=["#8bd3a3", "#ffe066", "#ff6b6b"]
        )
        axs[i].set_title(all_results[layout]["name"])

    axs[-1].axis("off")
    return fig


def create_ngram_bar(all_results):
    """
    Строит горизонтальные столбчатые диаграммы для сравнения удобных n-грамм
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
    fig, ax = plt.subplots(figsize=(12, 5))
    ngrams = ["двухграммы", "трехграммы", "четырехграммы"]
    bar_h = 0.12

    for i, layout in enumerate(layout_order):
        values = [all_results[layout]["combos"][n]["удобные"] for n in ngrams]
        y = [j + i * bar_h for j in range(len(ngrams))]

        bars = ax.barh(
            y, values,
            height=bar_h,
            color=layout_colors[layout],
            label=all_results[layout]["name"]
        )

        for b in bars:
            ax.text(b.get_width(), b.get_y() + b.get_height() / 2,
                    str(int(b.get_width())) , va="center", fontsize=7)

    ax.set_yticks([i + bar_h * 3 for i in range(len(ngrams))])
    ax.set_yticklabels(["2-граммы", "3-граммы", "4-граммы"])
    ax.legend(bbox_to_anchor=(1.02, 1))
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
        tabs.addTab(self.make_tab(create_ngram_bar), "2–4 граммы")

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
    win.resize(1350, 850)
    win.show()
    sys.exit(app.exec())
