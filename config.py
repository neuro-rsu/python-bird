"""Модуль содержит общие параметры."""

import os

from scripts.neural_network import NeuralNetwork


PROJECT_FOLDER = os.path.dirname(__file__)
APP_NAME = "Птица в клетке"
WIDTH = 1280
HEIGHT = 720
BIRD_SIZE = (60, 60)
NN_TOPOLOGY = (4, 4)
best_brain = NeuralNetwork(NN_TOPOLOGY, False)
