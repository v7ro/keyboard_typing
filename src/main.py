"""
Модуль анализатора раскладок клавиатуры
Анализирует нагрузку на пальцы при печати на разных раскладках
Рассчитывает штрафы за движения пальцев от home ряда
Автор: Vero
"""

class KeyboardAnalyzer:
    def __init__(self):
        # Объединяем все в один словарь: буква -> (код, палец)
        self.keys = {
            # Левый мизинец
            'й': (16, 'left_pinky'), 'ф': (30, 'left_pinky'), 'я': (44, 'left_pinky'), 'ё': (41, 'left_pinky'),
            
            # Левый безымянный
            'ц': (17, 'left_ring'), 'ы': (31, 'left_ring'), 'ч': (45, 'left_ring'),
            
            # Левый средний
            'у': (18, 'left_middle'), 'в': (32, 'left_middle'), 'с': (46, 'left_middle'),
            
            # Левый указательный
            'к': (19, 'left_index'), 'а': (33, 'left_index'), 'м': (47, 'left_index'), 
            'п': (34, 'left_index'), 'е': (20, 'left_index'), 'и': (48, 'left_index'),
            
            # Правый указательный
            'р': (35, 'right_index'), 'о': (36, 'right_index'), 'ь': (50, 'right_index'),
            'н': (21, 'right_index'), 'т': (49, 'right_index'), 'г': (22, 'right_index'),
            
            # Правый средний
            'ш': (23, 'right_middle'), 'л': (37, 'right_middle'), 'б': (51, 'right_middle'),
            
            # Правый безымянный
            'щ': (24, 'right_ring'), 'д': (38, 'right_ring'), 'ю': (52, 'right_ring'),
            
            # Правый мизинец
            'ж': (39, 'right_pinky'), 'з': (25, 'right_pinky'), 'х': (26, 'right_pinky'),
            'э': (40, 'right_pinky'), 'ъ': (27, 'right_pinky'), '.': (53, 'right_pinky'),
            '\\': (43, 'right_pinky'),
            
            # Большие пальцы
            ' ': (57, 'right_thumb')
        }

        # Символы с Shift
        self.shift_keys = {
            '!': (2, 'left_pinky'), '"': (3, 'left_ring'), '№': (4, 'left_middle'), ';': (5, 'left_index'),
            '%': (6, 'right_index'), ':': (7, 'right_middle'), '?': (8, 'right_ring'), 
            '*': (9, 'right_pinky'), '(': (10, 'right_pinky'), ')': (11, 'right_pinky'),
            '_': (12, 'right_pinky'), '+': (13, 'right_pinky'), '/': (43, 'right_pinky'),
            ',': (53, 'right_pinky')
        }
        
        # Домашние позиции для каждого пальца
        self.home_positions = {
            'left_pinky': 30,   # ф
            'left_ring': 31,    # ы
            'left_middle': 32,  # в
            'left_index': 33,   # а
            'right_index': 36,  # о
            'right_middle': 37, # л
            'right_ring': 38,   # д
            'right_pinky': 39,  # ж
            'left_thumb': 42,   # shift
            'right_thumb': 57   # пробел
        }
        
        # Карта клавиатуры: код -> (ряд, колонка)
        self.keyboard_map = {
            # Цифровой ряд
            2: (0, 0), 3: (0, 1), 4: (0, 2), 5: (0, 3), 6: (0, 4),
            7: (0, 5), 8: (0, 6), 9: (0, 7), 10: (0, 8), 11: (0, 9),
            12: (0, 10), 13: (0, 11), 14: (0, 12),
            
            # Верхний ряд
            16: (1, 0), 17: (1, 1), 18: (1, 2), 19: (1, 3), 20: (1, 4),
            21: (1, 5), 22: (1, 6), 23: (1, 7), 24: (1, 8), 25: (1, 9),
            26: (1, 10), 27: (1, 11),
            
            # Домашний ряд
            30: (2, 0), 31: (2, 1), 32: (2, 2), 33: (2, 3), 34: (2, 4),
            35: (2, 5), 36: (2, 6), 37: (2, 7), 38: (2, 8), 39: (2, 9),
            40: (2, 10),
            
            # Нижний ряд
            41: (3, 2), 44: (3, 0), 45: (3, 1), 46: (3, 2), 47: (3, 3), 
            48: (3, 4), 49: (3, 5), 50: (3, 6), 51: (3, 7), 52: (3, 8), 
            53: (3, 9),
            
            # Особые клавиши
            42: (3, -1),  # Shift
            43: (1, 12),  # \ (обратный слеш)
            57: (4, 5)    # Пробел
        }

    def _calculate_penalty(self, key_code, finger):
        """Автоматически вычисляет штраф на основе расстояния от домашней позиции"""
        if finger in ['left_thumb', 'right_thumb']:
            return 0
            
        home_code = self.home_positions[finger]
        
        # Получаем координаты домашней и целевой клавиш
        home_coords = self.keyboard_map.get(home_code)
        target_coords = self.keyboard_map.get(key_code)
        
        if not home_coords or not target_coords:
            return 0
            
        home_row, home_col = home_coords
        target_row, target_col = target_coords
        
        # Вычисляем манхэттенское расстояние (сумма разниц по рядам и колонкам)
        row_diff = abs(target_row - home_row)
        col_diff = abs(target_col - home_col)
        
        # Штраф = расстояние от домашней позиции
        penalty = row_diff + col_diff
        
        return penalty

    def _load_text_file(self, filename):
        """Загрузка текста из файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                text = file.read()
                print(f"Успешно загружен {filename}: {len(text)} символов")
                return text
        except FileNotFoundError:
            print(f"ОШИБКА: Файл {filename} не найден!")
            return ""
        except Exception as e:
            print(f"ОШИБКА загрузки файла {filename}: {e}")
            return ""

    def analyze_text(self, text, text_name):
        """Анализ конкретного текста"""
        if not text:
            print(f"Текст {text_name} пустой, пропускаем анализ")
            return None
            
        # Фильтруем русский текст + Shift символы
        all_chars = set(self.keys.keys()).union(set(self.shift_keys.keys()))
        clean_text = ''.join(c for c in text.lower() if c in all_chars)
        
        penalties = {finger: 0 for finger in [
            'left_pinky', 'left_ring', 'left_middle', 'left_index',
            'right_index', 'right_middle', 'right_ring', 'right_pinky', 
            'left_thumb', 'right_thumb'
        ]}
        
        finger_counts = {finger: 0 for finger in penalties.keys()}
        total_penalty = 0
        shift_count = 0
        character_count = len(clean_text)

        for char in clean_text:
            if char in self.keys:
                key_code, finger = self.keys[char]
                penalty = self._calculate_penalty(key_code, finger)
                penalties[finger] += penalty
                finger_counts[finger] += 1
                total_penalty += penalty
            elif char in self.shift_keys:
                key_code, finger = self.shift_keys[char]
                # Shift символ = штраф за клавишу + 1 за Shift
                key_penalty = self._calculate_penalty(key_code, finger)
                shift_penalty = 1
                total_penalty += key_penalty + shift_penalty
                penalties[finger] += key_penalty
                penalties['left_thumb'] += shift_penalty
                finger_counts[finger] += 1
                finger_counts['left_thumb'] += 1
                shift_count += 1
        
        average_penalty = total_penalty / character_count if character_count > 0 else 0
        
        # Статистика по рукам
        left_hand_count = sum(finger_counts[f] for f in ['left_pinky', 'left_ring', 'left_middle', 'left_index', 'left_thumb'])
        right_hand_count = sum(finger_counts[f] for f in ['right_pinky', 'right_ring', 'right_middle', 'right_index', 'right_thumb'])
        total_hand_count = left_hand_count + right_hand_count
        
        left_hand_percentage = (left_hand_count / total_hand_count * 100) if total_hand_count > 0 else 0
        right_hand_percentage = (right_hand_count / total_hand_count * 100) if total_hand_count > 0 else 0
        
        return {
            'text_name': text_name,
            'total_penalty': total_penalty,
            'finger_penalties': penalties,
            'finger_counts': finger_counts,
            'characters_analyzed': character_count,
            'shift_count': shift_count,
            'average_penalty': average_penalty,
            'left_hand_count': left_hand_count,
            'right_hand_count': right_hand_count,
            'left_hand_percentage': left_hand_percentage,
            'right_hand_percentage': right_hand_percentage
        }

    def analyze_all_files(self):
        """Анализ всех трех файлов"""
        files_to_analyze = [
            ('voina_i_mir.txt', 'Война и мир'),
            ('digramms.txt', 'Диграммы'),
            ('1grams.txt', '1-граммы')
        ]
        
        results = []
        
        for filename, text_name in files_to_analyze:
            print(f"\n--- Загрузка {filename} ---")
            text = self._load_text_file(filename)
            if text:
                result = self.analyze_text(text, text_name)
                if result:
                    results.append(result)
        
        return results

    def print_results(self, results):
        """Вывод результатов для всех текстов"""
        for result in results:
            print(f"\n{'='*50}")
            print(f"=== АНАЛИЗ ШТРАФОВ ДЛЯ: {result['text_name']} ===")
            print(f"{'='*50}")
            print(f"Всего проанализировано символов: {result['characters_analyzed']}")
            print(f"ОБЩИЙ ШТРАФ: {result['total_penalty']}")
            print(f"СРЕДНИЙ ШТРАФ НА СИМВОЛ: {result['average_penalty']:.2f}")
            print(f"Количество Shift-символов: {result['shift_count']}")

            print(f"\nРаспределение по рукам:")
            print(f"Левая рука: {result['left_hand_count']} нажатий ({result['left_hand_percentage']:.1f}%)")
            print(f"Правая рука: {result['right_hand_count']} нажатий ({result['right_hand_percentage']:.1f}%)")

            print(f"\nНагрузка по пальцам:")
            for finger in ['left_pinky', 'left_ring', 'left_middle', 'left_index', 
                          'right_index', 'right_middle', 'right_ring', 'right_pinky', 
                          'left_thumb', 'right_thumb']:
                count = result['finger_counts'][finger]
                if count > 0:  # Показываем только пальцы с ненулевой нагрузкой
                    percentage = (count / result['characters_analyzed'] * 100)
                    print(f"  {finger}: {count} нажатий ({percentage:.1f}%)")


# Запуск
analyzer = KeyboardAnalyzer()
all_results = analyzer.analyze_all_files()
analyzer.print_results(all_results)

# Сводная таблица для сравнения
if len(all_results) > 1:
    print(f"\n{'='*60}")
    print("СВОДНАЯ ТАБЛИЦА ДЛЯ СРАВНЕНИЯ")
    print(f"{'='*60}")
    print(f"{'Текст':<15} {'Символов':<10} {'Общий штраф':<12} {'Ср. штраф':<10} {'Левая рука':<12} {'Правая рука':<12}")
    print(f"{'-'*60}")
    for result in all_results:
        print(f"{result['text_name']:<15} {result['characters_analyzed']:<10} {result['total_penalty']:<12} {result['average_penalty']:<10.2f} {result['left_hand_percentage']:<10.1f}% {result['right_hand_percentage']:<10.1f}%")