==================================================
Модуль №1 — Анализатор раскладок клавиатуры
==================================================

📦 **main.py**  
Модуль реализует класс `KeyboardAnalyzer`, предназначенный для анализа физической нагрузки на пальцы при наборе текста на различных раскладках клавиатуры.

---

🎯 **Назначение**

- Моделировать движения пальцев при печати
- Рассчитывать штрафы за отклонения от домашнего ряда
- Сравнивать раскладки по метрикам эргономики
- Выводить статистику по пальцам, рукам и символам

Поддерживаемые раскладки:
- **standard** — стандартная русская (ЙЦУКЕН)
- **challenge** — экспериментальная (Вызов)
- **zubachev** — альтернативная (Зубачев)

---

🧩 **Класс: KeyboardAnalyzer**
================================

.. class:: KeyboardAnalyzer(layout='standard')

   Класс для анализа раскладок клавиатуры.

   :param layout: Название раскладки ('standard', 'challenge', 'zubachev')

   При инициализации загружает карту клавиш, домашние позиции пальцев и соответствующую раскладку.

---

🔧 **Методы класса**
=====================

.. method:: __init__(layout='standard')

   Инициализация анализатора с выбранной раскладкой.

.. method:: _init_standard_layout()

   Загружает стандартную русскую раскладку (ЙЦУКЕН).

.. method:: _init_challenge_layout()

   Загружает экспериментальную раскладку «Вызов».

.. method:: _init_zubachev_layout()

   Загружает альтернативную раскладку «Зубачев».

.. method:: _calculate_penalty(key_code, finger)

   Вычисляет штраф за движение пальца от домашней позиции до целевой клавиши.

   :returns: Целочисленный штраф

.. method:: _load_text_file(filename)

   Загружает текст из указанного файла.

   :returns: Строка с текстом

.. method:: analyze_text(text, text_name, common_chars=None)

   Анализирует текст: считает штрафы, распределение по пальцам и рукам.

   :returns: Словарь с результатами анализа

.. method:: analyze_all_files(common_chars=None)

   Анализирует три предопределённых файла: `voina_i_mir.txt`, `digramms.txt`, `1grams.txt`.

   :returns: Список словарей с результатами

.. method:: print_results(results)

   Выводит результаты анализа в консоль: статистику по символам, пальцам, рукам.

---

🔣 **Функция: get_common_chars**
===============================

.. function:: get_common_chars()

   Возвращает множество символов, общих для всех трёх раскладок.

   :returns: Множество символов (буквы, знаки препинания, пробел)

---

📌 **Пример использования**
===========================

.. code-block:: python

   from keyboard_analyzer import KeyboardAnalyzer, get_common_chars

   common_chars = get_common_chars()
   analyzer = KeyboardAnalyzer(layout='standard')
   text = analyzer._load_text_file('voina_i_mir.txt')
   result = analyzer.analyze_text(text, 'Война и мир', common_chars)
   analyzer.print_results([result])


.. contents::
   :local:
   :depth: 2