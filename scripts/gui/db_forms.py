"""Модуль содержит форму для сохранения данных."""

import tkinter as tk
from tkinter.messagebox import askyesno, showerror, showinfo

import config as conf
from scripts.db_class import CouchDB
from scripts.gui.base_form import BaseForm


class BaseDataForm(BaseForm):
    """Генерирует базовую форму для подключения к БД."""

    def __init__(self):
        super().__init__()
        self.create_elements()

    def create_elements(self):
        tk.Label(self, text="Сервер БД CouchDB").pack(pady=10)
        self.url = tk.Entry(self)
        self.url.pack(padx=50)
        tk.Label(self, text="Имя пользователя").pack(pady=10)
        self.user = tk.Entry(self)
        self.user.pack()
        tk.Label(self, text="Пароль").pack(pady=10)
        self._password = tk.Entry(self, show='*')
        self._password.pack()
        tk.Label(self, text="Имя документа").pack(pady=10)
        self.doc_name = tk.Entry(self)
        self.doc_name.pack()


class DataLoadForm(BaseDataForm):
    """Создает форму для получения данных из БД."""

    def __init__(self):
        super().__init__()
        self.__return_data = None
        tk.Button(self, text="Загрузить", command=self.get_from_db).pack(pady=10)
        self.set_window_params("БД", conf.ICONS["db"], False)

    @property
    def return_data(self):
        """Свойства для получения данных из БД."""
        return self.__return_data

    def get_from_db(self):
        """Загружает данные из БД."""
        try:
            db = CouchDB(self.url.get(), self.user.get(), self._password.get(), "bird-school")
            result = db.get_doc(self.doc_name.get())
            if result:
                self.__return_data = result
                self.destroy()
            else:
                self._password.delete(0, tk.END)
                showinfo("Выполнение", "Документ не найден")
        except Exception as _:
            showerror("Выполнение", "Ошибка при работе с БД")


class DataSaveForm(BaseDataForm):
    """Создает форму для сохранения данных в БД."""

    def __init__(self, data):
        super().__init__()
        self.data = data
        tk.Button(self, text="Сохранить", command=self.save_to_db).pack(pady=10)
        self.set_window_params("БД", conf.ICONS["db"], False)
        self.create_save_dialog()

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
            db = CouchDB(self.url.get(), self.user.get(), self._password.get(), "bird-school")
            showinfo("Выполнение", db.create_doc(self.doc_name.get(), self.data))
        except Exception as _:
            showerror("Выполнение", "Ошибка при работе с БД")
        finally:
            self._password.delete(0, tk.END)
