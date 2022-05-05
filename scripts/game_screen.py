"""Модуль описывает игровой экран и логику игры."""

import os

import pygame as pg

import config as conf
from scripts.bird import Bird
from scripts.neural_network import NeuralNetwork


class Game:
    """Описывает игровой экран и процесс игры."""
    FPS = 60
    BACKGROUND = (0, 178, 255)

    def __init__(self):
        # Установка параметров окна
        pg.init()
        self.screen = pg.display.set_mode((conf.WIDTH, conf.HEIGHT), pg.RESIZABLE)
        pg.display.set_caption(conf.APP_NAME)
        self.icon = self.load_icon()
        pg.display.set_icon(self.icon)

        # Состояние игрового процесса
        self.is_running = True
        self.clock = pg.time.Clock()

        # Инициализация игровых объектов
        self.neural_net = NeuralNetwork(conf.NN_TOPOLOGY, False)
        self.population = 1
        self.sprites = pg.sprite.Group()
        birds = self.create_objects()
        self.sprites.add(birds)

    @staticmethod
    def load_icon():
        """Загружает и возвращает иконку игрового окна."""
        img_folder = os.path.join(conf.PROJECT_FOLDER, "images")
        bird_img = pg.image.load(os.path.join(img_folder, "bird.png")).convert_alpha()
        bird_img = pg.transform.scale(bird_img, conf.BIRD_SIZE)
        return bird_img

    def create_objects(self):
        """Создаёт экземпляры класса Bird
        и возвращает их в качестве списка."""
        birds = []
        number_of_birds = int(self.screen.get_height() / conf.BIRD_SIZE[0])
        for i in range(number_of_birds):
            # Картинка с птичкой используется как иконка и как спрайт,
            # поэтому загружается только в этом классе и
            # используется при создании экземпляров класса Bird,
            # чтобы не загружать её дважды
            birds.append(Bird(self.icon, conf.BIRD_SIZE[0] * i, self.neural_net))
        return birds

    def get_text(self):
        """Возвращает текстовый объект с текущим номером популяции птичек."""
        font = pg.font.Font(None, 36)
        text = f"Population: {self.population}"
        text_surface = font.render(text, True, (255, 255, 255), Game.BACKGROUND)
        return text_surface

    def draw(self):
        """Занимается отрисовкой объектов."""
        self.screen.fill(Game.BACKGROUND)
        self.screen.blit(self.get_text(), (10, 10))
        self.sprites.draw(self.screen)

    def update(self):
        """Обновляет экран игры."""
        pg.display.update()
        scr_size = (self.screen.get_width(), self.screen.get_height())
        self.sprites.update(scr_size)

        # Создание новых популяций птичек
        if not self.sprites.sprites():
            self.sprites.add(self.create_objects())
            self.population += 1

    def handle_events(self):
        """Отслеживает нажатия клавиш и кнопок."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

    def run(self):
        """Запускает и контролирует игровой процесс."""
        while self.is_running:
            self.handle_events()
            self.draw()
            self.update()
            self.clock.tick(Game.FPS)

        pg.quit()
