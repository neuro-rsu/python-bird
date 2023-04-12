"""Модуль содержит классы, описывающие нейросеть."""

import numpy as np


class NeuralNetwork:
    """Создает нейросеть

    Параметры:
    topology - топология нейросети;
    clone - логический параметр, отмечающий необходимость клонирования нейросети.
    """

    def __init__(self, topology, clone):
        self.cost = 0

        if len(topology) < 2:
            raise ValueError("A Neural Network cannot contain less than 2 Layers.")

        for layer in topology:
            if layer < 1:
                raise ValueError("A single layer of neurons must contain, at least, one neuron.")

        self.the_topology = topology

        self.sections = np.empty(len(self.the_topology) - 1, dtype=object)

        if clone:
            return

        for i, _ in enumerate(self.sections):
            self.sections[i] = NeuralSection(self.the_topology[i], self.the_topology[i + 1])

    def clone(self):
        clone = NeuralNetwork(self.the_topology, True)
        clone.cost = self.cost

        for i, _ in enumerate(self.sections):
            clone.sections[i] = self.sections[i].clone()

        return clone

    @property
    def topology(self):
        """Возвращает топологию в виде массива."""
        res = np.zeros(len(self.the_topology), dtype=int) # Type to float - ?
        return res

    def feed_forward(self, input_data):
        if input_data is None:
            raise ValueError("The input array cannot be set to null.")
        elif len(input_data) != self.the_topology[0]:
            raise ValueError("The input array's length does not match the number of neurons in the input layer.")

        output = input_data

        for i, _ in enumerate(self.sections):
            output = self.sections[i].feed_forward(output)

        return output

    def mutate(self, mutation_probability=0.4, mutation_amount=1.0): #0.05, 1.0
        """Мутирует каждую секцию нейросети.

        Параметры: ..."""
        for i, _ in enumerate(self.sections):
            self.sections[i].mutate(mutation_probability, mutation_amount)

    def get_params(self):
        """Возвращает словарь с параметрами нейросети."""
        nn_params = self.__dict__

        # Преобразование весов из массива в список
        for i, section in enumerate(self.sections, 1):
            nn_params[f"weights{i}"] = vars(section)["weights"].tolist()

        del nn_params["sections"]
        return nn_params

    def set_params(self, nn_params):
        """Устанавливает параметры нейросети из словаря nn_params."""
        self.cost = nn_params["cost"]
        self.the_topology = nn_params["the_topology"]
        # Преобразование весов в массив
        for i, section in enumerate(self.sections, 1):
            section.weights = np.array(nn_params[f"weights{i}"])


class NeuralSection:

    def __init__(self, input_count=0, output_count=0):
        if input_count == 0:
            return
        elif output_count == 0:
            raise ValueError("You cannot create a Neural Layer with no output neurons.")

        self.weights = np.empty((input_count + 1, output_count))

        for i, _ in enumerate(self.weights):
            for j, _ in enumerate(self.weights[i]):
                self.weights[i][j] = np.random.random() - 0.5

    def clone(self):
        clone = NeuralSection()
        clone.weights = np.empty((len(self.weights), len(self.weights[0])))

        for i, _ in enumerate(self.weights):
            for j, _ in enumerate(self.weights[i]):
                clone.weights[i][j] = self.weights[i][j]

        return clone

    def feed_forward(self, input_data):
        if input_data is None:
            raise ValueError("The input array cannot be set to null.")
        elif len(input_data) != len(self.weights) - 1:
            raise ValueError("The input array's length does not match the number of neurons in the input layer.")

        output = np.zeros(len(self.weights[0]))

        for i, _ in enumerate(self.weights):
            for j in range(len(self.weights[i])):
                if i == len(self.weights) - 1:
                    output[j] += self.weights[i][j]
                else:
                    output[j] += self.weights[i][j] * input_data[i]

        for i, _ in enumerate(output):
            output[i] = ReLU(output[i])

        return output

    def mutate(self, mutation_probability, mutation_amount):
        for i, _ in enumerate(self.weights):
            for j, _ in enumerate(self.weights[i]):
                if np.random.random() < mutation_probability:
                    self.weights[i][j] = np.random.random() * (mutation_amount * 2) - mutation_amount


def ReLU(x):
    if x >= 0:
        return x
    else:
        return x / 20
