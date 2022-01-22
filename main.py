import os
import pygame as pg
from scripts.bird import Bird
from scripts import constants as const


def main():
    pg.init()
    screen = pg.display.set_mode((const.WIDTH, const.HEIGHT))
    pg.display.set_caption(const.APP_NAME)

    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, "images")
    bird_img = pg.image.load(os.path.join(img_folder, "bird.png")).convert_alpha()
    bird_img = pg.transform.scale(bird_img, const.SPRITE_SIZE)

    pg.display.set_icon(bird_img)
    running = True
    clock = pg.time.Clock()

    all_sprites = pg.sprite.Group()
    birds = [Bird(bird_img) for _ in range(const.NUMBER_OF_BIRDS)]
    all_sprites.add(birds)

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill(const.BACKGROUND)
        all_sprites.draw(screen)
        pg.display.update()
        clock.tick(const.FPS)

        for bird in birds:
            bird.move()

    pg.quit()


if __name__ == "__main__":
    main()
