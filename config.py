"""Модуль содержит общие параметры."""

import os

from scripts.neural_network import NeuralNetwork


PROJECT_FOLDER = os.path.dirname(__file__)
APP_NAME = "Птица в клетке"
WIDTH = 1280
HEIGHT = 720
NN_TOPOLOGY = (1, 2)
best_brain = NeuralNetwork(NN_TOPOLOGY, False)
