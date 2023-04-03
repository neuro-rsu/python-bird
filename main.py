"""Главный модуль игры."""

import time

from scripts.form import Form
from scripts.game_screen import Game


if __name__ == "__main__":
    form = Form()
    form.mainloop()
    # for _ in range(1):
    #     start = time.time()

    #     game = Game()
    #     game.run()

    #     finish = time.time()
    #     print(str(finish - start).replace('.', ','))
