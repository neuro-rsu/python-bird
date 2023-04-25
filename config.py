"""Модуль содержит общие параметры игры."""

from os.path import dirname, join

from scripts.neural.neural_network import NeuralNetwork


APP_NAME = "Птица в клетке"
WIDTH = 1280
HEIGHT = 720

PROJECT_FOLDER = dirname(__file__)
IMG_FOLDER = join(PROJECT_FOLDER, "images")
ICONS = {
    "bird": join(IMG_FOLDER, "bird.png"),
    "analysis": join(IMG_FOLDER, "data_analysis.png"),
    "db": join(IMG_FOLDER, "db.png"),
    "settings": join(IMG_FOLDER, "settings.png"),
    "stat": join(IMG_FOLDER, "stat.png")
}

NN_TOPOLOGY = [1, 2]
best_brain = NeuralNetwork(NN_TOPOLOGY, False)
best_score = 1000
