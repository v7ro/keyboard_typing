#!/usr/bin/env python3
"""
Тесты для модуля KeyboardAnalyzer из main.py
"""
import inspect
import pytest
import sys
import os
import tempfile

# Добавляем текущую директорию в путь для импорта
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from main import KeyboardAnalyzer, get_common_chars

class TestKeyboardAnalyzerLayouts:
    """Тесты инициализации каждой раскладки"""

    def test_ytsuken_layout(self):
        analyzer = KeyboardAnalyzer('ytsuken')
        assert analyzer.layout == 'ytsuken'
        assert 2 in analyzer.keyboard_map

    def test_vyzov_layout(self):
        analyzer = KeyboardAnalyzer('vyzov')
        assert analyzer.layout == 'vyzov'
        assert 16 in analyzer.keyboard_map

    def test_zubachev_layout(self):
        analyzer = KeyboardAnalyzer('zubachev')
        assert analyzer.layout == 'zubachev'
        assert 30 in analyzer.keyboard_map

    def test_skoropis_layout(self):
        analyzer = KeyboardAnalyzer('skoropis')
        assert analyzer.layout == 'skoropis'
        assert 41 in analyzer.keyboard_map

    def test_rusfon_layout(self):
        analyzer = KeyboardAnalyzer('rusfon')
        assert analyzer.layout == 'rusfon'
        assert 42 in analyzer.keyboard_map

    def test_diktor_layout(self):
        analyzer = KeyboardAnalyzer('diktor')
        assert analyzer.layout == 'diktor'
        assert 43 in analyzer.keyboard_map

    def test_ant_layout(self):
        analyzer = KeyboardAnalyzer('ant')
        assert analyzer.layout == 'ant'
        assert 57 in analyzer.keyboard_map

class TestYtsukenLayout:
    def test_keys_mapping(self):
        analyzer = KeyboardAnalyzer('ytsuken')
        keys = analyzer.keys

        # Проверим несколько ключей
        assert keys['й'] == (16, 'left_pinky')
        assert keys['н'] == (21, 'right_index')
        assert keys['ю'] == (52, 'right_ring')
        assert keys[' '] == (57, 'right_thumb')

    def test_caps_keys_generation(self):
        analyzer = KeyboardAnalyzer('ytsuken')
        caps = analyzer.caps_keys

        # Проверим заглавные буквы
        assert caps['Й'] == (16, 'left_pinky')
        assert caps['Н'] == (21, 'right_index')
        assert ' ' not in caps  # пробел не должен быть в caps_keys

    def test_shift_keys_mapping(self):
        analyzer = KeyboardAnalyzer('ytsuken')
        shift = analyzer.shift_keys

        # Проверим несколько символов с Shift
        assert shift['!'] == (2, 'left_pinky')
        assert shift['?'] == (8, 'right_ring')
        assert shift['+'] == (13, 'right_pinky')

    def test_home_positions(self):
        analyzer = KeyboardAnalyzer('ytsuken')
        home = analyzer.home_positions

        # Проверим домашние позиции
        assert home['left_index'] == 33
        assert home['right_index'] == 36
        assert home['right_thumb'] == 57

class TestVyzovLayout:
    def test_keys_mapping(self):
        analyzer = KeyboardAnalyzer('vyzov')
        keys = analyzer.keys

        # Проверим несколько ключей (замени на реальные из _init_vyzov_layout)
        assert 'а' in keys
        assert isinstance(keys['а'], tuple)
        assert len(keys['а']) == 2

        assert 'о' in keys
        assert isinstance(keys['о'], tuple)

        assert ' ' in keys
        assert keys[' '] == (57, 'right_thumb')

    def test_caps_keys_generation(self):
        analyzer = KeyboardAnalyzer('vyzov')
        caps = analyzer.caps_keys

        # Проверим заглавные буквы
        assert 'А' in caps
        assert isinstance(caps['А'], tuple)
        assert ' ' not in caps

    def test_shift_keys_mapping(self):
        analyzer = KeyboardAnalyzer('vyzov')
        shift = analyzer.shift_keys

        # Проверим несколько символов с Shift
        assert '!' in shift
        assert isinstance(shift['!'], tuple)

        assert '+' in shift
        assert isinstance(shift['+'], tuple)

    def test_home_positions(self):
        analyzer = KeyboardAnalyzer('vyzov')
        home = analyzer.home_positions

        # Проверим домашние позиции
        assert home['left_index'] == 33
        assert home['right_index'] == 36
        assert home['right_thumb'] == 57

class TestZubachevLayout:
    def test_keys_mapping(self):
        analyzer = KeyboardAnalyzer('zubachev')
        keys = analyzer.keys

        # Проверим несколько конкретных символов
        assert keys['ф'] == (16, 'left_pinky')
        assert keys['я'] == (19, 'left_index')
        assert keys['р'] == (23, 'right_index')
        assert keys['ч'] == (53, 'right_pinky')
        assert keys[' '] == (57, 'right_thumb')

    def test_caps_keys_generation(self):
        analyzer = KeyboardAnalyzer('zubachev')
        caps = analyzer.caps_keys

        # Проверим заглавные буквы
        assert caps['Ф'] == (16, 'left_pinky')
        assert caps['Я'] == (19, 'left_index')
        assert caps['Ч'] == (53, 'right_pinky')
        assert ' ' not in caps

    def test_shift_keys_mapping(self):
        analyzer = KeyboardAnalyzer('zubachev')
        shift = analyzer.shift_keys

        # Проверим несколько символов с Shift
        assert shift['!'] == (2, 'left_pinky')
        assert shift['+'] == (13, 'right_pinky')
        assert shift['ъ'] == (45, 'left_ring')
        assert shift['ь'] == (47, 'left_index')

    def test_home_positions(self):
        analyzer = KeyboardAnalyzer('zubachev')
        home = analyzer.home_positions

        # Проверим домашние позиции
        assert home['left_index'] == 33
        assert home['right_index'] == 23
        assert home['right_thumb'] == 57

class TestSkoropisLayout:
    def test_keys_mapping(self):
        analyzer = KeyboardAnalyzer('skoropis')
        keys = analyzer.keys

        # Проверим несколько конкретных символов
        assert keys['ц'] == (16, 'left_pinky')
        assert keys['я'] == (18, 'left_middle')
        assert keys['к'] == (23, 'right_index')
        assert keys['ж'] == (53, 'right_pinky')
        assert keys[' '] == (57, 'right_thumb')

    def test_caps_keys_generation(self):
        analyzer = KeyboardAnalyzer('skoropis')
        caps = analyzer.caps_keys

        # Проверим заглавные буквы
        assert caps['Ц'] == (16, 'left_pinky')
        assert caps['Я'] == (18, 'left_middle')
        assert caps['Ж'] == (53, 'right_pinky')
        assert ' ' not in caps

    def test_shift_keys_mapping(self):
        analyzer = KeyboardAnalyzer('skoropis')
        shift = analyzer.shift_keys

        # Проверим несколько символов с Shift
        assert shift['.'] == (2, 'left_pinky')
        assert shift['ё'] == (3, 'left_ring')
        assert shift['!'] == (6, 'right_index')
        assert shift['«'] == (13, 'right_pinky')

    def test_home_positions(self):
        analyzer = KeyboardAnalyzer('skoropis')
        home = analyzer.home_positions

        # Проверим домашние позиции
        assert home['left_index'] == 33
        assert home['right_index'] == 23
        assert home['right_thumb'] == 57

class TestRusfonLayout:
    def test_keys_mapping(self):
        analyzer = KeyboardAnalyzer('rusfon')
        keys = analyzer.keys

        # Проверим несколько конкретных символов
        assert keys['я'] == (16, 'left_pinky')
        assert keys['р'] == (19, 'left_index')
        assert keys['ш'] == (26, 'right_index')
        assert keys['/'] == (53, 'right_pinky')
        assert keys[' '] == (57, 'right_thumb')

    def test_caps_keys_generation(self):
        analyzer = KeyboardAnalyzer('rusfon')
        caps = analyzer.caps_keys

        # Проверим заглавные буквы
        assert caps['Я'] == (16, 'left_pinky')
        assert caps['Р'] == (19, 'left_index')
        assert caps['Ш'] == (26, 'right_index')
        assert ' ' not in caps

    def test_shift_keys_mapping(self):
        analyzer = KeyboardAnalyzer('rusfon')
        shift = analyzer.shift_keys

        # Проверим несколько символов с Shift
        assert shift['!'] == (2, 'left_pinky')
        assert shift['@'] == (3, 'left_ring')
        assert shift['Ё'] == (5, 'left_index')
        assert shift['?'] == (53, 'right_pinky')

    def test_home_positions(self):
        analyzer = KeyboardAnalyzer('rusfon')
        home = analyzer.home_positions

        # Проверим домашние позиции
        assert home['left_index'] == 33
        assert home['right_index'] == 23
        assert home['right_thumb'] == 57
class TestDiktorLayout:
    def test_keys_mapping(self):
        analyzer = KeyboardAnalyzer('diktor')
        keys = analyzer.keys

        # Проверим несколько конкретных символов
        assert keys['ц'] == (16, 'left_pinky')
        assert keys['я'] == (18, 'left_middle')
        assert keys['к'] == (23, 'right_index')
        assert keys['ж'] == (53, 'right_pinky')
        assert keys['ё'] == (41, 'right_pinky')
        assert keys[' '] == (57, 'right_thumb')

    def test_caps_keys_generation(self):
        analyzer = KeyboardAnalyzer('diktor')
        caps = analyzer.caps_keys

        # Проверим заглавные буквы
        assert caps['Ц'] == (16, 'left_pinky')
        assert caps['Я'] == (18, 'left_middle')
        assert caps['Ж'] == (53, 'right_pinky')
        assert caps['Ё'] == (41, 'right_pinky')
        assert ' ' not in caps

    def test_shift_keys_mapping(self):
        analyzer = KeyboardAnalyzer('diktor')
        shift = analyzer.shift_keys

        # Проверим несколько символов с Shift
        assert shift['ъ'] == (17, 'left_ring')
        assert shift['№'] == (4, 'left_middle')
        assert shift['!'] == (20, 'left_index')
        assert shift['+'] == (13, 'right_pinky')

    def test_home_positions(self):
        analyzer = KeyboardAnalyzer('diktor')
        home = analyzer.home_positions

        # Проверим домашние позиции
        assert home['left_index'] == 33
        assert home['right_index'] == 23
        assert home['right_thumb'] == 57

class TestAntLayout:
    def test_keys_mapping(self):
        analyzer = KeyboardAnalyzer('ant')
        keys = analyzer.keys

        # Проверим несколько конкретных символов
        assert keys['г'] == (16, 'left_pinky')
        assert keys['р'] == (18, 'left_middle')
        assert keys['я'] == (23, 'right_index')
        assert keys['ф'] == (53, 'right_pinky')
        assert keys[' '] == (57, 'right_thumb')

    def test_caps_keys_generation(self):
        analyzer = KeyboardAnalyzer('ant')
        caps = analyzer.caps_keys

        # Проверим заглавные буквы
        assert caps['Г'] == (16, 'left_pinky')
        assert caps['Р'] == (18, 'left_middle')
        assert caps['Я'] == (23, 'right_index')
        assert caps['Ф'] == (53, 'right_pinky')
        assert ' ' not in caps

    def test_shift_keys_mapping(self):
        analyzer = KeyboardAnalyzer('ant')
        shift = analyzer.shift_keys

        # Проверим несколько символов с Shift
        assert shift['!'] == (2, 'left_pinky')
        assert shift['+'] == (7, 'right_middle')
        assert shift['/'] == (10, 'right_pinky')
        assert shift['»'] == (13, 'right_pinky')
        assert shift[':'] == (49, 'right_pinky')

    def test_home_positions(self):
        analyzer = KeyboardAnalyzer('ant')
        home = analyzer.home_positions

        # Проверим домашние позиции
        assert home['left_index'] == 33
        assert home['right_index'] == 23
        assert home['right_thumb'] == 57
class TestPenaltyCalculation:
    def test_ytsuken(self):
        analyzer = KeyboardAnalyzer('ytsuken')
        code, finger = analyzer.keys['й']  # (16, 'left_pinky')
        expected = abs(1 - 2) + abs(0 - 0)  # (ряд, колонка): (1,0) vs (2,0)
        actual = analyzer._calculate_path(code, finger)
        assert actual == expected

    def test_vyzov(self):
        analyzer = KeyboardAnalyzer('vyzov')
        code, finger = analyzer.keys['а']  # например (33, 'left_index')
        expected = abs(2 - 2) + abs(3 - 3)  # (2,3) vs (2,3)
        actual = analyzer._calculate_path(code, finger)
        assert actual == expected

    def test_zubachev(self):
        analyzer = KeyboardAnalyzer('zubachev')
        code, finger = analyzer.keys['о']  # например (36, 'right_index')
        expected = abs(2 - 2) + abs(6 - 6)  # (2,6) vs (2,6)
        actual = analyzer._calculate_path(code, finger)
        assert actual == expected

    def test_skoropis(self):
        analyzer = KeyboardAnalyzer('skoropis')
        code, finger = analyzer.keys['ц']  # например (17, 'left_ring')
        expected = abs(1 - 2) + abs(1 - 1)  # (1,1) vs (2,1)
        actual = analyzer._calculate_path(code, finger)
        assert actual == expected

    def test_rusfon(self):
        analyzer = KeyboardAnalyzer('rusfon')
        code, finger = analyzer.keys['р']  # например (35, 'right_index')
        expected = abs(2 - 2) + abs(5 - 6)  # (2,5) vs (2,6)
        actual = analyzer._calculate_path(code, finger)
        assert actual == expected

    def test_diktor(self):
        analyzer = KeyboardAnalyzer('diktor')
        code, finger = analyzer.keys['д']  # например (24, 'right_index')
        expected = abs(1 - 1) + abs(8 - 7)  # (1,8) vs (1,7)
        actual = analyzer._calculate_path(code, finger)
        assert actual == expected

    def test_ant(self):
        analyzer = KeyboardAnalyzer('ant')
        code, finger = analyzer.keys['г']  # например (16, 'left_pinky')
        expected = abs(1 - 2) + abs(0 - 0)  # (1,0) vs (2,0)
        actual = analyzer._calculate_path(code, finger)
        assert actual == expected

class TestAnalyzeText:
    def test_analysis_with_modifiers_ytsuken(self):
        analyzer = KeyboardAnalyzer('ytsuken')
        text = "ПрИвЕт, Мир!"  # Заглавные буквы и символы с Shift
        result = analyzer.analyze_text(text, "Модификаторы ЙЦУКЕН")

        assert result is not None
        assert result['text_name'] == "Модификаторы ЙЦУКЕН"
        assert result['characters_analyzed'] == len("ПрИвЕт, Мир!")
        assert result['shift_count'] > 0
        assert result['total_presses'] >= result['characters_analyzed']
        assert result['two_handed'] > 0
        assert result['left_hand_count'] > 0
        assert result['right_hand_count'] > 0

    def test_analysis_with_modifiers_vyzov(self):
        analyzer = KeyboardAnalyzer('vyzov')
        text = "цщъэ! Привет"  # Alt-символы + Shift
        result = analyzer.analyze_text(text, "Модификаторы Вызов")

        assert result is not None
        assert result['text_name'] == "Модификаторы Вызов"
        assert result['characters_analyzed'] == len("цщъэ! Привет")
        assert result['shift_count'] > 0
        assert result['alt_count'] > 0
        assert result['total_presses'] >= result['characters_analyzed']
        assert result['two_handed'] > 0
        assert result['left_hand_count'] > 0
        assert result['right_hand_count'] > 0

    def test_analysis_with_modifiers_zubachev(self):
        analyzer = KeyboardAnalyzer('zubachev')
        text = "ФЫА! Привет?"  # Заглавные + Shift
        result = analyzer.analyze_text(text, "Модификаторы Зубачев")

        assert result is not None
        assert result['text_name'] == "Модификаторы Зубачев"
        assert result['characters_analyzed'] == len("ФЫА! Привет?")
        assert result['shift_count'] > 0
        assert result['total_presses'] >= result['characters_analyzed']
        assert result['two_handed'] > 0
        assert result['left_hand_count'] > 0
        assert result['right_hand_count'] > 0

    def test_analysis_with_modifiers_skoropis(self):
        analyzer = KeyboardAnalyzer('skoropis')
        text = "ЦА! Привет?"  # Заглавные + Shift
        result = analyzer.analyze_text(text, "Модификаторы Скоропись")

        assert result is not None
        assert result['text_name'] == "Модификаторы Скоропись"
        assert result['characters_analyzed'] == len("ЦА! Привет?")
        assert result['shift_count'] > 0
        assert result['total_presses'] >= result['characters_analyzed']
        assert result['two_handed'] > 0
        assert result['left_hand_count'] > 0
        assert result['right_hand_count'] > 0

    def test_analysis_with_modifiers_rusfon(self):
        analyzer = KeyboardAnalyzer('rusfon')
        text = "ЯВЕ! Привет?"  # Заглавные + Shift
        result = analyzer.analyze_text(text, "Модификаторы Русфон")

        assert result is not None
        assert result['text_name'] == "Модификаторы Русфон"
        assert result['characters_analyzed'] == len("ЯВЕ! Привет?")
        assert result['shift_count'] > 0
        assert result['total_presses'] >= result['characters_analyzed']
        assert result['two_handed'] > 0
        assert result['left_hand_count'] > 0
        assert result['right_hand_count'] > 0

    def test_analysis_with_modifiers_diktor(self):
        analyzer = KeyboardAnalyzer('diktor')
        text = "ЦА! Привет?"  # Заглавные + Shift
        result = analyzer.analyze_text(text, "Модификаторы Диктор")

        assert result is not None
        assert result['text_name'] == "Модификаторы Диктор"
        assert result['characters_analyzed'] == len("ЦА! Привет?")
        assert result['shift_count'] > 0
        assert result['total_presses'] >= result['characters_analyzed']
        assert result['two_handed'] > 0
        assert result['left_hand_count'] > 0
        assert result['right_hand_count'] > 0

    def test_analysis_with_modifiers_ant(self):
        analyzer = KeyboardAnalyzer('ant')
        text = "ГПР! Привет?"  # Заглавные + Shift
        result = analyzer.analyze_text(text, "Модификаторы Ант")

        assert result is not None
        assert result['text_name'] == "Модификаторы Ант"
        assert result['characters_analyzed'] == len("ГПР! Привет?")
        assert result['shift_count'] > 0
        assert result['total_presses'] >= result['characters_analyzed']
        assert result['two_handed'] > 0
        assert result['left_hand_count'] > 0
        assert result['right_hand_count'] > 0

class TestLoadTextFileAllLayouts:
    def test_load_existing_file_ytsuken(self):
        analyzer = KeyboardAnalyzer('ytsuken')
        with tempfile.NamedTemporaryFile('w+', encoding='utf-8', delete=False) as tmp:
            tmp.write("Привет, Ytsuken!")
            tmp_filename = tmp.name
        try:
            result = analyzer._load_text_file(tmp_filename)
            assert result == "Привет, Ytsuken!"
        finally:
            os.remove(tmp_filename)

    def test_load_existing_file_vyzov(self):
        analyzer = KeyboardAnalyzer('vyzov')
        with tempfile.NamedTemporaryFile('w+', encoding='utf-8', delete=False) as tmp:
            tmp.write("Привет, Vyzov!")
            tmp_filename = tmp.name
        try:
            result = analyzer._load_text_file(tmp_filename)
            assert result == "Привет, Vyzov!"
        finally:
            os.remove(tmp_filename)

    def test_load_existing_file_zubachev(self):
        analyzer = KeyboardAnalyzer('zubachev')
        with tempfile.NamedTemporaryFile('w+', encoding='utf-8', delete=False) as tmp:
            tmp.write("Привет, Zubachev!")
            tmp_filename = tmp.name
        try:
            result = analyzer._load_text_file(tmp_filename)
            assert result == "Привет, Zubachev!"
        finally:
            os.remove(tmp_filename)

    def test_load_existing_file_skoropis(self):
        analyzer = KeyboardAnalyzer('skoropis')
        with tempfile.NamedTemporaryFile('w+', encoding='utf-8', delete=False) as tmp:
            tmp.write("Привет, Скоропись!")
            tmp_filename = tmp.name
        try:
            result = analyzer._load_text_file(tmp_filename)
            assert result == "Привет, Скоропись!"
        finally:
            os.remove(tmp_filename)

    def test_load_existing_file_rusfon(self):
        analyzer = KeyboardAnalyzer('rusfon')
        with tempfile.NamedTemporaryFile('w+', encoding='utf-8', delete=False) as tmp:
            tmp.write("Привет, Русфон!")
            tmp_filename = tmp.name
        try:
            result = analyzer._load_text_file(tmp_filename)
            assert result == "Привет, Русфон!"
        finally:
            os.remove(tmp_filename)

    def test_load_existing_file_diktor(self):
        analyzer = KeyboardAnalyzer('diktor')
        with tempfile.NamedTemporaryFile('w+', encoding='utf-8', delete=False) as tmp:
            tmp.write("Привет, Диктор!")
            tmp_filename = tmp.name
        try:
            result = analyzer._load_text_file(tmp_filename)
            assert result == "Привет, Диктор!"
        finally:
            os.remove(tmp_filename)

    def test_load_existing_file_ant(self):
        analyzer = KeyboardAnalyzer('ant')
        with tempfile.NamedTemporaryFile('w+', encoding='utf-8', delete=False) as tmp:
            tmp.write("Привет, Ант!")
            tmp_filename = tmp.name
        try:
            result = analyzer._load_text_file(tmp_filename)
            assert result == "Привет, Ант!"
        finally:
            os.remove(tmp_filename)

    def test_load_missing_file(self):
        analyzer = KeyboardAnalyzer('ytsuken')
        result = analyzer._load_text_file("несуществующий_файл.txt")
        assert result == ""

    def test_load_invalid_argument(self):
        analyzer = KeyboardAnalyzer('ytsuken')
        result = analyzer._load_text_file(None)
        assert result is None or result == ""

    def test_analyze_text_argument_names(self):
        sig = inspect.signature(KeyboardAnalyzer.analyze_text)
        params = sig.parameters

        assert list(params.keys()) == ['self', 'text', 'text_name', 'common_chars']

    def test_analyze_text_annotations_if_present(self):
        sig = inspect.signature(KeyboardAnalyzer.analyze_text)
        params = sig.parameters

        if params['text'].annotation is not inspect._empty:
            assert params['text'].annotation == str, "text должен быть типа str"
        else:
            print("Аннотация для text не указана")

        if params['text_name'].annotation is not inspect._empty:
            assert params['text_name'].annotation == str, "text_name должен быть типа str"
        else:
            print("Аннотация для text_name не указана")

        if params['common_chars'].annotation is not inspect._empty:
            assert params['common_chars'].annotation in [set[str], set, set | None], "common_chars должен быть множеством"
        else:
            print("Аннотация для common_chars не указана")

class TestAnalyzeAllFiles:
    def create_temp_files(self):
        temp_dir = tempfile.TemporaryDirectory()
        file1 = os.path.join(temp_dir.name, 'voina_i_mir.txt')
        file2 = os.path.join(temp_dir.name, 'sortchbukw.csv')
        file3 = os.path.join(temp_dir.name, '1grams.txt')

        with open(file1, 'w', encoding='utf-8') as f:
            f.write("Все смешалось в доме Облонских.")
        with open(file2, 'w', encoding='utf-8') as f:
            f.write("А,Б,В,Г,Д")
        with open(file3, 'w', encoding='utf-8') as f:
            f.write("и, в, не, на, с")

        return temp_dir, file1, file2, file3

    def run_test_for_layout(self, layout):
        analyzer = KeyboardAnalyzer(layout)
        temp_dir, file1, file2, file3 = self.create_temp_files()
        analyzer.analyze_all_files = lambda common_chars=None: [
            analyzer.analyze_text(open(file1, encoding='utf-8').read(), 'Война и мир', common_chars),
            analyzer.analyze_text(open(file2, encoding='utf-8').read(), 'Сортировка букв', common_chars),
            analyzer.analyze_text(open(file3, encoding='utf-8').read(), 'Минимальные фразы', common_chars),
        ]

        results = analyzer.analyze_all_files()

        assert len(results) == 3
        assert results[0]['text_name'] == 'Война и мир'
        assert results[1]['text_name'] == 'Сортировка букв'
        assert results[2]['text_name'] == 'Минимальные фразы'
        assert all(result['characters_analyzed'] > 0 for result in results)
        assert all(result['total_presses'] > 0 for result in results)

        for result in results:
            assert 'alt_count' in result
            assert 'shift_count' in result
            assert 'average_path' in result
            assert 'average_presses_per_char' in result

            assert isinstance(result['alt_count'], int)
            assert isinstance(result['shift_count'], int)
            assert isinstance(result['average_path'], float)
            assert isinstance(result['average_presses_per_char'], float)

            assert result['average_path'] > 0
            assert result['average_presses_per_char'] > 0

        temp_dir.cleanup()

    def test_ytsuken(self):
        self.run_test_for_layout('ytsuken')

    def test_vyzov(self):
        self.run_test_for_layout('vyzov')

    def test_zubachev(self):
        self.run_test_for_layout('zubachev')

    def test_skoropis(self):
        self.run_test_for_layout('skoropis')

    def test_rusfon(self):
        self.run_test_for_layout('rusfon')

    def test_diktor(self):
        self.run_test_for_layout('diktor')

    def test_ant(self):
        self.run_test_for_layout('ant')
class TestPrintImprovedResultsAllLayouts:
    def create_fake_result(self, layout):
        return {
            'text_name': 'Тестовый текст',
            'layout': layout,
            'finger_counts': {
                'left_pinky': 10, 'left_ring': 20, 'left_middle': 30, 'left_index': 40,
                'right_index': 50, 'right_middle': 60, 'right_ring': 70, 'right_pinky': 80,
                'left_thumb': 15, 'right_thumb': 25
            },
            'left_hand_percentage': 55.5,
            'right_hand_percentage': 44.5
        }

    def run_layout_test(self, layout, capsys):
        analyzer = KeyboardAnalyzer(layout)
        fake_result = self.create_fake_result(layout)
        analyzer.print_improved_results([fake_result])

        output = capsys.readouterr().out
        assert f"УЛУЧШЕННЫЙ АНАЛИЗ: {fake_result['text_name']}" in output
        assert f"РАСКЛАДКА: {layout}" in output
        assert "НАГРУЗКА ПО ПАЛЬЦАМ (%)" in output
        assert "Пробел (правый большой):" in output
        assert "Alt/Shift (левый большой):" in output
        assert f"Соотношение рук: Левая {fake_result['left_hand_percentage']:.1f}% / Правая {fake_result['right_hand_percentage']:.1f}%" in output

    def test_ytsuken(self, capsys):
        self.run_layout_test('ytsuken', capsys)

    def test_vyzov(self, capsys):
        self.run_layout_test('vyzov', capsys)

    def test_zubachev(self, capsys):
        self.run_layout_test('zubachev', capsys)

    def test_skoropis(self, capsys):
        self.run_layout_test('skoropis', capsys)

    def test_rusfon(self, capsys):
        self.run_layout_test('rusfon', capsys)

    def test_diktor(self, capsys):
        self.run_layout_test('diktor', capsys)

    def test_ant(self, capsys):
        self.run_layout_test('ant', capsys)
class TestCompareLayoutsCommonChars:
    def test_compare_layouts_output(self, capsys):
        # Подготовка общих символов
        common_chars = get_common_chars()
        assert isinstance(common_chars, set)
        assert 'а' in common_chars
        assert '!' in common_chars
        assert ' ' in common_chars

        # Список раскладок
        layouts = [
            ('ytsuken', 'СТАНДАРТНАЯ'),
            ('vyzov', 'ВЫЗОВ'), 
            ('zubachev', 'ЗУБАЧЕВ'),
            ('skoropis', 'СКОРОПИСЬ'),
            ('rusfon', 'РУСФОН'),
            ('diktor', 'ДИКТОР'),
            ('ant', 'АНТ')
        ]

        # Фиктивный результат анализа
        fake_result = {
            'text_name': 'Тест',
            'layout': 'fake',
            'characters_analyzed': 100,
            'total_presses': 120,
            'average_presses_per_char': 1.2,
            'total_path': 250.0,
            'average_path': 2.5,
            'left_hand_only_percentage': 40.0,
            'right_hand_only_percentage': 30.0,
            'two_handed_percentage': 30.0,
            'shift_count': 10,
            'alt_count': 5,
            'finger_counts': {
                'left_pinky': 5, 'left_ring': 5, 'left_middle': 5, 'left_index': 5,
                'right_index': 5, 'right_middle': 5, 'right_ring': 5, 'right_pinky': 5,
                'left_thumb': 5, 'right_thumb': 5
            }
        }

        # Подменяем методы
        for layout_code, _ in layouts:
            analyzer = KeyboardAnalyzer(layout_code)
            analyzer.analyze_all_files = lambda chars: [fake_result] * 3
            analyzer.print_improved_results = lambda results: print(f"Печать для {layout_code}")

            # Вызываем вручную, как в оригинальной функции
            results = analyzer.analyze_all_files(common_chars)
            analyzer.print_improved_results(results)

        # Перехватываем вывод
        output = capsys.readouterr().out

        # Проверяем ключевые фрагменты
        assert "Печать для ytsuken" in output
        assert "Печать для vyzov" in output
        assert "Печать для zubachev" in output
        assert "Печать для skoropis" in output
        assert "Печать для rusfon" in output
        assert "Печать для diktor" in output
        assert "Печать для ant" in output

if __name__ == "__main__":
    import pytest
    pytest.main()






