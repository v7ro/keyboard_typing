"""
Модуль с данными раскладок клавиатуры для анализатора
Автор: Vero
"""

# Карта клавиатуры: код -> (ряд, колонка) - общая для всех раскладок
keyboard_map = {
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

# Домашние позиции
home_positions = {
    'left_pinky': 30, 'left_ring': 31, 'left_middle': 32, 'left_index': 33,
    'right_index': 36, 'right_middle': 37, 'right_ring': 38, 'right_pinky': 39,
    'left_thumb': 42, 'right_thumb': 57
}

# Раскладка ЙЦУКЕН
ytsuken_layout = {
    'keys': {
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
    },
    'shift_keys': {
        '!': (2, 'left_pinky'), '"': (3, 'left_ring'), '№': (4, 'left_middle'), 
        ';': (5, 'left_index'), '%': (6, 'right_index'), ':': (7, 'right_middle'), 
        '?': (8, 'right_ring'), '*': (9, 'right_pinky'), '(': (10, 'right_pinky'), 
        ')': (11, 'right_pinky'), '_': (12, 'right_pinky'), '+': (13, 'right_pinky'),
        '/': (43, 'right_pinky'), ',': (53, 'right_pinky')
    },
    'alt_keys': {},
    'home_positions': home_positions
}

# Раскладка ВЫЗОВ
vyzov_layout = {
    'keys': {
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
    },
    'shift_keys': {
        'ё': (2, 'left_pinky'), '[': (3, 'left_ring'), '{': (4, 'left_middle'),
        '}': (5, 'left_index'), '(': (6, 'right_index'), '=': (7, 'right_middle'),
        '*': (8, 'right_ring'), ')': (9, 'right_pinky'), '+': (10, 'right_pinky'),
        ']': (11, 'right_pinky'), '!': (12, 'right_pinky'), 
        ';': (34, 'left_index'), ':': (35, 'right_index'), "'": (20, 'left_index'),
        '-': (48, 'left_index'), '?': (49, 'right_pinky'), '@': (27, 'right_ring'),
        '$': (41, 'right_thumb')
    },
    'alt_keys': {
        'ц': (30, 'left_ring'),  
        'щ': (36, 'right_index'),   
        'ъ': (37, 'right_middle'),   
        '№': (39, 'right_pinky'),    
        'э': (32, 'left_middle')     
    },
    'home_positions': home_positions
}

# Раскладка ЗУБАЧЕВ
zubachev_layout = {
    'keys': {
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
    },
    'shift_keys': {
        '!': (2, 'left_pinky'), '"': (3, 'left_ring'), '№': (4, 'left_middle'),
        ';': (5, 'left_index'), '%': (6, 'right_index'), ':': (7, 'right_middle'),
        '?': (8, 'right_ring'), '*': (9, 'right_pinky'), '(': (10, 'right_pinky'),
        ')': (11, 'right_pinky'), '_': (12, 'right_pinky'), '+': (13, 'right_pinky'),
        '/': (43, 'right_index'), 'ъ': (45, 'left_ring'), 'ь': (47, 'left_index')
    },
    'alt_keys': {},
    'home_positions': {
        'left_pinky': 30, 'left_ring': 31, 'left_middle': 32, 'left_index': 33,
        'right_index': 23, 'right_middle': 36, 'right_ring': 38, 'right_pinky': 39,
        'left_thumb': 42, 'right_thumb': 57
    }
}

# Раскладка СКОРОПИСЬ
skoropis_layout = {
    'keys': {
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
    },
    'shift_keys': {
        '.': (2, 'left_pinky'), 'ё': (3, 'left_ring'), 'ъ': (4, 'left_middle'),
        '?': (5, 'left_index'), '!': (6, 'right_index'), '': (7, 'right_middle'),
        '-': (8, 'right_ring'), "'": (9, 'right_pinky'), '(': (10, 'right_pinky'),
        ')': (11, 'right_pinky'), '_': (12, 'right_pinky'), '«': (13, 'right_pinky')
    },
    'alt_keys': {},
    'home_positions': {
        'left_pinky': 30, 'left_ring': 31, 'left_middle': 32, 'left_index': 33,
        'right_index': 23, 'right_middle': 36, 'right_ring': 38, 'right_pinky': 39,
        'left_thumb': 42, 'right_thumb': 57
    }
}

# Раскладка РУСФОН
rusfon_layout = {
    'keys': {
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
    },
    'shift_keys': {
        '!': (2, 'left_pinky'), '@': (3, 'left_ring'), 'ё': (4, 'left_middle'),
        'Ё': (5, 'left_index'), 'ъ': (6, 'right_index'), 'Ъ': (7, 'right_middle'),
        '&': (8, 'right_ring'), '*': (9, 'right_pinky'), '(': (10, 'right_pinky'),
        ')': (11, 'right_pinky'), '_': (12, 'right_pinky'), 'ч': (13, 'right_pinky'),
        ':': (39, 'right_ring'), '"': (40, 'right_ring'), '<': (51, 'right_pinky'),
        '>': (52, 'right_pinky'), '?': (53, 'right_pinky')
    },
    'alt_keys': {},
    'home_positions': {
        'left_pinky': 30, 'left_ring': 31, 'left_middle': 32, 'left_index': 33,
        'right_index': 23, 'right_middle': 36, 'right_ring': 38, 'right_pinky': 39,
        'left_thumb': 42, 'right_thumb': 57
    }
}

# Раскладка ДИКТОР
diktor_layout = {
    'keys': {
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
    },
    'shift_keys': {
        'ь': (3, 'left_ring'), '№': (4, 'left_middle'),
        '%': (5, 'left_index'), ':': (6, 'right_index'), ';': (7, 'right_middle'),
        '-': (8, 'right_ring'), '"': (9, 'right_pinky'), '(': (10, 'right_pinky'),
        ')': (11, 'right_pinky'), '_': (12, 'right_pinky'), '+': (13, 'right_pinky'),
        'ъ': (17, 'left_ring'), '?': (19, 'left_index'), '!': (20, 'left_index')
    },
    'alt_keys': {},
    'home_positions': {
        'left_pinky': 30, 'left_ring': 31, 'left_middle': 32, 'left_index': 33,
        'right_index': 23, 'right_middle': 36, 'right_ring': 38, 'right_pinky': 39,
        'left_thumb': 42, 'right_thumb': 57
    }
}

# Раскладка АНТ
ant_layout = {
    'keys': {
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
    },
    'shift_keys': {
        '!': (2, 'left_pinky'), '?': (3, 'left_ring'), "'": (4, 'left_middle'),
        '"': (5, 'left_index'), '=': (6, 'right_index'), '+': (7, 'right_middle'),
        '-': (8, 'right_ring'), '*': (9, 'right_pinky'), '/': (10, 'right_pinky'),
        '%': (11, 'right_pinky'), '«': (12, 'right_pinky'), '»': (13, 'right_pinky'),
        ';': (48, 'right_pinky'), ':': (49, 'right_pinky')
    },
    'alt_keys': {},
    'home_positions': {
        'left_pinky': 30, 'left_ring': 31, 'left_middle': 32, 'left_index': 33,
        'right_index': 23, 'right_middle': 36, 'right_ring': 38, 'right_pinky': 39,
        'left_thumb': 42, 'right_thumb': 57
    }
}