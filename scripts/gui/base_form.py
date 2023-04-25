"""Модуль содержит базовый абстрактный класс формы."""

from abc import ABC, abstractmethod
import tkinter as tk


class BaseForm(ABC, tk.Tk):
    """Базовый абстрактный класс для всех форм."""

    def get_window_geometry(self):
        """Возвращает геометрию окна с размещением в центре экрана."""
        width, height = self.winfo_width(), self.winfo_height()
        x = round((self.winfo_screenwidth() - width) / 2)
        y = round((self.winfo_screenheight() - height) / 2)
        geometry = f"{width}x{height}+{x}+{y}"
        return geometry

    def set_window_params(self, title, icon_path, resizable):
        """Устанавливает параметры окна.
        
        Параметры:
        title - заголовок окна;
        icon_path - путь до иконки окна;
        resizable - логический параметр, запрещающий или разрешающий
        изменение размеров окна.
        """
        self.title(title)

        # Позволяет установить иконку в формате PNG
        icon = tk.PhotoImage(file=icon_path)
        self.tk.call('wm', 'iconphoto', self._w, icon)

        # Задание размеров окна
        self.update()
        self.geometry(self.get_window_geometry())
        self.resizable(resizable, resizable)

    @abstractmethod
    def create_elements(self):
        """Создает элементы главного окна приложения.
        """
        pass
