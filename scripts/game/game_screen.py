"""Модуль описывает игровой экран и логику игры."""

import time

import pygame as pg

import config as conf
from scripts.gui.db_forms import DataSaveForm
from scripts.game.bird import Bird
from scripts.neural.neural_network import NeuralNetwork


class GameManager:
    """Управляет данными data, передаваемыми в форму,
    и создает необходимое количество игр."""

    def __init__(self, data):
        self.data = data
        self.times = []

    def set_game_data(self):
        """Устанавливает параметры генетического алгоритма и игры."""
        Bird.mutation = self.data["mutation"]
        Bird.rotations = self.data["rotations"]
        Bird.multiplier = self.data["multiplier"]
        conf.best_score = round(1000 * conf.WIDTH / 1280 * Bird.rotations / 10)

    def create_games(self):
        """Создает заданное количество игр."""
        for i in range(1, self.data["repeat"] + 1):
            conf.best_brain = NeuralNetwork(conf.NN_TOPOLOGY, False)
            start = time.time()
            game = Game(i)
            game.run()
            finish = time.time()
            self.times.append(finish - start)
        pg.quit()

    def get_result_data(self):
        """Возвращает результаты обучения."""
        res = {"best_weights": conf.best_brain.get_params()}
        res["times"] = self.times
        return res

    def call_save_form(self):
        """Вызывает форму для сохранения результатов обучения."""
        save_form = DataSaveForm(self.get_result_data())
        save_form.mainloop()


class Game:
    """Описывает игровой экран и процесс игры.

    Параметр stage - этап обучения.
    """
    FPS = 60
    BACKGROUND = (0, 178, 255)
    SURF_INDENT = 10

    def __init__(self, stage):
        # Установка параметров окна
        pg.init()
        self.screen = pg.display.set_mode((conf.WIDTH, conf.HEIGHT))
        pg.display.set_caption(conf.APP_NAME)
        self.icon = self.load_icon()
        pg.display.set_icon(self.icon)

        # Состояние игрового процесса
        self.is_running = True
        self.clock = pg.time.Clock()
        self.stage = stage

        # Инициализация игровых объектов
        self.population = 1
        self.birds = pg.sprite.Group()

        self.game_surf = pg.Surface((conf.WIDTH,
                                conf.HEIGHT - self.get_text_surf_height()))

        birds = self.create_objects()
        self.birds.add(birds)

    @staticmethod
    def load_icon():
        """Загружает и возвращает иконку игрового окна."""
        bird_img = pg.image.load(conf.ICONS["bird"]).convert_alpha()
        bird_img = pg.transform.scale(bird_img, Bird.SIZE)
        return bird_img

    def create_objects(self):
        """Создаёт экземпляры класса Bird
        и возвращает их в качестве списка.
        """
        birds = []

        # number_of_birds = int(conf.HEIGHT / Bird.SIZE[0])
        # for i in range(number_of_birds):
        for i in range(10):
            for _ in range(Bird.multiplier):
            # Картинка с птичкой используется как иконка игры и как спрайт,
            # поэтому загружается в этом классе
                bird = Bird(self.icon, Bird.SIZE[0] * i)
                birds.append(bird)
        return birds

    def get_text(self):
        """Возвращает текстовый объект с отображаемыми параметрами игры."""
        font = pg.font.Font(None, 36)
        text = f"Этап: {self.stage} | Популяция: {self.population} | "
        text += f"Птиц: {len(self.birds.sprites())}"
        text_surface = font.render(text, True, (255, 255, 255), Game.BACKGROUND)
        return text_surface

    def get_text_surf_height(self):
        """Возвращает высоту текста с популяциями."""
        return self.get_text().get_height() + 2 * Game.SURF_INDENT

    def get_game_height(self):
        """Возвращает высоту поверхности игры."""
        return self.screen.get_height() - self.get_text_surf_height()

    def draw(self):
        """Отрисовывает объекты на главный экран."""
        self.screen.fill(Game.BACKGROUND)
        self.screen.blit(self.get_text(), (Game.SURF_INDENT, Game.SURF_INDENT))
        self.screen.blit(self.game_surf, (0, self.get_text_surf_height()))
        self.game_surf.fill(Game.BACKGROUND)
        self.birds.draw(self.game_surf)

        #print(conf.best_brain)

    def update(self):
        """Обновляет экран игры."""
        pg.display.update()
        self.birds.update()

        # Создание новых популяций птичек
        if not self.birds.sprites():
            self.birds.add(self.create_objects())
            self.population += 1

        # Для теста
        # if conf.best_brain.cost > 500:
        #     Bird.mutation = 0.1

    def handle_events(self):
        """Отслеживает нажатия клавиш и кнопок."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

            # Нажатие клавиш клавиатуры
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_SPACE:
            #         # print(conf.best_brain.get_params())

    def run(self):
        """Запускает и контролирует игровой процесс."""
        while self.is_running:
            self.handle_events()
            self.draw()

            # Обучение окончено
            if conf.best_brain.cost > conf.best_score:
                #print(conf.best_brain.get_params())
                return

            self.update()

            # if self.count == 0:
            #     time.sleep(3)
            # if self.count >= 0:
            #     self.count-= 1
            self.clock.tick(Game.FPS)

        pg.quit()
