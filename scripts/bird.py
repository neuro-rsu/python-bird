"""Модуль содержит класс, применяемый для создания спрайта птички,
а также вспомогательную функцию для преобразования координат."""

from random import randint

import numpy as np
import pygame as pg

import config


def transform(n, start1, stop1, start2, stop2):
    """Вспомогательная функция, преобразующая координаты."""
    return (n - start1) / (stop1 - start1) * (stop2 - start2) + start2


class Bird(pg.sprite.Sprite):
    """
    Описывает спрайт птички и его поведение.

    Параметры:
    bird_image - изображение птички;
    coord_y0 - начальная координата y.
    """
    MIN_SPEED = 10
    MAX_SPEED = 10
    count = 0
    rotation_count = 0

    def __init__(self, bird_image, coord_y0, number_of_birds):
        pg.sprite.Sprite.__init__(self)
        self.image_right = bird_image
        self.image_left = pg.transform.flip(bird_image, True, False)
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 10, coord_y0
        self.rotation_count = 0

        self.speed_x = randint(Bird.MIN_SPEED, Bird.MAX_SPEED)
        self.speed_y = 0 #randint(Bird.MIN_SPEED, Bird.MAX_SPEED)

        #self.best_brain = best_brain
        self.neuro_brain = config.best_brain.clone()
        self.neuro_brain.cost = 0
        self.neuro_brain.mutate()

        Bird.count = number_of_birds

    def update(self, screen_size):
        """Реализует поведение птички при обновлении экрана.

        Параметр:
        screen_size - кортеж, содержащий размеры игрового окна.
        """
        if self.speed_x >= 0:
            self.image = self.image_right
        else:
            self.image = self.image_left

        # inputs = np.array([[
        #     transform(self.rect.x, 0, screen_size[0], 0, 1),
        #     transform(self.rect.x + self.rect.width, 0, screen_size[0], 0, 1),
        #     transform(self.rect.y, 0, screen_size[1], 0, 1),
        #     transform(self.rect.y + self.rect.height, 0, screen_size[1], 0, 1)
        # ]], dtype=np.float32)

        inputs = np.array([[
            transform(screen_size[0] - self.rect.x if self.speed_x > 0 else self.rect.x, 0, screen_size[0], 0, 1)
        ]], dtype=np.float32)

        result = self.neuro_brain.feed_forward(inputs[0])

        # if result[1] > result[0]:
        #     self.speed_x = -self.speed_x
        #     rotation_count += 1;
        #     self.neuro_brain.cost -= 10

        if result[1] > result[0]:
            self.speed_x = -self.speed_x
            self.rotation_count += 1

        self.neuro_brain.cost += 1

        x = self.rect.x + self.speed_x

        if ((x + self.rect.width > screen_size[0] and self.speed_x > 0) or
                    (x < 0 and self.speed_x < 0)):
            self.kill()
            return

        """if result[3] > result[2]:
            self.speed_y = -self.speed_y
            self.neuro_brain.cost -= 10

        y = self.rect.y + self.speed_y

        if ((y + self.rect.height > screen_size[1] and self.speed_y > 0) or
                    (y < 0 and self.speed_y < 0)):
            self.kill()
            return"""

        if self.rotation_count > 10:
            self.kill()
            return

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def kill(self):
        """Переопределенный метод, который удаляет спрайт
        из всех спрайтовых групп.
        """
        Bird.count -= 1
        #print(config.best_brain.cost)

        if self.neuro_brain.cost > config.best_brain.cost:
            config.best_brain = self.neuro_brain.clone()

        super().kill()
