#!/usr/bin/env python3
"""
Тесты для модуля анализатора раскладок клавиатуры
"""

import pytest
import sys
import os

# Добавляем текущую директорию в путь для импорта
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from keyboard_Analyzer import KeyboardAnalyzer

class TestKeyboardAnalyzerInitialization:
    """Тесты инициализации"""
    
    def test_standard_layout_initialization(self):
        analyzer = KeyboardAnalyzer('standard')
        assert analyzer.layout == 'standard'
        assert len(analyzer.keys) > 0
    
    def test_challenge_layout_initialization(self):
        analyzer = KeyboardAnalyzer('challenge')
        assert analyzer.layout == 'challenge'
    
    def test_zubachev_layout_initialization(self):
        analyzer = KeyboardAnalyzer('zubachev')
        assert analyzer.layout == 'zubachev'

class TestKeyboardMap:
    """Тесты карты клавиатуры"""
    
    def test_keyboard_map_structure(self):
        analyzer = KeyboardAnalyzer('standard')
        assert 30 in analyzer.keyboard_map
        assert 57 in analyzer.keyboard_map
    
    def test_keyboard_map_coordinates(self):
        analyzer = KeyboardAnalyzer('standard')
        coords = analyzer.keyboard_map[30]
        assert isinstance(coords, tuple)
        assert len(coords) == 2

class TestLayoutSpecifics:
    """Тесты специфики раскладок"""
    
    def test_standard_layout_keys(self):
        analyzer = KeyboardAnalyzer('standard')
        assert 'а' in analyzer.keys
        assert 'о' in analyzer.keys
        assert analyzer.keys['а'] == (33, 'left_index')
    
    def test_challenge_layout_keys(self):
        analyzer = KeyboardAnalyzer('challenge')
        assert 'а' in analyzer.keys
        assert 'н' in analyzer.keys
    
    def test_zubachev_layout_keys(self):
        analyzer = KeyboardAnalyzer('zubachev')
        assert 'р' in analyzer.keys
        assert analyzer.keys['р'] == (23, 'right_index')

class TestPenaltyCalculation:
    """Тесты расчета штрафов"""
    
    def test_penalty_home_position(self):
        analyzer = KeyboardAnalyzer('standard')
        # Для домашней позиции left_pinky это клавиша 'ф' (код 30)
        penalty = analyzer._calculate_penalty(30, 'left_pinky')
        # Должен быть 0, так как это домашняя позиция
        assert penalty == 0
    
    def test_penalty_same_row(self):
        analyzer = KeyboardAnalyzer('standard')
        # Клавиша 'ы' (код 31) рядом с домашней 'ф' (30)
        penalty = analyzer._calculate_penalty(31, 'left_pinky')
        assert penalty == 1  # разница в одной колонке
    
    def test_penalty_thumb_keys(self):
        analyzer = KeyboardAnalyzer('standard')
        penalty_shift = analyzer._calculate_penalty(42, 'left_thumb')
        penalty_space = analyzer._calculate_penalty(57, 'right_thumb')
        assert penalty_shift == 0
        assert penalty_space == 0

class TestTextAnalysis:
    """Тесты анализа текста"""
    
    def test_analyze_empty_text(self):
        analyzer = KeyboardAnalyzer('standard')
        result = analyzer.analyze_text("", "empty_test")
        assert result is None
    
    def test_analyze_simple_text(self):
        analyzer = KeyboardAnalyzer('standard')
        text = "привет"
        result = analyzer.analyze_text(text, "simple_test")
        assert result is not None
        assert result['text_name'] == "simple_test"
        assert result['layout'] == 'standard'
        assert result['characters_analyzed'] == len(text)
    
    def test_analyze_text_with_shift(self):
        analyzer = KeyboardAnalyzer('standard')
        # Используем строчные буквы и символы, которые есть в раскладке
        text = "привет мир!"
        result = analyzer.analyze_text(text, "shift_test")
        assert result is not None
        # Проверяем, что есть ключ shift_count (может быть 0 если нет заглавных)
        assert 'shift_count' in result

    def test_basic_functionality(self):
        analyzer =KeyboardAnalyzer('standard')
        result = analyzer.analyze_text("тест", "basic_test")
        assert result is not None
        assert result['characters_analyzed'] == len("тест")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
#Результаты тестов
#test_keyboard2.py::TestKeyboardAnalyzerInitialization::test_standard_layout_initialization PASSED
#test_keyboard2.py::TestKeyboardAnalyzerInitialization::test_challenge_layout_initialization PASSED
#test_keyboard2.py::TestKeyboardAnalyzerInitialization::test_zubachev_layout_initialization PASSED
#test_keyboard2.py::TestKeyboardMap::test_keyboard_map_structure PASSED
#test_keyboard2.py::TestKeyboardMap::test_keyboard_map_coordinates PASSED
#test_keyboard2.py::TestLayoutSpecifics::test_standard_layout_keys PASSED
#test_keyboard2.py::TestLayoutSpecifics::test_challenge_layout_keys PASSED
#test_keyboard2.py::TestLayoutSpecifics::test_zubachev_layout_keys PASSED
#test_keyboard2.py::TestPenaltyCalculation::test_penalty_home_position PASSED
#test_keyboard2.py::TestPenaltyCalculation::test_penalty_same_row PASSED
#test_keyboard2.py::TestPenaltyCalculation::test_penalty_thumb_keys PASSED
#test_keyboard2.py::TestTextAnalysis::test_analyze_empty_text Текст empty_test пустой, пропускаем анализ PASSED
#test_keyboard2.py::TestTextAnalysis::test_analyze_simple_text PASSED
#test_keyboard2.py::TestTextAnalysis::test_analyze_text_with_shift PASSED
#test_keyboard2.py::TestTextAnalysis::test_basic_functionality PASSED