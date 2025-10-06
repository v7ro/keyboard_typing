'''
Модуль построения графиков 
Импортирует результаты анализа из модуля main.py
Строит два типа графиков(столбчатую и круговую диаграммы)
Столбчатая диаграмма показывает показывает абсолютные штрафы по каждому пальцу
Круговая диограмма показывает процентное распределение нагрузки по пальцам 
'''
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #импортируем класс Matplotlib, 
#который позволяет встроить графики внутрь окна Tikenter
import matplotlib.pyplot as plt #импортируем Matplotlib для построения графиков
from main import KeyboardAnalyzer #импортируем класс KeyboardAnalyzer из файла main.py

#создаем объект анализатора и запускаем его, что бы получить штрафы по пальцам
def show_bar_chart(): #функция для столбчатой диаграммы
    analyzer = KeyboardAnalyzer()
    results = analyzer.analyze()
#извлекаем словарь штрафов по пальцам и превращаем его в два списка
    penalties = results['finger_penalties']
    fingers = list(penalties.keys()) #название пальцев
    values = list(penalties.values()) #значение штрафов

#создаем график и ось, строим столбчатую диаграмму
    fig, ax = plt.subplots(figsize=(8, 5))
#добавляем подписи
    ax.bar(fingers, values, color="skyblue")
    ax.set_title("Нагрузка на пальцы (столбчатая диаграмма)")
    ax.set_ylabel("Суммарный штраф")
    ax.set_xlabel("Пальцы")
    ax.set_xticklabels(fingers, rotation=45, ha="right")
#встраиваем графики в окно Tkinter и отображаем его
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()
#функция для круговой диаграммы
def show_pie_chart():
    analyzer = KeyboardAnalyzer()
    results = analyzer.analyze()
#берем данные для графика
    penalties = results['finger_penalties']
    fingers = list(penalties.keys())
    values = list(penalties.values())

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(values, labels=fingers, autopct='%1.1f%%', startangle=90)
    ax.set_title("Распределение нагрузки по пальцам (круговая диаграмма)") #заголовок

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Tkinter окно
#создаем главное окно и задаем заголовок
window = tk.Tk()
window.title("Анализ раскладки клавиатуры")
#создаем кнопку, которая запускает функцию show_bar_chart
btn1 = tk.Button(window, text="Показать столбчатую диаграмму", command=show_bar_chart)
btn1.pack(pady=5)
#создаем кнопку для круговой диаграммы
btn2 = tk.Button(window, text="Показать круговую диаграмму", command=show_pie_chart)
btn2.pack(pady=5)
#после запуска программа ждет нажатий кнопок
window.mainloop()
