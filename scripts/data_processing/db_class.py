"""Модуль содержит класс для работы с БД в CouchDB."""

from re import sub

import couchdb3


class CouchDB:
    """Создает новую БД в CouchDB по ее имени
    или открывает ее, если она уже есть на сервере.

    Параметры:
    url - адрес сервера БД;
    username - логин;
    password - пароль;
    db_name - имя БД.
    """

    def __init__(self, url: str, username, password, db_name):
        url = sub(r"https?://", '', url)
        self.__server = couchdb3.Server(f"http://{username}:{password}@{url}")

        if db_name in self.__server:
            self.__db = self.__server.get(db_name)
        else:
            self.__db = self.__server.create(db_name)

    @property
    def name(self):
        """Свойство, возвращающее имя открытой БД."""
        return self.__db.name

    def delete(self):
        """Удаляет открытую БД."""
        if self.__server.delete(self.__db.name):
            return "БД успешно удалена"
        return "Ошибка при удалении БД"

    def create_doc(self, doc_name, data):
        """Создает новый документ с именем doc_name и данными data."""
        if doc_name not in self.__db:
            data["_id"] = doc_name
            self.__db.save(data)
            return "Документ успешно создан"
        return "Документ уже существует"

    def get_doc(self, doc_name):
        """Возвращает данные документа с именем doc_name"""
        if doc_name in self.__db:
            doc = dict(self.__db.get(doc_name))
            del doc["_id"]
            del doc["_rev"]
            return doc
        return None

    def update_doc(self, doc_name, data):
        """Обновляет информацию data в документе doc_name."""
        if doc_name in self.__db:
            data["_id"] = doc_name
            doc = self.__db.get(doc_name)
            doc.update(data)
            self.__db.save(doc)
            return "Документ успешно обновлен"
        return "Документ не найден"

    def delete_doc(self, doc_name):
        """Удаляет документ с именем doc_name."""
        if doc_name in self.__db:
            self.__db.delete(docid=doc_name, rev=self.__db.rev(doc_name))
            return "Документ успешно удален"
        return "Документ не найден"
