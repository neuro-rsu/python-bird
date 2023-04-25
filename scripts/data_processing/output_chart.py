"""Модуль для построения графика результата обучения нейросети."""

from matplotlib.figure import Figure
import numpy as np

from scripts.neural.neural_network import NeuralNetwork


class OutputChart:
    """Строит график для сравнения выходных сигналов нейросети.
    
    Параметры:
    train_data - статистика обучения из БД.
    """

    def __init__(self, train_data):
        self.data = train_data["best_weights"]

    def get_chart_points(self):
        """Возвращает списки с точками для построения графика."""
        # Создание нейросети
        net = NeuralNetwork(self.data["the_topology"], False)
        net.set_params(self.data)

        # Подготовка входного датасета
        x = np.linspace(0.0, 1.0, num=1000)

        y1, y2 = [], [] # Выходные списки
        # Получение выходных данных
        for i in x:
            result = net.feed_forward([i])
            y1.append(result[0])
            y2.append(result[1])
        return x, y1, y2

    def create_chart(self, x, y1, y2):
        """Генерирует графики выходных сигналов y1, y2 от x."""
        chart = Figure(figsize=(5, 4), dpi=100)
        subplot = chart.add_subplot(111)
        subplot.plot(x, y1, label="Y1", color="black")
        subplot.plot(x, y2, label="Y2", color="black", linestyle="--")
        subplot.set_xlabel("X")
        subplot.set_ylabel("Y")
        subplot.legend()
        subplot.grid(True)
        subplot.set_title("Выходные сигналы ИНС")
        return chart
