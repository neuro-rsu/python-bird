"""Модуль строит главный экран игры."""

import tkinter as tk
from tkinter.messagebox import askyesno

from scripts.gui.game_form import Form
from scripts.gui import ds_app
import config as conf


class MainScreen(tk.Tk):
    """Описывает главный экран."""

    def __init__(self):
        """Инициализирует основные элементы окна."""
        super().__init__()
        self.title(conf.APP_NAME)
        self.create_elements()

    def create_elements(self):
        """Создает элементы главного окна приложения."""
        elements = [
            tk.Label(self, text=conf.APP_NAME, fg="blue"),
            tk.Button(self, text="Запустить игру", command=self.launch_game),
            tk.Button(self, text="Анализ данных", command=self.launch_stat_app),
            tk.Button(self, text="Выйти", command=self.exit)
        ]

        for element in elements:
            element.pack(side=tk.TOP, fill=tk.BOTH)

    def launch_game(self):
        """Запускает форму для передачи параметров игры"""
        self.destroy()
        form = Form()
        form.mainloop()

    def launch_stat_app(self):
        """Запускает приложение для визуализации статистики."""
        self.destroy()
        ds_app.main()

    def exit(self):
        """Выводит диалоговое окно о выходе."""
        if askyesno(conf.APP_NAME, "Покинуть приложение?"):
            self.destroy()
