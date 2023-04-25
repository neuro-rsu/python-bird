"""Модуль строит главный экран игры."""

import tkinter as tk
from tkinter.messagebox import askyesno

import config as conf
from scripts.gui import ds_app
from scripts.gui.base_form import BaseForm
from scripts.gui.game_form import Form


class MainScreen(BaseForm):
    """Описывает главный экран."""

    def __init__(self):
        """Инициализирует основные элементы окна."""
        super().__init__()
        self.create_elements()
        self.set_window_params(conf.APP_NAME, conf.ICONS["bird"], False)

    def create_elements(self):
        self.image = tk.PhotoImage(file=conf.ICONS["bird"])

        elements = [
            tk.Label(self, text=conf.APP_NAME, fg="blue"),
            tk.Label(self, image=self.image),
            tk.Button(self, text="Запустить игру", bd=0, command=self.launch_game),
            tk.Button(self, text="Анализ данных", bd=0, command=self.launch_stat_app),
            tk.Button(self, text="Выйти", bd=0, command=self.exit)
        ]

        for element in elements:
            element.pack(side=tk.TOP, fill=tk.BOTH, padx=100)

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
