import tkinter as tk

import config as conf
from scripts.gui.base_form import BaseForm
from scripts.game.game_screen import GameManager


class Frame(tk.Frame):
    """Создает участок формы для ввода параметров генетического алгоритма."""

    def __init__(self, master):
        super().__init__(master)

        # Метки со значениями полей ввода
        labels = [
            "Число повторений", "Вероятность мутации, %",
            "Множитель, x (размер популяции - 10*x)", "Количество поворотов"
        ]
        for i, label in enumerate(labels):
            tk.Label(self, text=label).grid(row=i, column=0, sticky="W")

        # Поля для ввода
        self.repeat = tk.Entry(self)
        self.mutation = tk.Entry(self)
        self.bird_multiplier = tk.Entry(self)
        self.rotations = tk.Entry(self)

        # Позиционирование полей для ввода
        self.repeat.grid(row=0, column=1, sticky="E", pady=10)
        self.mutation.grid(row=1, column=1, sticky="E", pady=10)
        self.bird_multiplier.grid(row=2, column=1, sticky="E", pady=10)
        self.rotations.grid(row=3, column=1, sticky="E", pady=10)

        self.set_default_values()

    def set_default_values(self):
        """Устанавливает генетические параметры по умолчанию."""
        self.repeat.insert(0, "1")
        self.mutation.insert(0, "40")
        self.bird_multiplier.insert(0, "1")
        self.rotations.insert(0, "10")


class Form(BaseForm):
    """Генерирует форму для передачи данных и запуска игры."""

    def __init__(self):
        super().__init__()
        self.create_elements()
        self.set_window_params("Параметры", conf.ICONS["settings"], False)

    def create_elements(self):
        self.frame = Frame(self)
        self.frame.pack(side="top", padx=10)
        # Кнопка запуска и ее позиционирование
        tk.Button(self, text="Запустить", command=self.launch_game).pack(pady=10)

    def transform_data_to_dict(self):
        """Возвращает словарь с данными, введенными в форму."""
        return {
            "repeat": int(self.frame.repeat.get()),
            "mutation": int(self.frame.mutation.get()) / 100,
            "multiplier": int(self.frame.bird_multiplier.get()),
            "rotations": int(self.frame.rotations.get())
        }

    def launch_game(self):
        """Запускает игру с передачей необходимых параметров."""
        manager = GameManager(self.transform_data_to_dict())
        self.destroy()
        manager.set_game_data()
        manager.create_games()
        manager.call_save_form()
