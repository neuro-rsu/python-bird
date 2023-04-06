"""Модуль содержит класс для работы с БД в CouchDB."""

from couchdb3 import Server


class CouchDB:
    """Создает новую БД в CouchDB по ее имени
    или открывает ее, если она расположена на сервере.

    Параметры:
    url - адрес сервера БД;
    username - логин;
    password - пароль;
    db_name - имя БД.
    """

    def __init__(self, url, username, password, db_name):
        self.__server = Server(f"http://{username}:{password}@{url}")

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
        return self.__server.delete(self.__db.name)

    def create_doc(self, doc_name, data):
        """Создает новый документ с именем doc_name и данными data."""
        if doc_name not in self.__db:
            data["_id"] = doc_name
            return self.__db.save(data)
        return "Документ уже существует"

    def get_doc(self, doc_name):
        """Возвращает данные документа с именем doc_name"""
        if doc_name in self.__db:
            doc = dict(self.__db.get(doc_name))
            del doc["_id"]
            del doc["_rev"]
            return doc
        return "Документ не найден"

    def update_doc(self, doc_name, data):
        """Обновляет информацию data документе doc_name."""
        if doc_name in self.__db:
            data["_id"] = doc_name
            doc = self.__db.get(doc_name)
            doc.update(data)
            return self.__db.save(doc)
        return "Документ не найден"

    def delete_doc(self, doc_name):
        """Удаляет документ с именем doc_name."""
        if doc_name in self.__db:
            return self.__db.delete(docid=doc_name, rev=self.__db.rev(doc_name))
        return "Документ не найден"
