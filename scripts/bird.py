"""Модуль содержит класс, применяемый для создания спрайта птички,
а также вспомогательную функцию для преобразования координат."""

from random import randint

import numpy as np
import pygame as pg


def transform(n, start1, stop1, start2, stop2):
    """Вспомогательная функция, преобразующая координаты."""
    return (n - start1) / (stop1 - start1) * (stop2 - start2) + start2


class Bird(pg.sprite.Sprite):
    """
    Описывает спрайт птички и его поведение.

    Параметры:
    bird_image - изображение птички;
    coord_y0 - начальная координата y;
    best_brain - нейросеть для птички.
    """
    MIN_SPEED = 10
    MAX_SPEED = 10

    def __init__(self, bird_image, coord_y0, best_brain):
        pg.sprite.Sprite.__init__(self)
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, coord_y0

        self.speed_x = randint(Bird.MIN_SPEED, Bird.MAX_SPEED)
        self.speed_y = 0 #randint(Bird.MIN_SPEED, Bird.MAX_SPEED)
        if self.speed_x < 0:
            self.image = pg.transform.flip(self.image, True, False)

        self.neuro_brain = best_brain.clone()
        self.neuro_brain.mutate()

        self.is_ready = True

    def update(self, screen_size):
        """Реализует поведение птички при обновлении экрана.

        Параметр:
        screen_size - кортеж, содержащий размеры игрового окна.
        """

        if not self.is_ready:
            return

        inputs = np.array([[
            transform(self.rect.x, 0, screen_size[0], 0, 1),
            transform(self.rect.x + self.rect.width, 0, screen_size[0], 0, 1),
            transform(self.rect.y, 0, screen_size[1], 0, 1),
            transform(self.rect.y + self.rect.height, 0, screen_size[1], 0, 1)
        ]], dtype=np.float32)

        result = self.neuro_brain.feed_forward(inputs[0])
        if result[1] > result[0]:
            self.speed_x = -self.speed_x
            self.neuro_brain.cost -= 10

        x = self.rect.x + self.speed_x

        if ((x + self.rect.width > screen_size[0] and self.speed_x > 0) or
                    (x < 0 and self.speed_x < 0)):
            self.kill()
            return

        if result[3] > result[2]:
            self.speed_y = -self.speed_y
            self.neuro_brain.cost -= 10

        y = self.rect.y + self.speed_y

        if ((y + self.rect.height > screen_size[1] and self.speed_y > 0) or
                    (y < 0 and self.speed_y < 0)):
            self.kill()
            return

        if self.neuro_brain.cost < -100:
            self.kill()
            return

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
