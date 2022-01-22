from random import randint
import pygame as pg
from scripts import constants as const


class Bird(pg.sprite.Sprite):

    SIZE = const.SPRITE_SIZE[0]
    MIN_SPEED = 1
    MAX_SPEED = 10

    def __init__(self, bird_image):
        pg.sprite.Sprite.__init__(self)
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.center = (randint(self.SIZE/2, const.WIDTH/2 - self.SIZE/2),
                            randint(self.SIZE/2, const.HEIGHT/2 - self.SIZE/2))
        
        self.speed_x = (-1) ** randint(0, 1) * randint(self.MIN_SPEED, self.MAX_SPEED)
        self.speed_y = (-1) ** randint(0, 1) * randint(self.MIN_SPEED, self.MAX_SPEED)
        if self.speed_x < 0:
            self.image = pg.transform.flip(self.image, True, False)

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left < 0 or self.rect.right > const.WIDTH:
            self.image = pg.transform.flip(self.image, True, False)
            self.speed_x = -self.speed_x
        if self.rect.top < 0 or self.rect.bottom > const.HEIGHT:
            self.speed_y = -self.speed_y
