import numpy as np


class NeuralNetwork:
    def __init__(self, topology, clone):
        if len(topology) < 2:
            raise ValueError("A Neural Network cannot contain less than 2 Layers.")

        for layer in topology:
            if layer < 1:
                raise ValueError("A single layer of neurons must contain, at least, one neuron.")

        self.the_topology = topology

        self.sections = np.empty(len(self.the_topology) - 1)

        if clone:
            return

        for i, _ in enumerate(self.sections):
            self.sections[i] = NeuralSection(self.the_topology[i], self.the_topology[i + 1])

    def clone(self):
        CLONE = NeuralNetwork(self.the_topology, True)
        for i, _ in enumerate(self.sections):
            CLONE.sections[i] = self.sections[i].clone()

        return CLONE

    @property
    def topology(self):
        RES = np.zeros(len(self.the_topology), dtype = int)
        return RES

    def feed_forward(self, input_data):
        if input_data is None:
            raise ValueError("The input array cannot be set to null.")
        elif len(input_data) != self.the_topology[0]:
            raise ValueError("The input array's length does not match the number of neurons in the input layer.")

        output = input_data

        for i, _ in enumerate(self.sections):
            output = self.sections[i].feed_forward(output)

        return output

    def mutate(self, mutation_probability = 1, mutation_amount = 2.0):
        for i, _ in enumerate(self.sections):
            self.sections[i].mutate(mutation_probability, mutation_amount)


class NeuralSection:
    def __init__(self, input_count = 0, output_count = 0):
        if input_count == 0:
            return
        elif output_count == 0:
            raise ValueError("You cannot create a Neural Layer with no output neurons.")

        self.weights = np.empty(input_count + 1)

        for i, _ in enumerate(self.weights):
            self.weights[i] = np.empty(output_count)

        for i, _ in enumerate(self.weights):
            for j, _ in enumerate(self.weights[i]):
                self.weights[i][j] = np.random.random() - 0.5

    def clone(self):
        CLONE = NeuralSection()
        CLONE.weights = np.empty(len(self.weights))

        for i, _ in enumerate(self.weights):
            CLONE.weights[i] = np.empty(len(self.weights[i]))

        for i, _ in enumerate(self.weights):
            for j, _ in enumerate(self.weights[i]):
                CLONE.weights[i][j] = self.weights[i][j]

        return CLONE

    def feed_forward(self, input_data):
        if input_data is None:
            raise ValueError("The input array cannot be set to null.")
        elif len(input_data) != len(self.weights) - 1:
            raise ValueError("The input array's length does not match the number of neurons in the input layer.")

        output = np.zeros(len(self.weights[0]), dtype = int)

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
