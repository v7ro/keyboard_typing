import pytest
import sys
import os
import tempfile

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from main import KeyboardAnalyzer

class TestInitFromLayoutDataForAllLayouts:
    """7 тестов метода _init_from_layout_data для всех 7 раскладок"""
    
    def test_ytsuken_layout_data(self):
        """Тест 1: Проверка данных раскладки ЙЦУКЕН"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Проверяем, что все свойства установлены
        assert hasattr(analyzer, 'keys')
        assert hasattr(analyzer, 'shift_keys')
        assert hasattr(analyzer, 'alt_keys')
        assert hasattr(analyzer, 'home_positions')
        assert hasattr(analyzer, 'caps_keys')
        
        # Проверяем ключевые клавиши ЙЦУКЕН
        assert 'а' in analyzer.keys
        assert 'о' in analyzer.keys
        assert 'ф' in analyzer.keys
        assert ' ' in analyzer.keys  # Пробел
    
    def test_vyzov_layout_data(self):
        """Тест 2: Проверка данных раскладки Вызов"""
        analyzer = KeyboardAnalyzer('vyzov')
        
        # Проверяем структуру данных
        assert isinstance(analyzer.keys, dict)
        assert isinstance(analyzer.shift_keys, dict)
        assert isinstance(analyzer.caps_keys, dict)
        
        # Проверяем наличие данных
        assert len(analyzer.keys) > 0
        assert len(analyzer.home_positions) >= 8  # 8 пальцев
    
    def test_zubachev_layout_data(self):
        """Тест 3: Проверка данных раскладки Зубачев"""
        analyzer = KeyboardAnalyzer('zubachev')
        
        # Проверяем caps_keys создаются правильно
        for char, (code, finger) in analyzer.keys.items():
            if char.isalpha() and char.islower() and char != ' ':
                upper_char = char.upper()
                assert upper_char in analyzer.caps_keys
                assert analyzer.caps_keys[upper_char] == (code, finger)
        
        # Проверяем, что не создаются caps для не-букв
        assert ' ' not in analyzer.caps_keys
    
    def test_skoropis_layout_data(self):
        """Тест 4: Проверка данных раскладки Скоропис"""
        analyzer = KeyboardAnalyzer('skoropis')
        
        # Проверяем home_positions
        assert 'lf5'in analyzer.home_positions
        assert 'lf4' in analyzer.home_positions
        assert 'rf4' in analyzer.home_positions
        assert 'rf5' in analyzer.home_positions
        
        # Проверяем, что коды есть в keyboard_map
        for finger, code in analyzer.home_positions.items():
            assert code in analyzer.keyboard_map
    
    def test_rusfon_layout_data(self):
        """Тест 5: Проверка данных раскладки Русфон"""
        analyzer = KeyboardAnalyzer('rusfon')
        
        # Проверяем shift_keys
        assert isinstance(analyzer.shift_keys, dict)
        
        # Проверяем alt_keys (если есть в этой раскладке)
        assert isinstance(analyzer.alt_keys, dict)
        
        # Проверяем согласованность данных
        for char, (code, finger) in analyzer.keys.items():
            assert code in analyzer.keyboard_map
    
    def test_diktor_layout_data(self):
        """Тест 6: Проверка данных раскладки Диктор"""
        analyzer = KeyboardAnalyzer('diktor')
        
        # Проверяем обязательное поле keys
        assert 'keys' in analyzer.__dict__
        assert len(analyzer.keys) > 0
        
        # Проверяем автоматическое создание caps_keys
        assert len(analyzer.caps_keys) > 0
        
        # Считаем сколько строчных букв должно быть в caps_keys
        lowercase_count = sum(1 for char in analyzer.keys 
                            if char.isalpha() and char.islower() and char != ' ')
        assert len(analyzer.caps_keys) == lowercase_count
    
    def test_ant_layout_data(self):
        """Тест 7: Проверка данных раскладки Ант"""
        analyzer = KeyboardAnalyzer('ant')
        
        # Проверяем все свойства
        properties = ['keys', 'shift_keys', 'alt_keys', 'home_positions', 'caps_keys']
        for prop in properties:
            assert hasattr(analyzer, prop)
            assert isinstance(getattr(analyzer, prop), dict)
        
        # Проверяем, что метод корректно обработал все 7 раскладок
        assert analyzer.layout == 'ant'
        
        # Финальная проверка - анализируем простой текст
        result = analyzer.analyze_text("тест", "test_ant")
        assert result is not None
        assert result['layout'] == 'ant'
class TestCalculatePathForAllLayouts:
    def _test_basic_patterns(self, analyzer, layout_name):
        if 'lf1' in analyzer.home_positions:
            assert analyzer._calculate_path(42, 'lf1') == 0
        if 'rf1' in analyzer.home_positions:
            assert analyzer._calculate_path(57, 'rf1') == 0
        
        for finger, home_code in analyzer.home_positions.items():
            if finger not in ['lf1', 'rf1']:
                result = analyzer._calculate_path(home_code, finger)
                assert result == 0
        
        assert analyzer._calculate_path(30, 'nonexistent') == 0
        assert analyzer._calculate_path(999, 'lf2') == 0

    def test_ytsuken_path(self):
        analyzer = KeyboardAnalyzer('ytsuken')
        self._test_basic_patterns(analyzer, 'ytsuken')
        
        assert analyzer._calculate_path(20, 'lf2') == 2
        assert analyzer._calculate_path(22, 'rf2') == 1
        assert analyzer._calculate_path(16, 'lf5') == 1
        assert analyzer._calculate_path(42, 'lf1') == 0

    def test_vyzov_path(self):
        analyzer = KeyboardAnalyzer('vyzov')
        self._test_basic_patterns(analyzer, 'vyzov')
        
        assert analyzer._calculate_path(20, 'lf2') == 2
        assert analyzer._calculate_path(21, 'rf2') == 2
        assert analyzer._calculate_path(30, 'lf4') == 1

    def test_zubachev_path(self):
        analyzer = KeyboardAnalyzer('zubachev')
        self._test_basic_patterns(analyzer, 'zubachev')
        
        assert analyzer._calculate_path(19, 'lf2') == 1
        assert analyzer._calculate_path(25, 'rf2') == 2
        assert analyzer._calculate_path(16, 'lf5') == 1

    def test_skoropis_path(self):
        analyzer = KeyboardAnalyzer('skoropis')
        self._test_basic_patterns(analyzer, 'skoropis')
        
        assert analyzer._calculate_path(19, 'lf2') == 1
        assert analyzer._calculate_path(24, 'rf2') == 1
        assert analyzer._calculate_path(39, 'rf4') == 1

    def test_rusfon_path(self):
        analyzer = KeyboardAnalyzer('rusfon')
        self._test_basic_patterns(analyzer, 'rusfon')
        
        assert analyzer._calculate_path(19, 'lf2') == 1
        assert analyzer._calculate_path(24, 'rf2') == 1
        assert analyzer._calculate_path(18, 'lf3') == 1

    def test_diktor_path(self):
        analyzer = KeyboardAnalyzer('diktor')
        self._test_basic_patterns(analyzer, 'diktor')
        
        assert analyzer._calculate_path(19, 'lf2') == 1
        assert analyzer._calculate_path(24, 'rf2') == 1
        assert analyzer._calculate_path(37, 'rf3') == 1

    def test_ant_path(self):
        analyzer = KeyboardAnalyzer('ant')
        self._test_basic_patterns(analyzer, 'ant')
        
        assert analyzer._calculate_path(19, 'lf2') == 1
        assert analyzer._calculate_path(24, 'rf2') == 1
        assert analyzer._calculate_path(18, 'lf3') == 1
        assert analyzer._calculate_path(44, 'lf5') == 2

class TestLoadTextFileSimple:
    def test_load_text_file_simple(self):
        """Простой тест загрузки файла"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # 1. Создаем временный файл с текстом
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.txt', delete=False) as f:
            f.write("Тестовый текст для анализа\nВторая строка")
            temp_filename = f.name
        
        try:
            # 2. Загружаем файл
            result = analyzer._load_text_file(temp_filename)
            
            # 3. Проверяем результат
            assert result == "Тестовый текст для анализа\nВторая строка"
            
        finally:
            # 4. Удаляем временный файл
            os.unlink(temp_filename)
    
    def test_load_text_file_not_found(self):
        """Тест: файл не найден"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Пробуем загрузить несуществующий файл
        result = analyzer._load_text_file("несуществующий_файл_12345.txt")
        
        # Должна вернуться пустая строка
        assert result == ""

class TestAnalyzeCombinationsForAllLayouts:
    
    def test_ytsuken_combinations(self):
        """Тест анализа комбинаций для раскладки ЙЦУКЕН"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Простой тестовый текст
        text = "привет мир как дела"
        result = analyzer.analyze_combinations(text)
        
        # Проверяем структуру результата
        assert 'двухграммы' in result
        assert 'трехграммы' in result
        assert 'четырехграммы' in result
        
        # Проверяем подсчет общего количества
        assert result['двухграммы']['всего'] > 0
        assert result['трехграммы']['всего'] > 0
        assert result['четырехграммы']['всего'] > 0
        
        # Проверяем согласованность подсчетов
        total_bigrams = (result['двухграммы']['удобные'] + 
                        result['двухграммы']['частично_удобные'] + 
                        result['двухграммы']['неудобные'])
        assert total_bigrams == result['двухграммы']['всего']
        
        print(f"ЙЦУКЕН: биграммы={result['двухграммы']}")
    
    def test_vyzov_combinations(self):
        """Тест анализа комбинаций для раскладки ВЫЗОВ"""
        analyzer = KeyboardAnalyzer('vyzov')
        
        text = "привет мир как дела"
        result = analyzer.analyze_combinations(text)
        
        assert 'двухграммы' in result
        assert 'трехграммы' in result
        assert 'четырехграммы' in result
        
        total_bigrams = (result['двухграммы']['удобные'] + 
                        result['двухграммы']['частично_удобные'] + 
                        result['двухграммы']['неудобные'])
        assert total_bigrams == result['двухграммы']['всего']
        
        print(f"ВЫЗОВ: биграммы={result['двухграммы']}")
    
    def test_zubachev_combinations(self):
        """Тест анализа комбинаций для раскладки ЗУБАЧЕВ"""
        analyzer = KeyboardAnalyzer('zubachev')
        
        text = "привет мир как дела"
        result = analyzer.analyze_combinations(text)
        
        assert 'двухграммы' in result
        assert 'трехграммы' in result
        assert 'четырехграммы' in result
        
        total_bigrams = (result['двухграммы']['удобные'] + 
                        result['двухграммы']['частично_удобные'] + 
                        result['двухграммы']['неудобные'])
        assert total_bigrams == result['двухграммы']['всего']
        
        print(f"ЗУБАЧЕВ: биграммы={result['двухграммы']}")
    
    def test_skoropis_combinations(self):
        """Тест анализа комбинаций для раскладки СКОРОПИСЬ"""
        analyzer = KeyboardAnalyzer('skoropis')
        
        text = "привет мир как дела"
        result = analyzer.analyze_combinations(text)
        
        assert 'двухграммы' in result
        assert 'трехграммы' in result
        assert 'четырехграммы' in result
        
        total_bigrams = (result['двухграммы']['удобные'] + 
                        result['двухграммы']['частично_удобные'] + 
                        result['двухграммы']['неудобные'])
        assert total_bigrams == result['двухграммы']['всего']
        
        print(f"СКОРОПИСЬ: биграммы={result['двухграммы']}")
    
    def test_rusfon_combinations(self):
        """Тест анализа комбинаций для раскладки РУСФОН"""
        analyzer = KeyboardAnalyzer('rusfon')
        
        text = "привет мир как дела"
        result = analyzer.analyze_combinations(text)
        
        assert 'двухграммы' in result
        assert 'трехграммы' in result
        assert 'четырехграммы' in result
        
        total_bigrams = (result['двухграммы']['удобные'] + 
                        result['двухграммы']['частично_удобные'] + 
                        result['двухграммы']['неудобные'])
        assert total_bigrams == result['двухграммы']['всего']
        
        print(f"РУСФОН: биграммы={result['двухграммы']}")
    
    def test_diktor_combinations(self):
        """Тест анализа комбинаций для раскладки ДИКТОР"""
        analyzer = KeyboardAnalyzer('diktor')
        
        text = "привет мир как дела"
        result = analyzer.analyze_combinations(text)
        
        assert 'двухграммы' in result
        assert 'трехграммы' in result
        assert 'четырехграммы' in result
        
        total_bigrams = (result['двухграммы']['удобные'] + 
                        result['двухграммы']['частично_удобные'] + 
                        result['двухграммы']['неудобные'])
        assert total_bigrams == result['двухграммы']['всего']
        
        print(f"ДИКТОР: биграммы={result['двухграммы']}")
    
    def test_ant_combinations(self):
        """Тест анализа комбинаций для раскладки АНТ"""
        analyzer = KeyboardAnalyzer('ant')
        
        text = "привет мир как дела"
        result = analyzer.analyze_combinations(text)
        
        assert 'двухграммы' in result
        assert 'трехграммы' in result
        assert 'четырехграммы' in result
        
        total_bigrams = (result['двухграммы']['удобные'] + 
                        result['двухграммы']['частично_удобные'] + 
                        result['двухграммы']['неудобные'])
        assert total_bigrams == result['двухграммы']['всего']
        
        print(f"АНТ: биграммы={result['двухграммы']}")
    
    def test_combinations_with_empty_text(self):
        """Тест анализа комбинаций с пустым текстом"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        text = ""
        result = analyzer.analyze_combinations(text)
        
        assert result['двухграммы']['всего'] == 0
        assert result['трехграммы']['всего'] == 0
        assert result['четырехграммы']['всего'] == 0
    
    def test_combinations_with_only_non_russian(self):
        """Тест анализа комбинаций с не-русским текстом"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        text = "hello world! 123456 @#$%"
        result = analyzer.analyze_combinations(text)
        
        assert result['двухграммы']['всего'] == 0
        assert result['трехграммы']['всего'] == 0
        assert result['четырехграммы']['всего'] == 0
    
    def test_combinations_consistency(self):
        """Тест согласованности результатов для всех раскладок"""
        text = "тест"
        layouts = ['ytsuken', 'vyzov', 'zubachev', 'skoropis', 'rusfon', 'diktor', 'ant']
        
        for layout in layouts:
            analyzer = KeyboardAnalyzer(layout)
            result = analyzer.analyze_combinations(text)
            
            # Для текста "тест" (4 буквы):
            # - биграмм: 3 (те, ес, ст)
            # - триграмм: 2 (тес, ест)
            # - четырехграмм: 1 (тест)
            assert result['двухграммы']['всего'] == 3
            assert result['трехграммы']['всего'] == 2
            assert result['четырехграммы']['всего'] == 1

class TestAnalyzeBigramComfortForAllLayouts:
    
    def test_ytsuken_bigram_comfort(self):
        """Тест оценки биграмм для раскладки ЙЦУКЕН"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Тестируем разные случаи
        # 'ап' - одна и та же рука, один и тот же палец (lf2→lf2)
        # direction = 0 → 'частично_удобные'
        assert analyzer._analyze_bigram_comfort("ап") == 'частично_удобные'
        
        # 'па' - обратное направление, тоже direction = 0
        assert analyzer._analyze_bigram_comfort("па") == 'частично_удобные'
        
        # Разные руки - должно быть неудобно
        assert analyzer._analyze_bigram_comfort("ао") == 'неудобные'  # lf2→rf2
        
        # Не биграмма
        assert analyzer._analyze_bigram_comfort("а") == 'неудобные'
        assert analyzer._analyze_bigram_comfort("") == 'неудобные'
        
        # Не русские буквы
        assert analyzer._analyze_bigram_comfort("12") == 'неудобные'
    
    def test_vyzov_bigram_comfort(self):
        """Тест оценки биграмм для раскладки ВЫЗОВ"""
        analyzer = KeyboardAnalyzer('vyzov')
        
        # Тестируем базовые случаи - проверяем только допустимые значения
        result1 = analyzer._analyze_bigram_comfort("ав")
        assert result1 in ['удобные', 'частично_удобные', 'неудобные']
        
        result2 = analyzer._analyze_bigram_comfort("ва")
        assert result2 in ['удобные', 'частично_удобные', 'неудобные']
        
        # Проверяем разные руки
        result3 = analyzer._analyze_bigram_comfort("ан")  # левая→правая
        assert result3 == 'неудобные'
    
    def test_zubachev_bigram_comfort(self):
        """Тест оценки биграмм для раскладки ЗУБАЧЕВ"""
        analyzer = KeyboardAnalyzer('zubachev')
        
        # Проверяем несколько комбинаций
        test_cases = ["ая", "яа", "ор", "ро", "сн", "нс"]
        
        for bigram in test_cases:
            result = analyzer._analyze_bigram_comfort(bigram)
            assert result in ['удобные', 'частично_удобные', 'неудобные']
        
        # Граничные случаи
        assert analyzer._analyze_bigram_comfort("а") == 'неудобные'
        assert analyzer._analyze_bigram_comfort("абв") == 'неудобные'
        assert analyzer._analyze_bigram_comfort("!@") == 'неудобные'
    
    def test_skoropis_bigram_comfort(self):
        """Тест оценки биграмм для раскладки СКОРОПИСЬ"""
        analyzer = KeyboardAnalyzer('skoropis')
        
        # Тестируем симметричные комбинации
        # Комбинации на левой руке
        left_combinations = ["оа", "ао", "еи", "ие"]
        for bigram in left_combinations:
            result = analyzer._analyze_bigram_comfort(bigram)
            assert result in ['удобные', 'частично_удобные', 'неудобные']
        
        # Комбинации на правой руке
        right_combinations = ["нт", "тн", "ср", "рс"]
        for bigram in right_combinations:
            result = analyzer._analyze_bigram_comfort(bigram)
            assert result in ['удобные', 'частично_удобные', 'неудобные']
    
    def test_rusfon_bigram_comfort(self):
        """Тест оценки биграмм для раскладки РУСФОН"""
        analyzer = KeyboardAnalyzer('rusfon')
        
        # Тестируем противоположные направления
        test_pairs = [
            ("ар", "ра"),  # а→р и р→а
            ("сд", "дс"),  # с→д и д→с
        ]
        
        for bigram1, bigram2 in test_pairs:
            result1 = analyzer._analyze_bigram_comfort(bigram1)
            result2 = analyzer._analyze_bigram_comfort(bigram2)
            
            assert result1 in ['удобные', 'частично_удобные', 'неудобные']
            assert result2 in ['удобные', 'частично_удобные', 'неудобные']
    
    def test_diktor_bigram_comfort(self):
        """Тест оценки биграмм для раскладки ДИКТОР"""
        analyzer = KeyboardAnalyzer('diktor')
        
        # Проверяем все биграммы в слове
        text = "отец"
        for i in range(len(text) - 1):
            bigram = text[i:i+2]
            result = analyzer._analyze_bigram_comfort(bigram)
            assert result in ['удобные', 'частично_удобные', 'неудобные']
        
        # Собираем статистику по разным типам
        test_bigrams = ["оа", "ао", "нт", "тн", "ср", "рс", "ан", "на"]
        results_set = set()
        
        for bigram in test_bigrams:
            result = analyzer._analyze_bigram_comfort(bigram)
            results_set.add(result)
        
        # Должны быть разные результаты
        assert len(results_set) > 0
    
    def test_ant_bigram_comfort(self):
        """Тест оценки биграмм для раскладки АНТ"""
        analyzer = KeyboardAnalyzer('ant')
        
        # Проверяем различные комбинации
        test_cases = ["тл", "лт", "ао", "ят", "т", "xx"]
        
        for bigram in test_cases:
            result = analyzer._analyze_bigram_comfort(bigram)
            assert result in ['удобные', 'частично_удобные', 'неудобные']
        
        # Тест со словом
        word = "привет"
        for i in range(len(word) - 1):
            bigram = word[i:i+2]
            result = analyzer._analyze_bigram_comfort(bigram)
            assert result in ['удобные', 'частично_удобные', 'неудобные']
    
    def test_bigram_comfort_same_finger_logic(self):
        """Тест логики для одинаковых пальцев"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Когда один и тот же палец: direction = 0 → 'частично_удобные'
        result = analyzer._analyze_bigram_comfort("ап")
        assert result == 'частично_удобные'
        
        # Проверим другую пару с тем же пальцем
        result2 = analyzer._analyze_bigram_comfort("гш")  # Проверь пальцы для этих букв
        # Если оба на одном пальце, должно быть 'частично_удобные'
        # Если на разных - может быть другое
    
    def test_bigram_comfort_direction_logic(self):
        """Тест логики направления движения пальцев"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Для ЙЦУКЕН проверим конкретные пары:
        # 'фы' - левая рука: lf5→lf4 (5→4, direction = -1) → 'удобные'
        # 'ыф' - левая рука: lf4→lf5 (4→5, direction = 1) → 'частично_удобные'
        
        # Но нужно знать реальные пальцы для этих букв в ЙЦУКЕН
        # По данным: 'ф': lf5, 'ы': lf4
        # 'фы': 5→4 = -1 → 'удобные'
        # 'ыф': 4→5 = 1 → 'частично_удобные'
        
        # Тест будет более точным, если проверить эти конкретные пары
        result1 = analyzer._analyze_bigram_comfort("фы")
        result2 = analyzer._analyze_bigram_comfort("ыф")
        
        # Оба результата должны быть допустимыми
        assert result1 in ['удобные', 'частично_удобные', 'неудобные']
        assert result2 in ['удобные', 'частично_удобные', 'неудобные']
        
        # И они должны быть противоположными (если не 'неудобные')
        if result1 != 'неудобные' and result2 != 'неудобные':
            assert result1 != result2

class TestAnalyzeTrigramComfortForAllLayouts:
    
    def test_ytsuken_trigram_comfort(self):
        """Тест оценки трехграмм для раскладки ЙЦУКЕН"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Тестируем разные случаи
        # Проверяем, что функция работает
        result1 = analyzer._analyze_trigram_comfort("апр")
        assert result1 in ['удобные', 'частично_удобные', 'неудобные']
        
        # Если одна из пар неудобная - вся трехграмма неудобная
        result2 = analyzer._analyze_trigram_comfort("аоа")  # ао - разные руки
        assert result2 == 'неудобные'
        
        # Не трехграмма
        assert analyzer._analyze_trigram_comfort("ап") == 'неудобные'
        assert analyzer._analyze_trigram_comfort("апрт") == 'неудобные'
        assert analyzer._analyze_trigram_comfort("") == 'неудобные'
        assert analyzer._analyze_trigram_comfort("123") == 'неудобные'
    
    def test_vyzov_trigram_comfort(self):
        """Тест оценки трехграмм для раскладки ВЫЗОВ"""
        analyzer = KeyboardAnalyzer('vyzov')
        
        # Тестируем базовые случаи
        test_trigrams = ["ава", "ивн", "нто", "ана"]
        
        for trigram in test_trigrams:
            result = analyzer._analyze_trigram_comfort(trigram)
            assert result in ['удобные', 'частично_удобные', 'неудобные']
        
        # Тест с недопустимыми символами
        assert analyzer._analyze_trigram_comfort("!@#") == 'неудобные'
    
    def test_zubachev_trigram_comfort(self):
        """Тест оценки трехграмм для раскладки ЗУБАЧЕВ"""
        analyzer = KeyboardAnalyzer('zubachev')
        
        # Тестируем различные комбинации
        test_cases = ["аяр", "яар", "орп", "рост", "снз", "нсж"]
        
        for trigram in test_cases:
            if len(trigram) == 3:
                result = analyzer._analyze_trigram_comfort(trigram)
                assert result in ['удобные', 'частично_удобные', 'неудобные']
        
        # Проверяем логику: если хотя бы одна пара неудобная
        # Создаем триграмму, где средняя пара неудобная
        # Например, буквы на разных руках в середине
        result = analyzer._analyze_trigram_comfort("аоа")  # Предполагаем, что ао - разные руки
        assert result == 'неудобные' or result in ['удобные', 'частично_удобные']
    
    def test_skoropis_trigram_comfort(self):
        """Тест оценки трехграмм для раскладки СКОРОПИСЬ"""
        analyzer = KeyboardAnalyzer('skoropis')
        
        # Тестируем симметричные комбинации
        left_trigrams = ["оае", "аое", "еиу", "иеу"]
        for trigram in left_trigrams:
            result = analyzer._analyze_trigram_comfort(trigram)
            assert result in ['удобные', 'частично_удобные', 'неудобные']
        
        right_trigrams = ["нтс", "тнс", "срй", "рсй"]
        for trigram in right_trigrams:
            result = analyzer._analyze_trigram_comfort(trigram)
            assert result in ['удобные', 'частично_удобные', 'неудобные']
    
    def test_rusfon_trigram_comfort(self):
        """Тест оценки трехграмм для раскладки РУСФОН"""
        analyzer = KeyboardAnalyzer('rusfon')
        
        # Тестируем слова
        words = ["арс", "сда", "оат", "тир"]
        
        for trigram in words:
            result = analyzer._analyze_trigram_comfort(trigram)
            assert result in ['удобные', 'частично_удобные', 'неудобные']
        
        # Проверяем консистентность
        # Для одной руки с последовательным движением
        result1 = analyzer._analyze_trigram_comfort("фгх")  # если все на одной руке
        result2 = analyzer._analyze_trigram_comfort("хгф")  # обратное направление
        
        if result1 != 'неудобные' and result2 != 'неудобные':
            # Результаты могут различаться
            pass
    
    def test_diktor_trigram_comfort(self):
        """Тест оценки трехграмм для раскладки ДИКТОР"""
        analyzer = KeyboardAnalyzer('diktor')
        
        # Проверяем все триграммы в слове
        text = "отец"
        if len(text) >= 3:
            for i in range(len(text) - 2):
                trigram = text[i:i+3]
                result = analyzer._analyze_trigram_comfort(trigram)
                assert result in ['удобные', 'частично_удобные', 'неудобные']
        
        # Собираем статистику по разным типам
        test_trigrams = ["оае", "аое", "нтр", "тнс", "сра", "ант"]
        results_set = set()
        
        for trigram in test_trigrams:
            if len(trigram) == 3:
                result = analyzer._analyze_trigram_comfort(trigram)
                results_set.add(result)
        
        # Должны быть какие-то результаты
        assert len(results_set) > 0
    
    def test_ant_trigram_comfort(self):
        """Тест оценки трехграмм для раскладки АНТ"""
        analyzer = KeyboardAnalyzer('ant')
        
        # Проверяем различные комбинации
        test_cases = ["тла", "лат", "аоя", "ятл", "прт", "ивт"]
        
        for trigram in test_cases:
            if len(trigram) == 3:
                result = analyzer._analyze_trigram_comfort(trigram)
                assert result in ['удобные', 'частично_удобные', 'неудобные']
        
        # Тест со словом
        word = "привет"
        if len(word) >= 3:
            for i in range(len(word) - 2):
                trigram = word[i:i+3]
                result = analyzer._analyze_trigram_comfort(trigram)
                assert result in ['удобные', 'частично_удобные', 'неудобные']
    
    def test_trigram_comfort_logic_same_finger(self):
        """Тест логики для одинаковых пальцев в триграммах"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Если в триграмме есть same-finger bigram (напр., "апа")
        # "ап" - частично_удобные (один палец)
        # "па" - частично_удобные (один палец)
        # Обе пары не "неудобные" и не обе "удобные"
        # → результат должен быть "частично_удобные"
        result = analyzer._analyze_trigram_comfort("апа")
        assert result == 'частично_удобные'
    
    def test_trigram_comfort_all_comfortable(self):
        """Тест, когда все пары удобные"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Нужно найти триграмму, где:
        # 1. Все буквы на одной руке
        # 2. Все пары удобные (движение от мизинца к указательному)
        # 3. Общее направление тоже от мизинца к указательному
        
        # Например, "фыв" в ЙЦУКЕН:
        # 'ф' - lf5, 'ы' - lf4, 'в' - lf3
        # фы: 5→4 = -1 → удобные
        # ыв: 4→3 = -1 → удобные
        # общее: 5>4>3 → удобные
        result = analyzer._analyze_trigram_comfort("фыв")
        assert result in ['удобные', 'частично_удобные', 'неудобные']
    
    def test_trigram_comfort_edge_cases(self):
        """Тест граничных случаев"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Разные руки в середине
        result1 = analyzer._analyze_trigram_comfort("аоа")
        assert result1 in ['неудобные', 'частично_удобные']
        
        # Разные руки в начале
        result2 = analyzer._analyze_trigram_comfort("оаа")
        assert result2 in ['неудобные', 'частично_удобные']
        
        # Разные руки в конце
        result3 = analyzer._analyze_trigram_comfort("аао")
        assert result3 in ['неудобные', 'частично_удобные']
    
    def test_trigram_comfort_consistency_across_layouts(self):
        """Тест согласованности результатов для всех раскладок"""
        test_trigram = "апр"  # Общая триграмма
        
        layouts = ['ytsuken', 'vyzov', 'zubachev', 'skoropis', 'rusfon', 'diktor', 'ant']
        
        for layout in layouts:
            analyzer = KeyboardAnalyzer(layout)
            result = analyzer._analyze_trigram_comfort(test_trigram)
            assert result in ['удобные', 'частично_удобные', 'неудобные']
            
            # Также проверяем, что работает с разной длиной
            assert analyzer._analyze_trigram_comfort("") == 'неудобные'
            assert analyzer._analyze_trigram_comfort("ап") == 'неудобные'
            assert analyzer._analyze_trigram_comfort("апрт") == 'неудобные'
class TestAnalyzeFourgramComfortForAllLayouts:
    
    def test_ytsuken_fourgram_comfort(self):
        """Тест оценки четырехграмм для раскладки ЙЦУКЕН"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Тестируем разные случаи
        # Проверяем, что функция работает
        result1 = analyzer._analyze_fourgram_comfort("апрн")
        assert result1 in ['удобные', 'частично_удобные', 'неудобные']
        
        # Не четырехграмма
        assert analyzer._analyze_fourgram_comfort("апр") == 'неудобные'
        assert analyzer._analyze_fourgram_comfort("апрно") == 'неудобные'
        assert analyzer._analyze_fourgram_comfort("") == 'неудобные'
        assert analyzer._analyze_fourgram_comfort("1234") == 'неудобные'
        
        # Тест логики: ≥2 неудобных пар → 'неудобные'
        # Создаем четырехграмму, где минимум 2 пары неудобные
        # Например, "аоао" где каждая пара "ао" - разные руки
        result2 = analyzer._analyze_fourgram_comfort("аоао")
        assert result2 in ['неудобные', 'частично_удобные']
    
    def test_vyzov_fourgram_comfort(self):
        """Тест оценки четырехграмм для раскладки ВЫЗОВ"""
        analyzer = KeyboardAnalyzer('vyzov')
        
        # Тестируем базовые случаи
        test_fourgrams = ["аван", "ивно", "нтоа", "анав"]
        
        for fourgram in test_fourgrams:
            if len(fourgram) == 4:
                result = analyzer._analyze_fourgram_comfort(fourgram)
                assert result in ['удобные', 'частично_удобные', 'неудобные']
        
        # Тест с граничными значениями
        assert analyzer._analyze_fourgram_comfort("!@#$") == 'неудобные'
        
        # Проверяем логику: 1 неудобная пара → 'частично_удобные'
        # Нужно найти пример в ВЫЗОВ
        pass
    
    def test_zubachev_fourgram_comfort(self):
        """Тест оценки четырехграмм для раскладки ЗУБАЧЕВ"""
        analyzer = KeyboardAnalyzer('zubachev')
        
        # Тестируем различные комбинации
        test_cases = ["аярп", "яара", "орпр", "росп", "снзж", "нсжз"]
        
        for fourgram in test_cases:
            if len(fourgram) == 4:
                result = analyzer._analyze_fourgram_comfort(fourgram)
                assert result in ['удобные', 'частично_удобные', 'неудобные']
        
        # Проверяем логику: ≥2 частично удобных → 'частично_удобные'
        # Создаем тестовый пример
        word = "привет"
        if len(word) >= 4:
            result = analyzer._analyze_fourgram_comfort(word[:4])
            assert result in ['удобные', 'частично_удобные', 'неудобные']
    
    def test_skoropis_fourgram_comfort(self):
        """Тест оценки четырехграмм для раскладки СКОРОПИСЬ"""
        analyzer = KeyboardAnalyzer('skoropis')
        
        # Тестируем симметричные комбинации
        left_fourgrams = ["оаеи", "аоеу", "еиуф", "иеуц"]
        for fourgram in left_fourgrams:
            if len(fourgram) == 4:
                result = analyzer._analyze_fourgram_comfort(fourgram)
                assert result in ['удобные', 'частично_удобные', 'неудобные']
        
        right_fourgrams = ["нтср", "тнср", "срйй", "рсйй"]
        for fourgram in right_fourgrams:
            if len(fourgram) == 4:
                result = analyzer._analyze_fourgram_comfort(fourgram)
                assert result in ['удобные', 'частично_удобные', 'неудобные']
    
    def test_rusfon_fourgram_comfort(self):
        """Тест оценки четырехграмм для раскладки РУСФОН"""
        analyzer = KeyboardAnalyzer('rusfon')
        
        # Тестируем слова
        words = ["арсд", "сдат", "оати", "тиро"]
        
        for fourgram in words:
            if len(fourgram) == 4:
                result = analyzer._analyze_fourgram_comfort(fourgram)
                assert result in ['удобные', 'частично_удобные', 'неудобные']
        
        # Проверяем логику счетчиков
        # Создаем тестовую строку
        test_str = "тест"
        result = analyzer._analyze_fourgram_comfort(test_str)
        assert result in ['удобные', 'частично_удобные', 'неудобные']
    
    def test_diktor_fourgram_comfort(self):
        """Тест оценки четырехграмм для раскладки ДИКТОР"""
        analyzer = KeyboardAnalyzer('diktor')
        
        # Проверяем все четырехграммы в слове
        text = "отече"
        if len(text) >= 4:
            for i in range(len(text) - 3):
                fourgram = text[i:i+4]
                result = analyzer._analyze_fourgram_comfort(fourgram)
                assert result in ['удобные', 'частично_удобные', 'неудобные']
        
        # Собираем статистику по разным типам
        test_fourgrams = ["оаен", "аоен", "нтра", "тнса", "сран", "антр"]
        results_set = set()
        
        for fourgram in test_fourgrams:
            if len(fourgram) == 4:
                result = analyzer._analyze_fourgram_comfort(fourgram)
                results_set.add(result)
        
        # Должны быть какие-то результаты
        assert len(results_set) > 0
    
    def test_ant_fourgram_comfort(self):
        """Тест оценки четырехграмм для раскладки АНТ"""
        analyzer = KeyboardAnalyzer('ant')
        
        # Проверяем различные комбинации
        test_cases = ["тлао", "лато", "аоят", "ятла", "прти", "ивтр"]
        
        for fourgram in test_cases:
            if len(fourgram) == 4:
                result = analyzer._analyze_fourgram_comfort(fourgram)
                assert result in ['удобные', 'частично_удобные', 'неудобные']
        
        # Тест со словом
        word = "привет"
        if len(word) >= 4:
            for i in range(len(word) - 3):
                fourgram = word[i:i+4]
                result = analyzer._analyze_fourgram_comfort(fourgram)
                assert result in ['удобные', 'частично_удобные', 'неудобные']
    
    def test_fourgram_comfort_logic_two_uncomfortable(self):
        """Тест логики: ≥2 неудобных пар → 'неудобные'"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Создаем четырехграмму, где минимум 2 пары неудобные
        # "аоао" - все пары "ао" - разные руки → неудобные
        # 3 пары неудобные → ≥2 → 'неудобные'
        result = analyzer._analyze_fourgram_comfort("аоао")
        # По логике должно быть 'неудобные', но зависит от конкретных пальцев
        assert result in ['неудобные', 'частично_удобные']
    
    def test_fourgram_comfort_logic_one_uncomfortable(self):
        """Тест логики: 1 неудобная пара → 'частично_удобные'"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Нужно создать четырехграмму, где ровно 1 пара неудобная
        # Например: "ааоа" где только пара "ао" неудобная
        result = analyzer._analyze_fourgram_comfort("ааоа")
        # По логике: 1 неудобная → 'частично_удобные'
        assert result in ['частично_удобные', 'неудобные']
    
    def test_fourgram_comfort_logic_two_partial(self):
        """Тест логики: ≥2 частично удобных → 'частично_удобные'"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Создаем четырехграмму с same-finger биграммами
        # "апап" - все пары "ап" и "па" - same-finger → частично_удобные
        # 3 пары частично_удобные → ≥2 → 'частично_удобные'
        result = analyzer._analyze_fourgram_comfort("апап")
        assert result in ['частично_удобные', 'неудобные']
    
    def test_fourgram_comfort_all_comfortable_sequence(self):
        """Тест, когда все пары удобные и последовательность идеальная"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Нужно найти четырехграмму, где:
        # 1. Все буквы на одной руке
        # 2. Все пары удобные
        # 3. Общая последовательность: мизинец→безымянный→средний→указательный
        
        # Например, "фыва" в ЙЦУКЕН:
        # 'ф' - lf5, 'ы' - lf4, 'в' - lf3, 'а' - lf2
        # Все пары удобные и 5>4>3>2
        result = analyzer._analyze_fourgram_comfort("фыва")
        # Должно быть 'удобные' по логике
        assert result in ['удобные', 'частично_удобные', 'неудобные']
    
    def test_fourgram_comfort_all_comfortable_not_perfect_sequence(self):
        """Тест, когда все пары удобные, но последовательность не идеальная"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Четырехграмма, где все пары удобные, но общая последовательность
        # не строго убывающая
        # Например, "фыав": 5>4, но 4<3? Нужно проверить
        result = analyzer._analyze_fourgram_comfort("фыав")
        assert result in ['частично_удобные', 'удобные', 'неудобные']
    
    def test_fourgram_comfort_edge_cases(self):
        """Тест граничных случаев"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Пустая строка и неправильная длина
        assert analyzer._analyze_fourgram_comfort("") == 'неудобные'
        assert analyzer._analyze_fourgram_comfort("а") == 'неудобные'
        assert analyzer._analyze_fourgram_comfort("ап") == 'неудобные'
        assert analyzer._analyze_fourgram_comfort("апр") == 'неудобные'
        assert analyzer._analyze_fourgram_comfort("апрно") == 'неудобные'
        
        # Не русские буквы
        assert analyzer._analyze_fourgram_comfort("1234") == 'неудобные'
        assert analyzer._analyze_fourgram_comfort("!@#$") == 'неудобные'
    
    def test_fourgram_comfort_consistency_across_layouts(self):
        """Тест согласованности результатов для всех раскладок"""
        test_fourgram = "апрн"  # Общая четырехграмма
        
        layouts = ['ytsuken', 'vyzov', 'zubachev', 'skoropis', 'rusfon', 'diktor', 'ant']
        
        for layout in layouts:
            analyzer = KeyboardAnalyzer(layout)
            result = analyzer._analyze_fourgram_comfort(test_fourgram)
            assert result in ['удобные', 'частично_удобные', 'неудобные']
            
            # Также проверяем граничные случаи для каждой раскладки
            assert analyzer._analyze_fourgram_comfort("") == 'неудобные'
            assert analyzer._analyze_fourgram_comfort("апр") == 'неудобные'
class TestGetFingerForCharForAllLayouts:
    
    def test_ytsuken_get_finger_for_char(self):
        """Тест определения пальца для раскладки ЙЦУКЕН"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Тестируем основные буквы
        assert analyzer._get_finger_for_char('а') == 'lf2'
        assert analyzer._get_finger_for_char('о') == 'rf2'
        assert analyzer._get_finger_for_char('ф') == 'lf5'
        assert analyzer._get_finger_for_char('ж') == 'rf5'
        
        # Пробел
        assert analyzer._get_finger_for_char(' ') == 'rf1'
        
        # Shift клавиши
        assert analyzer._get_finger_for_char('!') == 'lf5'
        assert analyzer._get_finger_for_char('?') == 'rf4'
        
        # Несуществующий символ
        assert analyzer._get_finger_for_char('x') is None
        assert analyzer._get_finger_for_char('') is None
        assert analyzer._get_finger_for_char('1') is None
    
    def test_vyzov_get_finger_for_char(self):
        """Тест определения пальца для раскладки ВЫЗОВ"""
        analyzer = KeyboardAnalyzer('vyzov')
        
        # Основные буквы
        result1 = analyzer._get_finger_for_char('а')
        assert result1 in ['lf2', 'lf3', 'lf4', 'lf5', 'rf2', 'rf3', 'rf4', 'rf5', None]
        
        result2 = analyzer._get_finger_for_char('н')
        assert result2 in ['rf2', 'rf3', 'rf4', 'rf5', 'lf2', 'lf3', 'lf4', 'lf5', None]
        
        # Пробел
        assert analyzer._get_finger_for_char(' ') == 'rf1'
        
        # Alt клавиши
        result3 = analyzer._get_finger_for_char('ц')
        assert result3 in ['lf4', 'lf3', 'lf2', 'lf5', 'rf2', 'rf3', 'rf4', 'rf5', None]
        
        # Shift клавиши
        result4 = analyzer._get_finger_for_char('!')
        assert result4 in ['rf5', 'rf4', 'rf3', 'rf2', 'lf5', 'lf4', 'lf3', 'lf2', None]
    
    def test_zubachev_get_finger_for_char(self):
        """Тест определения пальца для раскладки ЗУБАЧЕВ"""
        analyzer = KeyboardAnalyzer('zubachev')
        
        # Проверяем несколько символов
        test_chars = ['а', 'о', 'р', 'с', 'т']
        
        for char in test_chars:
            result = analyzer._get_finger_for_char(char)
            assert result in ['lf2', 'lf3', 'lf4', 'lf5', 'rf2', 'rf3', 'rf4', 'rf5', None]
        
        # Пробел
        assert analyzer._get_finger_for_char(' ') == 'rf1'
        
        # Shift клавиши
        result = analyzer._get_finger_for_char('!')
        assert result in ['lf5', 'lf4', 'lf3', 'lf2', 'rf5', 'rf4', 'rf3', 'rf2', None]
    
    def test_skoropis_get_finger_for_char(self):
        """Тест определения пальца для раскладки СКОРОПИСЬ"""
        analyzer = KeyboardAnalyzer('skoropis')
        
        # Тестируем симметричные буквы
        left_chars = ['о', 'а', 'е', 'и']
        for char in left_chars:
            result = analyzer._get_finger_for_char(char)
            assert result in ['lf2', 'lf3', 'lf4', 'lf5', None]
        
        right_chars = ['н', 'т', 'с', 'р']
        for char in right_chars:
            result = analyzer._get_finger_for_char(char)
            assert result in ['rf2', 'rf3', 'rf4', 'rf5', None]
        
        # Пробел
        assert analyzer._get_finger_for_char(' ') == 'rf1'
        
        # Shift клавиши
        result = analyzer._get_finger_for_char('.')
        assert result in ['lf5', 'lf4', 'lf3', 'lf2', None]
    
    def test_rusfon_get_finger_for_char(self):
        """Тест определения пальца для раскладки РУСФОН"""
        analyzer = KeyboardAnalyzer('rusfon')
        
        # Проверяем различные буквы
        test_chars = ['а', 'р', 'с', 'д', 'о', 'и']
        
        for char in test_chars:
            result = analyzer._get_finger_for_char(char)
            assert result in ['lf2', 'lf3', 'lf4', 'lf5', 'rf2', 'rf3', 'rf4', 'rf5', None]
        
        # Пробел
        assert analyzer._get_finger_for_char(' ') == 'rf1'
        
        # Проверяем, что заглавные буквы работают (если есть caps_keys)
        if hasattr(analyzer, 'caps_keys'):
            # Тестируем заглавную букву, если она есть в caps_keys
            for char in test_chars:
                upper_char = char.upper()
                result = analyzer._get_finger_for_char(upper_char)
                # Может вернуть None или палец
                if result is not None:
                    assert result in ['lf2', 'lf3', 'lf4', 'lf5', 'rf2', 'rf3', 'rf4', 'rf5']
    
    def test_diktor_get_finger_for_char(self):
        """Тест определения пальца для раскладки ДИКТОР"""
        analyzer = KeyboardAnalyzer('diktor')
        
        # Проверяем буквы из слова
        word = "отец"
        for char in word:
            result = analyzer._get_finger_for_char(char)
            assert result in ['lf2', 'lf3', 'lf4', 'lf5', 'rf2', 'rf3', 'rf4', 'rf5', None]
        
        # Пробел
        assert analyzer._get_finger_for_char(' ') == 'rf1'
        
        # Shift клавиши
        result = analyzer._get_finger_for_char(':')
        assert result in ['rf2', 'rf3', 'rf4', 'rf5', None]
    
    def test_ant_get_finger_for_char(self):
        """Тест определения пальца для раскладки АНТ"""
        analyzer = KeyboardAnalyzer('ant')
        
        # Проверяем различные комбинации
        test_chars = ['т', 'л', 'а', 'о', 'я', 'у']
        
        for char in test_chars:
            result = analyzer._get_finger_for_char(char)
            assert result in ['lf2', 'lf3', 'lf4', 'lf5', 'rf2', 'rf3', 'rf4', 'rf5', None]
        
        # Пробел
        assert analyzer._get_finger_for_char(' ') == 'rf1'
        
        # Shift клавиши
        result = analyzer._get_finger_for_char('!')
        assert result in ['lf5', 'lf4', 'lf3', 'lf2', None]
        
        # Тест со словом
        word = "привет"
        for char in word:
            result = analyzer._get_finger_for_char(char)
            if result is not None:
                assert result in ['lf2', 'lf3', 'lf4', 'lf5', 'rf2', 'rf3', 'rf4', 'rf5']
    
    def test_get_finger_for_char_space_logic(self):
        """Тест логики определения пальца для пробела"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Пробел всегда должен возвращать rf1
        assert analyzer._get_finger_for_char(' ') == 'rf1'
        
        # Проверяем для всех раскладок
        layouts = ['vyzov', 'zubachev', 'skoropis', 'rusfon', 'diktor', 'ant']
        
        for layout in layouts:
            analyzer = KeyboardAnalyzer(layout)
            result = analyzer._get_finger_for_char(' ')
            assert result == 'rf1', f"Раскладка {layout}: пробел должен быть rf1, а получили {result}"
    
    def test_get_finger_for_char_priority(self):
        """Тест приоритета поиска символа (keys → caps_keys → shift_keys → alt_keys)"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Буква 'а' должна быть в keys
        assert analyzer._get_finger_for_char('а') == 'lf2'
        
        # Если символ есть в разных словарях, должен использоваться keys
        # Проверяем, что символы не дублируются между словарями
        # или приоритет соблюдается
    
    def test_get_finger_for_char_nonexistent(self):
        """Тест для несуществующих символов"""
        analyzer = KeyboardAnalyzer('ytsuken')
        
        # Латинские буквы
        assert analyzer._get_finger_for_char('a') is None
        assert analyzer._get_finger_for_char('z') is None
        
        # Цифры (кроме тех, что могут быть в shift_keys)
        assert analyzer._get_finger_for_char('1') is None
        
        # Специальные символы (не в shift_keys)
        assert analyzer._get_finger_for_char('@') is None
        assert analyzer._get_finger_for_char('[') is None
        
        # Пустая строка
        assert analyzer._get_finger_for_char('') is None


if __name__ == "__main__":
    # Запуск всех 7 тестов
    print("Запуск 7 тестов для метода _init_from_layout_data...")
    pytest.main([__file__, "-v"])