"""
Модуль анализатора раскладок клавиатуры
Анализирует нагрузку на пальцы при печати на разных раскладках
Рассчитывает пути за движения пальцев от home ряда
Автор: Vero
"""

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
        
        if layout == 'ytsuken':
            self._init_ytsuken_layout()
        elif layout == 'vyzov':
            self._init_vyzov_layout()
        elif layout == 'zubachev':
            self._init_zubachev_layout()
        elif layout == 'skoropis':
            self._init_skoropis_layout()
        elif layout == 'rusfon':
            self._init_rusfon_layout()
        elif layout == 'diktor':
            self._init_diktor_layout()
        elif layout == 'ant':
            self._init_ant_layout()
        
        # Карта клавиатуры: код -> (ряд, колонка) - общая для всех раскладок
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
            41: (3, 0), 44: (3, 1), 45: (3, 2), 46: (3, 3), 47: (3, 4), 
            48: (3, 5), 49: (3, 6), 50: (3, 7), 51: (3, 8), 52: (3, 9), 
            53: (3, 10),
            
            # Особые клавиши
            42: (3, -1),  # Shift
            43: (1, 12),  # \ (обратный слеш)
            57: (4, 5)    # Пробел
        }

    def _init_ytsuken_layout(self):
        """
        Инициализирует стандартную русскую раскладку ЙЦУКЕН.
        
        Устанавливает соответствие символов клавиш их кодам и пальцам, 
        а также определяет:
        - заглавные буквы (через Shift),
        - специальные символы с Shift,
        - домашние позиции пальцев.
        """
        self.keys = {
            # Основные буквы
            'й': (16, 'left_pinky'), 'ц': (17, 'left_ring'), 'у': (18, 'left_middle'), 
            'к': (19, 'left_index'), 'е': (20, 'left_index'), 'н': (21, 'right_index'),
            'г': (22, 'right_index'), 'ш': (23, 'right_middle'), 'щ': (24, 'right_ring'),
            'з': (25, 'right_pinky'), 'х': (26, 'right_pinky'), 'ъ': (27, 'right_pinky'),
            
            'ф': (30, 'left_pinky'), 'ы': (31, 'left_ring'), 'в': (32, 'left_middle'),
            'а': (33, 'left_index'), 'п': (34, 'left_index'), 'р': (35, 'right_index'),
            'о': (36, 'right_index'), 'л': (37, 'right_middle'), 'д': (38, 'right_ring'),
            'ж': (39, 'right_pinky'), 'э': (40, 'right_pinky'),
            
            'я': (44, 'left_pinky'), 'ч': (45, 'left_ring'), 'с': (46, 'left_middle'),
            'м': (47, 'left_index'), 'и': (48, 'right_index'), 'т': (49, 'right_index'),
            'ь': (50, 'right_index'), 'б': (51, 'right_middle'), 'ю': (52, 'right_ring'),
            
            'ё': (41, 'left_pinky'), ' ': (57, 'right_thumb')
        }

        # Заглавные буквы (буква + Shift)
        self.caps_keys = {}
        for char, (code, finger) in self.keys.items():
            if char.isalpha() and char != ' ':
                self.caps_keys[char.upper()] = (code, finger)

        # Символы с Shift
        self.shift_keys = {
            '!': (2, 'left_pinky'), '"': (3, 'left_ring'), '№': (4, 'left_middle'), 
            ';': (5, 'left_index'), '%': (6, 'right_index'), ':': (7, 'right_middle'), 
            '?': (8, 'right_ring'), '*': (9, 'right_pinky'), '(': (10, 'right_pinky'), 
            ')': (11, 'right_pinky'), '_': (12, 'right_pinky'), '+': (13, 'right_pinky'),
            '/': (43, 'right_pinky'), ',': (53, 'right_pinky')
        }

        # Домашние позиции
        self.home_positions = {
            'left_pinky': 30, 'left_ring': 31, 'left_middle': 32, 'left_index': 33,
            'right_index': 36, 'right_middle': 37, 'right_ring': 38, 'right_pinky': 39,
            'left_thumb': 42, 'right_thumb': 57
        }

    def _init_vyzov_layout(self):
        """
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
        """
        self.keys = {
            'б': (16, 'left_pinky'), 'ы': (17, 'left_ring'), 'о': (18, 'left_middle'),
            'у': (19, 'left_index'), 'ь': (20, 'left_index'), 'ё': (21, 'right_index'),
            '^': (22, 'right_index'), 'д': (23, 'right_index'), 'я': (24, 'right_middle'),
            'г': (25, 'right_middle'), 'ж': (26, 'right_middle'), 
            
            'ч': (30, 'left_pinky'), 'и': (31, 'left_ring'), 'е': (32, 'left_middle'),
            'а': (33, 'left_index'), ',': (34, 'left_index'), 'н': (36, 'right_index'),
            'т': (37, 'right_middle'), 'с': (38, 'right_ring'), 'в': (39, 'right_pinky'),
            'з': (40, 'right_ring'),
            
            'х': (45, 'left_ring'), 'й': (46, 'left_middle'),
            'к': (47, 'left_index'), '_': (48, 'left_index'), '/': (49, 'right_pinky'),
            'р': (50, 'right_index'), 'м': (51, 'right_ring'), 'ф': (52, 'right_pinky'),
            'п': (53, 'right_pinky'),
            
            ' ': (57, 'right_thumb'), '₽': (41, 'right_thumb')
        }

        # Заглавные буквы
        self.caps_keys = {}
        for char, (code, finger) in self.keys.items():
            if char.isalpha() and char != ' ':
                self.caps_keys[char.upper()] = (code, finger)

        # Символы с Shift
        self.shift_keys = {
            'ё': (2, 'left_pinky'), '[': (3, 'left_ring'), '{': (4, 'left_middle'),
            '}': (5, 'left_index'), '(': (6, 'right_index'), '=': (7, 'right_middle'),
            '*': (8, 'right_ring'), ')': (9, 'right_pinky'), '+': (10, 'right_pinky'),
            ']': (11, 'right_pinky'), '!': (12, 'right_pinky'), 
            ';': (34, 'left_index'), ':': (35, 'right_index'), "'": (20, 'left_index'),
            '-': (48, 'left_index'), '?': (49, 'right_pinky'), '@': (27, 'right_ring'),
            '$': (41, 'right_thumb')
        }

        # Alt-символы - оставляем только экономичные
        self.alt_keys = {
            'ц': (30, 'left_ring'),  
            'щ': (36, 'right_index'),   
            'ъ': (37, 'right_middle'),   
            '№': (39, 'right_pinky'),    
            'э': (32, 'left_middle')     
        }

        self.home_positions = {
            'left_pinky': 30, 'left_ring': 31, 'left_middle': 32, 'left_index': 33,
            'right_index': 36, 'right_middle': 37, 'right_ring': 38, 'right_pinky': 39,
            'left_thumb': 42, 'right_thumb': 57
        }

    def _init_zubachev_layout(self):
        """
        Инициализирует раскладку «Зубачев».

        Раскладка разработана с акцентом на симметрию, эргономику и частотное распределение символов.
        Часто используемые буквы расположены ближе к центру, чтобы снизить нагрузку на пальцы.

        Метод определяет:
        - основные символы и их расположение на клавиатуре,
        - заглавные буквы (через Shift),
        - специальные символы с Shift-модификатором,
        - домашние позиции пальцев для расчёта пути.
        """
        self.keys = {
            'ф': (16, 'left_pinky'), 'ы': (17, 'left_ring'), 'а': (18, 'left_middle'),
            'я': (19, 'left_index'), ',': (20, 'left_index'), 'й': (21, 'left_index'),
            'м': (22, 'left_index'), 'р': (23, 'right_index'), 'п': (24, 'right_index'),
            'х': (25, 'right_index'), 'ц': (26, 'right_index'), 'щ': (27, 'right_index'),
            
            'г': (30, 'left_pinky'), 'и': (31, 'left_ring'), 'у': (32, 'left_middle'),
            'о': (33, 'left_index'), 'у': (34, 'left_index'), 'л': (35, 'right_middle'),
            'т': (36, 'right_middle'), 'с': (37, 'right_middle'), 'н': (38, 'right_ring'),
            'з': (39, 'right_ring'), 'ж': (40, 'right_ring'),
            
            'ш': (44, 'left_pinky'), 'ь': (45, 'left_ring'), 'ю': (46, 'left_middle'),
            '.': (47, 'left_index'), 'э': (48, 'right_pinky'), 'б': (49, 'right_pinky'),
            'д': (50, 'right_pinky'), 'в': (51, 'right_pinky'), 'к': (52, 'right_pinky'),
            'ч': (53, 'right_pinky'),
            
            '\\': (43, 'right_index'), 'ё': (41, 'right_pinky'), ' ': (57, 'right_thumb')
        }

        # Заглавные буквы
        self.caps_keys = {}
        for char, (code, finger) in self.keys.items():
            if char.isalpha() and char != ' ':
                self.caps_keys[char.upper()] = (code, finger)

        # Символы с Shift
        self.shift_keys = {
            '!': (2, 'left_pinky'), '"': (3, 'left_ring'), '№': (4, 'left_middle'),
            ';': (5, 'left_index'), '%': (6, 'right_index'), ':': (7, 'right_middle'),
            '?': (8, 'right_ring'), '*': (9, 'right_pinky'), '(': (10, 'right_pinky'),
            ')': (11, 'right_pinky'), '_': (12, 'right_pinky'), '+': (13, 'right_pinky'),
            '/': (43, 'right_index'), 'ъ': (45, 'left_ring'), 'ь': (47, 'left_index')
        }

        self.home_positions = {
            'left_pinky': 30, 'left_ring': 31, 'left_middle': 32, 'left_index': 33,
            'right_index': 23, 'right_middle': 36, 'right_ring': 38, 'right_pinky': 39,
            'left_thumb': 42, 'right_thumb': 57
        }

    def _init_skoropis_layout(self):
        """
        Инициализирует раскладку «Скоропись».

        Раскладка разработана для скоростного набора текста с минимальной нагрузкой на пальцы.
        Частотные символы размещены ближе к сильным пальцам, а редкие — на периферии.

        Метод определяет:
        - основные символы и их расположение,
        - заглавные буквы (через Shift),
        - специальные символы с Shift-модификатором,
        - домашние позиции пальцев для расчёта пути.
        """
        self.keys = {
            'ц': (16, 'left_pinky'), 'ь': (17, 'left_ring'), 'я': (18, 'left_middle'),
            ',': (19, 'left_index'), '.': (20, 'left_index'), 'з': (21, 'left_index'),
            'в': (22, 'left_index'), 'к': (23, 'right_index'), 'д': (24, 'right_index'),
            'ч': (25, 'right_index'), 'ш': (26, 'right_index'), 'щ': (27, 'right_index'),
            
            'у': (30, 'left_pinky'), 'и': (31, 'left_ring'), 'е': (32, 'left_middle'),
            'о': (33, 'left_index'), 'а': (34, 'left_index'), 'л': (35, 'right_middle'),
            'н': (36, 'right_middle'), 'т': (37, 'right_middle'), 'с': (38, 'right_ring'),
            'р': (39, 'right_ring'), 'й': (40, 'right_ring'),
            
            'ф': (44, 'left_pinky'), 'э': (45, 'left_ring'), 'х': (46, 'left_middle'),
            'ы': (47, 'left_index'), 'ю': (48, 'right_pinky'), 'б': (49, 'right_pinky'),
            'м': (50, 'right_pinky'), 'п': (51, 'right_pinky'), 'г': (52, 'right_pinky'),
            'ж': (53, 'right_pinky'),
            
            '"': (43, 'right_index'), '*': (41, 'right_pinky'), ' ': (57, 'right_thumb')
        }

        # Заглавные буквы
        self.caps_keys = {}
        for char, (code, finger) in self.keys.items():
            if char.isalpha() and char != ' ':
                self.caps_keys[char.upper()] = (code, finger)

        # Символы с Shift (спецсимволы)
        self.shift_keys = {
            '.': (2, 'left_pinky'), 'ё': (3, 'left_ring'), 'ъ': (4, 'left_middle'),
            '?': (5, 'left_index'), '!': (6, 'right_index'), '': (7, 'right_middle'),
            '-': (8, 'right_ring'), "'": (9, 'right_pinky'), '(': (10, 'right_pinky'),
            ')': (11, 'right_pinky'), '_': (12, 'right_pinky'), '«': (13, 'right_pinky')
        }

        self.home_positions = {
            'left_pinky': 30, 'left_ring': 31, 'left_middle': 32, 'left_index': 33,
            'right_index': 23, 'right_middle': 36, 'right_ring': 38, 'right_pinky': 39,
            'left_thumb': 42, 'right_thumb': 57
        }

    def _init_rusfon_layout(self):
        """
        Инициализирует раскладку «Русфон» — русскую фонетическую клавиатуру.

        Раскладка разработана для интуитивного ввода русских символов, особенно полезна
        для начинающих пользователей и тех, кто привык к латинской клавиатуре.

        Метод определяет:
        - основные символы и их расположение на клавиатуре,
        - заглавные буквы (через Shift),
        - специальные символы с Shift-модификатором,
        - домашние позиции пальцев для расчёта пути.
        """
        self.keys = {
            'я': (16, 'left_pinky'), 'в': (17, 'left_ring'), 'е': (18, 'left_middle'),
            'р': (19, 'left_index'), 'т': (20, 'left_index'), 'ы': (21, 'left_index'),
            'у': (22, 'left_index'), 'и': (23, 'right_index'), 'о': (24, 'right_index'),
            'п': (25, 'right_index'), 'ш': (26, 'right_index'), 'щ': (27, 'right_index'),
            
            'а': (30, 'left_pinky'), 'с': (31, 'left_ring'), 'д': (32, 'left_middle'),
            'ф': (33, 'left_index'), 'г': (34, 'left_index'), 'х': (35, 'right_middle'),
            'й': (36, 'right_middle'), 'к': (37, 'right_middle'), 'л': (38, 'right_ring'),
            ';': (39, 'right_ring'), "'": (40, 'right_ring'),
            
            'з': (44, 'left_pinky'), 'ь': (45, 'left_ring'), 'ц': (46, 'left_middle'),
            'ж': (47, 'left_index'), 'б': (48, 'right_pinky'), 'н': (49, 'right_pinky'),
            'м': (50, 'right_pinky'), ',': (51, 'right_pinky'), '.': (52, 'right_pinky'),
            '/': (53, 'right_pinky'),
            
            'э': (43, 'right_index'), 'ю': (41, 'right_pinky'), ' ': (57, 'right_thumb')
        }

        # Заглавные буквы
        self.caps_keys = {}
        for char, (code, finger) in self.keys.items():
            if char.isalpha() and char != ' ':
                self.caps_keys[char.upper()] = (code, finger)

        # Символы с Shift
        self.shift_keys = {
            '!': (2, 'left_pinky'), '@': (3, 'left_ring'), 'ё': (4, 'left_middle'),
            'Ё': (5, 'left_index'), 'ъ': (6, 'right_index'), 'Ъ': (7, 'right_middle'),
            '&': (8, 'right_ring'), '*': (9, 'right_pinky'), '(': (10, 'right_pinky'),
            ')': (11, 'right_pinky'), '_': (12, 'right_pinky'), 'ч': (13, 'right_pinky'),
            ':': (39, 'right_ring'), '"': (40, 'right_ring'), '<': (51, 'right_pinky'),
            '>': (52, 'right_pinky'), '?': (53, 'right_pinky')
        }

        self.home_positions = {
            'left_pinky': 30, 'left_ring': 31, 'left_middle': 32, 'left_index': 33,
            'right_index': 23, 'right_middle': 36, 'right_ring': 38, 'right_pinky': 39,
            'left_thumb': 42, 'right_thumb': 57
        }

    def _init_diktor_layout(self):
        """
        Инициализирует раскладку «Диктор».
        
        Раскладка разработана для дикторов, стенографистов и пользователей, работающих с речевыми текстами.
        Оптимизирована для быстрого доступа к служебным символам, знакам препинания и часто используемым буквам.

        Метод определяет:
        - основные символы и их расположение на клавиатуре,
        - заглавные буквы (через Shift),
        - специальные символы с Shift-модификатором,
        - домашние позиции пальцев для расчёта пути.
        """
        self.keys = {
            'ц': (16, 'left_pinky'), 'ь': (17, 'left_ring'), 'я': (18, 'left_middle'),
            ',': (19, 'left_index'), '.': (20, 'left_index'), 'з': (21, 'left_index'),
            'в': (22, 'left_index'), 'к': (23, 'right_index'), 'д': (24, 'right_index'),
            'ч': (25, 'right_index'), 'ш': (26, 'right_index'), 'щ': (27, 'right_index'),
            
            'у': (30, 'left_pinky'), 'и': (31, 'left_ring'), 'е': (32, 'left_middle'),
            'о': (33, 'left_index'), 'а': (34, 'left_index'), 'л': (35, 'right_middle'),
            'н': (36, 'right_middle'), 'т': (37, 'right_middle'), 'с': (38, 'right_ring'),
            'р': (39, 'right_ring'), 'й': (40, 'right_ring'),
            
            'ф': (44, 'left_pinky'), 'э': (45, 'left_ring'), 'х': (46, 'left_middle'),
            'ы': (47, 'left_index'), 'ю': (48, 'right_pinky'), 'б': (49, 'right_pinky'),
            'м': (50, 'right_pinky'), 'п': (51, 'right_pinky'), 'г': (52, 'right_pinky'),
            'ж': (53, 'right_pinky'),
            
            ' ': (57, 'right_thumb'), 'ё': (41, 'right_pinky')
        }

        # Заглавные буквы
        self.caps_keys = {}
        for char, (code, finger) in self.keys.items():
            if char.isalpha() and char != ' ':
                self.caps_keys[char.upper()] = (code, finger)

        # Символы с Shift
        self.shift_keys = {
            'ь': (3, 'left_ring'), '№': (4, 'left_middle'),
            '%': (5, 'left_index'), ':': (6, 'right_index'), ';': (7, 'right_middle'),
            '-': (8, 'right_ring'), '"': (9, 'right_pinky'), '(': (10, 'right_pinky'),
            ')': (11, 'right_pinky'), '_': (12, 'right_pinky'), '+': (13, 'right_pinky'),
            'ъ': (17, 'left_ring'), '?': (19, 'left_index'), '!': (20, 'left_index')
        }

        self.home_positions = {
            'left_pinky': 30, 'left_ring': 31, 'left_middle': 32, 'left_index': 33,
            'right_index': 23, 'right_middle': 36, 'right_ring': 38, 'right_pinky': 39,
            'left_thumb': 42, 'right_thumb': 57
        }

    def _init_ant_layout(self):
        """
        Инициализирует раскладку «Ант» — альтернативную русскую клавиатуру с эргономическим смещением.

        Раскладка разработана для снижения нагрузки на пальцы и повышения скорости набора.
        Частотные символы размещены ближе к центру, а редкие — на периферии.
        Подходит для анализа эргоэкономичных конфигураций и нестандартных клавиатур.
        
        Метод определяет:
        - основные символы и их расположение на клавиатуре,
        - заглавные буквы (через Shift),
        - специальные символы с Shift-модификатором,
        - домашние позиции пальцев для расчёта пути.
        """
        self.keys = {
            'г': (16, 'left_pinky'), 'п': (17, 'left_ring'), 'р': (18, 'left_middle'),
            'д': (19, 'left_index'), 'м': (20, 'left_index'), 'ы': (21, 'left_index'),
            'и': (22, 'left_index'), 'я': (23, 'right_index'), 'у': (24, 'right_index'),
            'х': (25, 'right_index'), 'ц': (26, 'right_index'), 'ж': (27, 'right_index'),
            
            'в': (30, 'left_pinky'), 'н': (31, 'left_ring'), 'с': (32, 'left_middle'),
            'т': (33, 'left_index'), 'л': (34, 'left_index'), 'ь': (35, 'right_middle'),
            'о': (36, 'right_middle'), 'е': (37, 'right_middle'), 'а': (38, 'right_ring'),
            'к': (39, 'right_ring'), 'з': (40, 'right_ring'),
            
            'щ': (44, 'left_pinky'), 'й': (45, 'left_ring'), 'ш': (46, 'left_middle'),
            'ь': (47, 'left_index'), ',': (48, 'right_pinky'), '.': (49, 'right_pinky'),
            'ю': (50, 'right_pinky'), 'э': (51, 'right_pinky'), 'ё': (52, 'right_pinky'),
            'ф': (53, 'right_pinky'),
            
            'ч': (43, 'right_index'), '\\': (41, 'right_pinky'), ' ': (57, 'right_thumb')
        }

        # Заглавные буквы
        self.caps_keys = {}
        for char, (code, finger) in self.keys.items():
            if char.isalpha() and char != ' ':
                self.caps_keys[char.upper()] = (code, finger)

        # Символы с Shift
        self.shift_keys = {
            '!': (2, 'left_pinky'), '?': (3, 'left_ring'), "'": (4, 'left_middle'),
            '"': (5, 'left_index'), '=': (6, 'right_index'), '+': (7, 'right_middle'),
            '-': (8, 'right_ring'), '*': (9, 'right_pinky'), '/': (10, 'right_pinky'),
            '%': (11, 'right_pinky'), '«': (12, 'right_pinky'), '»': (13, 'right_pinky'),
            ';': (48, 'right_pinky'), ':': (49, 'right_pinky')
        }

        self.home_positions = {
            'left_pinky': 30, 'left_ring': 31, 'left_middle': 32, 'left_index': 33,
            'right_index': 23, 'right_middle': 36, 'right_ring': 38, 'right_pinky': 39,
            'left_thumb': 42, 'right_thumb': 57
        }

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
            
        clean_text = text  # Анализируем ВЕСЬ текст без фильтрации
        #print(f"  (анализируется весь текст: {len(clean_text)} символов)")
        
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

        # Статистика по типам нажатий - ИСПРАВЛЕННАЯ ЛОГИКА
        left_hand_only = 0      # Только левая рука (все нажатия левой рукой)
        right_hand_only = 0     # Только правая рука (все нажатия правой рукой)  
        both_hands = 0          # Обе руки одновременно (модификатор + буква)
        total_presses = 0       # Общее количество нажатий (буквы + модификаторы)
        
        # Определяем какие пальцы к каким рукам относятся
        left_hand_fingers = ['left_pinky', 'left_ring', 'left_middle', 'left_index', 'left_thumb']
        right_hand_fingers = ['right_pinky', 'right_ring', 'right_middle', 'right_index', 'right_thumb']

        for char in clean_text:
            # Собираем ВСЕ возможные варианты для этого символа
            options = []
            
            # Вариант 1: обычная буква
            if char in self.keys:
                key_code, finger = self.keys[char]
                path = self._calculate_path(key_code, finger)
                options.append(('normal', path, key_code, finger, 0, None))
            
            # Вариант 2: заглавная буква (буква + Shift)
            if char in getattr(self, 'caps_keys', {}):
                key_code, finger = self.caps_keys[char]
                path = self._calculate_path(key_code, finger)
                options.append(('caps', path + 1, key_code, finger, 1, 'left_thumb'))
            
            # Вариант 3: Shift-символ
            if char in getattr(self, 'shift_keys', {}):
                key_code, finger = self.shift_keys[char]
                path = self._calculate_path(key_code, finger)
                options.append(('shift', path + 1, key_code, finger, 1, 'left_thumb'))
            
            # Вариант 4: Alt-символ
            if char in getattr(self, 'alt_keys', {}):
                key_code, finger = self.alt_keys[char]
                path = self._calculate_path(key_code, finger)
                options.append(('alt', path + 1, key_code, finger, 1, 'right_thumb'))
            
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
                
                # Считаем типы нажатий 
                if mod_cost == 0:
                    # Одиночное нажатие - определяем какая рука
                    if finger in left_hand_fingers:
                        left_hand_only += 1
                    elif finger in right_hand_fingers:
                        right_hand_only += 1
                else:
                    # Двуручное нажатие - модификатор + основная клавиша
                    both_hands += 1
        
        average_path = total_path / character_count if character_count > 0 else 0
        
        # Статистика по рукам на основе finger_counts
        left_hand_count = sum(finger_counts[f] for f in left_hand_fingers)
        right_hand_count = sum(finger_counts[f] for f in right_hand_fingers)
        total_hand_count = left_hand_count + right_hand_count
        
        left_hand_percentage = (left_hand_count / total_hand_count * 100) if total_hand_count > 0 else 0
        right_hand_percentage = (right_hand_count / total_hand_count * 100) if total_hand_count > 0 else 0
        
        # Проверка корректности подсчета
        check_total = left_hand_only + right_hand_only + both_hands
        check_presses = left_hand_count + right_hand_count
        
        #print(f"  Проверка подсчета для {text_name}:")
        #print(f"    Всего нажатий: {total_presses}")
        #print(f"    Левая рука: {left_hand_count} ({left_hand_percentage:.1f}%)")
        #print(f"    Правая рука: {right_hand_count} ({right_hand_percentage:.1f}%)")
        #print(f"    Только левая: {left_hand_only} ({left_hand_only/total_presses*100:.1f}%)")
        #print(f"    Только правая: {right_hand_only} ({right_hand_only/total_presses*100:.1f}%)")
        #print(f"    Обе руки: {both_hands} ({both_hands/total_presses*100:.1f}%)")
        #print(f"    Shift: {shift_count}, Alt: {alt_count}")
        #print(f"    Проверка: {check_total} = {total_presses}? {check_total == total_presses}")
        
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
            'left_hand_only': left_hand_only,
            'right_hand_only': right_hand_only, 
            'two_handed': both_hands,  
            'total_presses': total_presses,
            'average_presses_per_char': total_presses / character_count if character_count > 0 else 0,
            'left_hand_only_percentage': (left_hand_only / total_presses * 100) if total_presses > 0 else 0,
            'right_hand_only_percentage': (right_hand_only / total_presses * 100) if total_presses > 0 else 0,
            'two_handed_percentage': (both_hands / total_presses * 100) if total_presses > 0 else 0,
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

#for layout_code, layout_name in layouts:
    #print(f"\n\n{'='*70}")
    #print(f"АНАЛИЗ РАСКЛАДКИ: {layout_name}")
    #print("="*70)
    
    #analyzer = KeyboardAnalyzer(layout=layout_code)
    #results = analyzer.analyze_all_files(common_chars)
    #if results:
        #analyzer.print_improved_results(results)
        #all_results[layout_code] = results

# Сводная таблица для сравнения всех раскладок
#print(f"\n{'='*140}")
#print("СВОДНАЯ ТАБЛИЦА ДЛЯ СРАВНЕНИЯ РАСКЛАДОК (ОБЩИЕ СИМВОЛЫ)")
#print(f"{'='*140}")
#print(f"{'Текст':<15} {'Раскладка':<12} {'Символов':<10} {'Нажатий':<10} {'Наж/симв':<10} {'Общий путь':<12} {'Ср. путь':<10} {'Левая':<8} {'Правая':<8} {'2 руки':<8} {'Shift':<8} {'Alt':<6}")
#print(f"{'-'*140}")

layout_display_names = {
    'ytsuken': 'Стандарт', 'vyzov': 'Вызов', 'zubachev': 'Зубачев',
    'skoropis': 'Скоропись', 'rusfon': 'Русфон', 'diktor': 'Диктор', 'ant': 'Ант'
}

for i in range(3):  # для трех текстов
    for layout_code, layout_name in layouts:
        if layout_code in all_results and i < len(all_results[layout_code]):
            result = all_results[layout_code][i]
            layout_display_name = layout_display_names.get(layout_code, layout_code)
            
           # print(f"{result['text_name']:<15} {layout_display_name:<12} {result['characters_analyzed']:<10} "
               ###   f"{result['total_presses']:<10} {result['average_presses_per_char']:<10.2f} "
                 # f"{result['total_path']:<12} {result['average_path']:<10.2f} "
                 # f"{result['left_hand_only_percentage']:<7.1f}% {result['right_hand_only_percentage']:<7.1f}% "
                  #f"{result['two_handed_percentage']:<7.1f}% {result['shift_count']:<8} {result['alt_count']:<6}")
    
    if i < 2:  # не печатать разделитель после последнего текста
        print(f"{'-'*140}")