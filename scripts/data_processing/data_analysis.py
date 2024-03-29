"""Модуль для обработки данных, поученных при обучении нейросети."""

from math import ceil, log10
from re import sub

from matplotlib.figure import Figure
import pandas as pd


class DataAnalyst:
    """Анализирует результаты обучения нейросети.
    
    Параметр train_data - данные, полученные при обучении.
    """

    def __init__(self, train_data):
        self.times = pd.Series(train_data["times"])
        # Число интервалов по правилу Стёрджеса
        self.interval_count = ceil(1 + 3.322*log10(len(self.times)))

    def split_into_intervals(self):
        """Разбивает данные на интервалы."""
        return pd.cut(self.times, bins=self.interval_count).value_counts().sort_index()

    def get_describe_stat(self):
        """Возвращает описательную статистику результатов обучения."""
        # Расчет моды
        intervals = self.split_into_intervals()
        frequencies = list(intervals)
        # Увеличение границ для предотвращения выхода за пределы списка
        frequencies.insert(0, 0)
        frequencies.append(0)
        # idmax() возвращает строку, а нужен кортеж
        max_int = str(intervals.idxmax())
        max_int = sub(r'[\(\)\[\]]', '', max_int) # Удаление всех скобок
        max_int = list(map(float, max_int.split(',')))

        mode_idx = frequencies.index(max(frequencies))
        # Расчет числителя, дроби и самой моды
        num = frequencies[mode_idx] - frequencies[mode_idx - 1]
        fraction = num / (num + (frequencies[mode_idx] - frequencies[mode_idx + 1]))
        mode = max_int[0] + (max_int[1] - max_int[0]) * fraction

        # Добавление моды к описательной статистике
        describe = self.times.describe()
        describe.at["mode"] = mode
        return describe

    def create_hist(self):
        """Строит гистограмму распределения."""
        hist = Figure(figsize=(5, 4), dpi=100)
        subplot = hist.add_subplot(111)
        subplot.hist(self.times, bins=self.interval_count, edgecolor="black")
        subplot.set_xlabel("Время обучения, с")
        subplot.set_ylabel("Частота")
        subplot.grid(True)
        subplot.set_title("Распределение времени обучения")
        return hist
