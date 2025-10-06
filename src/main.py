"""
Модуль анализатора раскладок клавиатуры
Анализирует нагрузку на пальцы при печати на разных раскладках
Рассчитывает штрафы за движения пальцев от home ряда
Автор: Vero
"""

class KeyboardAnalyzer:
    def __init__(self):
        self.text = self._load_text()
        
        # Объединяем все в один словарь: буква -> (код, палец)
        self.keys = {
            'й': (16, 'left_pinky'), 'ф': (30, 'left_pinky'), 'я': (44, 'left_pinky'),
            'ц': (17, 'left_ring'), 'ы': (31, 'left_ring'), 'ч': (45, 'left_ring'),
            'у': (18, 'left_middle'), 'в': (32, 'left_middle'), 'с': (46, 'left_middle'),
            'к': (19, 'left_index'), 'а': (33, 'left_index'), 'м': (47, 'left_index'), 'и': (34, 'left_index'),
            'н': (20, 'right_index'), 'р': (35, 'right_index'), 'т': (48, 'right_index'), 'ь': (49, 'right_index'),
            'г': (21, 'right_middle'), 'о': (36, 'right_middle'), 'б': (50, 'right_middle'),
            'ш': (22, 'right_ring'), 'л': (37, 'right_ring'), 'ю': (51, 'right_ring'),
            'щ': (23, 'right_pinky'), 'д': (38, 'right_pinky'), 'э': (52, 'right_pinky'),
            'ж': (24, 'right_pinky'), 'з': (25, 'right_pinky'), 'х': (26, 'right_pinky'), 'ъ': (27, 'right_pinky'),
            '.': (39, 'right_pinky'), ',': (40, 'right_pinky'),
            ' ': (57, 'thumbs')
        }

    def _get_penalty(self, key_code, finger):
        """Штраф для слепой печати"""
        if finger == 'thumbs':  # Пробел - нет штрафа
            return 0
            
        if 2 <= key_code <= 14:    return 2   # digit row
        elif 16 <= key_code <= 27: return 1   # upper row  
        elif 30 <= key_code <= 40: return 0   # home row
        elif 44 <= key_code <= 54: return 1   # lower row
        return 0

    def _load_text(self):
        """Загрузка текста"""
        try:
            with open('voina_i_mir.txt', 'r', encoding='utf-8') as file:
                text = file.read()
                print(f"Успешно загружен Война и мир: {len(text)} символов")
                return text
        except FileNotFoundError:
            print("ОШИБКА: Файл voina_i_mir.txt не найден!")
            return "война и мир " * 100
        except Exception as e:
            print(f"ОШИБКА загрузки файла: {e}")
            return "война и мир " * 100

    def analyze(self):
        """Основной анализ штрафов"""
        # Фильтруем русский текст
        clean_text = ''.join(c for c in self.text.lower() if c in self.keys)
        
        penalties = {finger: 0 for finger in [
            'left_pinky', 'left_ring', 'left_middle', 'left_index',
            'right_index', 'right_middle', 'right_ring', 'right_pinky', 'thumbs'
        ]}
        
        total_penalty = 0

        for char in clean_text:
            key_code, finger = self.keys[char]
            penalty = self._get_penalty(key_code, finger)
            penalties[finger] += penalty
            total_penalty += penalty
        
        return {
            'total_penalty': total_penalty,
            'finger_penalties': penalties,
            'characters_analyzed': len(clean_text)
        }


# Запуск
analyzer = KeyboardAnalyzer()
results = analyzer.analyze()

print("=== АНАЛИЗ ШТРАФОВ ДЛЯ РАСКЛАДКИ ===")
print(f"Всего проанализировано символов: {results['characters_analyzed']}")
print(f"ОБЩИЙ ШТРАФ: {results['total_penalty']}")
print("\nШтрафы по пальцам:")
for finger, penalty in results['finger_penalties'].items():
    print(f"  {finger}: {penalty}")