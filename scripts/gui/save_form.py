"""Модуль содержит форму для сохранения данных."""

import tkinter as tk
from tkinter.messagebox import askyesno, showerror, showinfo

from scripts.db_class import CouchDB


class DataSaveForm(tk.Tk):
    """Генерирует форму с данными для подключения к БД."""

    def __init__(self, data):
        super().__init__()
        self.data = data

        # Элементы формы
        tk.Label(self, text="Сервер БД CouchDB").pack(pady=10)
        self.url = tk.Entry(self)
        self.url.pack(padx=50)
        tk.Label(self, text="Имя пользователя").pack(pady=10)
        self.user = tk.Entry(self)
        self.user.pack()
        tk.Label(self, text="Пароль").pack(pady=10)
        self.password = tk.Entry(self, show='*')
        self.password.pack()
        tk.Label(self, text="Имя документа").pack(pady=10)
        self.doc_name = tk.Entry(self)
        self.doc_name.pack()
        tk.Button(self, text="Сохранить", command=self.save_to_db).pack(pady=10)

        self.set_window_params()

    def set_window_params(self):
        """Устанавливает начальные параметры окна."""
        self.update()
        self.geometry(self.set_window_coord())
        self.resizable(False, False)
        # self.withdraw()
        self.create_save_dialog()

    def set_window_coord(self):
        """Возвращает координаты центра экрана для окна."""
        width, height = self.winfo_width(), self.winfo_height()
        x = round((self.winfo_screenwidth() - width) / 2)
        y = round((self.winfo_screenheight() - height) / 2)
        coord = f"{width}x{height}+{x}+{y}"
        return coord

    def create_save_dialog(self):
        """Создает диалог для выбора сохранения в БД."""
        res = askyesno(title="Сохранение", message="Сохранить результаты обучения в БД?")
        if res:
            self.deiconify()
        else:
            self.destroy()

    def save_to_db(self):
        """Записывает данные в БД."""
        try:
            db = CouchDB(self.url.get(), self.user.get(), self.password.get(), "bird-school")
            showinfo("Выполнение", db.create_doc(self.doc_name.get(), self.data))
        except Exception as _:
            showerror("Выполнение", "Ошибка при работе с БД")
        # self.destroy()
