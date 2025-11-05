==================================================
Модуль №2 — Анализатор раскладок клавиатуры
==================================================

📦 **main.py**  
Модуль реализует класс `KeyboardAnalyzer`, предназначенный для анализа физической нагрузки на пальцы при наборе текста на различных раскладках клавиатуры.

---

🎯 **Назначение**

- Моделировать движения пальцев при печати
- Рассчитывать штрафы за отклонения от домашнего ряда
- Сравнивать раскладки по метрикам эргономики
- Выводить статистику по пальцам, рукам и символам

---

🧩 **Класс: KeyboardAnalyzer**
================================


.. class:: KeyboardAnalyzer(layout='ytsuken')

   Класс для анализа русскоязычных раскладок клавиатуры.

   :param layout: Название раскладки ('ytsuken', 'vyzov', 'zubachev', 'skoropis', 'rusfon', 'diktor', 'ant')

   При инициализации загружает карту клавиш, домашние позиции пальцев и соответствующую раскладку.

.. rubric:: Пример

.. code-block:: python

   analyzer = KeyboardAnalyzer(layout='vyzov')
---

🔧 **Методы класса**
=====================

.. method:: __init__(layout='ytsuken')

   Инициализирует анализатор клавиатурной раскладки.

   Загружает выбранную раскладку клавиатуры и формирует карту клавиш для анализа.
   Поддерживаются следующие раскладки: `'ytsuken'`, `'vyzov'`, `'zubachev'`, `'skoropis'`,
   `'rusfon'`, `'diktor'`, `'ant'`.

   Также создаётся универсальная карта клавиатуры, связывающая код клавиши с её
   позицией на физической клавиатуре (ряд, колонка), используемая для расчёта пути
   движения пальцев.

   :param layout: Название раскладки, которую нужно загрузить. По умолчанию — `'ytsuken'`.

.. rubric:: Пример

.. code-block:: python

   analyzer = KeyboardAnalyzer(layout='zubachev')

.. rubric:: Результат

.. code-block:: python

   analyzer.layout
   # → 'zubachev'

   analyzer.keyboard_map[30]
   # → (2, 0)  # Координаты клавиши 'ф' в домашнем ряду

.. method:: _init_ytsuken_layout()

   Инициализирует стандартную русскую раскладку ЙЦУКЕН.

   Устанавливает соответствие символов клавиш их кодам и пальцам, 
   а также определяет:
   - заглавные буквы (через Shift),
   - специальные символы с Shift,
   - домашние позиции пальцев.

   Этот метод вызывается автоматически при создании экземпляра `KeyboardAnalyzer(layout='ytsuken')`.

.. rubric:: Пример

.. code-block:: python

   analyzer = KeyboardAnalyzer(layout='ytsuken')
   analyzer.keys['ф']
   # → (30, 'left_pinky')

   analyzer.caps_keys['Ф']
   # → (30, 'left_pinky')

   analyzer.shift_keys['!']
   # → (2, 'left_pinky')

   analyzer.home_positions['right_index']
   # → 36

.. method:: _init_vyzov_layout()

   Инициализирует раскладку «Вызов» с оптимизацией через Alt-символы.

   Эта раскладка разработана для повышения эффективности набора текста за счёт:
   - переноса редко используемых символов на Alt-комбинации,
   - сокращения расстояний до часто используемых букв,
   - перераспределения нагрузки между пальцами.

   Метод определяет:
   - основные символы и их расположение,
   - заглавные буквы (через Shift),
   - символы с Shift-модификатором,
   - Alt-символы (альтернативные позиции для экономии движений),
   - домашние позиции пальцев.

   Вызывается автоматически при создании экземпляра `KeyboardAnalyzer(layout='vyzov')`.

.. rubric:: Пример

.. code-block:: python

   analyzer = KeyboardAnalyzer(layout='vyzov')
   analyzer.keys['о']
   # → (18, 'left_middle')

   analyzer.alt_keys['ц']
   # → (30, 'left_ring')  # Более удобная позиция, чем в стандартной раскладке

   analyzer.shift_keys['@']
   # → (27, 'right_ring')

   analyzer.home_positions['right_middle']
   # → 37

.. method:: _init_zubachev_layout()

   Инициализирует раскладку «Зубачев».

   Раскладка разработана с акцентом на симметрию, эргономику и частотное распределение символов.
   Часто используемые буквы расположены ближе к центру, чтобы снизить нагрузку на пальцы.

   Метод определяет:
   - основные символы и их расположение на клавиатуре,
   - заглавные буквы (через Shift),
   - специальные символы с Shift-модификатором,
   - домашние позиции пальцев для расчёта пути.

   Вызывается автоматически при создании экземпляра `KeyboardAnalyzer(layout='zubachev')`.

.. rubric:: Пример

.. code-block:: python

   analyzer = KeyboardAnalyzer(layout='zubachev')
   analyzer.keys['а']
   # → (18, 'left_middle')

   analyzer.caps_keys['А']
   # → (18, 'left_middle')

   analyzer.shift_keys['?']
   # → (8, 'right_ring')

   analyzer.home_positions['right_middle']
   # → 36

.. method:: _init_skoropis_layout()

   Инициализирует раскладку «Скоропись».

   Раскладка разработана для скоростного набора текста с минимальной нагрузкой на пальцы.
   Частотные символы размещены ближе к сильным пальцам, а редкие — на периферии.

   Метод определяет:
   - основные символы и их расположение,
   - заглавные буквы (через Shift),
   - специальные символы с Shift-модификатором,
   - домашние позиции пальцев для расчёта пути.

   Вызывается автоматически при создании экземпляра `KeyboardAnalyzer(layout='skoropis')`.

.. rubric:: Пример

.. code-block:: python

   analyzer = KeyboardAnalyzer(layout='skoropis')
   analyzer.keys['а']
   # → (34, 'left_index')

   analyzer.caps_keys['А']
   # → (34, 'left_index')

   analyzer.shift_keys['!']
   # → (6, 'right_index')

   analyzer.home_positions['right_ring']
   # → 38

.. method:: _init_rusfon_layout()

   Инициализирует раскладку «Русфон» — русскую фонетическую клавиатуру.

   Раскладка разработана для интуитивного ввода русских символов, особенно полезна
   для начинающих пользователей и тех, кто привык к латинской клавиатуре.

   Метод определяет:
   - основные символы и их расположение на клавиатуре,
   - заглавные буквы (через Shift),
   - специальные символы с Shift-модификатором,
   - домашние позиции пальцев для расчёта пути.

   Вызывается автоматически при создании экземпляра `KeyboardAnalyzer(layout='rusfon')`.

.. rubric:: Пример

.. code-block:: python

   analyzer = KeyboardAnalyzer(layout='rusfon')
   analyzer.keys['ф']
   # → (33, 'left_index')

   analyzer.caps_keys['Ф']
   # → (33, 'left_index')

   analyzer.shift_keys['@']
   # → (3, 'left_ring')

   analyzer.home_positions['right_pinky']
   # → 39

.. method:: _init_diktor_layout()

   Инициализирует раскладку «Диктор».

   Раскладка разработана для дикторов, стенографистов и пользователей, работающих с речевыми текстами.
   Оптимизирована для быстрого доступа к служебным символам, знакам препинания и часто используемым буквам.

   Метод определяет:
   - основные символы и их расположение на клавиатуре,
   - заглавные буквы (через Shift),
   - специальные символы с Shift-модификатором,
   - домашние позиции пальцев для расчёта пути.

   Вызывается автоматически при создании экземпляра `KeyboardAnalyzer(layout='diktor')`.

.. rubric:: Пример

.. code-block:: python

   analyzer = KeyboardAnalyzer(layout='diktor')
   analyzer.keys['о']
   # → (33, 'left_index')

   analyzer.caps_keys['О']
   # → (33, 'left_index')

   analyzer.shift_keys['!']
   # → (20, 'left_index')

   analyzer.home_positions['right_ring']
   # → 38

.. method:: _init_ant_layout()

   Инициализирует раскладку «Ант» — альтернативную русскую клавиатуру с эргономическим смещением.

   Раскладка разработана для снижения нагрузки на пальцы и повышения скорости набора.
   Частотные символы размещены ближе к центру, а редкие — на периферии.
   Подходит для анализа эргоэкономичных конфигураций и нестандартных клавиатур.

   Метод определяет:
   - основные символы и их расположение на клавиатуре,
   - заглавные буквы (через Shift),
   - специальные символы с Shift-модификатором,
   - домашние позиции пальцев для расчёта пути.

   Вызывается автоматически при создании экземпляра `KeyboardAnalyzer(layout='ant')`.

.. rubric:: Пример

.. code-block:: python

   analyzer = KeyboardAnalyzer(layout='ant')
   analyzer.keys['а']
   # → (38, 'right_ring')

   analyzer.caps_keys['А']
   # → (38, 'right_ring')

   analyzer.shift_keys['!']
   # → (2, 'left_pinky')

   analyzer.home_positions['left_index']
   # → 33

.. method:: _calculate_path(key_code, finger)

   Вычисляет путь движения пальца от домашней позиции до заданной клавиши.

   Расстояние рассчитывается как сумма вертикального и горизонтального смещения
   между координатами домашней позиции пальца и целевой клавиши на клавиатуре.

   Для больших пальцев (`left_thumb`, `right_thumb`) путь считается равным нулю.

   :param key_code: Целочисленный код клавиши (например, 30 для 'ф').
   :param finger: Название пальца, задействованного при нажатии (например, `'left_index'`).
   :return: Целое число, представляющее путь (количество шагов по рядам и колонкам).

.. rubric:: Пример

.. code-block:: python

   analyzer = KeyboardAnalyzer(layout='ytsuken')
   analyzer._calculate_path(16, 'left_index')  # 'й' — верхний ряд, левый указательный

.. rubric:: Результат

.. code-block:: python

   2  # Смещение: вверх на 1 ряд и влево на 1 колонку от позиции 'ф' (код 30)

.. method:: _load_text_file(filename)

   Загружает текст из указанного файла.

   Открывает файл в кодировке UTF-8 и считывает его содержимое.
   В случае ошибки выводит сообщение в консоль и возвращает пустую строку.

   :param filename: Путь к текстовому файлу.
   :return: Строка с содержимым файла или пустая строка при ошибке.

.. rubric:: Пример

.. code-block:: python

   analyzer = KeyboardAnalyzer()
   text = analyzer._load_text_file("voina_i_mir.txt")

.. rubric:: Результат

.. code-block:: python

   Успешно загружен voina_i_mir.txt: 1457321 символов

   # Возвращаемое значение:
   "Война и мир. Том первый. Часть первая.\n\n— Ну, князь, Генуя и Лукка стали не более как поместьями Бонапарте..."

.. method:: analyze_text(text, text_name, common_chars=None)

   Анализирует текст с точки зрения нагрузки на пальцы при печати на выбранной раскладке.

   Метод рассчитывает:
   - путь движения пальцев от домашней позиции до каждой клавиши,
   - количество нажатий с модификаторами (Shift, Alt),
   - распределение нагрузки по пальцам и рукам,
   - частоту использования левой, правой и обеих рук,
   - среднюю длину пути и количество нажатий на символ.

   Поддерживается фильтрация по общим символам, если задан параметр ``common_chars``.

   :param text: Строка текста для анализа.
   :param text_name: Название текста (используется в отчёте).
   :param common_chars: Множество символов, которые следует учитывать (опционально).
   :return: Словарь со статистикой по раскладке, включая путь, нагрузку, модификаторы и распределение.

.. rubric:: Пример

.. code-block:: python

   analyzer = KeyboardAnalyzer(layout='vyzov')
   result = analyzer.analyze_text("Привет, мир!", "Пример")

.. rubric:: Результат

.. code-block:: python

   {
       'text_name': 'Пример',
       'layout': 'vyzov',
       'total_path': 27,
       'finger_paths': {
           'left_pinky': 3,
           'left_ring': 2,
           'left_middle': 4,
           'left_index': 5,
           'right_index': 6,
           'right_middle': 3,
           'right_ring': 2,
           'right_pinky': 0,
           'left_thumb': 1,
           'right_thumb': 1
       },
       'finger_counts': {
           'left_pinky': 1,
           'left_ring': 1,
           'left_middle': 2,
           'left_index': 2,
           'right_index': 2,
           'right_middle': 1,
           'right_ring': 1,
           'right_pinky': 0,
           'left_thumb': 1,
           'right_thumb': 1
       },
       'characters_analyzed': 11,
       'shift_count': 1,
       'alt_count': 0,
       'average_path': 2.45,
       'left_hand_count': 7,
       'right_hand_count': 6,
       'left_hand_percentage': 53.85,
       'right_hand_percentage': 46.15,
       'left_hand_only': 4,
       'right_hand_only': 5,
       'two_handed': 2,
       'total_presses': 13,
       'average_presses_per_char': 1.18,
       'left_hand_only_percentage': 36.36,
       'right_hand_only_percentage': 45.45,
       'two_handed_percentage': 18.18
   }

.. method:: analyze_all_files(common_chars=None)

   Последовательно анализирует три предопределённых текстовых файла с раскладкой клавиатуры:

   - ``voina_i_mir.txt`` — художественный текст,
   - ``sortchbukw.csv`` — частотная сортировка букв,
   - ``1grams.txt`` — минимальные фразы.

   Для каждого файла:
   - загружает текст,
   - фильтрует символы (если задан ``common_chars``),
   - рассчитывает статистику по пути, нагрузке и модификаторам.

   Используется для пакетного анализа и сравнения раскладок на разных типах текстов.

   :param common_chars: Множество символов, которые следует учитывать при анализе (опционально).
   :return: Список словарей с результатами анализа для каждого файла.

.. rubric:: Пример

.. code-block:: python

   analyzer = KeyboardAnalyzer(layout='skoropis')
   results = analyzer.analyze_all_files()

.. rubric:: Результат

.. code-block:: python

   [
       {
           'text_name': 'Война и мир',
           'layout': 'skoropis',
           'characters_analyzed': 1457321,
           'total_path': 3129842,
           'average_path': 2.15,
           'shift_count': 18321,
           'alt_count': 0,
           'left_hand_percentage': 52.7,
           'right_hand_percentage': 47.3,
           ...
       },
       {
           'text_name': 'Сортировка букв',
           'layout': 'skoropis',
           'characters_analyzed': 33,
           'total_path': 71,
           'average_path': 2.15,
           ...
       },
       {
           'text_name': 'Минимальные фразы',
           'layout': 'skoropis',
           'characters_analyzed': 120,
           'total_path': 248,
           'average_path': 2.07,
           ...
       }
   ]

.. method:: print_results(results)

   Выводит результаты анализа текстов в консоль в структурированном виде.

   Для каждого текста отображается:
   - общее количество символов и путь движения пальцев,
   - средняя нагрузка на символ и общее количество нажатий,
   - статистика по модификаторам (Shift, Alt),
   - распределение нагрузки между руками,
   - типы нажатий (одноручные и двуручные),
   - нагрузка по каждому пальцу с процентным соотношением.

   :param results: Список словарей, полученных из метода ``analyze_text``, содержащих статистику по раскладке.

.. rubric:: Пример

.. code-block:: python

   analyzer = KeyboardAnalyzer(layout='vyzov')
   result = analyzer.analyze_text("Привет, мир!", "Пример")
   analyzer.print_results([result])

.. rubric:: Вывод в консоль

.. code-block:: text

   ============================================================
   === АНАЛИЗ ПУТЕЙ ДЛЯ: Пример ===
   === РАСКЛАДКА: vyzov ===
   ============================================================
   Всего проанализировано символов: 11
   ОБЩИЙ ПУТЬ: 27
   СРЕДНИЙ ПУТЬ НА СИМВОЛ: 2.45
   ОБЩЕЕ КОЛИЧЕСТВО НАЖАТИЙ: 13
   СРЕДНЕЕ НАЖАТИЙ НА СИМВОЛ: 1.18
   Количество Shift-символов: 1
   Количество Alt-символов: 0

   Распределение по рукам:
   Левая рука: 7 нажатий (53.8%)
   Правая рука: 6 нажатий (46.2%)

   Типы нажатий:
     Только левая рука: 4 (36.4%)
     Только правая рука: 5 (45.5%)
     Двуручные: 2 (18.2%)
       - Shift + буква: 1
       - Alt + буква: 0

   Нагрузка по пальцам:
     left_pinky: 1 нажатий (9.1%)
     left_ring: 1 нажатий (9.1%)
     left_middle: 2 нажатий (18.2%)
     left_index: 2 нажатий (18.2%)
     right_index: 2 нажатий (18.2%)
     right_middle: 1 нажатий (9.1%)
     right_ring: 1 нажатий (9.1%)
     left_thumb: 1 нажатий (9.1%)

---

🔣 **Функция: get_common_chars**
===============================

.. function:: get_common_chars()

   Возвращает множество символов, общих для всех раскладок клавиатуры.

   Включает:
   - базовые русские буквы (а–я, ё, пробел),
   - часто используемые спецсимволы, доступные через Shift во всех раскладках.

   Используется для унифицированного анализа раскладок по ограниченному набору символов.

   :return: Множество символов, пригодных для сравнения раскладок.

.. rubric:: Пример

.. code-block:: python

   common_chars = get_common_chars()
   print(f"Всего общих символов: {len(common_chars)}")
   print("Символы:", ''.join(sorted(common_chars)))

.. rubric:: Результат

.. code-block:: text

   Всего общих символов: 42
   Символы: !%()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`абвгдеёжзийклмнопрстуфхцчшщъыьэюя 

---

.. contents::
   :local:
   :depth: 3