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
        self.finger_counts = {}  
        
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
        Инициализирует объект раскладки клавиатуры на основе словаря данных.

        Логика:
        - сохраняет основные клавиши (`keys`),
        - добавляет дополнительные словари для клавиш с Shift, Alt и позиций на "домашней строке",
        - автоматически формирует словарь `caps_keys` для заглавных букв на основе `keys`.

        Args:
            layout_data (dict): Словарь с данными раскладки, содержащий:
                - 'keys' (dict): основные клавиши и их назначение (код, палец),
                - 'shift_keys' (dict, optional): клавиши, доступные через Shift,
                - 'alt_keys' (dict, optional): клавиши, доступные через Alt,
                - 'home_positions' (dict, optional): позиции пальцев на домашней строке.
        Returns:
            None: метод изменяет внутреннее состояние объекта.
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
            finger: Обозначение пальца (например, 'lf2').
        
        Returns:
            Целое число, представляющее путь (количество шагов по рядам и колонкам).
        """
        if finger in ['lf1', 'rf1']:  # Большие пальцы
            return 0
            
        home_code = self.home_positions.get(finger)
        if not home_code:
            return 0
            
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
                return text
        except FileNotFoundError:
            print(f"ОШИБКА: Файл {filename} не найден!")
            return ""
        except Exception as e:
            print(f"ОШИБКА загрузки файла {filename}: {e}")
            return ""
    
    def analyze_combinations(self, text):
        """
        АНАЛИЗ КОМБИНАЦИЙ ПО НОВОЙ ЛОГИКЕ:
        
        1. Берем ВСЕ возможные биграммы (пары подряд идущих букв)
        - Если разные руки → неудобное
        - Если одна рука → смотрим направление движения
        
        2. Трехграммы: Берем ВСЕ возможные тройки подряд идущих букв
        - Но анализируем только если ВСЕ 3 буквы на одной руке
        - Если есть смена руки внутри тройки → не анализируем эту тройку
        
        3. Четырехграммы: Берем ВСЕ возможные четверки подряд идущих букв
        - Но анализируем только если ВСЕ 4 буквы на одной руке
        - Если есть смена руки внутри четверки → не анализируем эту четверку
        """
        # Очищаем текст - оставляем только русские буквы
        clean_text = ''.join([c.lower() for c in text if c.lower() in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'])
        
        results = {
            'двухграммы': {'удобные': 0, 'частично_удобные': 0, 'неудобные': 0, 'всего': 0},
            'трехграммы': {'удобные': 0, 'частично_удобные': 0, 'всего': 0},
            'четырехграммы': {'удобные': 0, 'частично_удобные': 0, 'всего': 0}
        }
        
        # Разбиваем на слова
        import re
        words = re.findall(r'[а-яё]+', clean_text)
        
        for word in words:
            # 1. АНАЛИЗ ВСЕХ БИГРАММ (2 буквы)
            if len(word) >= 2:
                for i in range(len(word) - 1):
                    bigram = word[i:i+2]
                    comfort = self._analyze_bigram_comfort(bigram)
                    results['двухграммы'][comfort] += 1
                    results['двухграммы']['всего'] += 1
            
            # 2. АНАЛИЗ ТРЕХГРАММ (3 буквы) - только если все на одной руке
            if len(word) >= 3:
                for i in range(len(word) - 2):
                    trigram = word[i:i+3]
                    
                    # Проверяем, что ВСЕ 3 буквы на одной руке
                    hands = set()
                    valid = True
                    
                    for letter in trigram:
                        finger = self._get_finger_for_char(letter)
                        if not finger:
                            valid = False
                            break
                        hands.add(finger[0])  # 'l' или 'r'
                    
                    # Если все пальцы найдены и все на одной руке
                    if valid and len(hands) == 1:
                        comfort = self._analyze_trigram_comfort(trigram)
                        results['трехграммы'][comfort] += 1
                        results['трехграммы']['всего'] += 1
            
            # 3. АНАЛИЗ ЧЕТЫРЕХГРАММ (4 буквы) - только если все на одной руке
            if len(word) >= 4:
                for i in range(len(word) - 3):
                    fourgram = word[i:i+4]
                    
                    # Проверяем, что ВСЕ 4 буквы на одной руке
                    hands = set()
                    valid = True
                    
                    for letter in fourgram:
                        finger = self._get_finger_for_char(letter)
                        if not finger:
                            valid = False
                            break
                        hands.add(finger[0])  # 'l' или 'r'
                    
                    # Если все пальцы найдены и все на одной руке
                    if valid and len(hands) == 1:
                        comfort = self._analyze_fourgram_comfort(fourgram)
                        results['четырехграммы'][comfort] += 1
                        results['четырехграммы']['всего'] += 1
        
        return results
    
    def _analyze_bigram_comfort(self, bigram):
        """
        Оценивает удобство двухбуквенной комбинации (биграммы).

        Логика анализа:
        - если длина последовательности не равна 2, комбинация считается неудобной;
        - определяется палец для каждого символа через `_get_finger_for_char`;
        - если хотя бы один символ не имеет соответствия → 'неудобные';
        - если символы принадлежат разным рукам → 'неудобные';
        - если символы одной руки:
            * извлекаются номера пальцев (lf5=5, lf4=4, lf3=3, lf2=2 и т.д.),
            * направление движения определяется разницей номеров:
                - движение от мизинца к указательному (убывающая последовательность) → 'удобные',
                - движение от указательного к мизинцу (возрастающая последовательность) → 'частично_удобные'.

        Args:
            bigram (str): Строка из 2 символов для анализа.

        Returns:
            str: Оценка удобства комбинации:
                - 'удобные',
                - 'частично_удобные',
                - 'неудобные'.
            """
        if len(bigram) != 2:
            return 'неудобные'
            
        char1, char2 = bigram[0], bigram[1]
            
        # Получаем пальцы для каждого символа
        finger1 = self._get_finger_for_char(char1)
        finger2 = self._get_finger_for_char(char2)
            
        if finger1 is None or finger2 is None:
            return 'неудобные'
            
        # Проверяем, одна ли рука
        hand1 = finger1[0]  # 'l' или 'r'
        hand2 = finger2[0]
            
        if hand1 != hand2:
            return 'неудобные'  # Смена руки = неудобно
            
        # Получаем номера пальцев
        finger_num1 = int(finger1[2]) if len(finger1) >= 3 and finger1[2].isdigit() else None
        finger_num2 = int(finger2[2]) if len(finger2) >= 3 and finger2[2].isdigit() else None
            
        if finger_num1 is None or finger_num2 is None:
            return 'частично_удобные'
            
        # УДОБНЫЕ: от мизинца к указательному
        if finger_num1 > finger_num2:
            return 'удобные'
            
        # ЧАСТИЧНО УДОБНЫЕ: от указательного к мизинцу
        elif finger_num1 < finger_num2:
            return 'частично_удобные'
            
        # Одинаковые пальцы
        return 'частично_удобные'
    
    def _analyze_trigram_comfort(self, trigram):
        """
        Оценивает удобство трёхбуквенной комбинации (трёхграммы).

        Логика анализа:
        - если длина последовательности не равна 3, комбинация считается частично удобной;
        - для каждой пары символов внутри трёхграммы (2 биграммы) вызывается
          метод `_analyze_bigram_comfort`;
        - если хотя бы одна пара неудобная → вся трёхграмма 'частично_удобные';
        - если обе пары удобные → выполняется дополнительная проверка:
            * определяется палец для каждого символа,
            * извлекаются номера пальцев,
            * если движение идёт последовательно от мизинца к указательному
              (убывающая последовательность номеров), комбинация считается 'удобные',
              иначе — 'частично_удобные';
        - во всех остальных случаях результат — 'частично_удобные'.

        Args:
            trigram (str): Строка из 3 символов для анализа.

        Returns:
            str: Оценка удобства комбинации:
                - 'удобные',
                - 'частично_удобные'.
        """
        if len(trigram) != 3:
            return 'частично_удобные'
        
        # Получаем пальцы для всех трех символов
        finger1 = self._get_finger_for_char(trigram[0])
        finger2 = self._get_finger_for_char(trigram[1])
        finger3 = self._get_finger_for_char(trigram[2])
        
        if not (finger1 and finger2 and finger3):
            return 'частично_удобные'
        
        # Получаем номера пальцев
        num1 = int(finger1[2]) if len(finger1) >= 3 and finger1[2].isdigit() else None
        num2 = int(finger2[2]) if len(finger2) >= 3 and finger2[2].isdigit() else None
        num3 = int(finger3[2]) if len(finger3) >= 3 and finger3[2].isdigit() else None
        
        if num1 is None or num2 is None or num3 is None:
            return 'частично_удобные'
        
        # ВАЖНОЕ ИЗМЕНЕНИЕ! 
        # УДОБНЫЕ: движение от мизинца к указательному, НО НЕ ОБЯЗАТЕЛЬНО СТРОГОЕ УБЫВАНИЕ!
        # 5→4→3, 5→4→2, 5→3→2, 4→3→2, 5→3→3 и т.д.
        # Если первая буква на мизинце (5) и общее движение вниз к указательному
        
        # Более гибкая логика:
        # Если все три пальца разные и идут от большего к меньшему
        if num1 > num2 and num2 > num3:  # строгое убывание
            return 'удобные'
        # Если движение в целом от мизинца к указательному
        elif num1 > num3:  # первая буква на пальце с большим номером чем последняя
            return 'удобные'
        
        # ВСЕ остальное - частично удобные
        return 'частично_удобные'

    
    def _analyze_fourgram_comfort(self, fourgram):
        """
        Оценивает удобство четырёхбуквенной комбинации (четырёхграммы).

        Логика анализа:
        - если длина последовательности не равна 4, комбинация считается частично удобной;
        - для каждой пары символов внутри четырёхграммы (3 биграммы) вызывается
          метод `_analyze_bigram_comfort`, результаты собираются;
        - подсчитывается количество удобных, частично удобных и неудобных пар;
        - итоговая оценка:
            * ≥2 неудобных пар → 'частично_удобные',
            * 1 неудобная или ≥2 частично удобных → 'частично_удобные',
            * иначе выполняется дополнительная проверка:
                - определяется палец для каждого символа,
                - извлекаются номера пальцев,
                - если движение идёт последовательно от мизинца к указательному
                  (убывающая последовательность номеров), комбинация считается 'удобные',
                  иначе — 'частично_удобные'.

        Args:
            fourgram (str): Строка из 4 символов для анализа.

        Returns:
            str: Оценка удобства комбинации:
                - 'удобные',
                - 'частично_удобные'.
        """
        if len(fourgram) != 4:
            return 'частично_удобные'
        
        # Получаем пальцы для всех четырех символов
        fingers = []
        for char in fourgram:
            finger = self._get_finger_for_char(char)
            if not finger:
                return 'частично_удобные'
            fingers.append(finger)
        
        # Получаем номера пальцев
        nums = []
        for finger in fingers:
            num = int(finger[2]) if len(finger) >= 3 and finger[2].isdigit() else None
            if num is None:
                return 'частично_удобные'
            nums.append(num)
        
        # ВАЖНОЕ ИЗМЕНЕНИЕ!
        # Более гибкая логика для 4-грамм
        
        # Проверяем общее направление от мизинца к указательному
        if nums[0] > nums[-1]:  # первая буква на пальце с большим номером чем последняя
            # Если есть хотя бы одно движение вниз
            descending_count = 0
            for i in range(3):
                if nums[i] > nums[i+1]:
                    descending_count += 1
            
            if descending_count >= 2:  # хотя бы 2 движения вниз из 3
                return 'удобные'
        
        # ВСЕ остальное - частично удобные
        return 'частично_удобные'
    
    def _get_finger_for_char(self, char):
        """
        Определяет палец, используемый для нажатия заданного символа.

        Логика:
        - для пробела (' ') ищется правый большой палец (rf1, thumb, right),
          при отсутствии явного соответствия используется fallback 'rf1';
        - для остальных символов проверяются словари раскладки:
          * self.keys — основные клавиши,
          * self.caps_keys — клавиши с Caps,
          * self.shift_keys — клавиши с Shift,
          * self.alt_keys — клавиши с Alt.

        Args:
            char (str): Символ, для которого требуется определить палец.

        Returns:
            str | None: Код пальца (например, 'lf2', 'rf1'), либо None,
            если символ не найден в раскладке.
        """
        if char == ' ':
            # Ищем правый большой палец
            for finger_name in self.keys.values():
                if isinstance(finger_name, tuple) and len(finger_name) > 1:
                    finger = finger_name[1]
                    if 'right' in finger or 'rf1' in finger or 'thumb' in finger:
                        return finger
            return 'rf1'  # fallback
        
        if char in self.keys:
            return self.keys[char][1]
        elif char in getattr(self, 'caps_keys', {}):
            return self.caps_keys[char][1]
        elif char in getattr(self, 'shift_keys', {}):
            return self.shift_keys[char][1]
        elif char in getattr(self, 'alt_keys', {}):
            return self.alt_keys[char][1]
        
        return None

    def analyze_text(self, text, text_name, common_chars=None):
        """
        Анализирует текст с точки зрения нагрузки на пальцы при печати на выбранной раскладке.

        Метод рассчитывает:
        - путь движения пальцев от домашней позиции до каждой клавиши,
        - количество нажатий с модификаторов (Shift, Alt),
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
        
        # ВАЖНО: получаем все пальцы из раскладки, а не предопределенный список
        # Сначала получаем уникальные пальцы из всех возможных комбинаций
        all_fingers = set()
        
        # Добавляем пальцы из обычных клавиш
        for char, (code, finger) in self.keys.items():
            all_fingers.add(finger)
        
        # Добавляем пальцы из заглавных букв
        for char, (code, finger) in getattr(self, 'caps_keys', {}).items():
            all_fingers.add(finger)
        
        # Добавляем пальцы из shift клавиш
        for char, (code, finger) in getattr(self, 'shift_keys', {}).items():
            all_fingers.add(finger)
        
        # Добавляем пальцы из alt клавиш
        for char, (code, finger) in getattr(self, 'alt_keys', {}).items():
            all_fingers.add(finger)
        
        # Инициализируем словари с ВСЕМИ пальцами из этой раскладки
        paths = {finger: 0 for finger in all_fingers}
        finger_counts = {finger: 0 for finger in all_fingers}
        
        total_path = 0
        shift_count = 0
        alt_count = 0
        character_count = len(clean_text)

        # Определяем какие пальцы к каким рукам относятся
        # Сначала определим левые пальцы
        left_hand_fingers = [f for f in all_fingers if f.startswith('l') or f.startswith('left')]
        right_hand_fingers = [f for f in all_fingers if f.startswith('r') or f.startswith('right')]
        
        # Если не нашли по префиксам, пробуем другие варианты
        if not left_hand_fingers:
            # Предполагаемые обозначения левых пальцев
            left_hand_fingers = ['lf5', 'lf4', 'lf3', 'lf2', 'lf1', 'left_pinky', 'left_ring', 
                                'left_middle', 'left_index', 'left_thumb']
        if not right_hand_fingers:
            # Предполагаемые обозначения правых пальцев
            right_hand_fingers = ['rf5', 'rf4', 'rf3', 'rf2', 'rf1', 'right_pinky', 'right_ring',
                                 'right_middle', 'right_index', 'right_thumb']

        # НОВАЯ ЛОГИКА: считаем распределение рук
        left_hand_letters = 0      # Буквы, набранные левой рукой
        right_hand_letters = 0     # Буквы, набранные правой рукой  
        hand_switches = 0          # Смены рук (переход от левой к правой или наоборот)
        total_presses = 0          # Общее количество нажатий

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
                if any(finger.startswith(lhf[0]) or finger == lhf for lhf in left_hand_fingers):
                    current_hand = 'left'
                    left_hand_letters += 1
                elif any(finger.startswith(rhf[0]) or finger == rhf for rhf in right_hand_fingers):
                    current_hand = 'right' 
                    right_hand_letters += 1
            
            # Вариант 2: заглавная буква (буква + Shift)
            if char in getattr(self, 'caps_keys', {}):
                key_code, finger = self.caps_keys[char]
                path = self._calculate_path(key_code, finger)
                # Ищем большой палец для Shift
                shift_finger = None
                for f in left_hand_fingers:
                    if 'thumb' in f or '1' in f or f == 'lf1':
                        shift_finger = f
                        break
                if not shift_finger:
                    shift_finger = 'lf1'  # fallback
                    
                options.append(('caps', path + 1, key_code, finger, 1, shift_finger))
                # Определяем руку для основной клавиши
                if any(finger.startswith(lhf[0]) or finger == lhf for lhf in left_hand_fingers):
                    current_hand = 'left'
                    left_hand_letters += 1
                elif any(finger.startswith(rhf[0]) or finger == rhf for rhf in right_hand_fingers):
                    current_hand = 'right'
                    right_hand_letters += 1
            
            # Вариант 3: Shift-символ
            if char in getattr(self, 'shift_keys', {}):
                key_code, finger = self.shift_keys[char]
                path = self._calculate_path(key_code, finger)
                # Ищем большой палец для Shift
                shift_finger = None
                for f in left_hand_fingers:
                    if 'thumb' in f or '1' in f or f == 'lf1':
                        shift_finger = f
                        break
                if not shift_finger:
                    shift_finger = 'lf1'  # fallback
                    
                options.append(('shift', path + 1, key_code, finger, 1, shift_finger))
                # Определяем руку для основной клавиши
                if any(finger.startswith(lhf[0]) or finger == lhf for lhf in left_hand_fingers):
                    current_hand = 'left'
                    left_hand_letters += 1
                elif any(finger.startswith(rhf[0]) or finger == rhf for rhf in right_hand_fingers):
                    current_hand = 'right'
                    right_hand_letters += 1
            
            # Вариант 4: Alt-символ
            if char in getattr(self, 'alt_keys', {}):
                key_code, finger = self.alt_keys[char]
                path = self._calculate_path(key_code, finger)
                # Ищем большой палец для Alt
                alt_finger = None
                for f in right_hand_fingers:
                    if 'thumb' in f or '1' in f or f == 'rf1':
                        alt_finger = f
                        break
                if not alt_finger:
                    alt_finger = 'rf1'  # fallback
                    
                options.append(('alt', path + 1, key_code, finger, 1, alt_finger))
                # Определяем руку для основной клавиши
                if any(finger.startswith(lhf[0]) or finger == lhf for lhf in left_hand_fingers):
                    current_hand = 'left'
                    left_hand_letters += 1
                elif any(finger.startswith(rhf[0]) or finger == rhf for rhf in right_hand_fingers):
                    current_hand = 'right'
                    right_hand_letters += 1
            
            if options:
                # Выбираем вариант с минимальным общим путем
                best_option = min(options, key=lambda x: x[1])
                mode, total_path_option, key_code, finger, mod_cost, mod_finger = best_option
                
                # Убедимся, что палец есть в словаре
                if finger not in finger_counts:
                    finger_counts[finger] = 0
                    paths[finger] = 0
                
                # Считаем основную клавишу
                finger_counts[finger] += 1
                paths[finger] += total_path_option - mod_cost
                total_path += total_path_option
                total_presses += 1
                
                # Считаем модификатор если есть
                if mod_cost > 0 and mod_finger:
                    # Убедимся, что палец модификатора есть в словаре
                    if mod_finger not in finger_counts:
                        finger_counts[mod_finger] = 0
                        paths[mod_finger] = 0
                        
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
        left_hand_count = sum(finger_counts.get(f, 0) for f in left_hand_fingers)
        right_hand_count = sum(finger_counts.get(f, 0) for f in right_hand_fingers)
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
                'left_hand_letters': left_hand_letters,
                'right_hand_letters': right_hand_letters,
                'hand_switches': hand_switches,
                'total_presses': total_presses,
                'average_presses_per_char': total_presses / character_count if character_count > 0 else 0,
                'left_hand_letters_percentage': left_hand_letters_percentage,
                'right_hand_letters_percentage': right_hand_letters_percentage,
                'hand_switches_per_100_chars': (hand_switches / character_count * 100) if character_count > 0 else 0,
            }
            
    def analyze_all_files(self, common_chars=None): 
        """
        Последовательно анализирует два предопределённых текстовых файла с раскладкой клавиатуры.

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
            ('1grams.txt', 'Минимальные фразы')
        ]
        
        results = []
        
        for filename, text_name in files_to_analyze:
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
            print(f"\nНагрузка по пальцам:")
            total_presses = sum(result['finger_counts'].values())
            for finger in ['lf5', 'lf4', 'lf3', 'lf2', 
                          'rf2', 'rf3', 'rf4', 'rf5', 
                          'lf1', 'rf1']:
                count = result['finger_counts'][finger]
                if count > 0:
                    percentage = (count / total_presses * 100)
                    print(f"  {finger}: {count} нажатий ({percentage:.1f}%)")

    def print_improved_results(self, results):
        """
        Выводит расширенный анализ нагрузки по пальцам с акцентом на использование пробела.

        Включает:
        - сводку по каждому анализируемому тексту и выбранной раскладке,
        - процентное распределение нагрузки по пальцам (lf5–lf1, rf1–rf5),
        - отдельный акцент на пробел (правый большой палец rf1),
        - использование клавиш Alt/Shift (левый большой палец lf1),
        - соотношение нагрузки между левой и правой рукой.

        Используется для детального анализа эргономики раскладки и выявления особенностей
        распределения нагрузки по пальцам и рукам.

        Args:
            results (list[dict]): Список словарей с результатами анализа, содержащих:
                - 'text_name': название текста,
                - 'layout': код раскладки,
                - 'finger_counts': словарь с количеством нажатий по каждому пальцу,
                - 'left_hand_percentage': процент нагрузки на левую руку,
                - 'right_hand_percentage': процент нагрузки на правую руку.

        Returns:
            None: результаты выводятся в консоль в виде форматированного отчёта.
        """
        for result in results:
            print(f"\n{'='*60}")
            print(f"=== УЛУЧШЕННЫЙ АНАЛИЗ: {result['text_name']} ===")
            print(f"=== РАСКЛАДКА: {result['layout']} ===")
            print(f"{'='*60}")
            
            total_presses = sum(result['finger_counts'].values())
            
            # Процентное распределение
            print("НАГРУЗКА ПО ПАЛЬЦАМ (%):")
            finger_names = {
                'lf5': 'Лев. мизинец (lf5)', 'lf4': 'Лев. безым. (lf4)', 
                'lf3': 'Лев. средний (lf3)', 'lf2': 'Лев. указат. (lf2)',
                'rf2': 'Прав. указат. (rf2)', 'rf3': 'Прав. средний (rf3)',
                'rf4': 'Прав. безым. (rf4)', 'rf5': 'Прав. мизинец (rf5)',
                'lf1': 'Лев. большой (lf1)', 'rf1': 'Прав. большой (rf1)'
            }
            
            for finger in ['lf5', 'lf4', 'lf3', 'lf2', 
                          'rf2', 'rf3', 'rf4', 'rf5', 
                          'lf1', 'rf1']:
                count = result['finger_counts'][finger]
                percentage = (count / total_presses * 100)
                if count > 0:
                    print(f"  {finger_names[finger]:<25} {count:>4} нажатий ({percentage:>5.1f}%)")
            
            # Анализ пробела
            space_percentage = (result['finger_counts']['rf1'] / total_presses * 100)
            print(f"\nОСОБЕННОСТИ РАСКЛАДКИ:")
            print(f"  • Пробел (правый большой rf1): {space_percentage:.1f}%")
            print(f"  • Alt/Shift (левый большой lf1): {(result['finger_counts']['lf1'] / total_presses * 100):.1f}%")
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


def analyze_everything_in_one():
    """
    Выполняет комплексный анализ раскладок клавиатуры по нескольким текстам.

    Включает:
    - загрузку и предварительную обработку текстов (классические произведения, тестовые корпуса, минимальные фразы),
    - анализ нагрузки для каждой раскладки (количество символов, нажатий, путь, распределение по рукам, частота смен),
    - сводную таблицу результатов по всем текстам,
    - суммарный путь по раскладкам,
    - анализ двух-, трёх- и четырёхбуквенных комбинаций (n-грамм) для объединённого текста.

    Используется для получения полного представления о производительности и удобстве разных раскладок
    на основе реальных текстов и статистики комбинаций.

    Returns:
        dict: Словарь с двумя ключами:
            - 'нагрузка': результаты анализа нагрузки по раскладкам и текстам,
            - 'комбинации': результаты анализа n-грамм (2-, 3-, 4-буквенные) по раскладкам.
    """
    print("="*70)
    print("ПОЛНЫЙ АНАЛИЗ РАСКЛАДОК (ВСЕ ТЕКСТЫ)")
    print("="*70)
    
    # Загружаем ВСЕ тексты
    files_to_analyze = [
        ('voina_i_mir.txt', 'Война и мир'),
        ('1grams.txt', 'Минимальные фразы')
    ]
    
    all_texts_data = []
    
    print("Загрузка текстов...")
    for filename, text_name in files_to_analyze:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                text = file.read()
                if filename == '1grams.txt':
                    words = text.split()[:1000]
                    text = ' '.join(words)
                    print(f"  ✓ Загружено {len(words)} слов из {text_name}")
                else:
                    print(f"  ✓ Загружен {text_name}: {len(text):,} символов".replace(',', ' '))
                all_texts_data.append((text, text_name))
        except FileNotFoundError:
            print(f"  ✗ ОШИБКА: Файл {filename} не найден!")
            return
        except Exception as e:
            print(f"  ✗ ОШИБКА загрузки {filename}: {e}")
            return
    
    if not all_texts_data:
        print("Нет данных для анализа!")
        return
    
    layouts = [
        ('ytsuken', 'СТАНДАРТНАЯ'),
        ('vyzov', 'ВЫЗОВ'), 
        ('zubachev', 'ЗУБАЧЕВ'),
        ('skoropis', 'СКОРОПИСЬ'),
        ('rusfon', 'РУСФОН'),
        ('diktor', 'ДИКТОР'),
        ('ant', 'АНТ')
    ]
    
    common_chars = get_common_chars()
    
    # Словари для результатов
    all_results = {}  # {layout_code: [result_text1, result_text2, result_text3]}
    
    print(f"\nАнализ {len(layouts)} раскладок для {len(all_texts_data)} текстов...")
    for layout_code, layout_name in layouts:
        print(f"  Анализируем {layout_name}...")
        
        # Создаем анализатор
        analyzer = KeyboardAnalyzer(layout=layout_code)
        
        layout_results = []
        
        for text, text_name in all_texts_data:
            # Анализ нагрузки
            result = analyzer.analyze_text(text, text_name, common_chars)
            if result:
                layout_results.append(result)
        
        all_results[layout_code] = layout_results
    
    # ===== ВЫВОД ТАБЛИЦЫ НАГРУЗКИ ДЛЯ ВСЕХ ТЕКСТОВ =====
    print(f"\n{'='*140}")
    print("СВОДНАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ (НАГРУЗКА)")
    print(f"{'='*140}")
    print(f"{'Текст':<18} {'Раскладка':<12} {'Символов':<10} {'Нажатий':<10} {'Наж/симв':<10} {'Общий путь':<12} {'Ср. путь':<10} {'Левая':<8} {'Правая':<8} {'Смены':<8}")
    print(f"{'-'*140}")

    layout_display_names = {
        'ytsuken': 'Стандарт', 'vyzov': 'Вызов', 'zubachev': 'Зубачев',
        'skoropis': 'Скоропись', 'rusfon': 'Русфон', 'diktor': 'Диктор', 'ant': 'Ант'
    }

    for text_idx, (text, text_name) in enumerate(all_texts_data):
        for layout_code, layout_name in layouts:
            if layout_code in all_results and text_idx < len(all_results[layout_code]):
                result = all_results[layout_code][text_idx]
                layout_display_name = layout_display_names.get(layout_code, layout_code)
                
                print(f"{text_name:<18} {layout_display_name:<12} {result['characters_analyzed']:<10} "
                      f"{result['total_presses']:<10} {result['average_presses_per_char']:<10.2f} "
                      f"{result['total_path']:<12} {result['average_path']:<10.2f} "
                      f"{result['left_hand_letters_percentage']:<7.1f} "
                      f"{result['right_hand_letters_percentage']:<7.1f} "
                      f"{result['hand_switches_per_100_chars']:<7.1f}")
        
        if text_idx < len(all_texts_data) - 1:
            print(f"{'-'*140}")
    
    # ===== ВЫВОД СУММАРНОГО ПУТЯ ПО ВСЕМ ТЕКСТАМ =====
    print(f"\n{'='*60}")
    print("СУММАРНЫЙ ПУТЬ ПО РАСКЛАДКАМ (ВСЕ 2 ТЕКСТА):")
    print(f"{'='*60}")
    
    for layout_code, layout_name in layouts:
        if layout_code in all_results:
            total_path_all_texts = sum(r['total_path'] for r in all_results[layout_code])
            layout_display_name = layout_display_names.get(layout_code, layout_code)
            print(f"{layout_display_name}: {total_path_all_texts:,}")
    
    # ===== АНАЛИЗ КОМБИНАЦИЙ ДЛЯ ВСЕХ ТЕКСТОВ ВМЕСТЕ =====
    print(f"\n\n{'='*80}")
    print(f"АНАЛИЗ КОМБИНАЦИЙ (ВСЕ ТЕКСТЫ ВМЕСТЕ)")
    print(f"{'='*80}")
    
    all_combination_results = {}
    
    for layout_code, layout_name in layouts:
        print(f"  Анализируем комбинации для {layout_name}...")
        analyzer = KeyboardAnalyzer(layout=layout_code)
        
        # Объединяем все тексты в один для анализа комбинаций
        combined_text = ""
        for text, text_name in all_texts_data:
            combined_text += text
        
        combination_results = analyzer.analyze_combinations(combined_text)
        all_combination_results[layout_code] = combination_results
    
    # ДВУХГРАММЫ
    print(f"\nДВУХБУКВЕННЫЕ КОМБИНАЦИИ (2-граммы)")
    print(f"{'='*80}")
    print(f"{'Раскладка':<12} {'Удобные':<10} {'Частично':<12} {'Неудобные':<12} {'Всего':<8}")
    print(f"{'-'*80}")
    
    for layout_code, layout_name in layouts:
        if layout_code in all_combination_results:
            results = all_combination_results[layout_code]['двухграммы']
            layout_display = layout_display_names.get(layout_code, layout_code)
            
            print(f"{layout_display:<12} {results['удобные']:<10} "
                  f"{results['частично_удобные']:<12} "
                  f"{results['неудобные']:<12} "
                  f"{results['всего']:<8}")
    
    # ТРЕХГРАММЫ
    print(f"\n\nТРЕХБУКВЕННЫЕ КОМБИНАЦИИ (3-граммы)")
    print(f"{'='*80}")
    print(f"{'Раскладка':<12} {'Удобные':<10} {'Частично':<12} {'Всего':<8}")
    print(f"{'-'*80}")
    
    for layout_code, layout_name in layouts:
        if layout_code in all_combination_results:
            results = all_combination_results[layout_code]['трехграммы']
            layout_display = layout_display_names.get(layout_code, layout_code)
            
            print(f"{layout_display:<12} {results['удобные']:<10} "
                  f"{results['частично_удобные']:<12} "
                  f"{results['всего']:<8}")
    
    # ЧЕТЫРЕХГРАММЫ
    print(f"\n\nЧЕТЫРЕХБУКВЕННЫЕ КОМБИНАЦИИ (4-граммы)")
    print(f"{'='*80}")
    print(f"{'Раскладка':<12} {'Удобные':<10} {'Частично':<12} {'Всего':<8}")
    print(f"{'-'*80}")
    
    for layout_code, layout_name in layouts:
        if layout_code in all_combination_results:
            results = all_combination_results[layout_code]['четырехграммы']
            layout_display = layout_display_names.get(layout_code, layout_code)
            
            print(f"{layout_display:<12} {results['удобные']:<10} "
                  f"{results['частично_удобные']:<12} "
                  f"{results['всего']:<8}")
    
    print(f"\n{'='*70}")
    print("АНАЛИЗ ЗАВЕРШЕН! Проанализировано все 2 текста.")
    print(f"{'='*70}")
    
    # Возвращаем все результаты
    return {
        'нагрузка': all_results,
        'комбинации': all_combination_results
    }

if __name__ == "__main__":
    """
    Точка входа при запуске скрипта напрямую.

    Логика:
    - выполняет полный анализ раскладок клавиатуры по нескольким текстам,
    - вызывает функцию `analyze_everything_in_one()`,
    - сохраняет результаты анализа в переменной `results`.

    Используется для запуска программы как самостоятельного модуля
    (например, через `python script.py`).

    Returns:
        dict: Результаты анализа, включающие:
            - 'нагрузка': статистика нагрузки по раскладкам,
            - 'комбинации': статистика удобства n-грамм.
    """
    # Просто запускаем полный анализ
    results = analyze_everything_in_one()