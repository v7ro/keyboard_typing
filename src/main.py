"""
Модуль анализатора раскладок клавиатуры
Анализирует нагрузку на пальцы при печати на разных раскладках
Рассчитывает пути за движения пальцев от home ряда
Автор: Vero
"""

from keyboard_layouts import (
    keyboard_map, home_positions,
    ytsuken_layout, vyzov_layout, zubachev_layout, 
    skoropis_layout, rusfon_layout, diktor_layout, ant_layout
)

class KeyboardAnalyzer:
    """
    Класс для анализа раскладок клавиатуры.

    Позволяет оценить нагрузку на пальцы при печати текста на различных раскладках.
    Поддерживает анализ пути движения от домашнего ряда, учёт модификаторов (Shift, Alt),
    и статистику по рукам и типам нажатий.
    """
    
    def __init__(self, layout='ytsuken'):
        """
        Инициализирует анализатор клавиатурной раскладки.

        Загружает выбранную раскладку клавиатуры и формирует карту клавиш для анализа.
        Поддерживаются следующие раскладки: 'ytsuken', 'vyzov', 'zubachev', 'skoropis',
        'rusfon', 'diktor', 'ant'.

        Также создаётся универсальная карта клавиатуры, связывающая код клавиши с её
        позицией на физической клавиатуре (ряд, колонка), используемая для расчёта пути
        движения пальцев.

        Args:
            layout: Название раскладки, которую нужно загрузить. По умолчанию — 'ytsuken'.
        """
        self.layout = layout
        self.keyboard_map = keyboard_map
        
        if layout == 'ytsuken':
            self._init_from_layout_data(ytsuken_layout)
        elif layout == 'vyzov':
            self._init_from_layout_data(vyzov_layout)
        elif layout == 'zubachev':
            self._init_from_layout_data(zubachev_layout)
        elif layout == 'skoropis':
            self._init_from_layout_data(skoropis_layout)
        elif layout == 'rusfon':
            self._init_from_layout_data(rusfon_layout)
        elif layout == 'diktor':
            self._init_from_layout_data(diktor_layout)
        elif layout == 'ant':
            self._init_from_layout_data(ant_layout)

    def _init_from_layout_data(self, layout_data):
        """
        Инициализирует раскладку из данных словаря.

        Args:
            layout_data: Словарь с данными раскладки (keys, shift_keys, alt_keys, home_positions)
        """
        self.keys = layout_data['keys']
        self.shift_keys = layout_data.get('shift_keys', {})
        self.alt_keys = layout_data.get('alt_keys', {})
        self.home_positions = layout_data.get('home_positions', home_positions)
        
        # Создаем заглавные буквы автоматически
        self.caps_keys = {}
        for char, (code, finger) in self.keys.items():
            if char.isalpha() and char != ' ':
                self.caps_keys[char.upper()] = (code, finger)

    def _calculate_path(self, key_code, finger):
        """
        Вычисляет путь движения пальца от домашней позиции до заданной клавиши.

        Расстояние рассчитывается как сумма вертикального и горизонтального смещения
        между координатами домашней позиции пальца и целевой клавиши на клавиатуре.

        Для больших пальцев (Shift, Alt, Space) путь считается равным нулю.

        Args:
            key_code: Целочисленный код клавиши (например, 30 для 'ф').
            finger: Название пальца, задействованного при нажатии (например, 'left_index').
        
        Returns:
            Целое число, представляющее путь (количество шагов по рядам и колонкам).
        """
        if finger in ['left_thumb', 'right_thumb']:
            return 0
            
        home_code = self.home_positions[finger]
        
        home_coords = self.keyboard_map.get(home_code)
        target_coords = self.keyboard_map.get(key_code)
        
        if not home_coords or not target_coords:
            return 0
            
        home_row, home_col = home_coords
        target_row, target_col = target_coords
        
        row_diff = abs(target_row - home_row)
        col_diff = abs(target_col - home_col)
        
        path = row_diff + col_diff
        
        return path

    def _load_text_file(self, filename):
        """
        Загружает текст из указанного файла.

        Открывает файл в кодировке UTF-8 и считывает его содержимое.
        В случае ошибки выводит сообщение в консоль и возвращает пустую строку.

        Args:
            filename: Путь к текстовому файлу.
        
        Returns:
            Строка с содержимым файла или пустая строка при ошибке.
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                text = file.read()
                #print(f"Успешно загружен {filename}: {len(text)} символов")
                return text
        except FileNotFoundError:
            print(f"ОШИБКА: Файл {filename} не найден!")
            return ""
        except Exception as e:
            print(f"ОШИБКА загрузки файла {filename}: {e}")
            return ""

    def analyze_text(self, text, text_name, common_chars=None):
        """
        Анализирует текст с точки зрения нагрузки на пальцы при печати на выбранной раскладке.

        Метод рассчитывает:
        - путь движения пальцев от домашней позиции до каждой клавиши,
        - количество нажатий с модификаторами (Shift, Alt),
        - распределение нагрузки по пальцам и рукам,
        - частоту использования левой, правой и обеих рук,
        - среднюю длину пути и количество нажатий на символ.

        Поддерживается фильтрация по общим символам, если задан параметр common_chars.

        Args:
            text: Строка текста для анализа.
            text_name: Название текста (используется в отчёте).
            common_chars: Множество символов, которые следует учитывать (опционально).
        
        Returns:
            Словарь со статистикой по раскладке, включая путь, нагрузку, модификаторы и распределение.
        """
        if not text:
            print(f"Текст {text_name} пустой, пропускаем анализ")
            return None
            
        clean_text = text
        paths = {finger: 0 for finger in [
            'left_pinky', 'left_ring', 'left_middle', 'left_index',
            'right_index', 'right_middle', 'right_ring', 'right_pinky', 
            'left_thumb', 'right_thumb'
        ]}
        
        finger_counts = {finger: 0 for finger in paths.keys()}
        total_path = 0
        shift_count = 0
        alt_count = 0
        character_count = len(clean_text)

        # НОВАЯ ЛОГИКА: считаем распределение рук
        left_hand_letters = 0      # Буквы, набранные левой рукой
        right_hand_letters = 0     # Буквы, набранные правой рукой  
        hand_switches = 0          # Смены рук (переход от левой к правой или наоборот)
        total_presses = 0          # Общее количество нажатий
        
        # Определяем какие пальцы к каким рукам относятся
        left_hand_fingers = ['left_pinky', 'left_ring', 'left_middle', 'left_index', 'left_thumb']
        right_hand_fingers = ['right_pinky', 'right_ring', 'right_middle', 'right_index', 'right_thumb']

        # Переменная для отслеживания предыдущей руки
        previous_hand = None  # None, 'left', или 'right'
        
        for char in clean_text:
            # Собираем ВСЕ возможные варианты для этого символа
            options = []
            current_hand = None
            
            # Вариант 1: обычная буква
            if char in self.keys:
                key_code, finger = self.keys[char]
                path = self._calculate_path(key_code, finger)
                options.append(('normal', path, key_code, finger, 0, None))
                # Определяем руку для основной клавиши
                if finger in left_hand_fingers:
                    current_hand = 'left'
                    left_hand_letters += 1
                elif finger in right_hand_fingers:
                    current_hand = 'right' 
                    right_hand_letters += 1
            
            # Вариант 2: заглавная буква (буква + Shift)
            if char in getattr(self, 'caps_keys', {}):
                key_code, finger = self.caps_keys[char]
                path = self._calculate_path(key_code, finger)
                options.append(('caps', path + 1, key_code, finger, 1, 'left_thumb'))
                # Определяем руку для основной клавиши
                if finger in left_hand_fingers:
                    current_hand = 'left'
                    left_hand_letters += 1
                elif finger in right_hand_fingers:
                    current_hand = 'right'
                    right_hand_letters += 1
            
            # Вариант 3: Shift-символ
            if char in getattr(self, 'shift_keys', {}):
                key_code, finger = self.shift_keys[char]
                path = self._calculate_path(key_code, finger)
                options.append(('shift', path + 1, key_code, finger, 1, 'left_thumb'))
                # Определяем руку для основной клавиши
                if finger in left_hand_fingers:
                    current_hand = 'left'
                    left_hand_letters += 1
                elif finger in right_hand_fingers:
                    current_hand = 'right'
                    right_hand_letters += 1
            
            # Вариант 4: Alt-символ
            if char in getattr(self, 'alt_keys', {}):
                key_code, finger = self.alt_keys[char]
                path = self._calculate_path(key_code, finger)
                options.append(('alt', path + 1, key_code, finger, 1, 'right_thumb'))
                # Определяем руку для основной клавиши
                if finger in left_hand_fingers:
                    current_hand = 'left'
                    left_hand_letters += 1
                elif finger in right_hand_fingers:
                    current_hand = 'right'
                    right_hand_letters += 1
            
            if options:
                # Выбираем вариант с минимальным общим путем
                best_option = min(options, key=lambda x: x[1])
                mode, total_path_option, key_code, finger, mod_cost, mod_finger = best_option
                
                # Считаем основную клавишу
                finger_counts[finger] += 1
                paths[finger] += total_path_option - mod_cost
                total_path += total_path_option
                total_presses += 1
                
                # Считаем модификатор если есть
                if mod_cost > 0 and mod_finger:
                    finger_counts[mod_finger] += 1
                    paths[mod_finger] += 1
                    total_path += 1
                    total_presses += 1
                    
                    if mode in ['caps', 'shift']:
                        shift_count += 1
                    elif mode == 'alt':
                        alt_count += 1
                
                # Считаем смены рук (только для букв, не для пробелов и т.д.)
                if current_hand and previous_hand and current_hand != previous_hand:
                    hand_switches += 1
                
                # Обновляем предыдущую руку
                if current_hand:
                    previous_hand = current_hand
        
        average_path = total_path / character_count if character_count > 0 else 0
        
        # Статистика по рукам на основе finger_counts
        left_hand_count = sum(finger_counts[f] for f in left_hand_fingers)
        right_hand_count = sum(finger_counts[f] for f in right_hand_fingers)
        total_hand_count = left_hand_count + right_hand_count
        
        left_hand_percentage = (left_hand_count / total_hand_count * 100) if total_hand_count > 0 else 0
        right_hand_percentage = (right_hand_count / total_hand_count * 100) if total_hand_count > 0 else 0
        
        # Проценты для распределения рук
        total_letters = left_hand_letters + right_hand_letters
        left_hand_letters_percentage = (left_hand_letters / total_letters * 100) if total_letters > 0 else 0
        right_hand_letters_percentage = (right_hand_letters / total_letters * 100) if total_letters > 0 else 0
        
        return {
                'text_name': text_name,
                'layout': self.layout,
                'total_path': total_path,
                'finger_paths': paths,
                'finger_counts': finger_counts,
                'characters_analyzed': character_count,
                'shift_count': shift_count,
                'alt_count': alt_count,
                'average_path': average_path,
                'left_hand_count': left_hand_count,
                'right_hand_count': right_hand_count,
                'left_hand_percentage': left_hand_percentage,
                'right_hand_percentage': right_hand_percentage,
                'left_hand_letters': left_hand_letters,           # буквы левой рукой
                'right_hand_letters': right_hand_letters,         # буквы правой рукой
                'hand_switches': hand_switches,                   # смены рук
                'total_presses': total_presses,
                'average_presses_per_char': total_presses / character_count if character_count > 0 else 0,
                'left_hand_letters_percentage': left_hand_letters_percentage,
                'right_hand_letters_percentage': right_hand_letters_percentage,
                'hand_switches_per_100_chars': (hand_switches / character_count * 100) if character_count > 0 else 0,
            }
    def analyze_all_files(self, common_chars=None): 
        """
        Последовательно анализирует три предопределённых текстовых файла с раскладкой клавиатуры.

        Для каждого файла:
        - загружает текст,
        - фильтрует символы (если задан common_chars),
        - рассчитывает статистику по пути, нагрузке и модификаторам.

        Используется для пакетного анализа и сравнения раскладок на разных типах текстов.

        Args:
            common_chars: Множество символов, которые следует учитывать при анализе (опционально).
        
        Returns:
            Список словарей с результатами анализа для каждого файла.
        """
        files_to_analyze = [
            ('voina_i_mir.txt', 'Война и мир'),
            ('sortchbukw.csv', 'Сортировка букв'),
            ('1grams.txt', 'Минимальные фразы')
        ]
        
        results = []
        
        for filename, text_name in files_to_analyze:
            #print(f"\n--- Загрузка {filename} ---")
            text = self._load_text_file(filename)
            if text:
                result = self.analyze_text(text, text_name, common_chars)
                if result:
                    results.append(result)
        return results

    def print_results(self, results):
        """
        Выводит результаты анализа текстов в консоль в структурированном виде.

        Для каждого текста отображается:
        - общее количество символов и путь движения пальцев,
        - средняя нагрузка на символ и общее количество нажатий,
        - статистика по модификаторам (Shift, Alt),
        - распределение нагрузки между руками,
        - типы нажатий (одноручные и двуручные),
        - нагрузка по каждому пальцу с процентным соотношением.

        Args:
            results: Список словарей, полученных из метода analyze_text, содержащих статистику по раскладке.
        """
        for result in results:
            #print(f"\n{'='*60}")
            #print(f"=== АНАЛИЗ ПУТЕЙ ДЛЯ: {result['text_name']} ===")
            #print(f"=== РАСКЛАДКА: {result['layout']} ===")
            #print(f"{'='*60}")
            #print(f"Всего проанализировано символов: {result['characters_analyzed']}")
            #print(f"ОБЩИЙ ПУТЬ: {result['total_path']}")
            #print(f"СРЕДНИЙ ПУТЬ НА СИМВОЛ: {result['average_path']:.2f}")
            #print(f"ОБЩЕЕ КОЛИЧЕСТВО НАЖАТИЙ: {result['total_presses']}")
            #print(f"СРЕДНЕЕ НАЖАТИЙ НА СИМВОЛ: {result['average_presses_per_char']:.2f}")
            #print(f"Количество Shift-символов: {result['shift_count']}")
            #print(f"Количество Alt-символов: {result['alt_count']}")

            #print(f"\nРаспределение по рукам:")
            #print(f"Левая рука: {result['left_hand_count']} нажатий ({result['left_hand_percentage']:.1f}%)")
            #print(f"Правая рука: {result['right_hand_count']} нажатий ({result['right_hand_percentage']:.1f}%)")

            #print(f"\nТипы нажатий:")
            #print(f"  Только левая рука: {result['left_hand_only']} ({result['left_hand_only_percentage']:.1f}%)")
            #print(f"  Только правая рука: {result['right_hand_only']} ({result['right_hand_only_percentage']:.1f}%)")
            #print(f"  Двуручные: {result['two_handed']} ({result['two_handed_percentage']:.1f}%)")
            #print(f"    - Shift + буква: {result['shift_count']}")
            #print(f"    - Alt + буква: {result['alt_count']}")

            print(f"\nНагрузка по пальцам:")
            total_presses = sum(result['finger_counts'].values())
            for finger in ['left_pinky', 'left_ring', 'left_middle', 'left_index', 
                          'right_index', 'right_middle', 'right_ring', 'right_pinky', 
                          'left_thumb', 'right_thumb']:
                count = result['finger_counts'][finger]
                if count > 0:  # Показываем только пальцы с ненулевой нагрузкой
                    percentage = (count / total_presses * 100)
                    print(f"  {finger}: {count} нажатий ({percentage:.1f}%)")

    def print_improved_results(self, results):
        """Улучшенный вывод результатов с акцентом на пробел"""
        for result in results:
            print(f"\n{'='*60}")
            print(f"=== УЛУЧШЕННЫЙ АНАЛИЗ: {result['text_name']} ===")
            print(f"=== РАСКЛАДКА: {result['layout']} ===")
            print(f"{'='*60}")
            
            total_presses = sum(result['finger_counts'].values())
            
            # Процентное распределение
            print("НАГРУЗКА ПО ПАЛЬЦАМ (%):")
            finger_names = {
                'left_pinky': 'Лев. мизинец', 'left_ring': 'Лев. безым.', 
                'left_middle': 'Лев. средний', 'left_index': 'Лев. указ.',
                'right_index': 'Прав. указ.', 'right_middle': 'Прав. средний',
                'right_ring': 'Прав. безым.', 'right_pinky': 'Прав. мизинец',
                'left_thumb': 'Лев. большой', 'right_thumb': 'Прав. большой'
            }
            
            for finger in ['left_pinky', 'left_ring', 'left_middle', 'left_index', 
                          'right_index', 'right_middle', 'right_ring', 'right_pinky', 
                          'left_thumb', 'right_thumb']:
                count = result['finger_counts'][finger]
                percentage = (count / total_presses * 100)
                if count > 0:
                    print(f"  {finger_names[finger]:<15} {count:>4} нажатий ({percentage:>5.1f}%)")
            
            # Анализ пробела
            space_percentage = (result['finger_counts']['right_thumb'] / total_presses * 100)
            print(f"\nОСОБЕННОСТИ РАСКЛАДКИ:")
            print(f"  • Пробел (правый большой): {space_percentage:.1f}")
            print(f"  • Alt/Shift (левый большой): {(result['finger_counts']['left_thumb'] / total_presses * 100):.1f}%")
            print(f"  • Соотношение рук: Левая {result['left_hand_percentage']:.1f}% / Правая {result['right_hand_percentage']:.1f}%")


def get_common_chars():
    """
    Возвращает множество символов, общих для всех раскладок клавиатуры.

    Включает:
    - базовые русские буквы (а–я, ё, пробел),
    - часто используемые спецсимволы, доступные через Shift во всех раскладках.

    Используется для унифицированного анализа раскладок по ограниченному набору символов.

    Returns:
        Множество символов, пригодных для сравнения раскладок.
    """
    # Базовые русские буквы + пробел + общие символы
    basic_russian = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя ')
    
    # Общие символы из shift (которые есть во всех раскладках)
    common_shift = set('!№;%*()+/,.')
    
    return basic_russian.union(common_shift)


# Запуск для всех раскладок с ОБЩИМИ СИМВОЛАМИ
print("="*70)
print("СРАВНЕНИЕ РАСКЛАДОК НА ОБЩИХ СИМВОЛАХ")
print("="*70)

# Получаем общие символы
common_chars = get_common_chars()
print(f"Используется общих символов: {len(common_chars)}")
print(f"Общие символы: {''.join(sorted(common_chars))}")

# Анализ для каждой раскладки
layouts = [
    ('ytsuken', 'СТАНДАРТНАЯ'),
    ('vyzov', 'ВЫЗОВ'), 
    ('zubachev', 'ЗУБАЧЕВ'),
    ('skoropis', 'СКОРОПИСЬ'),
    ('rusfon', 'РУСФОН'),
    ('diktor', 'ДИКТОР'),
    ('ant', 'АНТ')
]

all_results = {}


def analyze_all_layouts_optimized():
    """Оптимизированный анализ всех раскладок с выбором текста"""
    print("="*70)
    print("УСКОРЕННЫЙ АНАЛИЗ РАСКЛАДОК")
    print("="*70)
    
    # МЕНЮ ВЫБОРА ТЕКСТА
    print("\nВЫБЕРИТЕ ТЕКСТ ДЛЯ АНАЛИЗА:")
    print("1 - Война и мир (большой художественный текст)")
    print("2 - Сортировка букв (частотный анализ)")
    print("3 - Минимальные фразы (первые 1000 слов)")
    print("4 - Все тексты")
    
    try:
        choice = input("Введите номер (1-4): ").strip()
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
        return
    
    files_to_analyze = []
    
    if choice == "1":
        files_to_analyze = [('voina_i_mir.txt', 'Война и мир')]
        print("Выбран: Война и мир")
    elif choice == "2":
        files_to_analyze = [('sortchbukw.csv', 'Сортировка букв')]
        print("Выбран: Сортировка букв")
    elif choice == "3":
        files_to_analyze = [('1grams.txt', 'Минимальные фразы')]
        print("Выбран: Минимальные фразы (первые 1000 слов)")
    elif choice == "4":
        files_to_analyze = [
            ('voina_i_mir.txt', 'Война и мир'),
            ('sortchbukw.csv', 'Сортировка букв'), 
            ('1grams.txt', 'Минимальные фразы')
        ]
        print("Выбраны все тексты")
    else:
        print("Неверный выбор! Загружаются все тексты по умолчанию")
        files_to_analyze = [
            ('voina_i_mir.txt', 'Война и мир'),
            ('sortchbukw.csv', 'Сортировка букв'), 
            ('1grams.txt', 'Минимальные фразы')
        ]
    
    # ЗАГРУЖАЕМ ВЫБРАННЫЕ ТЕКСТЫ
    texts_data = []
    
    print("\nЗагрузка текстов...")
    for filename, text_name in files_to_analyze:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                text = file.read()
                # ДЛЯ ФАЙЛА С ЛЕКСЕМАМИ БЕРЕМ ТОЛЬКО ПЕРВУЮ 1000 СЛОВ
                if filename == '1grams.txt':
                    words = text.split()[:1000]
                    text = ' '.join(words)
                    print(f"  ✓ Загружено {len(words)} слов из {text_name}")
                else:
                    print(f"  ✓ Загружен {text_name}: {len(text):,} символов".replace(',', ' '))
                texts_data.append((text, text_name))
        except FileNotFoundError:
            print(f"  ✗ ОШИБКА: Файл {filename} не найден!")
        except Exception as e:
            print(f"  ✗ ОШИБКА загрузки {filename}: {e}")
    
    if not texts_data:
        print("Нет данных для анализа!")
        return
    
    common_chars = get_common_chars()
    layouts = [
        ('ytsuken', 'СТАНДАРТНАЯ'),
        ('vyzov', 'ВЫЗОВ'), 
        ('zubachev', 'ЗУБАЧЕВ'),
        ('skoropis', 'СКОРОПИСЬ'),
        ('rusfon', 'РУСФОН'),
        ('diktor', 'ДИКТОР'),
        ('ant', 'АНТ')
    ]
    
    all_results = {}
    
    print(f"\nАнализ {len(layouts)} раскладок...")
    for layout_code, layout_name in layouts:
        print(f"  Анализируем {layout_name}...")
        analyzer = KeyboardAnalyzer(layout=layout_code)
        layout_results = []
        
        for text, text_name in texts_data:
            result = analyzer.analyze_text(text, text_name, common_chars)
            if result:
                layout_results.append(result)
        
        if layout_results:
            all_results[layout_code] = layout_results
    
    # ВЫВОД РЕЗУЛЬТАТОВ
    print(f"\n{'='*140}")
    print("СВОДНАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ")
    print(f"{'='*140}")
    print(f"{'Текст':<18} {'Раскладка':<12} {'Символов':<10} {'Нажатий':<10} {'Наж/симв':<10} {'Общий путь':<12} {'Ср. путь':<10} {'Левая':<8} {'Правая':<8} {'Смены':<8}")
    print(f"{'-'*140}")

    layout_display_names = {
        'ytsuken': 'Стандарт', 'vyzov': 'Вызов', 'zubachev': 'Зубачев',
        'skoropis': 'Скоропись', 'rusfon': 'Русфон', 'diktor': 'Диктор', 'ant': 'Ант'
    }

    for i in range(len(texts_data)):
        for layout_code, layout_name in layouts:
            if layout_code in all_results and i < len(all_results[layout_code]):
                result = all_results[layout_code][i]
                layout_display_name = layout_display_names.get(layout_code, layout_code)
                
                print(f"{result['text_name']:<18} {layout_display_name:<12} {result['characters_analyzed']:<10} "
                    f"{result['total_presses']:<10} {result['average_presses_per_char']:<10.2f} "
                    f"{result['total_path']:<12} {result['average_path']:<10.2f} "
                    f"{result['left_hand_letters_percentage']:<7.1f} {result['right_hand_letters_percentage']:<7.1f} "
                    f"{result['hand_switches_per_100_chars']:<7.1f}")
                        
        if i < len(texts_data) - 1:
            print(f"{'-'*140}")
    
    print(f"\nАнализ завершен! Проанализировано {len(texts_data)} текстов и {len(layouts)} раскладок.")

# ЗАПУСКАЕМ ОПТИМИЗИРОВАННУЮ ВЕРСИЮ
analyze_all_layouts_optimized()